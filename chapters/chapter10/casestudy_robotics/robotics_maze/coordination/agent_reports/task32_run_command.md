# Task 32/36 - Root Sim Command Doc Owner

Owned files:
- `robotics_maze/coordination/RUN_SIM_FROM_ROOT.md`
- `robotics_maze/coordination/agent_reports/task32_run_command.md`

## Goal
Document exact root-level `pixi` simulation commands for common modes (default GUI, no-gui, backend selection), validated against the current setup.

## What I changed
1. Added `robotics_maze/coordination/RUN_SIM_FROM_ROOT.md` with:
   - default root GUI command
   - non-interactive GUI variant
   - no-GUI command path
   - backend-specific commands (`auto`, `pybullet`, `mujoco`)
   - quick validation commands (`pixi task list`, backend probe)
2. Included concrete, tested command lines and expected runtime mode/backend markers.

## Validation run log (2026-02-26)

### Task availability
Command:
```bash
pixi task list
```
Result:
- tasks on this machine: `benchmark`, `sim`

### No-GUI (auto backend)
Command:
```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend auto
```
Result:
- exit code `0`
- `[START] ... gui=False backend=auto ...`
- `[DONE] success=1/1 ...`

### GUI (root sim task, no setup popup)
Command:
```bash
pixi run sim --no-gui-setup --gui-hold-seconds 0 --episodes 1 --maze-size 9 --seed 7
```
Result:
- exit code `0`
- pixi expanded command confirms root task defaults are active (`--gui-setup --gui ... --physics-backend auto ...`)
- `[START] ... gui=True backend=auto ...`
- `[DONE] success=1/1 ...`

### Backend selection
Command (PyBullet):
```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend pybullet
```
Result:
- exit code `0`
- `[START] ... gui=False backend=pybullet ...`
- `[DONE] success=1/1 ...`

Command (MuJoCo):
```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend mujoco
```
Result:
- exit code `0`
- `[START] ... gui=False backend=mujoco ...`
- `[DONE] success=1/1 ...`

### Environment backend probe
Command:
```bash
pixi run python robotics_maze/scripts/check_backends.py
```
Result:
- `pybullet available=yes`
- `mujoco available=yes`
- effective availability: `pybullet=1 mujoco=1`

## Notes
- Root `sim` task currently hardcodes `--gui`; for deterministic headless runs, use:
  - `pixi run python scripts/sim_runner.py ... --no-gui-setup --physics-backend <auto|pybullet|mujoco>`
