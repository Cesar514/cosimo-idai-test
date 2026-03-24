#!/usr/bin/env python3
"""Generate simulation screenshots from the robotics maze planners.

This renderer does not require PyBullet. It visualizes the real maze/planner
pipeline outputs as pseudo-3D snapshots suitable for presentation slides.
"""

from __future__ import annotations

import argparse
import math
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
import maze as maze_mod  # noqa: E402
import planners as base_planners  # noqa: E402
from alt_planners.r1_weighted_astar import plan_weighted_astar  # noqa: E402
from alt_planners.r8_fringe_search import plan_fringe_search  # noqa: E402


Grid = list[list[int]]
Cell = tuple[int, int]


@dataclass(frozen=True)
class SnapshotSpec:
    title: str
    planner_name: str
    planner_fn: Callable[[Grid, Cell, Cell], object]
    seed: int
    maze_size: tuple[int, int]
    algorithm: str = "backtracker"


def _to_path_and_metrics(result: object) -> tuple[list[Cell], dict]:
    if isinstance(result, tuple):
        path = result[0] if len(result) > 0 else []
        metrics = result[1] if len(result) > 1 and isinstance(result[1], dict) else {}
    elif isinstance(result, dict):
        path = result.get("path", [])
        metrics = result
    else:
        path = []
        metrics = {}

    parsed: list[Cell] = []
    for cell in path:
        if isinstance(cell, (list, tuple)) and len(cell) == 2:
            parsed.append((int(cell[0]), int(cell[1])))
    return parsed, metrics


def _render_snapshot(
    grid: Grid,
    start: Cell,
    goal: Cell,
    path: list[Cell],
    *,
    title: str,
    subtitle: str,
    output_path: Path,
) -> None:
    cell = 18
    margin = 42
    wall_h = 5
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    width = cols * cell + margin * 2
    height = rows * cell + margin * 2 + 56

    img = Image.new("RGB", (width, height), "#0f172a")
    draw = ImageDraw.Draw(img)

    floor_box = (
        margin - 6,
        margin - 6,
        margin + cols * cell + 6,
        margin + rows * cell + 6,
    )
    draw.rounded_rectangle(floor_box, radius=12, fill="#111827", outline="#334155", width=2)

    # Pseudo-3D walls.
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            x0 = margin + c * cell
            y0 = margin + r * cell
            x1 = x0 + cell
            y1 = y0 + cell
            draw.rectangle((x0, y0, x1, y1), fill="#475569")
            draw.polygon(
                [(x0, y0), (x1, y0), (x1 - 3, y0 - wall_h), (x0 - 3, y0 - wall_h)],
                fill="#64748b",
            )
            draw.polygon(
                [(x1, y0), (x1, y1), (x1 - 3, y1 - wall_h), (x1 - 3, y0 - wall_h)],
                fill="#334155",
            )

    # Path line.
    if len(path) >= 2:
        points = [
            (margin + c * cell + cell // 2, margin + r * cell + cell // 2)
            for r, c in path
        ]
        draw.line(points, fill="#22d3ee", width=4, joint="curve")

    def _draw_marker(cell_rc: Cell, color: str, radius: int) -> None:
        rr, cc = cell_rc
        cx = margin + cc * cell + cell // 2
        cy = margin + rr * cell + cell // 2
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)

    _draw_marker(start, "#22c55e", 6)
    _draw_marker(goal, "#ef4444", 7)

    # Robot at roughly 40% progress through path.
    if path:
        robot_idx = min(max(int(len(path) * 0.4), 0), len(path) - 1)
        robot_rc = path[robot_idx]
        rr, cc = robot_rc
        cx = margin + cc * cell + cell // 2
        cy = margin + rr * cell + cell // 2
        draw.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill="#f59e0b", outline="#fef3c7", width=2)

        # Heading arrow based on next waypoint if available.
        if robot_idx + 1 < len(path):
            nr, nc = path[robot_idx + 1]
            dx = (nc - cc) * cell
            dy = (nr - rr) * cell
            norm = math.hypot(dx, dy) or 1.0
            ux, uy = dx / norm, dy / norm
            tip = (cx + ux * 10, cy + uy * 10)
            left = (tip[0] - uy * 4 - ux * 3, tip[1] + ux * 4 - uy * 3)
            right = (tip[0] + uy * 4 - ux * 3, tip[1] - ux * 4 - uy * 3)
            draw.polygon([tip, left, right], fill="#fef3c7")

    font = ImageFont.load_default()
    draw.text((18, 12), title, fill="#e2e8f0", font=font)
    draw.text((18, height - 28), subtitle, fill="#94a3b8", font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate deterministic pseudo-3D simulation screenshots."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "screenshots",
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
    out_dir: Path = args.output_dir
    filename_prefix: str = args.filename_prefix
    specs = [
        SnapshotSpec(
            title="Simulation Snapshot 1: Baseline A*",
            planner_name="astar",
            planner_fn=base_planners.astar,
            seed=101,
            maze_size=(13, 13),
        ),
        SnapshotSpec(
            title="Simulation Snapshot 2: Weighted A*",
            planner_name="weighted_astar",
            planner_fn=lambda g, s, e: plan_weighted_astar(g, s, e, weight=1.6),
            seed=202,
            maze_size=(13, 13),
        ),
        SnapshotSpec(
            title="Simulation Snapshot 3: Fringe Search",
            planner_name="fringe_search",
            planner_fn=plan_fringe_search,
            seed=303,
            maze_size=(13, 13),
        ),
    ]

    for idx, spec in enumerate(specs, start=1):
        maze_obj = maze_mod.generate_maze(
            width=spec.maze_size[0],
            height=spec.maze_size[1],
            seed=spec.seed,
            algorithm=spec.algorithm,
        )
        grid, start, goal = benchmark.maze_to_occupancy_grid(maze_obj)
        result = spec.planner_fn(grid, start, goal)
        path, metrics = _to_path_and_metrics(result)
        elapsed = metrics.get("runtime_ms", metrics.get("elapsed_ms", metrics.get("time_ms", 0.0)))
        subtitle = (
            f"planner={spec.planner_name} seed={spec.seed} "
            f"path_len={max(len(path) - 1, 0)} elapsed_ms={float(elapsed):.3f}"
        )
        out_path = out_dir / f"{filename_prefix}sim_snapshot_{idx}_{spec.planner_name}.png"
        _render_snapshot(
            grid,
            start,
            goal,
            path,
            title=spec.title,
            subtitle=subtitle,
            output_path=out_path,
        )
        print(out_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
