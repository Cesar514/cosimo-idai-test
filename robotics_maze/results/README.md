# Benchmark Outputs

`robotics_maze/src/benchmark.py` writes benchmark artifacts into this folder.
The harness benchmarks baseline planners from `src/planners.py` plus available
alternative planners from `src/alt_planners/`.

## Run

```bash
python3 robotics_maze/src/benchmark.py \
  --mazes 100 \
  --width 15 \
  --height 15 \
  --algorithm backtracker \
  --seed 7 \
  --output-dir robotics_maze/results
```

Use `--no-alt` to benchmark only baseline planners. Use repeated `--planner`
flags to run a subset.

## Generated files

- `benchmark_results.csv`: One row per `(planner, maze)` trial.
- `benchmark_summary.md`: Aggregated planner comparison table.

## CSV columns (`benchmark_results.csv`)

- `planner`: Planner name.
- `maze_index`: Sequential maze id for the run.
- `maze_seed`: Seed used to generate that maze.
- `width`, `height`: Maze dimensions.
- `algorithm`: Maze generation algorithm (`backtracker` or `prim`).
- `success`: `1` if the planner reached goal, else `0`.
- `solve_time_ms`: Wall-clock solve time in milliseconds.
- `path_length`: Number of steps in the returned path (blank on failure).
- `expansions`: Expanded nodes reported by the planner.
- `error`: Exception text if the planner crashed.

## Summary metrics (`benchmark_summary.md`)

Each planner row reports:

- Success rate (`successes / runs`).
- Mean solve time (ms) over all trials.
- Mean path length over successful trials.
- Mean expansions over successful trials.
