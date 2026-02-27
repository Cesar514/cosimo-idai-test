# Experiments Writer Report

## Scope completed
- Drafted `sections/05_experiments.tex` with a protocol grounded in current repository benchmark and testing artifacts.
- Added `tables/experiment_protocol_table.tex` and included it from the experiments section.
- Explicitly separated executed experiments from planned future experiments.

## Evidence used
- Benchmark harness logic and defaults: `robotics_maze/src/benchmark.py`
- Current benchmark artifacts: `robotics_maze/results/benchmark_summary.md`, `robotics_maze/results/benchmark_results.csv`
- Deterministic regression pipeline: `robotics_maze/scripts/capture_regression_screenshots.py`
- Latest deterministic run outputs: `robotics_maze/testing/TEST_RUN_LOG.md`
- Planned future-method shortlist: `robotics_maze/research/sota_planners_2021_plus.md`

## Notes
- Executed protocol in the draft reflects committed artifacts (benchmark snapshot + deterministic regression checks).
- Planned experiments are marked as not executed and excluded from current quantitative claims.
