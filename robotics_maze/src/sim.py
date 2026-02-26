"""PyBullet maze simulation wrapper with waypoint execution support."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

try:
    from robotics_maze.src.robot import MobileRobotController
except ImportError:  # pragma: no cover - allows direct module loading in minimal test harnesses.
    from robot import MobileRobotController  # type: ignore[no-redef]

try:
    import pybullet as p
    import pybullet_data
except ImportError:  # pragma: no cover - dependency availability is environment specific.
    p = None  # type: ignore[assignment]
    pybullet_data = None  # type: ignore[assignment]

try:
    import mujoco
except ImportError:  # pragma: no cover - dependency availability is environment specific.
    mujoco = None  # type: ignore[assignment]


ObstacleInput = Union["ObstacleBox", Mapping[str, Any]]
GoalReachedHook = Callable[["PyBulletMazeSim"], None]


@dataclass(frozen=True)
class EpisodeResult:
    success: bool
    steps: int
    elapsed_s: float


@dataclass(frozen=True)
class ObstacleBox:
    """Axis-aligned box obstacle definition in world coordinates."""

    center: Tuple[float, float, float]
    size: Tuple[float, float, float]
    yaw: float = 0.0
    rgba: Tuple[float, float, float, float] = (0.35, 0.35, 0.35, 1.0)
    mass: float = 0.0

    @classmethod
    def from_definition(cls, definition: ObstacleInput) -> "ObstacleBox":
        if isinstance(definition, cls):
            return definition
        if not isinstance(definition, Mapping):
            raise TypeError(f"Unsupported obstacle definition: {definition!r}")

        size = _parse_xyz(definition, ("size", "dimensions", "extents"))
        if size is None:
            size = (
                float(definition.get("width", definition.get("w", 1.0))),
                float(definition.get("depth", definition.get("d", 1.0))),
                float(definition.get("height", definition.get("h", 1.0))),
            )

        center = _parse_xyz(definition, ("center", "position", "pos"))
        if center is None:
            center = (
                float(definition.get("x", 0.0)),
                float(definition.get("y", 0.0)),
                float(definition.get("z", size[2] * 0.5)),
            )

        color_like = definition.get("rgba", definition.get("color", (0.35, 0.35, 0.35, 1.0)))
        rgba = _ensure_rgba(color_like)
        yaw = float(definition.get("yaw", definition.get("rotation_z", 0.0)))
        mass = float(definition.get("mass", 0.0))
        return cls(
            center=(float(center[0]), float(center[1]), float(center[2])),
            size=(float(size[0]), float(size[1]), float(size[2])),
            yaw=yaw,
            rgba=rgba,
            mass=mass,
        )


class PyBulletMazeSim:
    """High-level simulation wrapper for 3D maze robot navigation."""

    def __init__(
        self,
        gui: bool = False,
        time_step: float = 1.0 / 240.0,
        gravity: Tuple[float, float, float] = (0.0, 0.0, -9.81),
        reset_environment_hook: Optional[GoalReachedHook] = None,
    ) -> None:
        if p is None or pybullet_data is None:
            raise RuntimeError("pybullet and pybullet_data are required for PyBulletMazeSim")

        self.gui = bool(gui)
        self.time_step = float(time_step)
        self.gravity = gravity
        self.client_id = p.connect(p.GUI if self.gui else p.DIRECT)
        if self.client_id < 0:
            raise RuntimeError("Failed to connect to PyBullet")

        self.robot_id: Optional[int] = None
        self.robot_name: Optional[str] = None
        self.robot_controller: Optional[MobileRobotController] = None
        self.wall_ids: List[int] = []
        self.goal_reached = False
        self.last_waypoints: List[Tuple[float, float]] = []
        self.last_obstacles: List[ObstacleBox] = []
        self.reset_environment_hook = reset_environment_hook

        self._configure_world()
        self.plane_id = p.loadURDF("plane.urdf", physicsClientId=self.client_id)
        self.load_mobile_robot()

    def close(self) -> None:
        if self.client_id >= 0:
            p.disconnect(self.client_id)
            self.client_id = -1

    def __enter__(self) -> "PyBulletMazeSim":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def load_mobile_robot(
        self,
        urdf_path: Optional[str] = None,
        start_position: Sequence[float] = (0.0, 0.0, 0.2),
        start_yaw: float = 0.0,
    ) -> int:
        if self.robot_id is not None:
            p.removeBody(self.robot_id, physicsClientId=self.client_id)
            self.robot_id = None

        quaternion = p.getQuaternionFromEuler((0.0, 0.0, float(start_yaw)))
        if urdf_path is not None:
            self.robot_id = p.loadURDF(
                urdf_path,
                start_position,
                quaternion,
                useFixedBase=False,
                physicsClientId=self.client_id,
            )
            self.robot_name = os.path.basename(urdf_path)
        else:
            self.robot_id, self.robot_name = self._load_default_robot(start_position, quaternion)

        self.robot_controller = MobileRobotController(
            client_id=self.client_id,
            body_id=self.robot_id,
        )
        self.goal_reached = False
        return self.robot_id

    def _load_default_robot(
        self,
        start_position: Sequence[float],
        quaternion: Sequence[float],
    ) -> Tuple[int, str]:
        candidates = [
            ("husky/husky.urdf", "husky"),
            ("r2d2.urdf", "r2d2"),
        ]
        data_dir = pybullet_data.getDataPath()
        for relative_urdf, label in candidates:
            candidate_path = os.path.join(data_dir, relative_urdf)
            if not os.path.exists(candidate_path):
                continue
            try:
                robot_id = p.loadURDF(
                    relative_urdf,
                    start_position,
                    quaternion,
                    useFixedBase=False,
                    physicsClientId=self.client_id,
                )
                return robot_id, label
            except p.error:
                continue
        raise RuntimeError("Unable to load a mobile robot URDF (husky/r2d2)")

    def spawn_maze_walls(self, obstacles: Iterable[ObstacleInput]) -> List[int]:
        self.clear_maze_walls()
        parsed: List[ObstacleBox] = []
        wall_ids: List[int] = []
        for obstacle in obstacles:
            box = ObstacleBox.from_definition(obstacle)
            parsed.append(box)
            half_extents = (box.size[0] * 0.5, box.size[1] * 0.5, box.size[2] * 0.5)
            collision = p.createCollisionShape(
                p.GEOM_BOX,
                halfExtents=half_extents,
                physicsClientId=self.client_id,
            )
            visual = p.createVisualShape(
                p.GEOM_BOX,
                halfExtents=half_extents,
                rgbaColor=box.rgba,
                physicsClientId=self.client_id,
            )
            orientation = p.getQuaternionFromEuler((0.0, 0.0, box.yaw))
            wall_id = p.createMultiBody(
                baseMass=box.mass,
                baseCollisionShapeIndex=collision,
                baseVisualShapeIndex=visual,
                basePosition=box.center,
                baseOrientation=orientation,
                physicsClientId=self.client_id,
            )
            wall_ids.append(wall_id)

        self.wall_ids = wall_ids
        self.last_obstacles = parsed
        return wall_ids

    def clear_maze_walls(self) -> None:
        for wall_id in self.wall_ids:
            p.removeBody(wall_id, physicsClientId=self.client_id)
        self.wall_ids = []

    def set_waypoints(self, waypoints: Iterable[Sequence[float]]) -> None:
        if self.robot_controller is None:
            raise RuntimeError("Robot is not loaded")
        parsed: List[Tuple[float, float]] = []
        for waypoint in waypoints:
            if len(waypoint) < 2:
                raise ValueError(f"Waypoint requires x/y coordinates: {waypoint!r}")
            parsed.append((float(waypoint[0]), float(waypoint[1])))
        self.last_waypoints = parsed
        self.goal_reached = False
        self.robot_controller.set_waypoints(parsed)

    def set_reset_environment_hook(self, hook: Optional[GoalReachedHook]) -> None:
        self.reset_environment_hook = hook

    def reset_environment(
        self,
        obstacles: Optional[Iterable[ObstacleInput]] = None,
        waypoints: Optional[Iterable[Sequence[float]]] = None,
    ) -> None:
        p.resetSimulation(physicsClientId=self.client_id)
        self._configure_world()
        self.plane_id = p.loadURDF("plane.urdf", physicsClientId=self.client_id)

        self.wall_ids = []
        self.load_mobile_robot()

        if obstacles is not None:
            self.spawn_maze_walls(obstacles)
        elif self.last_obstacles:
            self.spawn_maze_walls(self.last_obstacles)

        if waypoints is not None:
            self.set_waypoints(waypoints)
        else:
            self.goal_reached = False

    def step(self, steps: int = 1, realtime: bool = False) -> bool:
        goal_hit = False
        for _ in range(max(1, int(steps))):
            if self.robot_controller is not None and self.robot_controller.has_active_path:
                if self.robot_controller.step_path_follow():
                    goal_hit = True
            p.stepSimulation(physicsClientId=self.client_id)
            if realtime and self.gui:
                time.sleep(self.time_step)

        goal_reached_now = False
        if goal_hit and not self.goal_reached:
            self.goal_reached = True
            goal_reached_now = True
            if self.reset_environment_hook is not None:
                self.reset_environment_hook(self)
        return goal_reached_now or self.goal_reached

    def run_until_goal(self, max_steps: int = 10000, realtime: bool = False) -> bool:
        for _ in range(max_steps):
            if self.step(steps=1, realtime=realtime):
                return True
        return False

    def _configure_world(self) -> None:
        p.setAdditionalSearchPath(pybullet_data.getDataPath(), physicsClientId=self.client_id)
        p.setGravity(self.gravity[0], self.gravity[1], self.gravity[2], physicsClientId=self.client_id)
        p.setTimeStep(self.time_step, physicsClientId=self.client_id)


def _parse_xyz(definition: Mapping[str, Any], keys: Sequence[str]) -> Optional[Tuple[float, float, float]]:
    for key in keys:
        if key not in definition:
            continue
        raw = definition[key]
        if isinstance(raw, Sequence) and len(raw) >= 3:
            return float(raw[0]), float(raw[1]), float(raw[2])
    return None


def _ensure_rgba(raw: Any) -> Tuple[float, float, float, float]:
    if isinstance(raw, Sequence):
        if len(raw) == 3:
            return float(raw[0]), float(raw[1]), float(raw[2]), 1.0
        if len(raw) >= 4:
            return float(raw[0]), float(raw[1]), float(raw[2]), float(raw[3])
    return 0.35, 0.35, 0.35, 1.0


class MazeEpisodeSimulator:
    """Adapter exposing `run_episode` for the project CLI."""

    def __init__(
        self,
        max_steps: int = 5000,
        cell_size: float = 1.0,
        wall_thickness: float = 0.1,
        wall_height: float = 0.8,
    ) -> None:
        self.max_steps = int(max_steps)
        self.cell_size = float(cell_size)
        self.wall_thickness = float(wall_thickness)
        self.wall_height = float(wall_height)

    def run_episode(
        self,
        maze: Any,
        plan: Any,
        *,
        gui: bool,
        seed: int | None,
    ) -> EpisodeResult:
        del seed  # deterministic behavior is controlled upstream by maze/planner seed.
        started_at = time.perf_counter()
        waypoints = self._extract_waypoints(maze, plan)
        obstacles = self._extract_obstacles(maze)

        if not waypoints:
            return EpisodeResult(success=False, steps=0, elapsed_s=time.perf_counter() - started_at)

        if p is not None and pybullet_data is not None:
            sim = PyBulletMazeSim(gui=gui)
            try:
                if obstacles:
                    sim.spawn_maze_walls(obstacles)

                sim.set_waypoints(waypoints)
                success = False
                steps = 0
                for _ in range(self.max_steps):
                    steps += 1
                    if sim.step(steps=1, realtime=gui):
                        success = True
                        break
                elapsed = time.perf_counter() - started_at
                return EpisodeResult(success=success, steps=steps, elapsed_s=elapsed)
            finally:
                sim.close()

        if mujoco is not None:
            return self._run_episode_with_mujoco(
                waypoints=waypoints,
                obstacles=obstacles,
                started_at=started_at,
            )

        steps = max(len(waypoints) - 1, 1)
        return EpisodeResult(
            success=True,
            steps=steps,
            elapsed_s=time.perf_counter() - started_at,
        )

    def _run_episode_with_mujoco(
        self,
        *,
        waypoints: list[tuple[float, float]],
        obstacles: list[ObstacleInput],
        started_at: float,
    ) -> EpisodeResult:
        assert mujoco is not None

        xml = self._build_mujoco_xml(waypoints=waypoints, obstacles=obstacles)
        model = mujoco.MjModel.from_xml_string(xml)
        data = mujoco.MjData(model)

        steps = 0
        max_steps = min(self.max_steps, max(len(waypoints), 1))
        for waypoint in waypoints[:max_steps]:
            x, y = waypoint
            data.qpos[0] = x
            data.qpos[1] = y
            data.qpos[2] = 0.12
            data.qpos[3] = 1.0
            data.qpos[4] = 0.0
            data.qpos[5] = 0.0
            data.qpos[6] = 0.0
            mujoco.mj_forward(model, data)
            mujoco.mj_step(model, data)
            steps += 1

        elapsed = time.perf_counter() - started_at
        success = steps >= len(waypoints)
        return EpisodeResult(success=success, steps=max(steps, 1), elapsed_s=elapsed)

    def _build_mujoco_xml(
        self,
        *,
        waypoints: list[tuple[float, float]],
        obstacles: list[ObstacleInput],
    ) -> str:
        start_x, start_y = waypoints[0]
        geom_lines: list[str] = []
        for idx, obstacle in enumerate(obstacles):
            box = ObstacleBox.from_definition(obstacle)
            hx = max(box.size[0] * 0.5, 0.01)
            hy = max(box.size[1] * 0.5, 0.01)
            hz = max(box.size[2] * 0.5, 0.01)
            geom_lines.append(
                (
                    f'<geom name="wall_{idx}" type="box" '
                    f'pos="{box.center[0]:.4f} {box.center[1]:.4f} {box.center[2]:.4f}" '
                    f'size="{hx:.4f} {hy:.4f} {hz:.4f}" '
                    f'rgba="0.36 0.43 0.55 1"/>'
                )
            )

        geoms_blob = "\n      ".join(geom_lines)
        return f"""<mujoco model="maze_nav">
  <option timestep="0.01" gravity="0 0 -9.81"/>
  <worldbody>
    <geom name="ground" type="plane" pos="0 0 0" size="60 60 0.1" rgba="0.15 0.18 0.24 1"/>
    {geoms_blob}
    <body name="robot" pos="{start_x:.4f} {start_y:.4f} 0.12">
      <freejoint name="robot_root"/>
      <geom name="robot_geom" type="sphere" size="0.10" rgba="0.96 0.64 0.10 1"/>
    </body>
  </worldbody>
</mujoco>
"""

    def _extract_obstacles(self, maze: Any) -> list[ObstacleInput]:
        if isinstance(maze, Mapping):
            for key in ("obstacles", "obstacle_boxes", "walls"):
                raw = maze.get(key)
                if isinstance(raw, Sequence):
                    return list(raw)

        try:
            from geometry import maze_walls_to_box_dicts
        except ImportError:
            try:
                from .geometry import maze_walls_to_box_dicts  # type: ignore[import-not-found]
            except Exception:
                maze_walls_to_box_dicts = None  # type: ignore[assignment]

        if maze_walls_to_box_dicts is None:
            return []

        if hasattr(maze, "horizontal_walls") and hasattr(maze, "vertical_walls"):
            try:
                return list(
                    maze_walls_to_box_dicts(
                        maze,
                        cell_size=self.cell_size,
                        wall_thickness=self.wall_thickness,
                        wall_height=self.wall_height,
                    )
                )
            except Exception:
                return []

        return []

    def _extract_waypoints(self, maze: Any, plan: Any) -> list[tuple[float, float]]:
        raw_path = self._extract_raw_path(maze, plan)
        points = _coerce_path_points(raw_path)
        if not points:
            return []

        if _looks_like_grid_path(points, maze):
            return [
                ((point[0] + 0.5) * self.cell_size, (point[1] + 0.5) * self.cell_size)
                for point in points
            ]
        return points

    def _extract_raw_path(self, maze: Any, plan: Any) -> Any:
        if isinstance(plan, Mapping):
            for key in ("path", "waypoints", "trajectory"):
                if key in plan:
                    return plan[key]
            if "result" in plan and isinstance(plan["result"], Mapping):
                result = plan["result"]
                for key in ("path", "waypoints", "trajectory"):
                    if key in result:
                        return result[key]

        if isinstance(plan, Sequence) and not isinstance(plan, (str, bytes, bytearray)):
            return plan

        if hasattr(maze, "shortest_path") and callable(getattr(maze, "shortest_path")):
            try:
                return maze.shortest_path()
            except Exception:
                pass

        if hasattr(maze, "start") and hasattr(maze, "goal"):
            return [getattr(maze, "start"), getattr(maze, "goal")]

        if isinstance(maze, Mapping):
            start = maze.get("start")
            goal = maze.get("goal")
            if start is not None and goal is not None:
                return [start, goal]

        return []


def _coerce_path_points(raw_path: Any) -> list[tuple[float, float]]:
    if not isinstance(raw_path, Sequence) or isinstance(raw_path, (str, bytes, bytearray)):
        return []
    points: list[tuple[float, float]] = []
    for point in raw_path:
        if not isinstance(point, Sequence) or len(point) < 2:
            continue
        points.append((float(point[0]), float(point[1])))
    return points


def _looks_like_grid_path(points: Sequence[tuple[float, float]], maze: Any) -> bool:
    width = getattr(maze, "width", None)
    height = getattr(maze, "height", None)
    if not isinstance(width, int) or not isinstance(height, int):
        return False
    if width <= 0 or height <= 0:
        return False

    for x, y in points:
        xi = int(round(x))
        yi = int(round(y))
        if abs(x - xi) > 1e-6 or abs(y - yi) > 1e-6:
            return False
        if not (0 <= xi < width and 0 <= yi < height):
            return False
    return True


def create_simulator(**kwargs: Any) -> MazeEpisodeSimulator:
    """Factory used by the CLI auto-loader."""
    return MazeEpisodeSimulator(**kwargs)
