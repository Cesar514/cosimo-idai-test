# Robotics Maze README Refresh Report

## Scope
- Updated only: `robotics_maze/README.md`
- Goal: align run instructions with current root tasks and current CLI behavior.

## What Changed
1. Removed stale `sim-cli` guidance.
- Previous README referenced root `sim-cli` task and its command.
- Current root `pixi task list` shows only `sim` and `benchmark`.

2. Corrected root task alignment.
- Added explicit root task list (`sim`, `benchmark`).
- Kept all documented commands runnable from repo root.

3. Refreshed GUI/headless instructions.
- GUI path: `pixi run sim` and non-interactive variant with `--no-gui-setup`.
- Headless path: direct wrapper invocation via `pixi run python scripts/sim_runner.py ... --no-gui-setup`.

4. Updated backend section.
- Added explicit PyBullet headless, MuJoCo headless, and PyBullet GUI examples.
- Clarified MuJoCo behavior is headless in this project.

5. Fixed argument-passing guidance.
- Documented reliable pattern for root pixi tasks: append flags directly (no literal `--`).
- This avoids `argparse` failures on tasks that do not strip separator tokens.

## Validation Commands Run
- `pixi task list` (repo root) -> tasks: `benchmark`, `sim`.
- `pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend auto` -> exit 0.
- `pixi run sim --no-gui-setup --gui-hold-seconds 0 --episodes 1 --maze-size 9 --seed 7` -> exit 0.
- `pixi run sim -- --planner weighted_astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend mujoco --gui-hold-seconds 0` -> exit 0 (sim wrapper strips `--`).
- `pixi run benchmark -- --mazes 1 ...` -> fails (`unrecognized arguments: -- ...`).
- `pixi run benchmark --mazes 1 --width 9 --height 9 --seed 7 --algorithm backtracker --output-dir robotics_maze/results` -> exit 0.

## Result
`robotics_maze/README.md` now reflects actual root task availability and current CLI behavior, with executable examples for GUI, headless, backend selection, benchmark, and URDF usage.
