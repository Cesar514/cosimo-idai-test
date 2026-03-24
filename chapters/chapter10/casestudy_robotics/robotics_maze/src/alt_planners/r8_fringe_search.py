"""R8: Fringe Search planner for 2D occupancy grids.

Fringe Search is an A*-like method that replaces the global priority queue
with iterative "f-cost threshold" passes over two node lists (`now`/`later`).
This can reduce queue overhead while preserving optimality on unit-cost grids
with an admissible and consistent heuristic.
"""

from __future__ import annotations

from math import inf
from time import perf_counter
from typing import Dict, List, Sequence, Tuple

Coord = Tuple[int, int]
Grid = Sequence[Sequence[object]]

_MOVES: Tuple[Coord, ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))


def _grid_shape(grid: Grid) -> Tuple[int, int]:
    if not grid:
        raise ValueError("grid must not be empty")
    cols = len(grid[0])
    if cols == 0:
        raise ValueError("grid must have at least one column")
    for row in grid:
        if len(row) != cols:
            raise ValueError("grid must be rectangular")
    return len(grid), cols


def _in_bounds(node: Coord, rows: int, cols: int) -> bool:
    return 0 <= node[0] < rows and 0 <= node[1] < cols


def _is_blocked(cell: object) -> bool:
    if isinstance(cell, bool):
        return cell
    if isinstance(cell, (int, float)):
        return cell != 0
    if isinstance(cell, str):
        return cell.strip().lower() in {"1", "x", "#", "wall", "blocked", "true"}
    return bool(cell)


def _manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _reconstruct_path(came_from: Dict[Coord, Coord], goal: Coord) -> List[Coord]:
    path: List[Coord] = [goal]
    node = goal
    while node in came_from:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path


def plan_fringe_search(
    grid: Grid,
    start: Coord,
    goal: Coord,
) -> Tuple[List[Coord], Dict[str, object]]:
    """Plan a path with Fringe Search on a 4-connected occupancy grid.

    Returns:
        (path, metrics)
        - path: list of (row, col) from start to goal (inclusive), or [].
        - metrics: benchmark-focused execution counters and timings.
    """

    started = perf_counter()
    metrics: Dict[str, object] = {
        "planner": "fringe_search",
        "status": "ok",
        "iterations": 0,
        "expanded_nodes": 0,
        "generated_nodes": 1,  # includes start
        "reopened_nodes": 0,
        "max_now_size": 0,
        "max_later_size": 0,
        "max_active_fringe": 0,
        "threshold_history": [],
        "path_cost": None,
        "elapsed_ms": 0.0,
    }

    try:
        rows, cols = _grid_shape(grid)
        if not _in_bounds(start, rows, cols):
            raise ValueError("start is out of bounds")
        if not _in_bounds(goal, rows, cols):
            raise ValueError("goal is out of bounds")
        if _is_blocked(grid[start[0]][start[1]]):
            raise ValueError("start is blocked")
        if _is_blocked(grid[goal[0]][goal[1]]):
            raise ValueError("goal is blocked")
    except ValueError as exc:
        metrics["status"] = "invalid_input"
        metrics["error"] = str(exc)
        metrics["generated_nodes"] = 0
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [], metrics

    if start == goal:
        metrics["path_cost"] = 0
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [start], metrics

    threshold = float(_manhattan(start, goal))
    cast_thresholds = metrics["threshold_history"]
    assert isinstance(cast_thresholds, list)
    cast_thresholds.append(threshold)

    g_score: Dict[Coord, int] = {start: 0}
    came_from: Dict[Coord, Coord] = {}

    # Store (node, g_snapshot) entries. Snapshot lets us discard stale entries
    # when a better g-value is found later.
    now: List[Tuple[Coord, int]] = [(start, 0)]

    while now:
        metrics["iterations"] = int(metrics["iterations"]) + 1
        metrics["max_now_size"] = max(int(metrics["max_now_size"]), len(now))
        f_min = inf
        later: List[Tuple[Coord, int]] = []

        while now:
            metrics["max_active_fringe"] = max(
                int(metrics["max_active_fringe"]),
                len(now) + len(later),
            )

            node, queued_g = now.pop()
            current_g = g_score.get(node, inf)
            if queued_g != current_g:
                continue

            f_cost = current_g + _manhattan(node, goal)
            if f_cost > threshold:
                later.append((node, current_g))
                if f_cost < f_min:
                    f_min = float(f_cost)
                continue

            metrics["expanded_nodes"] = int(metrics["expanded_nodes"]) + 1
            if node == goal:
                path = _reconstruct_path(came_from, goal)
                metrics["status"] = "ok"
                metrics["path_cost"] = current_g
                metrics["max_later_size"] = max(int(metrics["max_later_size"]), len(later))
                metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
                return path, metrics

            r, c = node
            for dr, dc in _MOVES:
                neighbor = (r + dr, c + dc)
                if not _in_bounds(neighbor, rows, cols):
                    continue
                if _is_blocked(grid[neighbor[0]][neighbor[1]]):
                    continue

                tentative_g = current_g + 1
                known_g = g_score.get(neighbor, inf)
                if tentative_g >= known_g:
                    continue

                if known_g < inf:
                    metrics["reopened_nodes"] = int(metrics["reopened_nodes"]) + 1

                g_score[neighbor] = tentative_g
                came_from[neighbor] = node
                metrics["generated_nodes"] = int(metrics["generated_nodes"]) + 1

                neighbor_state = (neighbor, tentative_g)
                neighbor_f = tentative_g + _manhattan(neighbor, goal)
                if neighbor_f <= threshold:
                    now.append(neighbor_state)
                    metrics["max_now_size"] = max(int(metrics["max_now_size"]), len(now))
                else:
                    later.append(neighbor_state)
                    if neighbor_f < f_min:
                        f_min = float(neighbor_f)

        metrics["max_later_size"] = max(int(metrics["max_later_size"]), len(later))
        if not later or f_min == inf:
            metrics["status"] = "no_path"
            metrics["path_cost"] = None
            metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
            return [], metrics

        threshold = float(f_min)
        cast_thresholds.append(threshold)
        now = later

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
    demo_path, demo_metrics = plan_fringe_search(demo_grid, demo_start, demo_goal)
    print("path:", demo_path)
    print("metrics:", demo_metrics)


__all__ = ["plan_fringe_search"]
