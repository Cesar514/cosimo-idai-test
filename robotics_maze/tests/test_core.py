from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_benchmark_module():
    benchmark_path = Path(__file__).resolve().parents[1] / "src" / "benchmark.py"
    spec = importlib.util.spec_from_file_location("robotics_benchmark", benchmark_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


benchmark = _load_benchmark_module()


def test_maze_generation_smoke():
    grid_a, start_a, goal_a = benchmark.generate_benchmark_maze(
        width=10, height=8, seed=123, algorithm="backtracker"
    )
    grid_b, start_b, goal_b = benchmark.generate_benchmark_maze(
        width=10, height=8, seed=123, algorithm="backtracker"
    )

    assert grid_a == grid_b
    assert start_a == start_b == (1, 1)
    assert goal_a == goal_b == (9, 11)
    assert grid_a[start_a[0]][start_a[1]] == 0
    assert grid_a[goal_a[0]][goal_a[1]] == 0


def test_astar_solvability_assumption_smoke():
    planners = {"astar": benchmark.load_available_planners(include_alt=False)["astar"]}
    trials, _ = benchmark.run_benchmark(
        planners=planners,
        maze_count=5,
        width=12,
        height=12,
        seed=0,
        algorithm="backtracker",
    )

    assert len(trials) == 5
    assert all(trial.success for trial in trials)
    assert all((trial.path_length or 0) > 0 for trial in trials)
    assert all(trial.expansions >= 0 for trial in trials)


def test_benchmark_reports_written_to_output_dir(tmp_path):
    available = benchmark.load_available_planners(include_alt=False)
    planners = {"astar": available["astar"], "dijkstra": available["dijkstra"]}
    trials, summary, csv_path, summary_path = benchmark.run_benchmark_and_write_reports(
        planners=planners,
        maze_count=3,
        width=10,
        height=10,
        seed=9,
        algorithm="backtracker",
        output_dir=tmp_path,
    )

    assert len(trials) == 6
    assert len(summary) == 2
    assert csv_path.exists()
    assert summary_path.exists()

    csv_text = csv_path.read_text(encoding="utf-8")
    md_text = summary_path.read_text(encoding="utf-8")
    assert "solve_time_ms" in csv_text
    assert "algorithm" in csv_text
    assert "success_rate" not in csv_text  # CSV is per-trial detail.
    assert "| Planner | Success Rate |" in md_text


# ---------------------------------------------------------------------------
# Snapshot infrastructure tests
# ---------------------------------------------------------------------------

def _sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def test_snapshot_manifest_designates_valid_snapshot():
    manifest_path = (
        _REPO_ROOT / "paper" / "ieee_tro_robotics_maze" / "coordination" / "snapshot_manifest.json"
    )
    assert manifest_path.exists(), "snapshot_manifest.json must exist"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "designated_snapshot" in manifest
    assert "csv_sha256" in manifest
    snapshot_id = manifest["designated_snapshot"]
    snapshot_csv = _REPO_ROOT / "robotics_maze" / "results" / "snapshots" / snapshot_id / "benchmark_results.csv"
    assert snapshot_csv.exists(), f"Snapshot CSV not found: {snapshot_csv}"


def test_snapshot_csv_hash_matches_manifest():
    manifest_path = (
        _REPO_ROOT / "paper" / "ieee_tro_robotics_maze" / "coordination" / "snapshot_manifest.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    snapshot_id = manifest["designated_snapshot"]
    csv_path = _REPO_ROOT / "robotics_maze" / "results" / "snapshots" / snapshot_id / "benchmark_results.csv"
    actual = _sha256_of_file(csv_path)
    assert actual == manifest["csv_sha256"], (
        f"Snapshot CSV hash mismatch.\n"
        f"  snapshot_manifest.json : {manifest['csv_sha256']}\n"
        f"  actual file hash       : {actual}"
    )


def test_snapshot_csv_hash_matches_meta():
    snapshots_dir = _REPO_ROOT / "robotics_maze" / "results" / "snapshots"
    manifest_path = (
        _REPO_ROOT / "paper" / "ieee_tro_robotics_maze" / "coordination" / "snapshot_manifest.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    snapshot_id = manifest["designated_snapshot"]
    meta_path = snapshots_dir / snapshot_id / "snapshot_meta.json"
    assert meta_path.exists(), f"snapshot_meta.json not found: {meta_path}"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    csv_path = snapshots_dir / snapshot_id / "benchmark_results.csv"
    actual = _sha256_of_file(csv_path)
    assert actual == meta["csv_sha256"], (
        f"Snapshot CSV hash mismatch against snapshot_meta.json.\n"
        f"  snapshot_meta.json : {meta['csv_sha256']}\n"
        f"  actual file hash   : {actual}"
    )


def test_paper_tables_exist_for_designated_snapshot():
    tables_dir = _REPO_ROOT / "paper" / "ieee_tro_robotics_maze" / "tables"
    for table_name in ("main_results_table.tex", "statistical_comparison_table.tex"):
        assert (tables_dir / table_name).exists(), f"Paper table missing: {table_name}"

