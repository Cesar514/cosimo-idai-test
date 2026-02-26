"""R11: Dijkstra planner for 2D occupancy grids."""

from __future__ import annotations

import heapq
from math import inf, sqrt
from time import perf_counter
from typing import Dict, List, Sequence, Tuple

Coord = Tuple[int, int]
Grid = Sequence[Sequence[object]]

_CARDINAL_STEPS: Tuple[Coord, ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))
_DIAGONAL_STEPS: Tuple[Coord, ...] = ((-1, -1), (-1, 1), (1, 1), (1, -1))


def _grid_shape(grid: Grid) -> Tuple[int, int]:
    if not grid:
        raise ValueError("grid must not be empty")
    rows = len(grid)
    cols = len(grid[0])
    if cols == 0:
        raise ValueError("grid must have at least one column")
    for row in grid:
        if len(row) != cols:
            raise ValueError("grid must be rectangular")
    return rows, cols


def _in_bounds(rows: int, cols: int, node: Coord) -> bool:
    return 0 <= node[0] < rows and 0 <= node[1] < cols


def _is_blocked(cell: object) -> bool:
    if isinstance(cell, bool):
        return cell
    if isinstance(cell, (int, float)):
        return cell != 0
    if isinstance(cell, str):
        return cell.strip().lower() in {"1", "x", "#", "wall", "blocked", "true"}
    return bool(cell)


def _neighbors(node: Coord, rows: int, cols: int, allow_diagonal: bool) -> List[Coord]:
    steps = _CARDINAL_STEPS + _DIAGONAL_STEPS if allow_diagonal else _CARDINAL_STEPS
    neighbors: List[Coord] = []
    for dr, dc in steps:
        nxt = (node[0] + dr, node[1] + dc)
        if _in_bounds(rows, cols, nxt):
            neighbors.append(nxt)
    return neighbors


def _step_cost(current: Coord, nxt: Coord) -> float:
    return sqrt(2.0) if current[0] != nxt[0] and current[1] != nxt[1] else 1.0


def _reconstruct_path(came_from: Dict[Coord, Coord], goal: Coord) -> List[Coord]:
    path: List[Coord] = [goal]
    node = goal
    while node in came_from:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path


def plan_dijkstra(
    grid: Grid,
    start: Coord,
    goal: Coord,
    *,
    allow_diagonal: bool = False,
) -> Tuple[List[Coord], Dict[str, object]]:
    """Plan an optimal path with Dijkstra search on a 2D occupancy grid."""

    started = perf_counter()
    metrics: Dict[str, object] = {
        "planner": "r11_dijkstra",
        "status": "ok",
        "expanded_nodes": 0,
        "generated_nodes": 1,
        "frontier_peak": 1,
        "path_cost": None,
        "elapsed_ms": 0.0,
    }

    try:
        rows, cols = _grid_shape(grid)
        if not _in_bounds(rows, cols, start):
            raise ValueError("start is out of bounds")
        if not _in_bounds(rows, cols, goal):
            raise ValueError("goal is out of bounds")
        if _is_blocked(grid[start[0]][start[1]]):
            raise ValueError("start is blocked")
        if _is_blocked(grid[goal[0]][goal[1]]):
            raise ValueError("goal is blocked")
    except ValueError as exc:
        metrics["status"] = "invalid_input"
        metrics["error"] = str(exc)
        metrics["generated_nodes"] = 0
        metrics["frontier_peak"] = 0
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [], metrics

    if start == goal:
        metrics["path_cost"] = 0.0
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [start], metrics

    frontier: List[Tuple[float, int, Coord]] = [(0.0, 0, start)]
    tie = 1
    best_cost: Dict[Coord, float] = {start: 0.0}
    came_from: Dict[Coord, Coord] = {}

    while frontier:
        current_cost, _, current = heapq.heappop(frontier)
        if current_cost != best_cost.get(current):
            continue

        metrics["expanded_nodes"] = int(metrics["expanded_nodes"]) + 1
        if current == goal:
            path = _reconstruct_path(came_from, goal)
            metrics["path_cost"] = current_cost
            metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
            return path, metrics

        for nxt in _neighbors(current, rows, cols, allow_diagonal):
            if _is_blocked(grid[nxt[0]][nxt[1]]):
                continue

            new_cost = current_cost + _step_cost(current, nxt)
            if new_cost >= best_cost.get(nxt, inf):
                continue

            best_cost[nxt] = new_cost
            came_from[nxt] = current
            metrics["generated_nodes"] = int(metrics["generated_nodes"]) + 1
            heapq.heappush(frontier, (new_cost, tie, nxt))
            tie += 1

        metrics["frontier_peak"] = max(int(metrics["frontier_peak"]), len(frontier))

    metrics["status"] = "no_path"
    metrics["path_cost"] = None
    metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
    return [], metrics


def _extract_grid_triplet(maze: object) -> Tuple[Grid | None, Coord | None, Coord | None]:
    def _normalize_coord(value: object) -> Coord | None:
        if isinstance(value, (tuple, list)) and len(value) == 2:
            return int(value[0]), int(value[1])
        return None

    if isinstance(maze, dict):
        grid = maze.get("grid")
        start = maze.get("start")
        goal = maze.get("goal")
        start_coord = _normalize_coord(start)
        goal_coord = _normalize_coord(goal)
        if grid is not None and start_coord is not None and goal_coord is not None:
            return grid, start_coord, goal_coord

    if all(hasattr(maze, attr) for attr in ("grid", "start", "goal")):
        grid = getattr(maze, "grid", None)
        start_coord = _normalize_coord(getattr(maze, "start", None))
        goal_coord = _normalize_coord(getattr(maze, "goal", None))
        if grid is not None and start_coord is not None and goal_coord is not None:
            return grid, start_coord, goal_coord

    try:
        import benchmark as benchmark_mod
    except Exception:
        benchmark_mod = None
    if benchmark_mod is not None:
        converter = getattr(benchmark_mod, "maze_to_occupancy_grid", None)
        if callable(converter):
            try:
                grid, start, goal = converter(maze)
            except Exception:
                pass
            else:
                start_coord = _normalize_coord(start)
                goal_coord = _normalize_coord(goal)
                if start_coord is not None and goal_coord is not None:
                    return grid, start_coord, goal_coord
    return None, None, None


class R11DijkstraPlanner:
    """Planner adapter so main.py can load this module via `create_planner`."""

    def __init__(self, name: str = "r11_dijkstra", *, allow_diagonal: bool = False) -> None:
        self.name = name
        self._allow_diagonal = allow_diagonal

    def plan(self, maze: object, *, seed: int | None) -> Dict[str, object]:
        del seed
        grid, start, goal = _extract_grid_triplet(maze)
        if grid is None or start is None or goal is None:
            return {"path": [], "metrics": {"planner": self.name, "status": "invalid_maze"}}

        path, metrics = plan_dijkstra(
            grid,
            start,
            goal,
            allow_diagonal=self._allow_diagonal,
        )
        return {"path": path, "metrics": metrics}


Planner = R11DijkstraPlanner


def create_planner(name: str = "r11_dijkstra") -> R11DijkstraPlanner:
    return R11DijkstraPlanner(name=name)


__all__ = ["Planner", "R11DijkstraPlanner", "create_planner", "plan_dijkstra"]
