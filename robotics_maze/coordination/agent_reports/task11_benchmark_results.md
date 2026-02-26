# Task 11 Benchmark Results

- Run timestamp (UTC): 2026-02-26T22:31:51+00:00
- Command: `python3 src/benchmark.py`
- Working directory: `/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze`
- Configuration: 50 mazes, size 15x15, algorithm `backtracker`, seed `7`
- Planners benchmarked: 12 available planners (baseline + alt planners)

## Generated Outputs

- `robotics_maze/results/benchmark_results.csv`
- `robotics_maze/results/benchmark_summary.md`

## Fastest Methods Observed (by mean solve time)

| Rank | Planner | Success Rate | Mean Solve Time (ms) | Mean Expansions |
|---:|---|---:|---:|---:|
| 1 | `r1_weighted_astar` | 100.0% (50/50) | 0.47 | 187.16 |
| 2 | `r7_beam_search` | 100.0% (50/50) | 0.57 | 198.36 |
| 3 | `greedy_best_first` | 100.0% (50/50) | 0.64 | 171.96 |
| 4 | `r5_jump_point_search` | 100.0% (50/50) | 0.64 | 57.26 |
| 5 | `r9_bidirectional_bfs` | 100.0% (50/50) | 0.69 | 201.52 |

All planners reached 100% success on this benchmark run.
