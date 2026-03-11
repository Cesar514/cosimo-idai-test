"""PyBullet maze simulation wrapper with waypoint execution support."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
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
DEFAULT_ROBOT_URDF = "husky/husky.urdf"
SECONDARY_FALLBACK_ROBOT_URDF = "r2d2.urdf"


# Diagnostic reason codes for URDF and backend decisions
URDF_OK = "URDF_OK"
URDF_NOT_FOUND = "URDF_NOT_FOUND"
URDF_INVALID_EXTENSION = "URDF_INVALID_EXTENSION"
URDF_LOAD_ERROR = "URDF_LOAD_ERROR"
BACKEND_FALLBACK = "BACKEND_FALLBACK"


@dataclass(frozen=True)
class EpisodeResult:
    success: bool
    steps: int
    elapsed_s: float
    diagnostics: Mapping[str, Any] = field(default_factory=dict)


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
        gui_hold_seconds: float = 8.0,
        min_goal_hold_seconds: float = 0.75,
        gui_loop_step_seconds: Optional[float] = None,
    ) -> None:
        if p is None or pybullet_data is None:
            raise RuntimeError("pybullet and pybullet_data are required for PyBulletMazeSim")

        self.gui = bool(gui)
        self.time_step = float(time_step)
        self.gravity = gravity
        self.gui_hold_seconds = max(float(gui_hold_seconds), 0.0)
        self.min_goal_hold_seconds = max(float(min_goal_hold_seconds), 0.0)
        loop_step = self.time_step if gui_loop_step_seconds is None else float(gui_loop_step_seconds)
        self.gui_loop_step_seconds = max(loop_step, 1e-4)
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
        self._camera_bounds_xy: tuple[float, float, float, float] | None = None
        self._camera_target_xy: tuple[float, float] = (0.0, 0.0)
        self._camera_target_z = 0.28
        self._camera_distance = 8.0
        self._camera_yaw = 90.0
        self._camera_pitch = -78.0
        self._camera_update_interval_steps = 12
        self._camera_step_counter = 0

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
    ) -> tuple[int, Mapping[str, Any]]:
        if self.robot_id is not None:
            p.removeBody(self.robot_id, physicsClientId=self.client_id)
            self.robot_id = None

        diagnostics: dict[str, Any] = {
            "requested_urdf": urdf_path,
            "urdf_status": URDF_OK,
        }

        quaternion = p.getQuaternionFromEuler((0.0, 0.0, float(start_yaw)))
        if urdf_path is not None:
            try:
                resolved_urdf_path = _resolve_custom_urdf_path(urdf_path)
                self.robot_id = p.loadURDF(
                    resolved_urdf_path,
                    start_position,
                    quaternion,
                    useFixedBase=False,
                    physicsClientId=self.client_id,
                )
                self.robot_name = os.path.basename(resolved_urdf_path)
                diagnostics["final_urdf"] = resolved_urdf_path
            except (ValueError, FileNotFoundError) as exc:
                status = URDF_INVALID_EXTENSION if isinstance(exc, ValueError) else URDF_NOT_FOUND
                diagnostics["urdf_status"] = status
                diagnostics["urdf_error"] = str(exc)
                raise
            except p.error as exc:
                diagnostics["urdf_status"] = URDF_LOAD_ERROR
                diagnostics["urdf_error"] = str(exc)
                raise
        else:
            self.robot_id, self.robot_name, default_diag = self._load_default_robot(
                start_position, quaternion
            )
            diagnostics.update(default_diag)

        self._configure_robot_contact_dynamics(self.robot_id)
        self.robot_controller = MobileRobotController(
            client_id=self.client_id,
            body_id=self.robot_id,
        )
        self.goal_reached = False
        return self.robot_id, diagnostics

    def focus_camera(
        self,
        *,
        waypoints: Sequence[Tuple[float, float]] | None = None,
        obstacles: Sequence[ObstacleInput] | None = None,
    ) -> None:
        if not self.gui:
            return

        xs: list[float] = []
        ys: list[float] = []
        parsed_obstacles: list[ObstacleBox] = []
        if waypoints:
            for x, y in waypoints:
                xs.append(float(x))
                ys.append(float(y))
        if obstacles:
            for obstacle in obstacles:
                box = ObstacleBox.from_definition(obstacle)
                parsed_obstacles.append(box)
                xs.extend([box.center[0] - box.size[0] * 0.5, box.center[0] + box.size[0] * 0.5])
                ys.extend([box.center[1] - box.size[1] * 0.5, box.center[1] + box.size[1] * 0.5])

        robot_position = self._get_robot_position()
        if robot_position is not None:
            xs.append(robot_position[0])
            ys.append(robot_position[1])

        if not xs or not ys:
            xs = [0.0, 6.0]
            ys = [0.0, 6.0]

        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        span = max(max_x - min_x, max_y - min_y, 4.0)
        margin = max(span * 0.12, 1.0)
        min_x -= margin
        max_x += margin
        min_y -= margin
        max_y += margin
        span = max(max_x - min_x, max_y - min_y, 4.0)
        target_x = (min_x + max_x) * 0.5
        target_y = (min_y + max_y) * 0.5
        self._camera_bounds_xy = (min_x, max_x, min_y, max_y)
        self._camera_target_xy = (target_x, target_y)
        if robot_position is not None:
            self._camera_target_z = _camera_target_z_for_robot(robot_position[2])
        elif parsed_obstacles:
            max_obstacle_top = max(box.center[2] + (box.size[2] * 0.5) for box in parsed_obstacles)
            self._camera_target_z = max(max_obstacle_top * 0.5, 0.28)
        else:
            self._camera_target_z = 0.28
        self._camera_distance = max(span * 1.35, 7.5)
        self._camera_step_counter = 0

        self._apply_camera(
            target_x=target_x,
            target_y=target_y,
            target_z=self._camera_target_z,
        )
        p.configureDebugVisualizer(
            p.COV_ENABLE_GUI,
            0,
            physicsClientId=self.client_id,
        )

    def _run_gui_hold_loop(self, hold_seconds: float, loop_step_seconds: float) -> None:
        deadline = time.perf_counter() + hold_seconds
        next_tick = time.perf_counter()
        while self.client_id >= 0:
            if time.perf_counter() >= deadline:
                return
            try:
                p.stepSimulation(physicsClientId=self.client_id)
            except Exception:
                return

            next_tick += loop_step_seconds
            sleep_for = next_tick - time.perf_counter()
            if sleep_for > 0.0:
                time.sleep(sleep_for)
            else:
                # If the host is busy, realign cadence instead of spinning.
                next_tick = time.perf_counter()

    def hold_gui(
        self,
        hold_seconds: Optional[float] = None,
        *,
        min_hold_seconds: float = 0.0,
        loop_step_seconds: Optional[float] = None,
    ) -> None:
        if not self.gui or self.client_id < 0:
            return
        requested_hold = self.gui_hold_seconds if hold_seconds is None else float(hold_seconds)
        total_hold_seconds = max(requested_hold, float(min_hold_seconds), 0.0)
        if total_hold_seconds <= 0.0:
            return

        loop_step = self.gui_loop_step_seconds if loop_step_seconds is None else float(loop_step_seconds)
        self._run_gui_hold_loop(total_hold_seconds, max(loop_step, 1e-4))

    def _load_default_robot(
        self,
        start_position: Sequence[float],
        quaternion: Sequence[float],
    ) -> Tuple[int, str, Mapping[str, Any]]:
        candidates = [
            (DEFAULT_ROBOT_URDF, "husky", 0.15),
            (SECONDARY_FALLBACK_ROBOT_URDF, "r2d2", 1.0),
        ]
        data_dir = pybullet_data.getDataPath()
        primary_failure_reason: str | None = None
        diagnostics: dict[str, Any] = {"urdf_status": URDF_OK}

        for relative_urdf, label, scaling in candidates:
            candidate_path = os.path.join(data_dir, relative_urdf)
            if not os.path.exists(candidate_path):
                if relative_urdf == DEFAULT_ROBOT_URDF:
                    primary_failure_reason = (
                        f"'{DEFAULT_ROBOT_URDF}' was not found in pybullet_data ({candidate_path})."
                    )
                continue
            try:
                robot_id = p.loadURDF(
                    relative_urdf,
                    start_position,
                    quaternion,
                    useFixedBase=False,
                    globalScaling=float(scaling),
                    physicsClientId=self.client_id,
                )
                diagnostics["final_urdf"] = relative_urdf
                if relative_urdf != DEFAULT_ROBOT_URDF:
                    reason = (
                        primary_failure_reason
                        or f"'{DEFAULT_ROBOT_URDF}' failed to load."
                    )
                    _warn(
                        "Default robot URDF fallback engaged: "
                        f"{reason} Using '{relative_urdf}'."
                    )
                    diagnostics["urdf_fallback_reason"] = reason
                return robot_id, label, diagnostics
            except p.error as exc:
                if relative_urdf == DEFAULT_ROBOT_URDF:
                    primary_failure_reason = (
                        f"'{DEFAULT_ROBOT_URDF}' raised a PyBullet load error: {exc}."
                    )
                continue
        message = (
            "Unable to load default robot URDFs "
            f"('{DEFAULT_ROBOT_URDF}' then '{SECONDARY_FALLBACK_ROBOT_URDF}')."
        )
        if primary_failure_reason:
            message = f"{message} Primary failure: {primary_failure_reason}"
        diagnostics["urdf_status"] = URDF_LOAD_ERROR
        diagnostics["urdf_error"] = message
        raise RuntimeError(message)

    def _configure_robot_contact_dynamics(self, body_id: int) -> None:
        num_joints = p.getNumJoints(body_id, physicsClientId=self.client_id)

        for link_idx in range(-1, num_joints):
            try:
                p.changeDynamics(
                    body_id,
                    link_idx,
                    linearDamping=0.06,
                    angularDamping=0.08,
                    restitution=0.0,
                    physicsClientId=self.client_id,
                )
            except Exception:
                continue

        for joint_idx in range(num_joints):
            info = p.getJointInfo(body_id, joint_idx, physicsClientId=self.client_id)
            joint_name = info[1].decode("utf-8", errors="ignore").lower()
            if "wheel" not in joint_name:
                continue
            try:
                p.changeDynamics(
                    body_id,
                    joint_idx,
                    lateralFriction=1.55,
                    spinningFriction=0.03,
                    rollingFriction=0.02,
                    linearDamping=0.03,
                    angularDamping=0.06,
                    frictionAnchor=1,
                    physicsClientId=self.client_id,
                )
            except Exception:
                continue

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
            if self.gui:
                self._camera_step_counter += 1
                if self._camera_step_counter >= self._camera_update_interval_steps:
                    self._camera_step_counter = 0
                    self._update_camera_tracking()
            if realtime and self.gui:
                time.sleep(self.time_step)

        goal_reached_now = False
        if goal_hit and not self.goal_reached:
            self.goal_reached = True
            goal_reached_now = True
            if self.reset_environment_hook is not None:
                self.reset_environment_hook(self)
        return goal_reached_now or self.goal_reached

    def run_until_goal(
        self,
        max_steps: int = 10000,
        realtime: bool = False,
        *,
        hold_gui_on_success: bool = True,
        gui_hold_seconds: Optional[float] = None,
        min_hold_seconds: Optional[float] = None,
        loop_step_seconds: Optional[float] = None,
    ) -> bool:
        for _ in range(max_steps):
            if self.step(steps=1, realtime=realtime):
                if hold_gui_on_success and self.gui:
                    minimum = self.min_goal_hold_seconds if min_hold_seconds is None else float(min_hold_seconds)
                    self.hold_gui(
                        hold_seconds=gui_hold_seconds,
                        min_hold_seconds=minimum,
                        loop_step_seconds=loop_step_seconds,
                    )
                return True
        return False

    def _configure_world(self) -> None:
        p.setAdditionalSearchPath(pybullet_data.getDataPath(), physicsClientId=self.client_id)
        p.setGravity(self.gravity[0], self.gravity[1], self.gravity[2], physicsClientId=self.client_id)
        p.setTimeStep(self.time_step, physicsClientId=self.client_id)

    def _apply_camera(self, *, target_x: float, target_y: float, target_z: float) -> None:
        p.resetDebugVisualizerCamera(
            cameraDistance=self._camera_distance,
            cameraYaw=self._camera_yaw,
            cameraPitch=self._camera_pitch,
            cameraTargetPosition=(target_x, target_y, target_z),
            physicsClientId=self.client_id,
        )

    def _get_robot_position(self) -> tuple[float, float, float] | None:
        if self.robot_id is None:
            return None
        try:
            position, _ = p.getBasePositionAndOrientation(self.robot_id, physicsClientId=self.client_id)
        except p.error:
            return None
        return float(position[0]), float(position[1]), float(position[2])

    def _get_robot_xy(self) -> tuple[float, float] | None:
        position = self._get_robot_position()
        if position is None:
            return None
        return position[0], position[1]

    def _update_camera_tracking(self) -> None:
        if not self.gui or self._camera_bounds_xy is None:
            return
        robot_position = self._get_robot_position()
        if robot_position is None:
            return

        min_x, max_x, min_y, max_y = self._camera_bounds_xy
        span_x = max_x - min_x
        span_y = max_y - min_y

        # Keep most of the maze in view while nudging focus toward the robot.
        follow_margin_x = max(span_x * 0.16, 1.0)
        follow_margin_y = max(span_y * 0.16, 1.0)

        lo_x = min_x + follow_margin_x
        hi_x = max_x - follow_margin_x
        lo_y = min_y + follow_margin_y
        hi_y = max_y - follow_margin_y

        target_x = robot_position[0]
        target_y = robot_position[1]
        if lo_x <= hi_x:
            target_x = min(max(target_x, lo_x), hi_x)
        if lo_y <= hi_y:
            target_y = min(max(target_y, lo_y), hi_y)

        previous_x, previous_y = self._camera_target_xy
        previous_z = self._camera_target_z
        blend = 0.2
        smoothed_x = previous_x + (target_x - previous_x) * blend
        smoothed_y = previous_y + (target_y - previous_y) * blend
        target_z = _camera_target_z_for_robot(robot_position[2])
        smoothed_z = previous_z + (target_z - previous_z) * blend
        self._camera_target_xy = (smoothed_x, smoothed_y)
        self._camera_target_z = smoothed_z
        self._apply_camera(
            target_x=smoothed_x,
            target_y=smoothed_y,
            target_z=smoothed_z,
        )


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


def _camera_target_z_for_robot(robot_z: float) -> float:
    # Keep the camera target slightly above the robot base so the body stays centered in frame.
    return max(float(robot_z) + 0.18, 0.28)


def _resolve_custom_urdf_path(urdf_path: str) -> str:
    candidate = urdf_path.strip()
    if not candidate:
        raise ValueError("URDF path cannot be empty.")
    if not candidate.lower().endswith(".urdf"):
        raise ValueError(f"URDF path must end with '.urdf': {candidate!r}")

    expanded = os.path.abspath(os.path.expanduser(candidate))
    if os.path.isfile(expanded):
        return expanded

    if pybullet_data is not None:
        data_dir = pybullet_data.getDataPath()
        if os.path.isfile(os.path.join(data_dir, candidate)):
            return candidate

    raise FileNotFoundError(f"URDF file not found: {candidate!r}")


def _warn(message: str) -> None:
    print(f"[WARN] {message}")


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
        robot_urdf: str | None = None,
        gui_hold_seconds: float = 8.0,
        physics_backend: str = "auto",
    ) -> EpisodeResult:
        del seed  # deterministic behavior is controlled upstream by maze/planner seed.
        started_at = time.perf_counter()
        waypoints = self._extract_waypoints(maze, plan)
        obstacles = self._extract_obstacles(maze)

        if not waypoints:
            return EpisodeResult(success=False, steps=0, elapsed_s=time.perf_counter() - started_at)

        all_diagnostics: dict[str, Any] = {
            "physics_backend": physics_backend,
            "requested_urdf": robot_urdf,
            "urdf_status": URDF_OK,
        }

        if robot_urdf is not None:
            try:
                _resolve_custom_urdf_path(robot_urdf)
            except (ValueError, FileNotFoundError) as exc:
                all_diagnostics["urdf_status"] = BACKEND_FALLBACK
                all_diagnostics["urdf_fallback_reason"] = str(exc)
                robot_urdf = None

        backend = physics_backend.strip().lower()
        if backend not in {"auto", "pybullet", "mujoco"}:
            _warn(
                f"Unknown physics backend '{physics_backend}'; falling back to automatic backend selection."
            )
            backend = "auto"

        pybullet_available = p is not None and pybullet_data is not None
        mujoco_available = mujoco is not None

        if backend == "auto":
            if pybullet_available:
                backend_order = ("pybullet", "mujoco")
            elif mujoco_available:
                _warn("PyBullet is unavailable; falling back to MuJoCo.")
                backend_order = ("mujoco",)
            else:
                backend_order = ()
        elif backend == "pybullet":
            if pybullet_available:
                backend_order = ("pybullet", "mujoco")
            elif mujoco_available:
                _warn(
                    "Requested physics_backend='pybullet', but PyBullet is unavailable; "
                    "falling back to MuJoCo."
                )
                backend_order = ("mujoco",)
            else:
                backend_order = ()
        else:
            if mujoco_available:
                backend_order = ("mujoco", "pybullet")
            elif pybullet_available:
                _warn(
                    "Requested physics_backend='mujoco', but MuJoCo is unavailable; "
                    "falling back to PyBullet."
                )
                backend_order = ("pybullet",)
            else:
                backend_order = ()

        all_diagnostics.update({"physics_backend": backend, "backend_order": backend_order})

        for backend_name in backend_order:
            if backend_name == "pybullet" and pybullet_available:
                sim: PyBulletMazeSim | None = None
                try:
                    all_diagnostics["actual_backend"] = "pybullet"
                    sim = PyBulletMazeSim(gui=gui, gui_hold_seconds=gui_hold_seconds)
                    start_x, start_y = waypoints[0]
                    start_pose = (start_x, start_y, 0.24)
                    try:
                        _, urdf_diag = sim.load_mobile_robot(
                            urdf_path=robot_urdf,
                            start_position=start_pose,
                        )
                        # Preserve existing status (like BACKEND_FALLBACK from path validation)
                        if all_diagnostics.get("urdf_status") != BACKEND_FALLBACK:
                            all_diagnostics.update(urdf_diag)
                        else:
                            # If we are already in fallback, only update with details but keep status
                            for k, v in urdf_diag.items():
                                if k != "urdf_status":
                                    all_diagnostics[k] = v
                    except Exception as exc:
                        if robot_urdf:
                            _warn(
                                f"Unable to load custom robot URDF '{robot_urdf}': {exc}. "
                                "Falling back to defaults "
                                f"('{DEFAULT_ROBOT_URDF}' then '{SECONDARY_FALLBACK_ROBOT_URDF}')."
                            )
                            _, urdf_diag = sim.load_mobile_robot(
                                urdf_path=None,
                                start_position=start_pose,
                            )
                            # Ensure we don't lose the original requested_urdf in diagnostics
                            original_request = all_diagnostics.get("requested_urdf")
                            all_diagnostics.update(urdf_diag)
                            if original_request:
                                all_diagnostics["requested_urdf"] = original_request
                            # Overwrite status because we had a fallback due to custom URDF failure
                            all_diagnostics["urdf_status"] = BACKEND_FALLBACK
                            all_diagnostics["urdf_fallback_reason"] = f"Custom URDF failed: {exc}"
                        else:
                            all_diagnostics["urdf_status"] = URDF_LOAD_ERROR
                            all_diagnostics["urdf_error"] = str(exc)
                            raise RuntimeError(
                                "Unable to load default robot URDFs "
                                f"('{DEFAULT_ROBOT_URDF}' then '{SECONDARY_FALLBACK_ROBOT_URDF}')."
                            ) from exc

                    if obstacles:
                        sim.spawn_maze_walls(obstacles)

                    sim.set_waypoints(waypoints)
                    if gui:
                        sim.focus_camera(waypoints=waypoints, obstacles=obstacles)

                    success = False
                    steps = 0
                    effective_max_steps = max(self.max_steps, len(waypoints) * 350)
                    for _ in range(effective_max_steps):
                        steps += 1
                        if sim.step(steps=1, realtime=False):
                            success = True
                            break

                    if gui:
                        sim.hold_gui(
                            hold_seconds=gui_hold_seconds,
                            min_hold_seconds=sim.min_goal_hold_seconds if success else 0.0,
                        )

                    elapsed = time.perf_counter() - started_at
                    return EpisodeResult(
                        success=success,
                        steps=steps,
                        elapsed_s=elapsed,
                        diagnostics=all_diagnostics,
                    )
                except Exception as exc:
                    _warn(f"PyBullet backend failed ({exc}); trying the next available backend.")
                    all_diagnostics["pybullet_failure"] = str(exc)
                finally:
                    if sim is not None:
                        sim.close()

            if backend_name == "mujoco" and mujoco_available:
                all_diagnostics["actual_backend"] = "mujoco"
                if gui:
                    _warn(
                        "GUI visualization requires PyBullet in this project; "
                        "running MuJoCo headless fallback."
                    )
                    all_diagnostics["gui_fallback"] = True
                res = self._run_episode_with_mujoco(
                    waypoints=waypoints,
                    obstacles=obstacles,
                    started_at=started_at,
                )
                return EpisodeResult(
                    success=res.success,
                    steps=res.steps,
                    elapsed_s=res.elapsed_s,
                    diagnostics=all_diagnostics,
                )

        _warn(
            "Neither PyBullet nor MuJoCo is available; using deterministic kinematic fallback."
        )
        all_diagnostics["actual_backend"] = "kinematic_fallback"
        steps = max(len(waypoints) - 1, 1)
        return EpisodeResult(
            success=True,
            steps=steps,
            elapsed_s=time.perf_counter() - started_at,
            diagnostics=all_diagnostics,
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
            data.qvel[:] = 0.0
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
        points = _coerce_path_points(raw_path, swap_xy=_plan_path_uses_row_col(plan))
        if not points:
            return []

        if _looks_like_grid_path(points, maze):
            points = [
                ((point[0] + 0.5) * self.cell_size, (point[1] + 0.5) * self.cell_size)
                for point in points
            ]
            return _compress_collinear_waypoints(points)
        elif _looks_like_occupancy_grid_path(points, maze):
            # Occupancy-grid planners usually operate on a `(2W+1, 2H+1)` lattice.
            # Convert lattice coordinates into world meters at half-cell resolution.
            return [
                (point[0] * 0.5 * self.cell_size, point[1] * 0.5 * self.cell_size)
                for point in points
            ]
        return _compress_collinear_waypoints(points)

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

        if isinstance(plan, tuple) and len(plan) >= 1:
            # Many planners return `(path, metrics)`.
            candidate_path = plan[0]
            if isinstance(candidate_path, Sequence) and not isinstance(
                candidate_path, (str, bytes, bytearray)
            ):
                return candidate_path

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


def _coerce_path_points(raw_path: Any, *, swap_xy: bool = False) -> list[tuple[float, float]]:
    if not isinstance(raw_path, Sequence) or isinstance(raw_path, (str, bytes, bytearray)):
        return []
    points: list[tuple[float, float]] = []
    for point in raw_path:
        parsed = _extract_xy(point, swap_xy=swap_xy)
        if parsed is None:
            continue
        points.append(parsed)
    return points


def _plan_path_uses_row_col(plan: Any) -> bool:
    if not isinstance(plan, Mapping):
        return False
    metric_hints = {
        "expanded_nodes",
        "runtime_ms",
        "runtime_sec",
        "generated_nodes",
        "queue_pushes",
        "queue_pops",
    }
    return any(key in plan for key in metric_hints)


def _compress_collinear_waypoints(
    points: Sequence[tuple[float, float]],
) -> list[tuple[float, float]]:
    if len(points) <= 2:
        return list(points)

    compressed: list[tuple[float, float]] = [points[0]]
    previous_direction: tuple[int, int] | None = None
    for index in range(1, len(points)):
        dx = points[index][0] - points[index - 1][0]
        dy = points[index][1] - points[index - 1][1]
        direction = (
            0 if abs(dx) < 1e-9 else (1 if dx > 0 else -1),
            0 if abs(dy) < 1e-9 else (1 if dy > 0 else -1),
        )
        if previous_direction is None:
            previous_direction = direction
            continue
        if direction != previous_direction:
            compressed.append(points[index - 1])
            previous_direction = direction

    compressed.append(points[-1])
    return compressed


def _extract_xy(point: Any, *, swap_xy: bool = False) -> tuple[float, float] | None:
    """Normalize common path node representations into `(x, y)` floats."""
    if isinstance(point, Mapping):
        for x_key, y_key in (("x", "y"), ("col", "row"), ("c", "r")):
            if x_key in point and y_key in point:
                try:
                    return float(point[x_key]), float(point[y_key])
                except (TypeError, ValueError):
                    return None
        return None

    if not isinstance(point, Sequence) or isinstance(point, (str, bytes, bytearray)):
        return None
    if len(point) < 2:
        return None

    first, second = point[0], point[1]
    if isinstance(first, (int, float)) and isinstance(second, (int, float)):
        if swap_xy:
            return float(second), float(first)
        return float(first), float(second)

    # Some planners return tuples like `((x, y), score)` or `((x, y), parent)`.
    if isinstance(first, Sequence) and not isinstance(first, (str, bytes, bytearray)) and len(first) >= 2:
        x0, y0 = first[0], first[1]
        if isinstance(x0, (int, float)) and isinstance(y0, (int, float)):
            if swap_xy:
                return float(y0), float(x0)
            return float(x0), float(y0)

    if isinstance(second, Sequence) and not isinstance(second, (str, bytes, bytearray)) and len(second) >= 2:
        x1, y1 = second[0], second[1]
        if isinstance(x1, (int, float)) and isinstance(y1, (int, float)):
            if swap_xy:
                return float(y1), float(x1)
            return float(x1), float(y1)

    return None


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


def _looks_like_occupancy_grid_path(points: Sequence[tuple[float, float]], maze: Any) -> bool:
    width = getattr(maze, "width", None)
    height = getattr(maze, "height", None)
    if not isinstance(width, int) or not isinstance(height, int):
        return False
    if width <= 0 or height <= 0:
        return False

    limit_x = (2 * width) + 1
    limit_y = (2 * height) + 1
    inside = 0
    for x, y in points:
        xi = int(round(x))
        yi = int(round(y))
        if abs(x - xi) > 1e-6 or abs(y - yi) > 1e-6:
            return False
        if 0 <= xi <= limit_x and 0 <= yi <= limit_y:
            inside += 1

    # Require every point in range and at least one point outside the cell-grid range,
    # otherwise it is just a normal cell path.
    if inside != len(points):
        return False
    return any(x > (width - 1) or y > (height - 1) for x, y in points)


def create_simulator(**kwargs: Any) -> MazeEpisodeSimulator:
    """Factory used by the CLI auto-loader."""
    return MazeEpisodeSimulator(**kwargs)
