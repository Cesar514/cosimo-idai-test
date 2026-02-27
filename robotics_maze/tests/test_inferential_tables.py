"""Tests for scripts/generate_inferential_tables.py."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Load the script as a module
# ---------------------------------------------------------------------------

def _load_module():
    script_path = (
        Path(__file__).resolve().parents[2] / "scripts" / "generate_inferential_tables.py"
    )
    spec = importlib.util.spec_from_file_location("generate_inferential_tables", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


git = _load_module()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _write_simple_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = ["planner", "maze_index", "maze_seed", "width", "height",
                  "algorithm", "success", "solve_time_ms", "path_length", "expansions", "error"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _make_benchmark_rows(n_mazes: int = 5) -> list[dict]:
    """Generate synthetic benchmark rows for two planners across n_mazes mazes."""
    rows = []
    for maze_index in range(n_mazes):
        baseline_time = 0.5 + maze_index * 0.01
        comparator_time = baseline_time + 0.1 + maze_index * 0.005
        for planner, t in [("r1_weighted_astar", baseline_time), ("astar", comparator_time)]:
            rows.append({
                "planner": planner,
                "maze_index": maze_index,
                "maze_seed": 7 + maze_index,
                "width": 9,
                "height": 9,
                "algorithm": "backtracker",
                "success": 1,
                "solve_time_ms": t,
                "path_length": 50,
                "expansions": 100,
                "error": "",
            })
    return rows


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def test_sign_test_all_slower():
    """p-value when every delta is positive (all slower)."""
    deltas = [0.1] * 50
    p = git._sign_test_two_sided(deltas)
    # 2 * 0.5**50
    expected = 2.0 * (0.5 ** 50)
    assert abs(p - expected) < 1e-20


def test_sign_test_48_slower_2_faster():
    """p-value for 48 slower / 2 faster."""
    from math import comb
    deltas = [0.1] * 48 + [-0.05] * 2
    p = git._sign_test_two_sided(deltas)
    expected = 2.0 * sum(comb(50, i) * 0.5 ** 50 for i in range(3))
    assert abs(p - expected) < 1e-20


def test_sign_test_all_tied():
    """All tied deltas → p=1."""
    deltas = [0.0] * 10
    assert git._sign_test_two_sided(deltas) == 1.0


def test_holm_correction_order():
    """Holm correction increases adjusted values from smallest raw p."""
    raw = [0.04, 0.01, 0.03]
    adj = git._holm_correction(raw)
    # Rank 1: idx 1 (p=0.01): adj = 0.01 * 3 = 0.03
    # Rank 2: idx 2 (p=0.03): adj = 0.03 * 2 = 0.06
    # Rank 3: idx 0 (p=0.04): adj = 0.04 * 1 = 0.04
    # cummax ensures monotone non-decrease
    assert adj[1] <= adj[2]
    assert adj[1] <= adj[0]


def test_holm_correction_empty():
    assert git._holm_correction([]) == []


def test_build_paired_deltas_basic(tmp_path):
    csv_path = tmp_path / "bench.csv"
    _write_simple_csv(csv_path, _make_benchmark_rows(5))
    rows = git._read_benchmark_csv(csv_path)
    deltas = git._build_paired_deltas(rows, baseline="r1_weighted_astar")
    assert "astar" in deltas
    assert len(deltas["astar"]) == 5
    # All deltas should be positive (comparator is slower)
    assert all(d > 0 for d in deltas["astar"])


def test_build_paired_deltas_excludes_failures(tmp_path):
    """Rows where success=0 are excluded from pairing."""
    rows = _make_benchmark_rows(3)
    # Mark maze_index=1 for astar as failed
    for row in rows:
        if row["planner"] == "astar" and row["maze_index"] == 1:
            row["success"] = 0
    csv_path = tmp_path / "bench.csv"
    _write_simple_csv(csv_path, rows)
    loaded = git._read_benchmark_csv(csv_path)
    deltas = git._build_paired_deltas(loaded, baseline="r1_weighted_astar")
    # Only mazes 0 and 2 are common successful pairs
    assert len(deltas["astar"]) == 2


def test_sanity_check_missing_baseline(tmp_path):
    csv_path = tmp_path / "bench.csv"
    _write_simple_csv(csv_path, _make_benchmark_rows(3))
    rows = git._read_benchmark_csv(csv_path)
    deltas = git._build_paired_deltas(rows, baseline="r1_weighted_astar")
    with pytest.raises(ValueError, match="not found"):
        git._sanity_checks(deltas, rows, baseline="nonexistent", expected_planners=None, expected_mazes=None)


def test_sanity_check_wrong_planner_count(tmp_path):
    csv_path = tmp_path / "bench.csv"
    _write_simple_csv(csv_path, _make_benchmark_rows(3))
    rows = git._read_benchmark_csv(csv_path)
    deltas = git._build_paired_deltas(rows, baseline="r1_weighted_astar")
    with pytest.raises(ValueError, match="Expected 5 planners"):
        git._sanity_checks(deltas, rows, "r1_weighted_astar", expected_planners=5, expected_mazes=None)


def test_sanity_check_wrong_maze_count(tmp_path):
    csv_path = tmp_path / "bench.csv"
    _write_simple_csv(csv_path, _make_benchmark_rows(3))
    rows = git._read_benchmark_csv(csv_path)
    deltas = git._build_paired_deltas(rows, baseline="r1_weighted_astar")
    with pytest.raises(ValueError, match="Expected 10 paired mazes"):
        git._sanity_checks(deltas, rows, "r1_weighted_astar", expected_planners=None, expected_mazes=10)


def test_run_pipeline_produces_outputs(tmp_path):
    """Full pipeline integration test: CSV and TeX outputs are created."""
    csv_path = tmp_path / "bench.csv"
    _write_simple_csv(csv_path, _make_benchmark_rows(10))
    out_csv = tmp_path / "inferential.csv"
    out_tex = tmp_path / "table.tex"

    results = git.run_pipeline(
        input_path=csv_path,
        output_csv=out_csv,
        output_tex=out_tex,
        baseline="r1_weighted_astar",
        seed=42,
        n_resamples=1000,
        expected_planners=None,
        expected_mazes=None,
    )

    assert out_csv.exists()
    assert out_tex.exists()
    assert len(results) == 1  # only "astar" comparator

    # Verify CSV schema
    csv_text = out_csv.read_text(encoding="utf-8")
    assert "median_delta_ms" in csv_text
    assert "holm_adjusted_p" in csv_text
    assert "bootstrap_resamples" in csv_text

    # Verify TeX structure
    tex_text = out_tex.read_text(encoding="utf-8")
    assert r"\begin{table*}" in tex_text
    assert r"\end{table*}" in tex_text
    assert "Holm" in tex_text


def test_run_pipeline_reproducible(tmp_path):
    """Same seed must produce identical outputs on two runs."""
    csv_path = tmp_path / "bench.csv"
    _write_simple_csv(csv_path, _make_benchmark_rows(8))

    out1_csv = tmp_path / "out1.csv"
    out1_tex = tmp_path / "out1.tex"
    out2_csv = tmp_path / "out2.csv"
    out2_tex = tmp_path / "out2.tex"

    kwargs = dict(
        input_path=csv_path,
        baseline="r1_weighted_astar",
        seed=99,
        n_resamples=500,
        expected_planners=None,
        expected_mazes=None,
    )

    git.run_pipeline(output_csv=out1_csv, output_tex=out1_tex, **kwargs)
    git.run_pipeline(output_csv=out2_csv, output_tex=out2_tex, **kwargs)

    assert out1_csv.read_text() == out2_csv.read_text()
    assert out1_tex.read_text() == out2_tex.read_text()


def test_cli_main_smoke(tmp_path):
    """CLI main() returns 0 on valid input."""
    csv_path = tmp_path / "bench.csv"
    _write_simple_csv(csv_path, _make_benchmark_rows(5))
    out_csv = tmp_path / "out.csv"
    out_tex = tmp_path / "out.tex"

    rc = git.main([
        "--input", str(csv_path),
        "--output-csv", str(out_csv),
        "--output-tex", str(out_tex),
        "--seed", "1",
        "--bootstrap-resamples", "200",
    ])
    assert rc == 0
    assert out_csv.exists()
    assert out_tex.exists()


def test_cli_main_missing_baseline_returns_error(tmp_path):
    """CLI main() returns 1 when baseline is not present in CSV."""
    csv_path = tmp_path / "bench.csv"
    _write_simple_csv(csv_path, _make_benchmark_rows(3))
    out_csv = tmp_path / "out.csv"
    out_tex = tmp_path / "out.tex"

    rc = git.main([
        "--input", str(csv_path),
        "--output-csv", str(out_csv),
        "--output-tex", str(out_tex),
        "--baseline", "nonexistent_planner",
    ])
    assert rc == 1
