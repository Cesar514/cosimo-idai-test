"""R12: Breadth-First Search planner for 2D occupancy grids.

Grid conventions:
- `grid[r][c] == 0` means free space.
- Non-zero means blocked.
- Motion model is 4-connected with unit edge cost.
"""

from __future__ import annotations

from collections import deque
from time import perf_counter
from typing import Deque, Dict, List, Sequence, Tuple

Coord = Tuple[int, int]
Grid = Sequence[Sequence[object]]

_MOVES: Tuple[Coord, ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))


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


def _is_blocked(grid: Grid, node: Coord) -> bool:
    cell = grid[node[0]][node[1]]
    if isinstance(cell, bool):
        return cell
    if isinstance(cell, (int, float)):
        return cell != 0
    if isinstance(cell, str):
        return cell.strip().lower() in {"1", "x", "#", "wall", "blocked", "true"}
    return bool(cell)


def _neighbors(grid: Grid, node: Coord, rows: int, cols: int) -> List[Coord]:
    r, c = node
    out: List[Coord] = []
    for dr, dc in _MOVES:
        nxt = (r + dr, c + dc)
        if _in_bounds(nxt, rows, cols) and not _is_blocked(grid, nxt):
            out.append(nxt)
    return out


def _reconstruct_path(parent: Dict[Coord, Coord], goal: Coord) -> List[Coord]:
    path: List[Coord] = [goal]
    node = goal
    while node in parent:
        node = parent[node]
        path.append(node)
    path.reverse()
    return path


def plan_bfs(grid: Grid, start: Coord, goal: Coord) -> Tuple[List[Coord], Dict[str, object]]:
    """Plan a shortest-hop path with BFS on a 2D occupancy grid.

    Returns:
        (path, metrics)
        - path: list of (row, col) coordinates from start to goal (inclusive),
          or [] if no path is found.
        - metrics: execution/diagnostic data for benchmarking and comparison.
    """

    started = perf_counter()
    metrics: Dict[str, object] = {
        "planner": "r12_bfs",
        "status": "ok",
        "expanded_nodes": 0,
        "generated_nodes": 0,
        "frontier_peak": 0,
        "path_cost": None,
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
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [], metrics

    if start == goal:
        metrics["generated_nodes"] = 1
        metrics["frontier_peak"] = 1
        metrics["path_cost"] = 0
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [start], metrics

    queue: Deque[Coord] = deque([start])
    visited = {start}
    parent: Dict[Coord, Coord] = {}

    metrics["generated_nodes"] = 1
    metrics["frontier_peak"] = 1

    while queue:
        current = queue.popleft()
        metrics["expanded_nodes"] = int(metrics["expanded_nodes"]) + 1

        if current == goal:
            path = _reconstruct_path(parent, goal)
            metrics["status"] = "ok"
            metrics["path_cost"] = len(path) - 1
            metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
            return path, metrics

        for nxt in _neighbors(grid, current, rows, cols):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = current
            queue.append(nxt)
            metrics["generated_nodes"] = int(metrics["generated_nodes"]) + 1

        metrics["frontier_peak"] = max(int(metrics["frontier_peak"]), len(queue))

    metrics["status"] = "no_path"
    metrics["path_cost"] = None
    metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
    return [], metrics


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
    demo_path, demo_metrics = plan_bfs(demo_grid, demo_start, demo_goal)
    print("path:", demo_path)
    print("metrics:", demo_metrics)


__all__ = ["plan_bfs"]
