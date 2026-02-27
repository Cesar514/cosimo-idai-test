from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path


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
    assert "repeat_index" in csv_text
    assert "success_rate" not in csv_text  # CSV is per-trial detail.
    assert "| Planner | Success Rate |" in md_text
    assert "Repeats per planner-maze pair: 1" in md_text


def test_benchmark_repeats_trial_count():
    """With repeats=3, each planner-maze pair produces 3 TrialResult rows."""
    available = benchmark.load_available_planners(include_alt=False)
    planners = {"astar": available["astar"]}
    trials, _ = benchmark.run_benchmark(
        planners=planners,
        maze_count=2,
        width=10,
        height=10,
        seed=0,
        algorithm="backtracker",
        repeats=3,
        warmup=1,
    )
    # 2 mazes × 1 planner × 3 repeats = 6 trials
    assert len(trials) == 6
    repeat_indices = {t.repeat_index for t in trials}
    assert repeat_indices == {0, 1, 2}
    assert all(t.success for t in trials)


def test_compute_repeat_stats():
    """compute_repeat_stats aggregates mean/median/std per (planner, maze)."""
    available = benchmark.load_available_planners(include_alt=False)
    planners = {"astar": available["astar"]}
    trials, _ = benchmark.run_benchmark(
        planners=planners,
        maze_count=2,
        width=10,
        height=10,
        seed=0,
        algorithm="backtracker",
        repeats=3,
    )
    stats = benchmark.compute_repeat_stats(trials)
    # 2 mazes × 1 planner = 2 groups
    assert len(stats) == 2
    for row in stats:
        assert row["repeats"] == 3
        assert row["mean_solve_time_ms"] >= 0
        assert row["median_solve_time_ms"] >= 0
        assert math.isnan(row["std_solve_time_ms"]) or row["std_solve_time_ms"] >= 0
        assert row["min_solve_time_ms"] <= row["max_solve_time_ms"]


def test_compute_rank_stability():
    """compute_rank_stability returns pairwise Spearman rho for repeat rounds."""
    available = benchmark.load_available_planners(include_alt=False)
    planners = {"astar": available["astar"], "dijkstra": available["dijkstra"]}
    trials, _ = benchmark.run_benchmark(
        planners=planners,
        maze_count=3,
        width=10,
        height=10,
        seed=0,
        algorithm="backtracker",
        repeats=3,
    )
    stability = benchmark.compute_rank_stability(trials)
    assert stability["repeat_count"] == 3
    # C(3, 2) = 3 pairs
    assert len(stability["pairs"]) == 3
    assert not math.isnan(stability["mean_spearman_rho"])
    # Spearman rho is in [-1, 1]
    for pair in stability["pairs"]:
        assert math.isnan(pair["spearman_rho"]) or -1.0 <= pair["spearman_rho"] <= 1.0


def test_compute_rank_stability_single_repeat():
    """compute_rank_stability with only one repeat returns nan mean rho."""
    available = benchmark.load_available_planners(include_alt=False)
    planners = {"astar": available["astar"]}
    trials, _ = benchmark.run_benchmark(
        planners=planners,
        maze_count=2,
        width=10,
        height=10,
        seed=0,
        algorithm="backtracker",
        repeats=1,
    )
    stability = benchmark.compute_rank_stability(trials)
    assert stability["repeat_count"] == 1
    assert len(stability["pairs"]) == 0
    assert math.isnan(stability["mean_spearman_rho"])


def test_repeat_reports_written(tmp_path):
    """run_benchmark_and_write_reports writes repeat stats and rank stability when repeats > 1."""
    available = benchmark.load_available_planners(include_alt=False)
    planners = {"astar": available["astar"], "dijkstra": available["dijkstra"]}
    trials, summary, csv_path, summary_path = benchmark.run_benchmark_and_write_reports(
        planners=planners,
        maze_count=2,
        width=10,
        height=10,
        seed=0,
        algorithm="backtracker",
        output_dir=tmp_path,
        repeats=3,
        warmup=1,
    )

    # 2 mazes × 2 planners × 3 repeats = 12 trials
    assert len(trials) == 12

    repeat_stats_path = tmp_path / "benchmark_repeat_stats.csv"
    rank_stability_path = tmp_path / "benchmark_rank_stability.md"
    assert repeat_stats_path.exists()
    assert rank_stability_path.exists()

    repeat_csv_text = repeat_stats_path.read_text(encoding="utf-8")
    assert "mean_solve_time_ms" in repeat_csv_text
    assert "std_solve_time_ms" in repeat_csv_text

    stability_md = rank_stability_path.read_text(encoding="utf-8")
    assert "Rank Stability Report" in stability_md
    assert "Spearman" in stability_md

    md_text = summary_path.read_text(encoding="utf-8")
    assert "Repeats per planner-maze pair: 3" in md_text
    assert "Warm-up runs (discarded): 1" in md_text

