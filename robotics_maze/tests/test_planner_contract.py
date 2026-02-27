from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add src to path so we can import benchmark
_SRC_DIR = str(Path(__file__).resolve().parents[1] / "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import benchmark

def test_canonical_planner_set_integrity():
    """Assert that load_available_planners() returns exactly the 12 expected planners."""
    expected = set(benchmark.DEFAULT_BENCHMARK_PLANNERS)
    assert len(expected) == 12

    discovered = set(benchmark.load_available_planners(include_alt=True))

    missing = expected - discovered
    unexpected = discovered - expected

    assert not missing, f"Missing canonical planners: {missing}"
    assert not unexpected, f"Unexpected planners discovered: {unexpected}"
    assert discovered == expected

def test_benchmark_mismatch_raises_error():
    """Mocks available planners to verify _resolve_default_benchmark_planners raises ValueError."""
    # Scenario 1: Missing planner
    available_missing = {name: (lambda x, s, g: None) for name in list(benchmark.DEFAULT_BENCHMARK_PLANNERS)[:-1]}
    with pytest.raises(ValueError) as excinfo:
        benchmark._resolve_default_benchmark_planners(available_missing)
    assert "missing:" in str(excinfo.value)

    # Scenario 2: Unexpected planner
    available_unexpected = {name: (lambda x, s, g: None) for name in benchmark.DEFAULT_BENCHMARK_PLANNERS}
    available_unexpected["extra_planner"] = (lambda x, s, g: None)
    with pytest.raises(ValueError) as excinfo:
        benchmark._resolve_default_benchmark_planners(available_unexpected)
    assert "unexpected:" in str(excinfo.value)

def test_benchmark_cli_mismatch_behavior():
    """Verifies that calling main() with a mismatch results in an error via parser.error."""
    # We mock load_available_planners to return a mismatching set
    mismatched_available = {"astar": (lambda x, s, g: None)} # Only one planner, missing many

    with patch("benchmark.load_available_planners", return_value=mismatched_available):
        with patch("sys.argv", ["benchmark.py"]):
            with pytest.raises(SystemExit):
                # We expect parser.error to be called, which calls sys.exit
                benchmark.main()
