# Root Pixi Usage

The repo root now has a `pixi.toml` so simulation and benchmark commands can run from the main folder.

## Setup

- Install/update environment from repo root: `pixi install`

## Tasks

- GUI simulation launcher: `pixi run sim`
- CLI simulation launcher: `pixi run sim-cli`
- Benchmark harness: `pixi run benchmark`

## Passing Custom CLI Args

`scripts/sim_runner.py` forwards all arguments to `robotics_maze/src/main.py`.

Examples:

- `pixi run sim-cli -- --planner r1_weighted_astar --episodes 5 --maze-size 11 --seed 7`
- `pixi run sim -- --planner astar --episodes 1 --maze-size 9`
