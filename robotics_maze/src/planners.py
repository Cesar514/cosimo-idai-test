"""Grid planner baselines and registry interface."""

from __future__ import annotations

import heapq
import time
from itertools import count
from math import sqrt
from typing import Any, Callable, Dict, Iterable, List, Sequence, Tuple

try:
    from .heuristics import HeuristicFn, Point, resolve_heuristic
except ImportError:  # pragma: no cover - allows running as a standalone module
    from heuristics import HeuristicFn, Point, resolve_heuristic


GridLike = Sequence[Sequence[Any]]
Path = List[Point]
PlannerResult = Dict[str, Any]
PlannerFn = Callable[..., PlannerResult]

_PLANNERS: Dict[str, PlannerFn] = {}

CARDINAL_STEPS: Tuple[Point, ...] = (
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
)
DIAGONAL_STEPS: Tuple[Point, ...] = (
    (-1, -1),
    (-1, 1),
    (1, 1),
    (1, -1),
)


def register_planner(
    name: str,
    planner: PlannerFn | None = None,
    *,
    overwrite: bool = False,
):
    """Register a planner function by name."""

    key = name.strip().lower()
    if not key:
        raise ValueError("Planner name must be non-empty.")

    def _register(fn: PlannerFn) -> PlannerFn:
        if key in _PLANNERS and not overwrite:
            raise ValueError(f"Planner '{key}' is already registered.")
        _PLANNERS[key] = fn
        return fn

    if planner is None:
        return _register
    return _register(planner)


def list_planners() -> Tuple[str, ...]:
    """Return registered planner names."""

    return tuple(sorted(_PLANNERS))


def get_planner(name: str) -> PlannerFn:
    """Fetch a registered planner by name."""

    key = name.strip().lower()
    try:
        return _PLANNERS[key]
    except KeyError as exc:
        available = ", ".join(list_planners()) or "<none>"
        raise KeyError(f"Unknown planner '{name}'. Available: {available}") from exc


def plan_path(
    planner_name: str,
    grid: GridLike,
    start: Point,
    goal: Point,
    **kwargs: Any,
) -> PlannerResult:
    """Run a planner by registry name."""

    planner = get_planner(planner_name)
    return planner(grid, start, goal, **kwargs)


def _grid_shape(grid: GridLike) -> Tuple[int, int]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    return rows, cols


def _in_bounds(point: Point, rows: int, cols: int) -> bool:
    return 0 <= point[0] < rows and 0 <= point[1] < cols


def _is_blocked_cell(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "x", "#", "wall", "blocked", "true"}
    return False


def _is_passable(grid: GridLike, point: Point) -> bool:
    return not _is_blocked_cell(grid[point[0]][point[1]])


def _neighbors(point: Point, rows: int, cols: int, allow_diagonal: bool) -> Iterable[Point]:
    steps = CARDINAL_STEPS + DIAGONAL_STEPS if allow_diagonal else CARDINAL_STEPS
    for dr, dc in steps:
        nxt = (point[0] + dr, point[1] + dc)
        if _in_bounds(nxt, rows, cols):
            yield nxt


def _step_cost(current: Point, nxt: Point) -> float:
    return sqrt(2.0) if current[0] != nxt[0] and current[1] != nxt[1] else 1.0


def _reconstruct_path(came_from: Dict[Point, Point], goal: Point) -> Path:
    path: Path = [goal]
    node = goal
    while node in came_from:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path


def _result(path: Path, expanded_nodes: int, started_at: float) -> PlannerResult:
    elapsed = time.perf_counter() - started_at
    return {
        "path": path,
        "expanded_nodes": expanded_nodes,
        "runtime_sec": elapsed,
        "runtime_ms": elapsed * 1000.0,
    }


def _best_first_search(
    grid: GridLike,
    start: Point,
    goal: Point,
    *,
    mode: str,
    heuristic: str | HeuristicFn | None = None,
    allow_diagonal: bool = False,
) -> PlannerResult:
    started_at = time.perf_counter()
    rows, cols = _grid_shape(grid)
    if rows == 0 or cols == 0:
        return _result([], 0, started_at)
    if not _in_bounds(start, rows, cols) or not _in_bounds(goal, rows, cols):
        return _result([], 0, started_at)
    if not _is_passable(grid, start) or not _is_passable(grid, goal):
        return _result([], 0, started_at)

    heuristic_fn = resolve_heuristic(heuristic)
    frontier: List[Tuple[float, int, Point]] = []
    tie_breaker = count()
    came_from: Dict[Point, Point] = {}
    g_score: Dict[Point, float] = {start: 0.0}
    closed: set[Point] = set()
    expanded_nodes = 0

    initial_h = 0.0 if mode == "dijkstra" else heuristic_fn(start, goal)
    heapq.heappush(frontier, (initial_h, next(tie_breaker), start))

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in closed:
            continue
        closed.add(current)
        expanded_nodes += 1

        if current == goal:
            return _result(_reconstruct_path(came_from, goal), expanded_nodes, started_at)

        current_cost = g_score.get(current, float("inf"))
        for nxt in _neighbors(current, rows, cols, allow_diagonal):
            if not _is_passable(grid, nxt):
                continue

            step = _step_cost(current, nxt)
            tentative_cost = current_cost + step
            known_cost = g_score.get(nxt, float("inf"))
            if tentative_cost >= known_cost:
                continue

            came_from[nxt] = current
            g_score[nxt] = tentative_cost
            heuristic_cost = heuristic_fn(nxt, goal)

            if mode == "astar":
                priority = tentative_cost + heuristic_cost
            elif mode == "dijkstra":
                priority = tentative_cost
            elif mode == "greedy_best_first":
                priority = heuristic_cost
            else:
                raise ValueError(f"Unsupported search mode '{mode}'.")

            heapq.heappush(frontier, (priority, next(tie_breaker), nxt))

    return _result([], expanded_nodes, started_at)


@register_planner("astar")
def astar(
    grid: GridLike,
    start: Point,
    goal: Point,
    *,
    heuristic: str | HeuristicFn | None = "manhattan",
    allow_diagonal: bool = False,
) -> PlannerResult:
    """A* baseline on a grid maze."""

    return _best_first_search(
        grid,
        start,
        goal,
        mode="astar",
        heuristic=heuristic,
        allow_diagonal=allow_diagonal,
    )


@register_planner("dijkstra")
def dijkstra(
    grid: GridLike,
    start: Point,
    goal: Point,
    *,
    heuristic: str | HeuristicFn | None = "manhattan",
    allow_diagonal: bool = False,
) -> PlannerResult:
    """Dijkstra baseline on a grid maze."""

    return _best_first_search(
        grid,
        start,
        goal,
        mode="dijkstra",
        heuristic=heuristic,
        allow_diagonal=allow_diagonal,
    )


@register_planner("greedy_best_first")
def greedy_best_first(
    grid: GridLike,
    start: Point,
    goal: Point,
    *,
    heuristic: str | HeuristicFn | None = "manhattan",
    allow_diagonal: bool = False,
) -> PlannerResult:
    """Greedy Best-First Search baseline on a grid maze."""

    return _best_first_search(
        grid,
        start,
        goal,
        mode="greedy_best_first",
        heuristic=heuristic,
        allow_diagonal=allow_diagonal,
    )


register_planner("greedy", greedy_best_first)
register_planner("gbfs", greedy_best_first)


__all__ = [
    "GridLike",
    "Path",
    "PlannerFn",
    "PlannerResult",
    "astar",
    "dijkstra",
    "get_planner",
    "greedy_best_first",
    "list_planners",
    "plan_path",
    "register_planner",
]
