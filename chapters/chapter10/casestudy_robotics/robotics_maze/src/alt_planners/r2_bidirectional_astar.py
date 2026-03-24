"""R2 planner: Bidirectional A* for 2D grid mazes.

The planner assumes 4-connected motion with unit step cost.
Cell conventions:
- Numeric/bool grids: 0 is free, non-zero is blocked.
- String grids: ".", " ", "S", "G", "0" are treated as free.
"""

from __future__ import annotations

import heapq
from math import inf
from time import perf_counter
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Grid = Sequence[Sequence[object]]
Point = Tuple[int, int]
Path = List[Point]


def _normalize_point(point: Sequence[int]) -> Point:
    if len(point) != 2:
        raise ValueError("Point must have 2 elements: (row, col)")
    return int(point[0]), int(point[1])


def _is_free_cell(cell: object) -> bool:
    if isinstance(cell, str):
        return cell in {".", " ", "S", "G", "0"}
    try:
        return int(cell) == 0
    except (TypeError, ValueError):
        return not bool(cell)


def _manhattan(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _neighbors(point: Point, rows: int, cols: int) -> Iterable[Point]:
    r, c = point
    for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


def _pop_valid(
    heap: List[Tuple[float, float, int, Point]],
    g_scores: Dict[Point, float],
) -> Optional[Tuple[float, float, Point]]:
    while heap:
        f_score, g_score, _, node = heapq.heappop(heap)
        if g_score == g_scores.get(node):
            return f_score, g_score, node
    return None


def _peek_valid(
    heap: List[Tuple[float, float, int, Point]],
    g_scores: Dict[Point, float],
) -> Optional[Tuple[float, float, Point]]:
    while heap:
        f_score, g_score, _, node = heap[0]
        if g_score == g_scores.get(node):
            return f_score, g_score, node
        heapq.heappop(heap)
    return None


def _reconstruct_path(
    parent_forward: Dict[Point, Optional[Point]],
    parent_backward: Dict[Point, Optional[Point]],
    bridge: Tuple[Point, Point],
) -> Path:
    meet_forward, meet_backward = bridge

    left: Path = []
    cursor: Optional[Point] = meet_forward
    while cursor is not None:
        left.append(cursor)
        cursor = parent_forward.get(cursor)
    left.reverse()

    right: Path = []
    cursor = meet_backward
    while cursor is not None:
        right.append(cursor)
        cursor = parent_backward.get(cursor)

    if left and right and left[-1] == right[0]:
        return left + right[1:]
    return left + right


def plan_bidirectional_astar(
    grid: Grid,
    start: Sequence[int],
    goal: Sequence[int],
) -> Tuple[Path, Dict[str, object]]:
    """Run bidirectional A* on a 2D grid maze.

    Returns:
        (path, metrics)
        - path: list of (row, col). Empty if no path or invalid input.
        - metrics: status/runtime/expansion details.
    """

    t0 = perf_counter()
    metrics: Dict[str, object] = {
        "algorithm": "bidirectional_astar",
        "status": "unknown",
        "path_length": 0,
        "path_cost": inf,
        "nodes_expanded_forward": 0,
        "nodes_expanded_backward": 0,
        "nodes_expanded_total": 0,
        "nodes_generated": 0,
        "runtime_ms": 0.0,
    }

    if not grid or not grid[0]:
        metrics["status"] = "invalid_grid"
        metrics["runtime_ms"] = (perf_counter() - t0) * 1000.0
        return [], metrics

    try:
        start_pt = _normalize_point(start)
        goal_pt = _normalize_point(goal)
    except (TypeError, ValueError):
        metrics["status"] = "invalid_points"
        metrics["runtime_ms"] = (perf_counter() - t0) * 1000.0
        return [], metrics

    rows, cols = len(grid), len(grid[0])

    def in_bounds(p: Point) -> bool:
        return 0 <= p[0] < rows and 0 <= p[1] < cols

    if not in_bounds(start_pt) or not in_bounds(goal_pt):
        metrics["status"] = "out_of_bounds"
        metrics["runtime_ms"] = (perf_counter() - t0) * 1000.0
        return [], metrics

    if not _is_free_cell(grid[start_pt[0]][start_pt[1]]) or not _is_free_cell(
        grid[goal_pt[0]][goal_pt[1]]
    ):
        metrics["status"] = "blocked_start_or_goal"
        metrics["runtime_ms"] = (perf_counter() - t0) * 1000.0
        return [], metrics

    if start_pt == goal_pt:
        metrics.update(
            {
                "status": "success",
                "path_length": 1,
                "path_cost": 0.0,
                "runtime_ms": (perf_counter() - t0) * 1000.0,
            }
        )
        return [start_pt], metrics

    open_forward: List[Tuple[float, float, int, Point]] = []
    open_backward: List[Tuple[float, float, int, Point]] = []
    counter = 0

    def push(heap: List[Tuple[float, float, int, Point]], node: Point, g_val: float, h_val: float) -> None:
        nonlocal counter
        counter += 1
        heapq.heappush(heap, (g_val + h_val, g_val, counter, node))

    g_forward: Dict[Point, float] = {start_pt: 0.0}
    g_backward: Dict[Point, float] = {goal_pt: 0.0}
    parent_forward: Dict[Point, Optional[Point]] = {start_pt: None}
    parent_backward: Dict[Point, Optional[Point]] = {goal_pt: None}

    push(open_forward, start_pt, 0.0, float(_manhattan(start_pt, goal_pt)))
    push(open_backward, goal_pt, 0.0, float(_manhattan(goal_pt, start_pt)))
    metrics["nodes_generated"] = 2

    best_cost = inf
    best_bridge: Optional[Tuple[Point, Point]] = None
    expanded_forward = 0
    expanded_backward = 0

    while True:
        top_forward = _peek_valid(open_forward, g_forward)
        top_backward = _peek_valid(open_backward, g_backward)

        if top_forward is None or top_backward is None:
            break

        if (
            best_bridge is not None
            and top_forward[0] >= best_cost
            and top_backward[0] >= best_cost
        ):
            break

        if top_forward[0] < top_backward[0]:
            expand_forward = True
        elif top_backward[0] < top_forward[0]:
            expand_forward = False
        else:
            expand_forward = expanded_forward <= expanded_backward
        popped = _pop_valid(
            open_forward if expand_forward else open_backward,
            g_forward if expand_forward else g_backward,
        )
        if popped is None:
            break

        _, g_current, current = popped

        if expand_forward:
            expanded_forward += 1
            other_current = g_backward.get(current)
            if other_current is not None:
                candidate = g_current + other_current
                if candidate < best_cost:
                    best_cost = candidate
                    best_bridge = (current, current)

            for nxt in _neighbors(current, rows, cols):
                if not _is_free_cell(grid[nxt[0]][nxt[1]]):
                    continue

                metrics["nodes_generated"] = int(metrics["nodes_generated"]) + 1
                tentative = g_current + 1.0

                if tentative < g_forward.get(nxt, inf):
                    g_forward[nxt] = tentative
                    parent_forward[nxt] = current
                    push(open_forward, nxt, tentative, float(_manhattan(nxt, goal_pt)))

                other = g_backward.get(nxt)
                if other is not None:
                    candidate = tentative + other
                    if candidate < best_cost:
                        best_cost = candidate
                        best_bridge = (current, nxt)
        else:
            expanded_backward += 1
            other_current = g_forward.get(current)
            if other_current is not None:
                candidate = g_current + other_current
                if candidate < best_cost:
                    best_cost = candidate
                    best_bridge = (current, current)

            for nxt in _neighbors(current, rows, cols):
                if not _is_free_cell(grid[nxt[0]][nxt[1]]):
                    continue

                metrics["nodes_generated"] = int(metrics["nodes_generated"]) + 1
                tentative = g_current + 1.0

                if tentative < g_backward.get(nxt, inf):
                    g_backward[nxt] = tentative
                    parent_backward[nxt] = current
                    push(open_backward, nxt, tentative, float(_manhattan(nxt, start_pt)))

                other = g_forward.get(nxt)
                if other is not None:
                    candidate = tentative + other
                    if candidate < best_cost:
                        best_cost = candidate
                        best_bridge = (nxt, current)

    if best_bridge is None:
        metrics.update(
            {
                "status": "no_path",
                "runtime_ms": (perf_counter() - t0) * 1000.0,
                "nodes_expanded_forward": expanded_forward,
                "nodes_expanded_backward": expanded_backward,
                "nodes_expanded_total": expanded_forward + expanded_backward,
            }
        )
        return [], metrics

    path = _reconstruct_path(parent_forward, parent_backward, best_bridge)
    metrics.update(
        {
            "status": "success",
            "path_length": len(path),
            "path_cost": float(len(path) - 1),
            "runtime_ms": (perf_counter() - t0) * 1000.0,
            "nodes_expanded_forward": expanded_forward,
            "nodes_expanded_backward": expanded_backward,
            "nodes_expanded_total": expanded_forward + expanded_backward,
            "meeting_bridge": {
                "forward_node": best_bridge[0],
                "backward_node": best_bridge[1],
            },
        }
    )
    return path, metrics


if __name__ == "__main__":
    demo_grid = [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    demo_path, demo_metrics = plan_bidirectional_astar(demo_grid, (0, 0), (4, 4))
    print("Path:", demo_path)
    print("Metrics:", demo_metrics)
