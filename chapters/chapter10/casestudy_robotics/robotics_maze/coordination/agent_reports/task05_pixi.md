# Task 05 - Root Pixi UX

## Scope
- Updated root `pixi.toml` for straightforward simulation launch from repository root.

## Final `sim` Task Behavior
- Command: `pixi run sim`
- Effective task command:
  - `python scripts/sim_runner.py --gui-setup --gui --planner astar --episodes 1 --maze-size 15 --seed 42 --physics-backend auto --gui-hold-seconds 20`

## Interactive Defaults
- `--gui-setup`: opens setup dialog first (when display/Tk is available).
- `--gui`: runs in GUI mode by default.
- `--episodes 1`: short interactive run.
- `--physics-backend auto`: prefers PyBullet, falls back as needed.
- `--gui-hold-seconds 20`: keeps GUI visible after episode completion.

## Validation
- `pixi task list` now shows tasks without deprecated-manifest warning.
- Verified passthrough override behavior from repo root:
  - `pixi run sim -- --no-gui-setup --physics-backend mujoco --gui-hold-seconds 0 --episodes 1`
  - Result: command succeeded (`[DONE] success=1/1 ...`) and overrides were applied.
