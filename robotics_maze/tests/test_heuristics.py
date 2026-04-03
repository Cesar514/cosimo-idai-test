import pytest
from math import sqrt
try:
    from heuristics import (
        manhattan_distance,
        euclidean_distance,
        chebyshev_distance,
        register_heuristic,
        get_heuristic,
        list_heuristics,
        resolve_heuristic,
    )
except ImportError:
    from robotics_maze.src.heuristics import (
        manhattan_distance,
        euclidean_distance,
        chebyshev_distance,
        register_heuristic,
        get_heuristic,
        list_heuristics,
        resolve_heuristic,
    )

def test_manhattan_distance():
    assert manhattan_distance((0, 0), (0, 0)) == 0.0
    assert manhattan_distance((0, 0), (1, 1)) == 2.0
    assert manhattan_distance((1, 1), (0, 0)) == 2.0
    assert manhattan_distance((-1, -1), (1, 1)) == 4.0
    assert manhattan_distance((10, 20), (15, 25)) == 10.0

def test_euclidean_distance():
    assert euclidean_distance((0, 0), (0, 0)) == 0.0
    assert euclidean_distance((0, 0), (3, 4)) == 5.0
    assert euclidean_distance((3, 4), (0, 0)) == 5.0
    assert euclidean_distance((-1, -1), (1, 1)) == sqrt(8)

def test_chebyshev_distance():
    assert chebyshev_distance((0, 0), (0, 0)) == 0.0
    assert chebyshev_distance((0, 0), (1, 5)) == 5.0
    assert chebyshev_distance((5, 1), (0, 0)) == 5.0
    assert chebyshev_distance((-1, -1), (1, 1)) == 2.0

def test_heuristic_registry():
    # Test list_heuristics
    heuristics = list_heuristics()
    assert "manhattan" in heuristics
    assert "euclidean" in heuristics
    assert "chebyshev" in heuristics

    # Test get_heuristic
    assert get_heuristic("manhattan") == manhattan_distance
    assert get_heuristic("EUCLIDEAN") == euclidean_distance

    with pytest.raises(KeyError):
        get_heuristic("non_existent")

def test_register_heuristic():
    def custom_heuristic(a, b):
        return 1.0

    register_heuristic("custom", custom_heuristic)
    assert "custom" in list_heuristics()
    assert get_heuristic("custom") == custom_heuristic

    # Test overwrite protection
    with pytest.raises(ValueError, match="already registered"):
        register_heuristic("custom", custom_heuristic)

    # Test explicit overwrite
    register_heuristic("custom", lambda a, b: 2.0, overwrite=True)
    assert get_heuristic("custom")((0,0), (0,0)) == 2.0

    # Test empty name
    with pytest.raises(ValueError, match="non-empty"):
        register_heuristic("", custom_heuristic)

def test_resolve_heuristic():
    # Resolve None (default to manhattan)
    assert resolve_heuristic(None) == manhattan_distance

    # Resolve by name
    assert resolve_heuristic("euclidean") == euclidean_distance

    # Resolve by callable
    custom = lambda a, b: 0.0
    assert resolve_heuristic(custom) == custom

    # Resolve unknown name
    with pytest.raises(KeyError):
        resolve_heuristic("unknown")
