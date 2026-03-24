# Task 01/36 - GUI Owner Report

Date: 2026-02-26

## Owned Files Updated
- `robotics_maze/src/gui_setup.py`
- `robotics_maze/src/main.py`
- `scripts/sim_runner.py`

## Implemented Fixes
1. Improved GUI setup dialog visibility and focus behavior:
- Centered the Tk window on screen.
- Lifted it to the foreground and briefly set top-most to avoid hidden startup.
- Added a short arming delay for Enter-to-launch to prevent accidental immediate submit from carried keypresses.
2. Added headless/automation-safe GUI setup mode override via `ROBOTICS_MAZE_GUI_SETUP_MODE`:
- `dialog` (default), `accept`, `cancel`, `skip`.
3. Changed GUI setup cancel behavior in `main.py`:
- Cancel now exits cleanly without launching a simulation run.
4. Strengthened interactive GUI defaults:
- If GUI is selected from setup and backend is `auto`, runtime now prefers `pybullet` for visual runs.
- In `sim_runner.py`, interactive GUI invocations without explicit hold/setup flags now get sensible defaults (`--gui-hold-seconds 20`, `--gui-setup`).

## Verification

Syntax check:
- Command: `pixi run python -m py_compile robotics_maze/src/gui_setup.py robotics_maze/src/main.py scripts/sim_runner.py`
- Result: pass (exit `0`)

Smoke command (GUI setup path, headless-safe):
- Command: `ROBOTICS_MAZE_GUI_SETUP_MODE=accept pixi run sim -- --physics-backend mujoco --gui-hold-seconds 0 --episodes 1 --maze-size 7`
- Result: pass (exit `0`)
- Key output:
  - `[START] ... gui=True backend=mujoco ... gui_hold_s=0.0`
  - `[DONE] success=1/1 avg_steps=61.00 avg_elapsed_s=0.0025`
