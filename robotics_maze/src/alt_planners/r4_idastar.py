"""R4: Iterative Deepening A* (IDA*) planner for 2D occupancy grids.

Grid conventions:
- `grid[r][c] == 0` means free space.
- Non-zero means blocked.
- Motion model is 4-connected with unit edge cost.
"""

from __future__ import annotations

from math import inf
from time import perf_counter
from typing import Dict, List, Sequence, Set, Tuple, Union

Coord = Tuple[int, int]
Grid = Sequence[Sequence[object]]
SearchResult = Union[float, str]
_FOUND = "FOUND"

_MOVES: Tuple[Coord, ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))


def _heuristic(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _grid_shape(grid: Grid) -> Tuple[int, int]:
    if not grid:
        raise ValueError("grid cannot be empty")
    cols = len(grid[0])
    if cols == 0:
        raise ValueError("grid rows cannot be empty")
    for row in grid:
        if len(row) != cols:
            raise ValueError("grid must be rectangular")
    return len(grid), cols


def _in_bounds(node: Coord, rows: int, cols: int) -> bool:
    return 0 <= node[0] < rows and 0 <= node[1] < cols


def _is_blocked_cell(cell: object) -> bool:
    if cell is None:
        return True
    if isinstance(cell, bool):
        return cell
    if isinstance(cell, (int, float)):
        return cell != 0
    if isinstance(cell, str):
        return cell.strip().lower() in {"1", "x", "#", "wall", "blocked", "true", "w", "@"}
    return bool(cell)


def _is_blocked(grid: Grid, node: Coord) -> bool:
    return _is_blocked_cell(grid[node[0]][node[1]])


def _ordered_neighbors(
    grid: Grid,
    node: Coord,
    goal: Coord,
    rows: int,
    cols: int,
) -> List[Coord]:
    ranked: List[Tuple[int, int, int, Coord]] = []
    r, c = node
    for dr, dc in _MOVES:
        nxt = (r + dr, c + dc)
        if not _in_bounds(nxt, rows, cols) or _is_blocked(grid, nxt):
            continue
        ranked.append((_heuristic(nxt, goal), nxt[0], nxt[1], nxt))
    ranked.sort()
    return [item[-1] for item in ranked]


def plan_idastar(grid: Grid, start: Coord, goal: Coord) -> Tuple[List[Coord], Dict[str, object]]:
    """Plan a path with IDA* on a 2D occupancy grid.

    Returns:
        (path, metrics)
        - path: list of (row, col) coordinates from start to goal (inclusive),
          or [] if no path is found.
        - metrics: execution/diagnostic data for benchmarking and comparison.
    """

    started = perf_counter()
    metrics: Dict[str, object] = {
        "planner": "idastar",
        "status": "ok",
        "iterations": 0,
        "expanded_nodes": 0,
        "generated_nodes": 0,
        "max_depth": 0,
        "threshold_history": [],
        "path_cost": None,
        "runtime_ms": 0.0,
        "elapsed_ms": 0.0,
    }

    try:
        rows, cols = _grid_shape(grid)
        if not _in_bounds(start, rows, cols):
            raise ValueError("start is out of bounds")
        if not _in_bounds(goal, rows, cols):
            raise ValueError("goal is out of bounds")
        if _is_blocked(grid, start):
            raise ValueError("start is blocked")
        if _is_blocked(grid, goal):
            raise ValueError("goal is blocked")
    except ValueError as exc:
        metrics["status"] = "invalid_input"
        metrics["error"] = str(exc)
        runtime_ms = (perf_counter() - started) * 1000.0
        metrics["runtime_ms"] = runtime_ms
        metrics["elapsed_ms"] = runtime_ms
        return [], metrics

    if start == goal:
        metrics["path_cost"] = 0
        runtime_ms = (perf_counter() - started) * 1000.0
        metrics["runtime_ms"] = runtime_ms
        metrics["elapsed_ms"] = runtime_ms
        return [start], metrics

    path: List[Coord] = [start]
    in_path: Set[Coord] = {start}

    def _search(node: Coord, g_cost: int, threshold: float) -> SearchResult:
        f_cost = g_cost + _heuristic(node, goal)
        if f_cost > threshold:
            return float(f_cost)
        if node == goal:
            return _FOUND

        metrics["expanded_nodes"] = int(metrics["expanded_nodes"]) + 1
        metrics["max_depth"] = max(int(metrics["max_depth"]), g_cost)
        next_threshold = inf

        for neighbor in _ordered_neighbors(grid, node, goal, rows, cols):
            metrics["generated_nodes"] = int(metrics["generated_nodes"]) + 1
            if neighbor in in_path:
                continue

            in_path.add(neighbor)
            path.append(neighbor)
            result = _search(neighbor, g_cost + 1, threshold)
            if result == _FOUND:
                return _FOUND
            if isinstance(result, (int, float)) and result < next_threshold:
                next_threshold = float(result)
            path.pop()
            in_path.remove(neighbor)

        return next_threshold

    threshold = float(_heuristic(start, goal))
    while True:
        metrics["iterations"] = int(metrics["iterations"]) + 1
        cast_thresholds = metrics["threshold_history"]
        assert isinstance(cast_thresholds, list)
        cast_thresholds.append(threshold)

        result = _search(start, 0, threshold)
        if result == _FOUND:
            metrics["status"] = "ok"
            metrics["path_cost"] = len(path) - 1
            runtime_ms = (perf_counter() - started) * 1000.0
            metrics["runtime_ms"] = runtime_ms
            metrics["elapsed_ms"] = runtime_ms
            return list(path), metrics

        if result == inf:
            metrics["status"] = "no_path"
            metrics["path_cost"] = None
            runtime_ms = (perf_counter() - started) * 1000.0
            metrics["runtime_ms"] = runtime_ms
            metrics["elapsed_ms"] = runtime_ms
            return [], metrics

        threshold = float(result)


if __name__ == "__main__":
    demo_grid = [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0],
    ]
    demo_start = (0, 0)
    demo_goal = (4, 4)
    demo_path, demo_metrics = plan_idastar(demo_grid, demo_start, demo_goal)
    print("path:", demo_path)
    print("metrics:", demo_metrics)
