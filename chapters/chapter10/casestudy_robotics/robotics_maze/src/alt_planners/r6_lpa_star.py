"""Incremental LPA* planner candidate for repeated grid replanning.

This module exposes a practical function:
    plan_lpa_star(grid, start, goal) -> (path, metrics)

Scope:
- Incremental updates are supported when `start` and `goal` stay fixed and only
  map occupancy changes between calls.
- If `start` or `goal` changes, state is reset (clear approximation boundary).
"""

from __future__ import annotations

from dataclasses import dataclass
import heapq
from time import perf_counter
from typing import Dict, List, Optional, Sequence, Tuple

GridLike = Sequence[Sequence[int]]
Node = Tuple[int, int]

_INF = float("inf")
_DIRS_4: Tuple[Tuple[int, int], ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))


@dataclass
class _CallCounters:
    """Per-call internal accounting from the priority queue."""

    pushes: int = 0
    pops: int = 0
    expanded: int = 0


class _LPAStarPlanner:
    """Forward LPA* with cached search tree for fixed start/goal."""

    def __init__(self, grid: List[List[bool]], start: Node, goal: Node) -> None:
        self.grid = [row[:] for row in grid]
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows else 0
        self.start = start
        self.goal = goal

        self.g: List[List[float]] = [[_INF] * self.cols for _ in range(self.rows)]
        self.rhs: List[List[float]] = [[_INF] * self.cols for _ in range(self.rows)]

        self._heap: List[Tuple[float, float, int, Node]] = []
        self._entry: Dict[Node, Tuple[float, float, int]] = {}
        self._counter = 0

        sr, sc = self.start
        self.rhs[sr][sc] = 0.0
        self._push_open(self.start, counters=None)

    def _in_bounds(self, node: Node) -> bool:
        r, c = node
        return 0 <= r < self.rows and 0 <= c < self.cols

    def _is_free(self, node: Node) -> bool:
        r, c = node
        return not self.grid[r][c]

    def _neighbors(self, node: Node, *, only_free: bool) -> List[Node]:
        r, c = node
        out: List[Node] = []
        for dr, dc in _DIRS_4:
            nr, nc = r + dr, c + dc
            nb = (nr, nc)
            if not self._in_bounds(nb):
                continue
            if only_free and not self._is_free(nb):
                continue
            out.append(nb)
        return out

    @staticmethod
    def _heuristic(a: Node, b: Node) -> float:
        return float(abs(a[0] - b[0]) + abs(a[1] - b[1]))

    @staticmethod
    def _key_lt(a: Tuple[float, float], b: Tuple[float, float]) -> bool:
        return a[0] < b[0] or (a[0] == b[0] and a[1] < b[1])

    def _calc_key(self, node: Node) -> Tuple[float, float]:
        r, c = node
        base = min(self.g[r][c], self.rhs[r][c])
        return (base + self._heuristic(node, self.goal), base)

    def _push_open(self, node: Node, counters: Optional[_CallCounters]) -> None:
        if node != self.start and not self._is_free(node):
            return
        k1, k2 = self._calc_key(node)
        self._counter += 1
        stamp = self._counter
        heapq.heappush(self._heap, (k1, k2, stamp, node))
        self._entry[node] = (k1, k2, stamp)
        if counters is not None:
            counters.pushes += 1

    def _discard_open(self, node: Node) -> None:
        self._entry.pop(node, None)

    def _peek_open_key(self) -> Tuple[float, float]:
        while self._heap:
            k1, k2, stamp, node = self._heap[0]
            current = self._entry.get(node)
            if current is None or current != (k1, k2, stamp):
                heapq.heappop(self._heap)
                continue
            return (k1, k2)
        return (_INF, _INF)

    def _pop_open(self, counters: _CallCounters) -> Tuple[Tuple[float, float], Optional[Node]]:
        while self._heap:
            k1, k2, stamp, node = heapq.heappop(self._heap)
            current = self._entry.get(node)
            if current is None or current != (k1, k2, stamp):
                continue
            del self._entry[node]
            counters.pops += 1
            return (k1, k2), node
        return (_INF, _INF), None

    def _update_vertex(self, node: Node, counters: Optional[_CallCounters]) -> None:
        if node != self.start:
            r, c = node
            if not self._is_free(node):
                self.rhs[r][c] = _INF
            else:
                best = _INF
                for pred in self._neighbors(node, only_free=True):
                    pr, pc = pred
                    candidate = self.g[pr][pc] + 1.0
                    if candidate < best:
                        best = candidate
                self.rhs[r][c] = best

        self._discard_open(node)
        r, c = node
        if self.g[r][c] != self.rhs[r][c]:
            self._push_open(node, counters=counters)

    def apply_grid_updates(self, new_grid: List[List[bool]], counters: _CallCounters) -> int:
        toggled = 0
        affected: set[Node] = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == new_grid[r][c]:
                    continue
                toggled += 1
                cell = (r, c)
                affected.add(cell)
                affected.update(self._neighbors(cell, only_free=False))

        if toggled == 0:
            return 0

        self.grid = [row[:] for row in new_grid]
        for node in affected:
            self._update_vertex(node, counters=counters)
        return toggled

    def compute_shortest_path(self, counters: _CallCounters) -> None:
        gr, gc = self.goal
        while self._key_lt(self._peek_open_key(), self._calc_key(self.goal)) or self.rhs[gr][gc] != self.g[gr][gc]:
            key_old, node = self._pop_open(counters)
            if node is None:
                return

            if self._key_lt(key_old, self._calc_key(node)):
                self._push_open(node, counters=counters)
                continue

            nr, nc = node
            if self.g[nr][nc] > self.rhs[nr][nc]:
                self.g[nr][nc] = self.rhs[nr][nc]
                counters.expanded += 1
                for succ in self._neighbors(node, only_free=False):
                    self._update_vertex(succ, counters=counters)
            else:
                self.g[nr][nc] = _INF
                self._update_vertex(node, counters=counters)
                counters.expanded += 1
                for succ in self._neighbors(node, only_free=False):
                    self._update_vertex(succ, counters=counters)

    def extract_path(self) -> List[Node]:
        gr, gc = self.goal
        if self.g[gr][gc] == _INF:
            return []

        path_rev: List[Node] = [self.goal]
        seen = {self.goal}
        current = self.goal
        while current != self.start:
            best_prev: Optional[Node] = None
            best_cost = _INF
            for prev in self._neighbors(current, only_free=True):
                pr, pc = prev
                candidate = self.g[pr][pc] + 1.0
                if candidate < best_cost:
                    best_cost = candidate
                    best_prev = prev

            if best_prev is None or best_cost == _INF or best_prev in seen:
                return []
            seen.add(best_prev)
            path_rev.append(best_prev)
            current = best_prev

        return list(reversed(path_rev))


_CACHE: Optional[_LPAStarPlanner] = None


def _normalize_grid(grid: GridLike) -> List[List[bool]]:
    if not grid:
        raise ValueError("grid must not be empty")
    width = len(grid[0])
    if width == 0:
        raise ValueError("grid rows must not be empty")

    normalized: List[List[bool]] = []
    for row in grid:
        if len(row) != width:
            raise ValueError("grid must be rectangular")
        normalized.append([bool(value) for value in row])
    return normalized


def _in_bounds(node: Node, rows: int, cols: int) -> bool:
    r, c = node
    return 0 <= r < rows and 0 <= c < cols


def plan_lpa_star(grid: GridLike, start: Node, goal: Node) -> Tuple[List[Node], Dict[str, object]]:
    """Plan with incremental LPA* (fixed start/goal incremental mode).

    Returns:
    - path: [(r, c), ...] from start to goal inclusive; empty if no path.
    - metrics: planner and run metadata.
    """

    t0 = perf_counter()
    counters = _CallCounters()
    normalized = _normalize_grid(grid)
    rows = len(normalized)
    cols = len(normalized[0])

    out_of_bounds = not _in_bounds(start, rows, cols) or not _in_bounds(goal, rows, cols)
    blocked_endpoint = (not out_of_bounds) and (normalized[start[0]][start[1]] or normalized[goal[0]][goal[1]])

    if out_of_bounds or blocked_endpoint:
        metrics: Dict[str, object] = {
            "planner": "lpa_star_incremental",
            "status": "invalid_query",
            "reason": "start_or_goal_out_of_bounds_or_blocked",
            "reused_tree": False,
            "full_reset": False,
            "changed_cells": 0,
            "expanded_nodes": 0,
            "queue_pushes": 0,
            "queue_pops": 0,
            "path_cost": _INF,
            "path_length": 0,
            "time_ms": round((perf_counter() - t0) * 1000.0, 3),
        }
        return [], metrics

    global _CACHE
    full_reset = False
    reused_tree = False
    changed_cells = 0
    reset_reason = "none"

    if _CACHE is None:
        _CACHE = _LPAStarPlanner(normalized, start, goal)
        full_reset = True
        reset_reason = "cold_start"
    else:
        shape_changed = (_CACHE.rows, _CACHE.cols) != (rows, cols)
        endpoints_changed = (_CACHE.start != start) or (_CACHE.goal != goal)
        if shape_changed or endpoints_changed:
            _CACHE = _LPAStarPlanner(normalized, start, goal)
            full_reset = True
            reset_reason = "shape_or_endpoint_change"
        else:
            reused_tree = True
            changed_cells = _CACHE.apply_grid_updates(normalized, counters=counters)

    _CACHE.compute_shortest_path(counters=counters)
    path = _CACHE.extract_path()
    goal_r, goal_c = _CACHE.goal
    path_cost = _CACHE.g[goal_r][goal_c]
    status = "ok" if path else "no_path"

    metrics = {
        "planner": "lpa_star_incremental",
        "status": status,
        "reused_tree": reused_tree,
        "full_reset": full_reset,
        "reset_reason": reset_reason,
        "changed_cells": changed_cells,
        "expanded_nodes": counters.expanded,
        "queue_pushes": counters.pushes,
        "queue_pops": counters.pops,
        "path_cost": path_cost,
        "path_length": max(len(path) - 1, 0),
        "time_ms": round((perf_counter() - t0) * 1000.0, 3),
    }
    return path, metrics


__all__ = ["plan_lpa_star"]
