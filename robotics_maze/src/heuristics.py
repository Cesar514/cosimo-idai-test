"""Heuristic helpers for grid-based planning."""

from __future__ import annotations

from math import sqrt
from typing import Callable, Dict, Tuple

Point = Tuple[int, int]
HeuristicFn = Callable[[Point, Point], float]

_HEURISTICS: Dict[str, HeuristicFn] = {}


def register_heuristic(
    name: str,
    heuristic: HeuristicFn | None = None,
    *,
    overwrite: bool = False,
):
    """Register a heuristic function by name."""

    key = name.strip().lower()
    if not key:
        raise ValueError("Heuristic name must be non-empty.")

    def _register(fn: HeuristicFn) -> HeuristicFn:
        if key in _HEURISTICS and not overwrite:
            raise ValueError(f"Heuristic '{key}' is already registered.")
        _HEURISTICS[key] = fn
        return fn

    if heuristic is None:
        return _register
    return _register(heuristic)


def list_heuristics() -> Tuple[str, ...]:
    """Return registered heuristic names in sorted order."""

    return tuple(sorted(_HEURISTICS))


def get_heuristic(name: str) -> HeuristicFn:
    """Fetch a registered heuristic by name."""

    key = name.strip().lower()
    try:
        return _HEURISTICS[key]
    except KeyError as exc:
        available = ", ".join(list_heuristics()) or "<none>"
        raise KeyError(f"Unknown heuristic '{name}'. Available: {available}") from exc


def resolve_heuristic(heuristic: str | HeuristicFn | None) -> HeuristicFn:
    """Resolve either a function, name, or None to a callable heuristic."""

    if heuristic is None:
        return get_heuristic("manhattan")
    if callable(heuristic):
        return heuristic
    return get_heuristic(heuristic)


@register_heuristic("manhattan")
def manhattan_distance(a: Point, b: Point) -> float:
    """L1 distance."""

    return float(abs(a[0] - b[0]) + abs(a[1] - b[1]))


@register_heuristic("euclidean")
def euclidean_distance(a: Point, b: Point) -> float:
    """L2 distance."""

    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


@register_heuristic("chebyshev")
def chebyshev_distance(a: Point, b: Point) -> float:
    """L-infinity distance."""

    return float(max(abs(a[0] - b[0]), abs(a[1] - b[1])))


__all__ = [
    "HeuristicFn",
    "Point",
    "chebyshev_distance",
    "euclidean_distance",
    "get_heuristic",
    "list_heuristics",
    "manhattan_distance",
    "register_heuristic",
    "resolve_heuristic",
]
