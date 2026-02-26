"""R7 Beam Search planner.

Beam search is a bounded-best-first approximation: at each depth we only keep
the `beam_width` most promising states by heuristic score.
"""

from __future__ import annotations

from math import inf
from time import perf_counter
from typing import Dict, List, Optional, Sequence, Tuple

Coord = Tuple[int, int]
Grid = Sequence[Sequence[int]]

_CARDINAL_STEPS: Tuple[Coord, ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))


def _manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _in_bounds(rows: int, cols: int, node: Coord) -> bool:
    return 0 <= node[0] < rows and 0 <= node[1] < cols


def _is_blocked(grid: Grid, node: Coord) -> bool:
    # Convention: 0/False = free, non-zero/True = blocked.
    return bool(grid[node[0]][node[1]])


def _reconstruct_path(parents: Dict[Coord, Optional[Coord]], end: Coord) -> List[Coord]:
    path: List[Coord] = []
    node: Optional[Coord] = end
    while node is not None:
        path.append(node)
        node = parents[node]
    path.reverse()
    return path


def _validate_grid(grid: Grid) -> Tuple[int, int]:
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


def plan_beam_search(
    grid: Grid,
    start: Coord,
    goal: Coord,
    beam_width: int = 32,
) -> Tuple[List[Coord], Dict[str, object]]:
    """Plan an approximate path from `start` to `goal` with beam search.

    Args:
        grid: 2D occupancy map (`0` free, non-zero blocked).
        start: Start coordinate as `(row, col)`.
        goal: Goal coordinate as `(row, col)`.
        beam_width: Number of states to keep per depth (>=1).

    Returns:
        Tuple `(path, metrics)`:
          - `path`: list of coordinates from start to goal, or empty if no path.
          - `metrics`: runtime and search statistics.
    """

    if beam_width < 1:
        raise ValueError("beam_width must be >= 1")

    rows, cols = _validate_grid(grid)
    if not _in_bounds(rows, cols, start) or not _in_bounds(rows, cols, goal):
        raise ValueError("start and goal must be inside grid bounds")

    t0 = perf_counter()

    if _is_blocked(grid, start) or _is_blocked(grid, goal):
        runtime_ms = (perf_counter() - t0) * 1000.0
        return [], {
            "found": False,
            "failure_reason": "blocked_start_or_goal",
            "beam_width": beam_width,
            "expanded_nodes": 0,
            "generated_nodes": 1,
            "visited_nodes": 1,
            "max_frontier_size": 1,
            "path_length": None,
            "runtime_ms": round(runtime_ms, 3),
            "optimality_guaranteed": False,
        }

    if start == goal:
        runtime_ms = (perf_counter() - t0) * 1000.0
        return [start], {
            "found": True,
            "failure_reason": None,
            "beam_width": beam_width,
            "expanded_nodes": 0,
            "generated_nodes": 1,
            "visited_nodes": 1,
            "max_frontier_size": 1,
            "path_length": 0,
            "runtime_ms": round(runtime_ms, 3),
            "optimality_guaranteed": False,
        }

    parents: Dict[Coord, Optional[Coord]] = {start: None}
    g_score: Dict[Coord, int] = {start: 0}
    beam: List[Coord] = [start]

    expanded_nodes = 0
    generated_nodes = 1
    max_frontier_size = 1
    found_goal = False

    while beam and not found_goal:
        candidate_scores: Dict[Coord, Tuple[int, int, int, int, int]] = {}

        for node in beam:
            expanded_nodes += 1
            base_g = g_score[node]

            for dr, dc in _CARDINAL_STEPS:
                nxt = (node[0] + dr, node[1] + dc)
                if not _in_bounds(rows, cols, nxt) or _is_blocked(grid, nxt):
                    continue

                new_g = base_g + 1
                if new_g >= g_score.get(nxt, inf):
                    continue

                g_score[nxt] = new_g
                parents[nxt] = node
                generated_nodes += 1

                if nxt == goal:
                    found_goal = True
                    break

                h = _manhattan(nxt, goal)
                rank = (new_g + h, h, new_g, nxt[0], nxt[1])
                prev = candidate_scores.get(nxt)
                if prev is None or rank < prev:
                    candidate_scores[nxt] = rank

            if found_goal:
                break

        if found_goal:
            break

        if not candidate_scores:
            break

        ordered = sorted(candidate_scores.values())
        beam = [(r, c) for _, _, _, r, c in ordered[:beam_width]]
        max_frontier_size = max(max_frontier_size, len(beam))

    path: List[Coord] = _reconstruct_path(parents, goal) if found_goal else []
    runtime_ms = (perf_counter() - t0) * 1000.0
    metrics: Dict[str, object] = {
        "found": found_goal,
        "failure_reason": None if found_goal else "beam_exhausted",
        "beam_width": beam_width,
        "expanded_nodes": expanded_nodes,
        "generated_nodes": generated_nodes,
        "visited_nodes": len(g_score),
        "max_frontier_size": max_frontier_size,
        "path_length": (len(path) - 1) if found_goal else None,
        "runtime_ms": round(runtime_ms, 3),
        "optimality_guaranteed": False,
    }
    return path, metrics


__all__ = ["plan_beam_search"]
