"""R13: Greedy Best-First Search planner for occupancy grids."""

from __future__ import annotations

import heapq
from math import sqrt
from time import perf_counter
from typing import Callable, Dict, List, Sequence, Tuple

Coord = Tuple[int, int]
Grid = Sequence[Sequence[object]]
HeuristicFn = Callable[[Coord, Coord], float]

_CARDINAL_STEPS: Tuple[Coord, ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))
_DIAGONAL_STEPS: Tuple[Coord, ...] = ((-1, -1), (-1, 1), (1, 1), (1, -1))


def _manhattan(a: Coord, b: Coord) -> float:
    return float(abs(a[0] - b[0]) + abs(a[1] - b[1]))


def _euclidean(a: Coord, b: Coord) -> float:
    return sqrt(float((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))


def _chebyshev(a: Coord, b: Coord) -> float:
    return float(max(abs(a[0] - b[0]), abs(a[1] - b[1])))


def _resolve_heuristic(heuristic: str | HeuristicFn | None) -> HeuristicFn:
    if callable(heuristic):
        return heuristic
    key = "manhattan" if heuristic is None else str(heuristic).strip().lower()
    if key in {"manhattan", "l1"}:
        return _manhattan
    if key in {"euclidean", "l2"}:
        return _euclidean
    if key in {"chebyshev", "linf", "chessboard"}:
        return _chebyshev
    raise ValueError(f"Unsupported heuristic '{heuristic}'.")


def _validate_grid(grid: Grid) -> Tuple[int, int]:
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


def _is_blocked(cell: object) -> bool:
    if cell is None:
        return True
    if isinstance(cell, bool):
        return cell
    if isinstance(cell, (int, float)):
        return cell != 0
    if isinstance(cell, str):
        return cell.strip().lower() in {"1", "x", "#", "@", "wall", "blocked", "true"}
    return bool(cell)


def _neighbors(node: Coord, rows: int, cols: int, allow_diagonal: bool) -> List[Coord]:
    steps = _CARDINAL_STEPS + _DIAGONAL_STEPS if allow_diagonal else _CARDINAL_STEPS
    r, c = node
    out: List[Coord] = []
    for dr, dc in steps:
        nxt = (r + dr, c + dc)
        if _in_bounds(nxt, rows, cols):
            out.append(nxt)
    return out


def _reconstruct_path(parents: Dict[Coord, Coord], end: Coord) -> List[Coord]:
    path = [end]
    node = end
    while node in parents:
        node = parents[node]
        path.append(node)
    path.reverse()
    return path


def plan_greedy_best_first(
    grid: Grid,
    start: Coord,
    goal: Coord,
    *,
    heuristic: str | HeuristicFn | None = "manhattan",
    allow_diagonal: bool = False,
) -> Tuple[List[Coord], Dict[str, object]]:
    """Run Greedy Best-First Search on a grid using heuristic-only frontier order."""

    started = perf_counter()
    metrics: Dict[str, object] = {
        "planner": "r13_greedy_best_first",
        "status": "ok",
        "expanded_nodes": 0,
        "generated_nodes": 0,
        "visited_nodes": 0,
        "path_cost": None,
        "elapsed_ms": 0.0,
    }

    try:
        rows, cols = _validate_grid(grid)
        if not _in_bounds(start, rows, cols):
            raise ValueError("start is out of bounds")
        if not _in_bounds(goal, rows, cols):
            raise ValueError("goal is out of bounds")
        if _is_blocked(grid[start[0]][start[1]]):
            raise ValueError("start is blocked")
        if _is_blocked(grid[goal[0]][goal[1]]):
            raise ValueError("goal is blocked")
        heuristic_fn = _resolve_heuristic(heuristic)
    except ValueError as exc:
        metrics["status"] = "invalid_input"
        metrics["error"] = str(exc)
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [], metrics

    if start == goal:
        metrics["generated_nodes"] = 1
        metrics["visited_nodes"] = 1
        metrics["path_cost"] = 0
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [start], metrics

    parents: Dict[Coord, Coord] = {}
    frontier: List[Tuple[float, int, Coord]] = []
    tie = 0
    discovered: set[Coord] = {start}
    visited: set[Coord] = set()

    heapq.heappush(frontier, (heuristic_fn(start, goal), tie, start))
    tie += 1
    metrics["generated_nodes"] = 1

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in visited:
            continue

        visited.add(current)
        metrics["expanded_nodes"] = int(metrics["expanded_nodes"]) + 1

        if current == goal:
            path = _reconstruct_path(parents, current)
            metrics["visited_nodes"] = len(visited)
            metrics["path_cost"] = max(len(path) - 1, 0)
            metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
            return path, metrics

        for nxt in _neighbors(current, rows, cols, allow_diagonal):
            if nxt in discovered:
                continue
            if _is_blocked(grid[nxt[0]][nxt[1]]):
                continue

            parents[nxt] = current
            discovered.add(nxt)
            heapq.heappush(frontier, (heuristic_fn(nxt, goal), tie, nxt))
            tie += 1
            metrics["generated_nodes"] = int(metrics["generated_nodes"]) + 1

    metrics["status"] = "no_path"
    metrics["visited_nodes"] = len(visited)
    metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
    return [], metrics


__all__ = ["plan_greedy_best_first"]
