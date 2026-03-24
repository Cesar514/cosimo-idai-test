# Task 10 Benchmark Harness

- Run timestamp (UTC): 2026-02-26T22:36:26+00:00
- Owned files updated:
  - `robotics_maze/src/benchmark.py`
  - `robotics_maze/coordination/agent_reports/task10_benchmark_harness.md`

## What Changed

1. Added path validation for planner outputs before counting success:
   - Validates start/goal endpoints.
   - Validates all path cells are in bounds and not blocked.
   - Rasterizes each path segment (Bresenham) so non-adjacent/any-angle outputs are measured consistently.
   - Stores validation failures in the per-trial `error` field.
2. Added shared-success comparability metrics in summaries:
   - `Comparable Mazes` (mazes solved by every planner in the run).
   - `Comparable Solve Time (ms)` and `Comparable Path Length` computed on that shared set.
   - Ranking now prioritizes success rate, then comparable runtime/path metrics.
3. Reduced execution-order bias:
   - Planner execution order is rotated per maze index (deterministic round-robin) to avoid the same planner always running first.

## Sample Run

- Command:

```bash
python3 robotics_maze/src/benchmark.py \
  --mazes 20 \
  --width 15 \
  --height 15 \
  --seed 17 \
  --algorithm backtracker \
  --planner astar \
  --planner dijkstra \
  --planner greedy_best_first \
  --planner r1_weighted_astar \
  --planner r5_jump_point_search \
  --planner r7_beam_search \
  --output-dir /tmp/cosimi_task10_benchmark
```

- Output artifacts:
  - `/tmp/cosimi_task10_benchmark/benchmark_results.csv`
  - `/tmp/cosimi_task10_benchmark/benchmark_summary.md`

## Sample Result Snapshot

| Rank | Planner | Success Rate | Comparable Mazes | Comparable Time (ms) | Comparable Path | Mean Expansions |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `r1_weighted_astar` | 100.0% (20/20) | 20 | 0.44 | 128.60 | 169.45 |
| 2 | `r7_beam_search` | 100.0% (20/20) | 20 | 0.52 | 128.60 | 182.40 |
| 3 | `greedy_best_first` | 100.0% (20/20) | 20 | 0.57 | 128.60 | 153.65 |
| 4 | `r5_jump_point_search` | 100.0% (20/20) | 20 | 0.58 | 128.60 | 51.10 |
| 5 | `astar` | 100.0% (20/20) | 20 | 0.65 | 128.60 | 170.85 |
| 6 | `dijkstra` | 100.0% (20/20) | 20 | 0.69 | 128.60 | 184.75 |

All tested planners solved all 20 mazes, and comparable metrics were computed on the same shared maze set (20/20), enabling consistent runtime/path-length comparison.
