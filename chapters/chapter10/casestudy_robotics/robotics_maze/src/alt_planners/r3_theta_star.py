"""Theta* any-angle planner for 8-connected occupancy grids.

This module exposes a single entry point:
    plan_theta_star(grid, start, goal) -> (path, metrics)

Coordinate convention: (row, col).
Blocked cells are truthy values in `grid`; free cells are falsy.
"""

from __future__ import annotations

from heapq import heappop, heappush
from math import inf, sqrt
from time import perf_counter
from typing import Dict, List, Sequence, Tuple

Coord = Tuple[int, int]
GridLike = Sequence[Sequence[int]]

_CARDINAL_COST = 1.0
_DIAGONAL_COST = sqrt(2.0)
_EPS = 1e-9


def _grid_shape(grid: GridLike) -> Tuple[int, int]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    return rows, cols


def _in_bounds(grid: GridLike, node: Coord) -> bool:
    rows, cols = _grid_shape(grid)
    r, c = node
    return 0 <= r < rows and 0 <= c < cols


def _is_blocked(grid: GridLike, node: Coord) -> bool:
    if not _in_bounds(grid, node):
        return True
    r, c = node
    return bool(grid[r][c])


def _distance(a: Coord, b: Coord) -> float:
    dr = abs(a[0] - b[0])
    dc = abs(a[1] - b[1])
    if dr == 1 and dc == 1:
        return _DIAGONAL_COST
    if dr + dc == 1:
        return _CARDINAL_COST
    return sqrt(float(dr * dr + dc * dc))


def _heuristic(a: Coord, b: Coord) -> float:
    dr = a[0] - b[0]
    dc = a[1] - b[1]
    return sqrt(float(dr * dr + dc * dc))


def _neighbors_8(grid: GridLike, node: Coord) -> List[Coord]:
    r, c = node
    out: List[Coord] = []

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            nxt = (r + dr, c + dc)
            if _is_blocked(grid, nxt):
                continue

            # Disallow squeezing through a blocked diagonal pinch.
            if dr != 0 and dc != 0:
                side_a = (r + dr, c)
                side_b = (r, c + dc)
                if _is_blocked(grid, side_a) and _is_blocked(grid, side_b):
                    continue

            out.append(nxt)

    return out


def _supercover_cells(a: Coord, b: Coord) -> List[Coord]:
    """Return all grid cells touched by a line segment (center-to-center)."""
    r0, c0 = a
    r1, c1 = b
    dr = r1 - r0
    dc = c1 - c0
    sr = 1 if dr > 0 else -1 if dr < 0 else 0
    sc = 1 if dc > 0 else -1 if dc < 0 else 0
    ny = abs(dr)
    nx = abs(dc)

    cells: List[Coord] = [(r0, c0)]
    if nx == 0 and ny == 0:
        return cells

    r, c = r0, c0
    ix = 0
    iy = 0
    while ix < nx or iy < ny:
        left = (1 + 2 * ix) * ny
        right = (1 + 2 * iy) * nx
        if left == right:
            c += sc
            r += sr
            ix += 1
            iy += 1
        elif left < right:
            c += sc
            ix += 1
        else:
            r += sr
            iy += 1
        cells.append((r, c))

    return cells


def _line_of_sight(grid: GridLike, a: Coord, b: Coord) -> bool:
    """Check collision-free visibility between two cells."""
    cells = _supercover_cells(a, b)

    for cell in cells:
        if _is_blocked(grid, cell):
            return False

    # Extra diagonal pinch guard for corner-touching blocked cells.
    for i in range(1, len(cells)):
        r0, c0 = cells[i - 1]
        r1, c1 = cells[i]
        if abs(r1 - r0) == 1 and abs(c1 - c0) == 1:
            if _is_blocked(grid, (r0, c1)) and _is_blocked(grid, (r1, c0)):
                return False

    return True


def _reconstruct_path(parent: Dict[Coord, Coord], start: Coord, goal: Coord) -> List[Coord]:
    if goal not in parent:
        return []

    path = [goal]
    cur = goal
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def plan_theta_star(grid: GridLike, start: Coord, goal: Coord) -> Tuple[List[Coord], Dict[str, float]]:
    """Plan an any-angle path with Theta* on an 8-connected occupancy grid.

    Returns:
        path: List[(row, col)] from start to goal, or [] if no path exists.
        metrics: Dictionary with planner timings/counters/cost info.
    """
    t0 = perf_counter()
    metrics: Dict[str, float] = {
        "success": 0.0,
        "expanded_nodes": 0.0,
        "open_pushes": 0.0,
        "los_checks": 0.0,
        "los_successes": 0.0,
        "los_cache_hits": 0.0,
        "path_nodes": 0.0,
        "path_cost": inf,
        "smoothed_segments": 0.0,
        "wall_time_ms": 0.0,
    }

    rows, cols = _grid_shape(grid)
    if rows == 0 or cols == 0:
        metrics["wall_time_ms"] = (perf_counter() - t0) * 1000.0
        return [], metrics

    if _is_blocked(grid, start) or _is_blocked(grid, goal):
        metrics["wall_time_ms"] = (perf_counter() - t0) * 1000.0
        return [], metrics

    g: Dict[Coord, float] = {start: 0.0}
    parent: Dict[Coord, Coord] = {start: start}
    open_heap: List[Tuple[float, int, Coord]] = []
    closed: set[Coord] = set()
    los_cache: Dict[Tuple[Coord, Coord], bool] = {}
    push_index = 0

    start_f = _heuristic(start, goal)
    heappush(open_heap, (start_f, push_index, start))
    metrics["open_pushes"] += 1.0
    push_index += 1

    def has_line_of_sight(a: Coord, b: Coord) -> bool:
        key = (a, b) if a <= b else (b, a)
        if key in los_cache:
            metrics["los_cache_hits"] += 1.0
            return los_cache[key]
        metrics["los_checks"] += 1.0
        visible = _line_of_sight(grid, a, b)
        if visible:
            metrics["los_successes"] += 1.0
        los_cache[key] = visible
        return visible

    while open_heap:
        _, _, current = heappop(open_heap)
        if current in closed:
            continue

        closed.add(current)
        metrics["expanded_nodes"] += 1.0

        if current == goal:
            break

        current_parent = parent[current]
        for neighbor in _neighbors_8(grid, current):
            if neighbor in closed:
                continue

            if current_parent != current and has_line_of_sight(current_parent, neighbor):
                tentative_g = g[current_parent] + _distance(current_parent, neighbor)
                tentative_parent = current_parent
            else:
                tentative_g = g[current] + _distance(current, neighbor)
                tentative_parent = current

            old_g = g.get(neighbor, inf)
            if tentative_g + _EPS < old_g:
                g[neighbor] = tentative_g
                parent[neighbor] = tentative_parent
                f = tentative_g + _heuristic(neighbor, goal)
                heappush(open_heap, (f, push_index, neighbor))
                metrics["open_pushes"] += 1.0
                push_index += 1

    path = _reconstruct_path(parent, start, goal)
    if path:
        metrics["success"] = 1.0
        metrics["path_nodes"] = float(len(path))
        metrics["path_cost"] = float(g[goal])
        smoothed = 0
        for i in range(1, len(path)):
            dr = abs(path[i][0] - path[i - 1][0])
            dc = abs(path[i][1] - path[i - 1][1])
            if max(dr, dc) > 1:
                smoothed += 1
        metrics["smoothed_segments"] = float(smoothed)
    else:
        metrics["path_nodes"] = 0.0
        metrics["path_cost"] = inf
        metrics["smoothed_segments"] = 0.0

    metrics["wall_time_ms"] = (perf_counter() - t0) * 1000.0
    return path, metrics
