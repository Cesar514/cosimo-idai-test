"""R1 Weighted A* planner for grid mazes."""

from __future__ import annotations

import heapq
import math
import time
from typing import Dict, List, Sequence, Tuple

Coord = Tuple[int, int]
Grid = Sequence[Sequence[object]]


def _is_blocked(cell: object) -> bool:
    """Interpret common maze encodings: 0/free, non-zero or wall symbols/blocked."""
    if cell is None:
        return True
    if isinstance(cell, bool):
        return cell
    if isinstance(cell, (int, float)):
        return cell != 0
    if isinstance(cell, str):
        return cell in {"#", "X", "x", "@", "W"}
    return bool(cell)


def _validate_grid(grid: Grid) -> Tuple[int, int]:
    if not grid or not grid[0]:
        raise ValueError("grid must be a non-empty 2D structure")
    row_len = len(grid[0])
    for row in grid:
        if len(row) != row_len:
            raise ValueError("grid must be rectangular")
    return len(grid), row_len


def _manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _reconstruct_path(came_from: Dict[Coord, Coord], current: Coord) -> List[Coord]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def plan_weighted_astar(
    grid: Grid,
    start: Coord,
    goal: Coord,
    weight: float = 1.5,
) -> Tuple[List[Coord], Dict[str, float]]:
    """Plan a path with Weighted A* on a 4-connected grid.

    Args:
        grid: 2D maze grid (0/free, non-zero or wall symbols/blocked).
        start: (row, col) start coordinate.
        goal: (row, col) goal coordinate.
        weight: Heuristic inflation factor (>= 1.0).

    Returns:
        (path, metrics):
          - path: list of (row, col), empty when no path exists.
          - metrics: runtime_ms, expanded_nodes, path_cost (inf if no path).
    """
    if weight < 1.0:
        raise ValueError("weight must be >= 1.0")

    rows, cols = _validate_grid(grid)

    def in_bounds(node: Coord) -> bool:
        r, c = node
        return 0 <= r < rows and 0 <= c < cols

    if not in_bounds(start) or not in_bounds(goal):
        raise ValueError("start and goal must be within grid bounds")
    if _is_blocked(grid[start[0]][start[1]]) or _is_blocked(grid[goal[0]][goal[1]]):
        raise ValueError("start and goal must be on free cells")

    t0 = time.perf_counter()

    # (f_score, tie_breaker, g_score, node)
    open_heap: List[Tuple[float, int, int, Coord]] = [
        (weight * _manhattan(start, goal), 0, 0, start)
    ]
    tie = 1
    came_from: Dict[Coord, Coord] = {}
    g_score: Dict[Coord, int] = {start: 0}
    expanded_nodes = 0

    while open_heap:
        _, _, current_g, current = heapq.heappop(open_heap)
        # Skip stale queue entries; supports node re-expansions if a better g arrives.
        if current_g != g_score.get(current):
            continue

        expanded_nodes += 1

        if current == goal:
            path = _reconstruct_path(came_from, current)
            runtime_ms = (time.perf_counter() - t0) * 1000.0
            metrics = {
                "runtime_ms": runtime_ms,
                "expanded_nodes": float(expanded_nodes),
                "path_cost": float(current_g),
            }
            return path, metrics

        r, c = current
        for neighbor in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if not in_bounds(neighbor):
                continue
            if _is_blocked(grid[neighbor[0]][neighbor[1]]):
                continue

            tentative_g = current_g + 1
            if tentative_g < g_score.get(neighbor, math.inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + weight * _manhattan(neighbor, goal)
                heapq.heappush(open_heap, (f, tie, tentative_g, neighbor))
                tie += 1

    runtime_ms = (time.perf_counter() - t0) * 1000.0
    metrics = {
        "runtime_ms": runtime_ms,
        "expanded_nodes": float(expanded_nodes),
        "path_cost": float("inf"),
    }
    return [], metrics


if __name__ == "__main__":
    demo_grid = [
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    demo_path, demo_metrics = plan_weighted_astar(demo_grid, (0, 0), (4, 4), weight=1.5)
    print("path:", demo_path)
    print("metrics:", demo_metrics)
