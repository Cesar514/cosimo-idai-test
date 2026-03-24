"""R9: Bidirectional BFS planner for 2D occupancy grids.

Grid conventions:
- `grid[r][c] == 0` means free space.
- Non-zero means blocked.
- Motion model is 4-connected with unit edge cost.
"""

from __future__ import annotations

from collections import deque
from math import inf
from time import perf_counter
from typing import Deque, Dict, List, Optional, Sequence, Tuple

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


def _is_blocked(grid: Grid, node: Coord) -> bool:
    return bool(grid[node[0]][node[1]])


def _neighbors(grid: Grid, node: Coord, rows: int, cols: int) -> List[Coord]:
    r, c = node
    out: List[Coord] = []
    for dr, dc in _MOVES:
        nxt = (r + dr, c + dc)
        if _in_bounds(nxt, rows, cols) and not _is_blocked(grid, nxt):
            out.append(nxt)
    return out


def _pick_better_meeting(
    best_node: Optional[Coord],
    best_cost: float,
    candidate_node: Optional[Coord],
    candidate_cost: float,
) -> Tuple[Optional[Coord], float]:
    if candidate_node is None:
        return best_node, best_cost
    if best_node is None:
        return candidate_node, candidate_cost
    if candidate_cost < best_cost:
        return candidate_node, candidate_cost
    if candidate_cost > best_cost:
        return best_node, best_cost
    return (candidate_node, candidate_cost) if candidate_node < best_node else (best_node, best_cost)


def _expand_layer(
    grid: Grid,
    queue: Deque[Coord],
    this_dist: Dict[Coord, int],
    this_parent: Dict[Coord, Optional[Coord]],
    other_dist: Dict[Coord, int],
    rows: int,
    cols: int,
    metrics: Dict[str, object],
    *,
    direction: str,
) -> Tuple[Optional[Coord], float]:
    if not queue:
        return None, inf

    layer_depth = this_dist[queue[0]]
    best_node: Optional[Coord] = None
    best_cost = inf

    while queue and this_dist[queue[0]] == layer_depth:
        node = queue.popleft()

        metrics["expanded_nodes"] = int(metrics["expanded_nodes"]) + 1
        if direction == "forward":
            metrics["expanded_forward"] = int(metrics["expanded_forward"]) + 1
        else:
            metrics["expanded_backward"] = int(metrics["expanded_backward"]) + 1

        if node in other_dist:
            candidate_cost = float(this_dist[node] + other_dist[node])
            best_node, best_cost = _pick_better_meeting(best_node, best_cost, node, candidate_cost)

        for nxt in _neighbors(grid, node, rows, cols):
            metrics["generated_nodes"] = int(metrics["generated_nodes"]) + 1
            if direction == "forward":
                metrics["generated_forward"] = int(metrics["generated_forward"]) + 1
            else:
                metrics["generated_backward"] = int(metrics["generated_backward"]) + 1

            if nxt not in this_dist:
                this_dist[nxt] = this_dist[node] + 1
                this_parent[nxt] = node
                queue.append(nxt)

            if nxt in other_dist:
                candidate_cost = float(this_dist[nxt] + other_dist[nxt])
                best_node, best_cost = _pick_better_meeting(best_node, best_cost, nxt, candidate_cost)

    return best_node, best_cost


def _reconstruct_path(
    parent_forward: Dict[Coord, Optional[Coord]],
    parent_backward: Dict[Coord, Optional[Coord]],
    meeting: Coord,
) -> List[Coord]:
    forward_segment: List[Coord] = []
    node: Optional[Coord] = meeting
    while node is not None:
        forward_segment.append(node)
        node = parent_forward[node]
    forward_segment.reverse()

    backward_segment: List[Coord] = []
    node = parent_backward[meeting]
    while node is not None:
        backward_segment.append(node)
        node = parent_backward[node]

    return forward_segment + backward_segment


def plan_bidirectional_bfs(grid: Grid, start: Coord, goal: Coord) -> Tuple[List[Coord], Dict[str, object]]:
    """Plan a shortest path with bidirectional BFS on a 2D occupancy grid.

    Returns:
        (path, metrics)
        - path: list of (row, col) coordinates from start to goal (inclusive),
          or [] if no path is found.
        - metrics: execution/diagnostic data for benchmarking and comparison.
    """

    started = perf_counter()
    metrics: Dict[str, object] = {
        "planner": "bidirectional_bfs",
        "status": "ok",
        "iterations": 0,
        "expanded_nodes": 0,
        "generated_nodes": 0,
        "expanded_forward": 0,
        "expanded_backward": 0,
        "generated_forward": 0,
        "generated_backward": 0,
        "frontier_peak": 0,
        "meeting_node": None,
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
        metrics["path_cost"] = 0
        metrics["frontier_peak"] = 1
        metrics["meeting_node"] = start
        metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
        return [start], metrics

    forward_queue: Deque[Coord] = deque([start])
    backward_queue: Deque[Coord] = deque([goal])
    forward_dist: Dict[Coord, int] = {start: 0}
    backward_dist: Dict[Coord, int] = {goal: 0}
    forward_parent: Dict[Coord, Optional[Coord]] = {start: None}
    backward_parent: Dict[Coord, Optional[Coord]] = {goal: None}

    metrics["frontier_peak"] = len(forward_queue) + len(backward_queue)

    best_meeting: Optional[Coord] = None
    best_cost = inf

    while forward_queue and backward_queue:
        metrics["iterations"] = int(metrics["iterations"]) + 1

        expand_forward = len(forward_queue) < len(backward_queue)
        if len(forward_queue) == len(backward_queue):
            expand_forward = int(metrics["iterations"]) % 2 == 1
        if expand_forward:
            candidate_node, candidate_cost = _expand_layer(
                grid,
                forward_queue,
                forward_dist,
                forward_parent,
                backward_dist,
                rows,
                cols,
                metrics,
                direction="forward",
            )
        else:
            candidate_node, candidate_cost = _expand_layer(
                grid,
                backward_queue,
                backward_dist,
                backward_parent,
                forward_dist,
                rows,
                cols,
                metrics,
                direction="backward",
            )

        best_meeting, best_cost = _pick_better_meeting(
            best_meeting,
            best_cost,
            candidate_node,
            candidate_cost,
        )
        if best_meeting is not None:
            metrics["meeting_node"] = best_meeting

        metrics["frontier_peak"] = max(
            int(metrics["frontier_peak"]),
            len(forward_queue) + len(backward_queue),
        )

        if best_meeting is not None:
            next_depth_forward = forward_dist[forward_queue[0]] if forward_queue else inf
            next_depth_backward = backward_dist[backward_queue[0]] if backward_queue else inf
            if next_depth_forward + next_depth_backward >= best_cost:
                path = _reconstruct_path(forward_parent, backward_parent, best_meeting)
                metrics["status"] = "ok"
                metrics["path_cost"] = len(path) - 1
                metrics["elapsed_ms"] = (perf_counter() - started) * 1000.0
                return path, metrics

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
    demo_path, demo_metrics = plan_bidirectional_bfs(demo_grid, demo_start, demo_goal)
    print("path:", demo_path)
    print("metrics:", demo_metrics)
