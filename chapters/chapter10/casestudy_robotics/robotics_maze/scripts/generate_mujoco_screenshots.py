#!/usr/bin/env python3
"""Generate MuJoCo screenshots for the robotics maze simulation."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import benchmark  # noqa: E402
import geometry  # noqa: E402
import maze as maze_mod  # noqa: E402
import mujoco  # noqa: E402
import planners as base_planners  # noqa: E402
from alt_planners.r1_weighted_astar import plan_weighted_astar  # noqa: E402
from alt_planners.r8_fringe_search import plan_fringe_search  # noqa: E402


Grid = list[list[int]]
Cell = tuple[int, int]


@dataclass(frozen=True)
class ShotSpec:
    name: str
    planner_fn: Callable[[Grid, Cell, Cell], object]
    seed: int
    size: tuple[int, int]


def _to_path(result: object) -> list[Cell]:
    raw = []
    if isinstance(result, tuple) and result:
        raw = result[0]
    elif isinstance(result, dict):
        raw = result.get("path", [])
    parsed: list[Cell] = []
    for cell in raw:
        if isinstance(cell, (list, tuple)) and len(cell) == 2:
            parsed.append((int(cell[0]), int(cell[1])))
    return parsed


def _build_model_xml(
    *,
    maze_obj: maze_mod.Maze,
    start_xy: tuple[float, float],
) -> str:
    boxes = geometry.maze_walls_to_box_dicts(
        maze_obj,
        cell_size=1.0,
        wall_thickness=0.08,
        wall_height=0.55,
        merge_collinear=True,
    )

    wall_geoms: list[str] = []
    for idx, box in enumerate(boxes):
        pos = box["position"]
        dims = box["dimensions"]
        wall_geoms.append(
            (
                f'<geom name="wall_{idx}" type="box" '
                f'pos="{pos[0]:.4f} {pos[1]:.4f} {pos[2]:.4f}" '
                f'size="{dims[0] * 0.5:.4f} {dims[1] * 0.5:.4f} {dims[2] * 0.5:.4f}" '
                f'rgba="0.35 0.42 0.55 1"/>'
            )
        )

    wall_blob = "\n    ".join(wall_geoms)
    return f"""<mujoco model="maze_visual">
  <option timestep="0.01" gravity="0 0 -9.81"/>
  <visual>
    <global offwidth="1280" offheight="960"/>
    <headlight diffuse="0.95 0.95 0.95" ambient="0.25 0.25 0.25" specular="0.2 0.2 0.2"/>
    <rgba haze="0.05 0.08 0.12 1"/>
  </visual>
  <worldbody>
    <geom name="ground" type="plane" pos="0 0 0" size="60 60 0.1" rgba="0.08 0.12 0.18 1"/>
    {wall_blob}
    <body name="robot" pos="{start_xy[0]:.4f} {start_xy[1]:.4f} 0.10">
      <freejoint/>
      <geom name="robot_geom" type="sphere" size="0.12" rgba="0.96 0.67 0.12 1"/>
    </body>
  </worldbody>
</mujoco>
"""


def _render_shot(
    *,
    maze_obj: maze_mod.Maze,
    robot_xy: tuple[float, float],
    path_xy: list[tuple[float, float]],
    start_xy: tuple[float, float],
    goal_xy: tuple[float, float],
    title: str,
    subtitle: str,
    output_path: Path,
) -> None:
    xml = _build_model_xml(maze_obj=maze_obj, start_xy=robot_xy)
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    data.qpos[0] = robot_xy[0]
    data.qpos[1] = robot_xy[1]
    data.qpos[2] = 0.10
    data.qpos[3] = 1.0
    data.qpos[4] = 0.0
    data.qpos[5] = 0.0
    data.qpos[6] = 0.0
    mujoco.mj_forward(model, data)

    camera = mujoco.MjvCamera()
    mujoco.mjv_defaultCamera(camera)
    camera.type = mujoco.mjtCamera.mjCAMERA_FREE
    camera.lookat[:] = [maze_obj.width / 2.0, maze_obj.height / 2.0, 0.0]
    camera.distance = max(maze_obj.width, maze_obj.height) * 1.45
    camera.azimuth = 90.0
    camera.elevation = -89.5

    renderer = mujoco.Renderer(model, height=720, width=960)
    renderer.update_scene(data, camera=camera)
    frame = renderer.render()
    renderer.close()

    image = Image.fromarray(frame)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Overlay approximate 2D projection for debug visibility: path + start/goal + robot.
    maze_span = min(image.height - 100, image.width - 340)
    origin_x = (image.width - maze_span) // 2
    origin_y = (image.height - maze_span) // 2

    def map_xy(point: tuple[float, float]) -> tuple[int, int]:
        x, y = point
        px = int(origin_x + (x / max(maze_obj.width, 1)) * maze_span)
        py = int(origin_y + (y / max(maze_obj.height, 1)) * maze_span)
        return px, py

    if len(path_xy) >= 2:
        draw.line([map_xy(p) for p in path_xy], fill=(31, 214, 240), width=3)

    sx, sy = map_xy(start_xy)
    gx, gy = map_xy(goal_xy)
    rx, ry = map_xy(robot_xy)
    draw.ellipse((sx - 6, sy - 6, sx + 6, sy + 6), fill=(34, 197, 94))
    draw.ellipse((gx - 7, gy - 7, gx + 7, gy + 7), fill=(239, 68, 68))
    draw.ellipse((rx - 6, ry - 6, rx + 6, ry + 6), fill=(250, 204, 21))
    draw.rectangle((0, 0, image.width, 32), fill=(10, 20, 34))
    draw.text((12, 10), title, fill=(230, 236, 244), font=font)
    draw.rectangle((0, image.height - 26, image.width, image.height), fill=(10, 20, 34))
    draw.text((12, image.height - 18), subtitle, fill=(172, 184, 201), font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate deterministic MuJoCo screenshots for maze regressions."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "screenshots_mujoco",
        help="Directory where screenshots will be written.",
    )
    parser.add_argument(
        "--filename-prefix",
        default="",
        help="Optional prefix prepended to every generated PNG filename.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    output_dir: Path = args.output_dir
    filename_prefix: str = args.filename_prefix
    shots = [
        ShotSpec("astar", base_planners.astar, 111, (13, 13)),
        ShotSpec("weighted_astar", lambda g, s, e: plan_weighted_astar(g, s, e, weight=1.6), 222, (13, 13)),
        ShotSpec("fringe_search", plan_fringe_search, 333, (13, 13)),
    ]

    for idx, spec in enumerate(shots, start=1):
        maze_obj = maze_mod.generate_maze(
            width=spec.size[0],
            height=spec.size[1],
            seed=spec.seed,
            algorithm="backtracker",
        )
        grid, start, goal = benchmark.maze_to_occupancy_grid(maze_obj)
        result = spec.planner_fn(grid, start, goal)
        path = _to_path(result)
        path_xy = [(cell[1] * 0.5, cell[0] * 0.5) for cell in path]
        start_xy = (start[1] * 0.5, start[0] * 0.5)
        goal_xy = (goal[1] * 0.5, goal[0] * 0.5)
        if path:
            focus = path[min(max(int(len(path) * 0.45), 0), len(path) - 1)]
            robot_xy = (focus[1] * 0.5, focus[0] * 0.5)
        else:
            robot_xy = (maze_obj.start[0] + 0.5, maze_obj.start[1] + 0.5)

        subtitle = f"planner={spec.name} seed={spec.seed} path_nodes={len(path)}"
        out = output_dir / f"{filename_prefix}sim_mujoco_{idx}_{spec.name}.png"
        _render_shot(
            maze_obj=maze_obj,
            robot_xy=robot_xy,
            path_xy=path_xy,
            start_xy=start_xy,
            goal_xy=goal_xy,
            title=f"MuJoCo Maze Snapshot {idx}: {spec.name}",
            subtitle=subtitle,
            output_path=out,
        )
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
