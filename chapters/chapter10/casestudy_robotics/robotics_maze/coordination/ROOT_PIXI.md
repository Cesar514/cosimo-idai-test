# Root Pixi Usage

The repo root has a `pixi.toml` so simulation and benchmark commands run from the main folder.

## Setup

- Install/update environment from repo root: `pixi install`
- Show available tasks: `pixi task list`

## Tasks

- GUI simulation launcher: `pixi run sim`
  - Root command: `python scripts/sim_runner.py --gui-setup --gui --planner astar --episodes 1 --maze-size 15 --seed 42 --physics-backend auto --gui-hold-seconds 20`
- Benchmark harness: `pixi run benchmark`
  - Root command: `python robotics_maze/src/benchmark.py --mazes 50 --width 15 --height 15 --seed 7 --algorithm backtracker`

## Passing Custom CLI Args

Pass extra flags directly after each task (Pixi appends them to the task command).

Examples:

- `pixi run sim --planner r1_weighted_astar --episodes 5 --maze-size 11 --seed 7 --no-gui-setup`
- `pixi run benchmark --mazes 100 --width 21 --height 21 --algorithm prim --planner astar`

Notes:

- There is currently no root `sim-cli` task.
- `scripts/sim_runner.py` normalizes passthrough args for `sim` (including optional `--` separators).
- For `benchmark`, avoid `--` separators like `pixi run benchmark -- --help`; pass flags directly (for example `pixi run benchmark --help`).
