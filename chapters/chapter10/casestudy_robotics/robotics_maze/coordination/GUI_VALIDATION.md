# GUI Validation (Worker C)

Last refreshed: 2026-02-27 (UTC)  
Refresh run location: repository root (`.`)  
Previous full baseline in this note: 2026-02-26

## Latest Cycle Revalidation (2026-02-27)

| Check | Command | Revalidated this cycle | Result | Evidence |
|---|---|---|---|---|
| Root Pixi task discoverability | `pixi task list` | Yes | PASS | Tasks listed now: `benchmark`, `sim` (no `sim-cli`). |
| Legacy `sim-cli` task availability | `pixi run sim-cli` | Yes | FAIL (task missing) | `sim-cli: command not found` plus available tasks `benchmark`, `sim`. |
| GUI command path (no setup popup) | `pixi run sim --no-gui-setup --gui-hold-seconds 0 --episodes 1 --maze-size 9 --seed 7` | Yes | PASS | `[START] ... gui=True ...`, `[DONE] success=1/1 ...` (exit `0`). |
| CLI override forwarding on `sim` task | `pixi run sim -- --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --gui-hold-seconds 0` | Yes | PASS | Forwarded overrides were applied; `[START] planner=astar ...`, `[DONE] success=1/1 ...` (exit `0`). |
| Weighted planner override smoke on GUI path | `pixi run sim -- --planner weighted_astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --gui-hold-seconds 0` | Yes | FAIL (runtime outcome) | Command parsed and executed, but run ended `[DONE] success=0/1 ...` (exit `1`). |
| Headless runner path from root | `pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend auto` | Yes | PASS | `[START] ... gui=False ...`, `[DONE] success=1/1 ...` (exit `0`). |

## What Changed Since 2026-02-26

- Root task set drifted: `sim-cli` is no longer exposed from root `pixi task list`.
- The prior argparse caveat tied to `sim-cli -- --...` is no longer the active behavior on current root workflow.
- Current root override path is `pixi run sim -- ...`; argument forwarding works, but planner success still depends on runtime behavior.

## Not Revalidated In This Cycle (2026-02-27)

- Manual visual confirmation of GUI window contents (maze visibility, robot motion on screen).
- Multi-planner GUI pass matrix at `3/3` episode scope.
- Explicit backend-forced GUI checks (`--physics-backend pybullet` and `--physics-backend mujoco` in GUI mode).
- Screenshot artifact regeneration and visual regression analysis (latest logged set remains 2026-02-26 in `robotics_maze/testing/TEST_RUN_LOG.md`).
