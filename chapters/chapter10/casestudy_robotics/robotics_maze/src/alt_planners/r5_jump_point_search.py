"""R5: Jump Point Search (JPS) variant for uniform-cost 4-connected grids.

Grid conventions:
- `grid[r][c] == 0` means free space.
- Non-zero means blocked.
- Motion model is 4-connected with unit edge cost.

Notes:
- This is a practical 4-way JPS variant (not full 8-way JPS).
- It keeps A* optimality guarantees for this move model with Manhattan heuristic.
"""

from __future__ import annotations

from heapq import heappop, heappush
from time import perf_counter
from typing import Dict, List, Mapping, Optional, Sequence, Set, Tuple

Coord = Tuple[int, int]
Grid = Sequence[Sequence[int]]

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


def _is_walkable(grid: Grid, node: Coord, rows: int, cols: int) -> bool:
    return _in_bounds(node, rows, cols) and not bool(grid[node[0]][node[1]])


def _is_blocked_or_oob(grid: Grid, node: Coord, rows: int, cols: int) -> bool:
    return (not _in_bounds(node, rows, cols)) or bool(grid[node[0]][node[1]])


def _heuristic(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _sign(value: int) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def _direction(a: Coord, b: Coord) -> Coord:
    return (_sign(b[0] - a[0]), _sign(b[1] - a[1]))


def _has_forced_neighbor(
    grid: Grid,
    node: Coord,
    direction: Coord,
    rows: int,
    cols: int,
) -> bool:
    r, c = node
    dr, dc = direction

    if dr == 0:
        back_c = c - dc
        return (
            _is_blocked_or_oob(grid, (r - 1, back_c), rows, cols)
            and _is_walkable(grid, (r - 1, c), rows, cols)
        ) or (
            _is_blocked_or_oob(grid, (r + 1, back_c), rows, cols)
            and _is_walkable(grid, (r + 1, c), rows, cols)
        )

    back_r = r - dr
    return (
        _is_blocked_or_oob(grid, (back_r, c - 1), rows, cols)
        and _is_walkable(grid, (r, c - 1), rows, cols)
    ) or (
        _is_blocked_or_oob(grid, (back_r, c + 1), rows, cols)
        and _is_walkable(grid, (r, c + 1), rows, cols)
    )


def _successor_directions(
    grid: Grid,
    node: Coord,
    parent: Optional[Coord],
    rows: int,
    cols: int,
) -> List[Coord]:
    r, c = node
    if parent is None:
        directions: List[Coord] = []
        for dr, dc in _MOVES:
            nxt = (r + dr, c + dc)
            if _is_walkable(grid, nxt, rows, cols):
                directions.append((dr, dc))
        return directions

    dr, dc = _direction(parent, node)
    directions = []
    forward = (dr, dc)
    if _is_walkable(grid, (r + dr, c + dc), rows, cols):
        directions.append(forward)

    if dr == 0:
        back_c = c - dc
        if (
            _is_blocked_or_oob(grid, (r - 1, back_c), rows, cols)
            and _is_walkable(grid, (r - 1, c), rows, cols)
        ):
            directions.append((-1, 0))
        if (
            _is_blocked_or_oob(grid, (r + 1, back_c), rows, cols)
            and _is_walkable(grid, (r + 1, c), rows, cols)
        ):
            directions.append((1, 0))
    else:
        back_r = r - dr
        if (
            _is_blocked_or_oob(grid, (back_r, c - 1), rows, cols)
            and _is_walkable(grid, (r, c - 1), rows, cols)
        ):
            directions.append((0, -1))
        if (
            _is_blocked_or_oob(grid, (back_r, c + 1), rows, cols)
            and _is_walkable(grid, (r, c + 1), rows, cols)
        ):
            directions.append((0, 1))

    return directions


def _jump(
    grid: Grid,
    node: Coord,
    direction: Coord,
    goal: Coord,
    rows: int,
    cols: int,
    metrics: Dict[str, object],
) -> Optional[Coord]:
    dr, dc = direction
    r, c = node
    metrics["jump_calls"] = int(metrics["jump_calls"]) + 1

    while True:
        r += dr
        c += dc
        metrics["jump_steps"] = int(metrics["jump_steps"]) + 1
        current = (r, c)

        if not _is_walkable(grid, current, rows, cols):
            return None
        if current == goal:
            return current
        if _has_forced_neighbor(grid, current, direction, rows, cols):
            metrics["forced_stops"] = int(metrics["forced_stops"]) + 1
            return current


def _reconstruct_jump_path(
    start: Coord,
    goal: Coord,
    came_from: Mapping[Coord, Coord],
) -> List[Coord]:
    path = [goal]
    node = goal
    while node != start:
        parent = came_from.get(node)
        if parent is None:
            return []
        node = parent
        path.append(node)
    path.reverse()
    return path


def _expand_jump_path(jump_path: Sequence[Coord]) -> List[Coord]:
    if not jump_path:
        return []

    expanded: List[Coord] = [jump_path[0]]
    for idx in range(1, len(jump_path)):
        a = jump_path[idx - 1]
        b = jump_path[idx]
        dr, dc = _direction(a, b)
        if dr != 0 and dc != 0:
            raise ValueError("non-cardinal segment found in jump-point path")

        r, c = a
        while (r, c) != b:
            r += dr
            c += dc
            expanded.append((r, c))

    return expanded


def plan_jps(grid: Grid, start: Coord, goal: Coord) -> Tuple[List[Coord], Dict[str, object]]:
    """Plan a path using a practical 4-way Jump Point Search variant.

    Returns:
        (path, metrics)
        - path: list of (row, col) coordinates from start to goal (inclusive),
          or [] if no path is found.
        - metrics: execution and diagnostic values for benchmarking.
    """

    started = perf_counter()
    metrics: Dict[str, object] = {
        "planner": "jps_4way",
        "status": "ok",
        "expanded_nodes": 0,
        "generated_nodes": 0,
        "jump_calls": 0,
        "jump_steps": 0,
        "forced_stops": 0,
        "open_pushes": 0,
        "open_pops": 0,
        "max_open_size": 0,
        "pruned_neighbors": 0,
        "jump_path_length": 0,
        "path_cost": None,
        "elapsed_ms": 0.0,
    }

    try:
        rows, cols = _grid_shape(grid)
        if not _in_bounds(start, rows, cols):
            raise ValueError("start is out of bounds")
        if not _in_bounds(goal, rows, cols):
            raise ValueError("goal is out of bounds")
        if not _is_walkable(grid, start, rows, cols):
            raise ValueError("start is blocked")
        if not _is_walkable(grid, goal, rows, cols):
            raise ValueError("goal is blocked")
    except ValueError as exc:
        metrics["status"] = "invalid_input"
        metrics["error"] = str(exc)
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [], metrics

    if start == goal:
        metrics["jump_path_length"] = 1
        metrics["path_cost"] = 0
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [start], metrics

    open_heap: List[Tuple[int, int, int, Coord]] = []
    push_index = 0
    start_h = _heuristic(start, goal)
    heappush(open_heap, (start_h, 0, push_index, start))
    metrics["open_pushes"] = 1
    metrics["max_open_size"] = 1

    g_score: Dict[Coord, int] = {start: 0}
    came_from: Dict[Coord, Coord] = {}
    closed: Set[Coord] = set()
    found = False

    while open_heap:
        _, current_g, _, current = heappop(open_heap)
        metrics["open_pops"] = int(metrics["open_pops"]) + 1

        best_g = g_score.get(current)
        if best_g is None or current_g != best_g:
            continue

        if current == goal:
            found = True
            break

        if current in closed:
            continue
        closed.add(current)
        metrics["expanded_nodes"] = int(metrics["expanded_nodes"]) + 1

        parent = came_from.get(current)
        directions = _successor_directions(grid, current, parent, rows, cols)
        metrics["pruned_neighbors"] = int(metrics["pruned_neighbors"]) + (4 - len(directions))

        for direction in directions:
            jump_node = _jump(grid, current, direction, goal, rows, cols, metrics)
            if jump_node is None:
                continue

            metrics["generated_nodes"] = int(metrics["generated_nodes"]) + 1
            tentative_g = current_g + _heuristic(current, jump_node)
            if tentative_g >= g_score.get(jump_node, 10**18):
                continue

            g_score[jump_node] = tentative_g
            came_from[jump_node] = current
            push_index += 1
            priority = tentative_g + _heuristic(jump_node, goal)
            heappush(open_heap, (priority, tentative_g, push_index, jump_node))
            metrics["open_pushes"] = int(metrics["open_pushes"]) + 1
            metrics["max_open_size"] = max(int(metrics["max_open_size"]), len(open_heap))

    if not found:
        metrics["status"] = "no_path"
        metrics["path_cost"] = None
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [], metrics

    jump_path = _reconstruct_jump_path(start, goal, came_from)
    if not jump_path:
        metrics["status"] = "internal_error"
        metrics["error"] = "failed to reconstruct jump-point path"
        metrics["path_cost"] = None
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [], metrics

    full_path = _expand_jump_path(jump_path)
    metrics["jump_path_length"] = len(jump_path)
    metrics["path_cost"] = len(full_path) - 1
    metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
    return full_path, metrics


if __name__ == "__main__":
    demo_grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 1, 0, 1],
        [0, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    demo_start = (0, 0)
    demo_goal = (6, 6)
    demo_path, demo_metrics = plan_jps(demo_grid, demo_start, demo_goal)
    print("path:", demo_path)
    print("metrics:", demo_metrics)


__all__ = ["plan_jps"]
