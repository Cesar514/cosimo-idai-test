# Benchmark Outputs

`robotics_maze/src/benchmark.py` writes benchmark artifacts to this directory by default (`--output-dir robotics_maze/results`).

## Default benchmark contract

- Defaults: `--mazes 50 --width 15 --height 15 --seed 7 --algorithm backtracker`.
- Default planner run (when `--planner` is not provided and `--no-alt` is not set) requires this fixed set:
  - `astar`, `dijkstra`, `greedy_best_first`
  - `r1_weighted_astar`, `r2_bidirectional_astar`, `r3_theta_star`, `r4_idastar`, `r5_jump_point_search`, `r6_lpa_star`, `r7_beam_search`, `r8_fringe_search`, `r9_bidirectional_bfs`
- If that full default set is not discoverable, the CLI errors and asks for explicit `--planner` selection.
- `--no-alt` restricts discovery to baseline planners in `src/planners.py`.

## Run

```bash
python3 robotics_maze/src/benchmark.py
```

Use repeated `--planner <name>` flags to run an explicit subset.

## Output files

- `benchmark_results.csv`: One row per `(planner, maze)` trial.
- `benchmark_summary.md`: Metadata plus ranked planner comparison table.

### `benchmark_results.csv` columns

`planner, maze_index, maze_seed, width, height, algorithm, success, solve_time_ms, path_length, expansions, error`

### Ranking policy (`benchmark_summary.md`)

- Primary sort: success rate (descending).
- Tie-breakers: comparable solve time (ascending), mean expansions (ascending), mean solve time (ascending), planner name (ascending).
- Comparable metrics use the shared-success set (mazes solved by every planner); comparable solve time falls back to mean solve time if needed.
