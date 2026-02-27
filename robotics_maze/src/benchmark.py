"""Benchmark harness for comparing maze planners across many generated mazes."""

from __future__ import annotations

import argparse
import csv
import importlib
import math
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Callable, Mapping

# Ensure sibling modules (maze.py, planners.py, alt_planners/*) are importable
# when benchmark.py is loaded directly from a file path.
_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

import maze as maze_mod
import planners as baseline_planners

Grid = list[list[int]]
Cell = tuple[int, int]
PlannerFn = Callable[[Grid, Cell, Cell], Any]
TrialKey = tuple[int, int, int, int, str]

ALT_PLANNER_SPECS: tuple[tuple[str, str, str], ...] = (
    ("r1_weighted_astar", "alt_planners.r1_weighted_astar", "plan_weighted_astar"),
    ("r2_bidirectional_astar", "alt_planners.r2_bidirectional_astar", "plan_bidirectional_astar"),
    ("r3_theta_star", "alt_planners.r3_theta_star", "plan_theta_star"),
    ("r4_idastar", "alt_planners.r4_idastar", "plan_idastar"),
    ("r5_jump_point_search", "alt_planners.r5_jump_point_search", "plan_jps"),
    ("r6_lpa_star", "alt_planners.r6_lpa_star", "plan_lpa_star"),
    ("r7_beam_search", "alt_planners.r7_beam_search", "plan_beam_search"),
    ("r8_fringe_search", "alt_planners.r8_fringe_search", "plan_fringe_search"),
    ("r9_bidirectional_bfs", "alt_planners.r9_bidirectional_bfs", "plan_bidirectional_bfs"),
)

DEFAULT_BENCHMARK_PLANNERS: tuple[str, ...] = (
    "astar",
    "dijkstra",
    "greedy_best_first",
    "r1_weighted_astar",
    "r2_bidirectional_astar",
    "r3_theta_star",
    "r4_idastar",
    "r5_jump_point_search",
    "r6_lpa_star",
    "r7_beam_search",
    "r8_fringe_search",
    "r9_bidirectional_bfs",
)


@dataclass(frozen=True)
class TrialResult:
    planner: str
    maze_index: int
    maze_seed: int
    width: int
    height: int
    algorithm: str
    success: bool
    solve_time_ms: float
    path_length: int | None
    expansions: int | None
    error: str | None = None


def _copy_grid(grid: Grid) -> Grid:
    return [row[:] for row in grid]


def _coerce_path(raw_path: Any) -> list[Cell]:
    if not isinstance(raw_path, (list, tuple)):
        return []
    path: list[Cell] = []
    for node in raw_path:
        if not isinstance(node, (list, tuple)) or len(node) != 2:
            return []
        try:
            path.append((int(node[0]), int(node[1])))
        except (TypeError, ValueError):
            return []
    return path


def _to_int_metric(value: Any) -> int | None:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not math.isfinite(value):
            return None
        return int(value)
    return None


def _extract_expansions(metrics: Mapping[str, Any]) -> int | None:
    preferred_keys = (
        "expansions",
        "expanded_nodes",
        "nodes_expanded",
        "nodes_expanded_total",
        "expanded",
    )
    for key in preferred_keys:
        if key in metrics:
            value = _to_int_metric(metrics[key])
            return max(value, 0) if value is not None else None

    forward = _to_int_metric(metrics.get("expanded_forward"))
    backward = _to_int_metric(metrics.get("expanded_backward"))
    if forward is not None or backward is not None:
        return max((forward or 0) + (backward or 0), 0)
    return None


def _is_blocked_cell(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "x", "#", "wall", "blocked", "true"}
    return bool(value)


def _in_bounds(cell: Cell, rows: int, cols: int) -> bool:
    return 0 <= cell[0] < rows and 0 <= cell[1] < cols


def _bresenham_segment(start: Cell, end: Cell) -> list[Cell]:
    if start == end:
        return [start]

    r0, c0 = start
    r1, c1 = end
    dr = abs(r1 - r0)
    dc = abs(c1 - c0)
    step_r = 1 if r0 < r1 else -1
    step_c = 1 if c0 < c1 else -1

    err = dc - dr
    row, col = r0, c0
    out = [(row, col)]

    while (row, col) != (r1, c1):
        e2 = 2 * err
        if e2 > -dr:
            err -= dr
            col += step_c
        if e2 < dc:
            err += dc
            row += step_r
        out.append((row, col))

    return out


def _validate_and_measure_path(
    grid: Grid,
    path: list[Cell],
    start: Cell,
    goal: Cell,
) -> tuple[bool, int | None, str | None]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if not path:
        return False, None, "Planner did not return a path."
    if path[0] != start or path[-1] != goal:
        return False, None, "Path endpoints do not match benchmark start/goal."
    if not rows or not cols:
        return False, None, "Benchmark grid is empty."

    for cell in (start, goal):
        if not _in_bounds(cell, rows, cols):
            return False, None, f"Endpoint {cell} is out of grid bounds."
        if _is_blocked_cell(grid[cell[0]][cell[1]]):
            return False, None, f"Endpoint {cell} is blocked."

    for idx, cell in enumerate(path):
        if not _in_bounds(cell, rows, cols):
            return False, None, f"Path cell out of bounds at index {idx}: {cell}."
        if _is_blocked_cell(grid[cell[0]][cell[1]]):
            return False, None, f"Path crosses blocked cell at index {idx}: {cell}."

    measured_steps = 0
    for idx in range(1, len(path)):
        segment = _bresenham_segment(path[idx - 1], path[idx])
        if segment[0] != path[idx - 1] or segment[-1] != path[idx]:
            return False, None, f"Path segment {idx - 1}->{idx} could not be rasterized."
        for segment_cell in segment[1:]:
            if not _in_bounds(segment_cell, rows, cols):
                return False, None, f"Path segment exits grid at {segment_cell}."
            if _is_blocked_cell(grid[segment_cell[0]][segment_cell[1]]):
                return False, None, f"Path segment crosses blocked cell at {segment_cell}."
        measured_steps += len(segment) - 1

    return True, measured_steps, None


def _normalize_planner_output(
    result: Any, start: Cell, goal: Cell
) -> tuple[bool, list[Cell], int | None]:
    payload: dict[str, Any] = {}
    path: list[Cell] = []

    if isinstance(result, tuple):
        if len(result) >= 1:
            path = _coerce_path(result[0])
        if len(result) >= 2 and isinstance(result[1], Mapping):
            payload = dict(result[1])
    elif isinstance(result, Mapping):
        payload = dict(result)
        path = _coerce_path(
            payload.get("path", payload.get("solution", payload.get("route", [])))
        )
    else:
        path = _coerce_path(result)

    endpoint_success = bool(path) and path[0] == start and path[-1] == goal
    explicit_success = payload.get("success")
    status = str(payload.get("status", "")).lower()

    if explicit_success is not None:
        success = bool(explicit_success) and endpoint_success
    elif status in {"success", "ok", "solved"}:
        success = endpoint_success
    else:
        success = endpoint_success

    expansions = _extract_expansions(payload)
    if not success:
        return False, [], expansions
    return True, path, expansions


def _trial_key(row: TrialResult) -> TrialKey:
    return (row.maze_index, row.maze_seed, row.width, row.height, row.algorithm)


def _safe_import(module_name: str):
    module_candidates = (module_name, f"robotics_maze.src.{module_name}")
    for name in module_candidates:
        try:
            return importlib.import_module(name)
        except ModuleNotFoundError:
            continue
    return None


def load_available_planners(include_alt: bool = True) -> dict[str, PlannerFn]:
    planners: dict[str, PlannerFn] = {}

    for name in ("astar", "dijkstra", "greedy_best_first"):
        planner_fn = getattr(baseline_planners, name, None)
        if callable(planner_fn):
            planners[name] = planner_fn

    if include_alt:
        for planner_name, module_name, fn_name in ALT_PLANNER_SPECS:
            module = _safe_import(module_name)
            planner_fn = getattr(module, fn_name, None) if module is not None else None
            if callable(planner_fn):
                planners[planner_name] = planner_fn

    return planners


def _resolve_default_benchmark_planners(available: Mapping[str, PlannerFn]) -> dict[str, PlannerFn]:
    expected = set(DEFAULT_BENCHMARK_PLANNERS)
    discovered = set(available)
    missing = sorted(expected - discovered)
    unexpected = sorted(discovered - expected)
    if missing or unexpected:
        details: list[str] = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if unexpected:
            details.append(f"unexpected: {', '.join(unexpected)}")
        raise ValueError(
            "Default benchmark planner set mismatch "
            f"({' ; '.join(details)}). "
            "Specify --planner explicitly to run a custom subset."
        )
    return {name: available[name] for name in DEFAULT_BENCHMARK_PLANNERS}


def maze_to_occupancy_grid(maze: Any) -> tuple[Grid, Cell, Cell]:
    """Convert wall-based maze representation to occupancy grid expected by planners."""
    width = int(maze.width)
    height = int(maze.height)
    grid_rows = 2 * height + 1
    grid_cols = 2 * width + 1
    grid: Grid = [[1 for _ in range(grid_cols)] for _ in range(grid_rows)]

    for y in range(height):
        for x in range(width):
            row = 2 * y + 1
            col = 2 * x + 1
            grid[row][col] = 0

            if x < width - 1 and not maze.has_wall_between((x, y), (x + 1, y)):
                grid[row][col + 1] = 0
            if y < height - 1 and not maze.has_wall_between((x, y), (x, y + 1)):
                grid[row + 1][col] = 0

    start = (2 * int(maze.start[1]) + 1, 2 * int(maze.start[0]) + 1)
    goal = (2 * int(maze.goal[1]) + 1, 2 * int(maze.goal[0]) + 1)
    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]] = 0
    return grid, start, goal


def generate_benchmark_maze(
    width: int,
    height: int,
    seed: int,
    algorithm: str = "backtracker",
) -> tuple[Grid, Cell, Cell]:
    maze = maze_mod.generate_maze(
        width=width,
        height=height,
        seed=seed,
        algorithm=algorithm,
    )
    return maze_to_occupancy_grid(maze)


def summarize_trials(trials: list[TrialResult]) -> list[dict[str, Any]]:
    grouped: dict[str, list[TrialResult]] = defaultdict(list)
    by_maze_key: dict[TrialKey, dict[str, TrialResult]] = defaultdict(dict)
    for trial in trials:
        grouped[trial.planner].append(trial)
        by_maze_key[_trial_key(trial)][trial.planner] = trial

    planner_count = len(grouped)
    shared_success_keys = {
        key
        for key, planner_trials in by_maze_key.items()
        if len(planner_trials) == planner_count and all(row.success for row in planner_trials.values())
    }

    summary_rows: list[dict[str, Any]] = []
    for planner_name in sorted(grouped):
        rows = grouped[planner_name]
        successes = [row for row in rows if row.success]
        shared_rows = [row for row in rows if _trial_key(row) in shared_success_keys]
        summary_rows.append(
            {
                "planner": planner_name,
                "runs": len(rows),
                "successes": len(successes),
                "failures": len(rows) - len(successes),
                "success_rate": len(successes) / len(rows) if rows else 0.0,
                "mean_solve_time_ms": mean(row.solve_time_ms for row in rows) if rows else 0.0,
                "shared_success_maze_count": len(shared_rows),
                "mean_shared_solve_time_ms": (
                    mean(row.solve_time_ms for row in shared_rows) if shared_rows else math.nan
                ),
                "mean_path_length": (
                    mean(row.path_length for row in successes if row.path_length is not None)
                    if successes
                    else math.nan
                ),
                "mean_shared_path_length": (
                    mean(row.path_length for row in shared_rows if row.path_length is not None)
                    if shared_rows
                    else math.nan
                ),
                "mean_expansions": (
                    mean(valid_expansions)
                    if (
                        valid_expansions := [
                            row.expansions for row in successes if row.expansions is not None
                        ]
                    )
                    else math.nan
                ),
            }
        )
    return rank_summary_rows(summary_rows)


def _rank_metric(value: float) -> float:
    return value if not math.isnan(value) else math.inf


def _comparison_time_ms(row: Mapping[str, Any]) -> float:
    shared_time = float(row.get("mean_shared_solve_time_ms", math.nan))
    if not math.isnan(shared_time):
        return shared_time
    return float(row["mean_solve_time_ms"])


def _comparison_path_length(row: Mapping[str, Any]) -> float:
    shared_path = float(row.get("mean_shared_path_length", math.nan))
    if not math.isnan(shared_path):
        return shared_path
    return float(row["mean_path_length"])


def rank_summary_rows(summary_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ranked = sorted(
        summary_rows,
        key=lambda row: (
            -float(row["success_rate"]),
            _rank_metric(_comparison_time_ms(row)),
            _rank_metric(float(row["mean_expansions"])),
            float(row["mean_solve_time_ms"]),
            str(row["planner"]),
        ),
    )
    return [{**row, "rank": idx} for idx, row in enumerate(ranked, start=1)]


def write_results_csv(trials: list[TrialResult], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "planner",
                "maze_index",
                "maze_seed",
                "width",
                "height",
                "algorithm",
                "success",
                "solve_time_ms",
                "path_length",
                "expansions",
                "error",
            ]
        )
        for row in trials:
            writer.writerow(
                [
                    row.planner,
                    row.maze_index,
                    row.maze_seed,
                    row.width,
                    row.height,
                    row.algorithm,
                    int(row.success),
                    f"{row.solve_time_ms:.6f}",
                    row.path_length if row.path_length is not None else "",
                    row.expansions if row.expansions is not None else "",
                    row.error or "",
                ]
            )
    return output_path


def _fmt_metric(value: float) -> str:
    if math.isnan(value):
        return "n/a"
    return f"{value:.2f}"


def _fmt_success(successes: int, runs: int) -> str:
    if runs <= 0:
        return "0.0% (0/0)"
    return f"{(successes / runs) * 100:.1f}% ({successes}/{runs})"


def _fmt_delta_ms(value: float) -> str:
    return f"{value:+.2f}"


def render_console_summary_table(summary_rows: list[dict[str, Any]]) -> str:
    ranked_rows = rank_summary_rows(summary_rows)
    if not ranked_rows:
        return "No planner rows to display."

    baseline_time_ms = _comparison_time_ms(ranked_rows[0])
    headers = [
        ("Rank", "right"),
        ("Planner", "left"),
        ("Success Rate", "right"),
        ("Comparable Mazes", "right"),
        ("Comparable Time (ms)", "right"),
        ("Delta vs #1 (ms)", "right"),
        ("Comparable Path", "right"),
        ("Mean Expansions", "right"),
    ]
    rows = [
        [
            str(row["rank"]),
            str(row["planner"]),
            _fmt_success(int(row["successes"]), int(row["runs"])),
            str(int(row.get("shared_success_maze_count", 0))),
            f"{_comparison_time_ms(row):.2f}",
            _fmt_delta_ms(_comparison_time_ms(row) - baseline_time_ms),
            _fmt_metric(_comparison_path_length(row)),
            _fmt_metric(float(row["mean_expansions"])),
        ]
        for row in ranked_rows
    ]
    widths = [
        max(len(headers[idx][0]), max(len(row[idx]) for row in rows))
        for idx in range(len(headers))
    ]

    def _render_row(cells: list[str]) -> str:
        rendered: list[str] = []
        for idx, cell in enumerate(cells):
            align = headers[idx][1]
            width = widths[idx]
            rendered.append(cell.rjust(width) if align == "right" else cell.ljust(width))
        return " | ".join(rendered)

    header_line = _render_row([name for name, _ in headers])
    separator_line = "-+-".join("-" * width for width in widths)
    body_lines = [_render_row(row) for row in rows]
    return "\n".join([header_line, separator_line, *body_lines])


def write_summary_markdown(
    summary_rows: list[dict[str, Any]],
    output_path: Path,
    maze_count: int,
    width: int,
    height: int,
    seed: int,
    algorithm: str,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
    ranked_rows = rank_summary_rows(summary_rows)
    baseline_time_ms = _comparison_time_ms(ranked_rows[0]) if ranked_rows else 0.0
    top_planner = str(ranked_rows[0]["planner"]) if ranked_rows else "n/a"
    lines = [
        "# Benchmark Summary",
        "",
        f"- Generated (UTC): {generated_at}",
        f"- Mazes: {maze_count}",
        f"- Maze size (cells): {width}x{height}",
        f"- Maze algorithm: {algorithm}",
        f"- Seed: {seed}",
        f"- Top planner: {top_planner}",
        "- Comparable mazes: mazes solved by every planner (shared-success set).",
        "- Ranking policy: success rate (desc), comparable solve time (asc), mean expansions (asc), mean solve time (asc), planner name (asc).",
        "",
        "| Rank | Planner | Success Rate | Comparable Mazes | Comparable Solve Time (ms) | Delta vs #1 (ms) | Comparable Path Length | Mean Expansions |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]

    for row in ranked_rows:
        lines.append(
            "| "
            + f"{row['rank']} | "
            + f"{row['planner']} | "
            + f"{_fmt_success(int(row['successes']), int(row['runs']))} | "
            + f"{int(row.get('shared_success_maze_count', 0))} | "
            + f"{_comparison_time_ms(row):.2f} | "
            + f"{_fmt_delta_ms(_comparison_time_ms(row) - baseline_time_ms)} | "
            + f"{_fmt_metric(_comparison_path_length(row))} | "
            + f"{_fmt_metric(row['mean_expansions'])} |"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def run_benchmark(
    planners: Mapping[str, PlannerFn] | None = None,
    maze_count: int = 50,
    width: int = 15,
    height: int = 15,
    seed: int = 7,
    algorithm: str = "backtracker",
) -> tuple[list[TrialResult], list[dict[str, Any]]]:
    if maze_count < 1:
        raise ValueError("maze_count must be >= 1.")
    if width < 2 or height < 2:
        raise ValueError("Maze width and height must be >= 2.")

    available = load_available_planners(include_alt=True)
    if planners is None:
        planners = _resolve_default_benchmark_planners(available)
    planner_items = sorted(planners.items(), key=lambda item: item[0])
    if not planner_items:
        raise ValueError("At least one planner is required.")
    if algorithm not in maze_mod.SUPPORTED_MAZE_ALGORITHMS:
        raise ValueError(
            f"Unsupported maze algorithm '{algorithm}'. "
            f"Expected one of {sorted(maze_mod.SUPPORTED_MAZE_ALGORITHMS)}."
        )

    trials: list[TrialResult] = []

    for maze_index in range(maze_count):
        maze_seed = seed + maze_index
        grid, start, goal = generate_benchmark_maze(
            width=width,
            height=height,
            seed=maze_seed,
            algorithm=algorithm,
        )

        # Rotate planner execution order per maze to reduce first-run cache bias.
        offset = maze_index % len(planner_items)
        ordered_items = planner_items[offset:] + planner_items[:offset]

        for planner_name, planner_fn in ordered_items:
            trial_grid = _copy_grid(grid)
            started = time.perf_counter()
            error_text: str | None = None
            try:
                raw_result = planner_fn(trial_grid, start, goal)
            except Exception as exc:
                raw_result = None
                error_text = f"{type(exc).__name__}: {exc}"
            elapsed_ms = (time.perf_counter() - started) * 1000.0

            reported_success, path, expansions = _normalize_planner_output(raw_result, start, goal)
            valid_path, path_length, validation_error = _validate_and_measure_path(
                grid=grid,
                path=path,
                start=start,
                goal=goal,
            )
            success = reported_success and valid_path
            if reported_success and not valid_path and error_text is None:
                error_text = validation_error
            trials.append(
                TrialResult(
                    planner=planner_name,
                    maze_index=maze_index,
                    maze_seed=maze_seed,
                    width=width,
                    height=height,
                    algorithm=algorithm,
                    success=success,
                    solve_time_ms=elapsed_ms,
                    path_length=path_length if success else None,
                    expansions=expansions,
                    error=error_text,
                )
            )

    return trials, summarize_trials(trials)


def run_benchmark_and_write_reports(
    planners: Mapping[str, PlannerFn] | None = None,
    maze_count: int = 50,
    width: int = 15,
    height: int = 15,
    seed: int = 7,
    algorithm: str = "backtracker",
    output_dir: Path | str | None = None,
) -> tuple[list[TrialResult], list[dict[str, Any]], Path, Path]:
    output_dir = (
        Path(output_dir)
        if output_dir is not None
        else Path(__file__).resolve().parents[1] / "results"
    )
    trials, summary_rows = run_benchmark(
        planners=planners,
        maze_count=maze_count,
        width=width,
        height=height,
        seed=seed,
        algorithm=algorithm,
    )
    csv_path = write_results_csv(trials, output_dir / "benchmark_results.csv")
    summary_path = write_summary_markdown(
        summary_rows=summary_rows,
        output_path=output_dir / "benchmark_summary.md",
        maze_count=maze_count,
        width=width,
        height=height,
        seed=seed,
        algorithm=algorithm,
    )
    return trials, summary_rows, csv_path, summary_path


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Benchmark maze planners over many generated mazes."
    )
    parser.add_argument("--mazes", type=int, default=50, help="Number of mazes to evaluate.")
    parser.add_argument("--width", type=int, default=15, help="Maze width in cells.")
    parser.add_argument("--height", type=int, default=15, help="Maze height in cells.")
    parser.add_argument("--seed", type=int, default=7, help="Benchmark seed.")
    parser.add_argument(
        "--algorithm",
        choices=sorted(maze_mod.SUPPORTED_MAZE_ALGORITHMS),
        default="backtracker",
        help="Maze generation algorithm.",
    )
    parser.add_argument(
        "--planner",
        action="append",
        help="Planner to include. Repeat to include multiple planners. Default is all available planners.",
    )
    parser.add_argument(
        "--no-alt",
        action="store_true",
        help="Only benchmark baseline planners from src/planners.py.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parents[1] / "results"),
        help="Directory where CSV + Markdown outputs are written.",
    )
    return parser


def main() -> None:
    parser = _build_cli_parser()
    args = parser.parse_args()

    available = load_available_planners(include_alt=not args.no_alt)
    if not available:
        parser.error("No planners were discovered.")

    if args.planner:
        missing = [name for name in args.planner if name not in available]
        if missing:
            parser.error(
                f"Unknown planner(s): {', '.join(missing)}. "
                f"Available: {', '.join(sorted(available))}"
            )
        selected = {name: available[name] for name in args.planner}
    elif args.no_alt:
        selected = {name: available[name] for name in sorted(available)}
    else:
        try:
            selected = _resolve_default_benchmark_planners(available)
        except ValueError as exc:
            parser.error(str(exc))

    _, summary_rows, csv_path, summary_path = run_benchmark_and_write_reports(
        planners=selected,
        maze_count=args.mazes,
        width=args.width,
        height=args.height,
        seed=args.seed,
        algorithm=args.algorithm,
        output_dir=args.output_dir,
    )

    print(f"Wrote: {csv_path}")
    print(f"Wrote: {summary_path}")
    print(
        f"Planner comparison ({args.mazes} mazes, {args.width}x{args.height}, "
        f"algorithm={args.algorithm}, seed={args.seed}):"
    )
    print(render_console_summary_table(summary_rows))


if __name__ == "__main__":
    main()
