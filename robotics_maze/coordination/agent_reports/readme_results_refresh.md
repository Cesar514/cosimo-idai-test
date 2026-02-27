# README Results Refresh

## Scope
- Updated only: `robotics_maze/results/README.md`.

## What was changed
- Aligned defaults with `benchmark.py`:
  - `--mazes 50`
  - `--seed 7`
  - retained `--width 15 --height 15 --algorithm backtracker`
- Updated planner contract wording to match current CLI behavior:
  - default run requires the fixed `DEFAULT_BENCHMARK_PLANNERS` set
  - clarified `--no-alt` behavior
  - clarified explicit subset via repeated `--planner`
- Updated outputs section to match current artifacts:
  - `benchmark_results.csv`
  - `benchmark_summary.md`
- Updated ranking policy text to match current implementation:
  - success rate desc
  - comparable solve time asc
  - mean expansions asc
  - mean solve time asc
  - planner name asc
  - noted shared-success set usage and comparable-time fallback

## Source of truth checked
- `robotics_maze/src/benchmark.py`:
  - `run_benchmark` defaults
  - `_build_cli_parser` defaults/options
  - `rank_summary_rows` sort order
  - `_comparison_time_ms` shared-success fallback behavior
  - `run_benchmark_and_write_reports` output filenames
