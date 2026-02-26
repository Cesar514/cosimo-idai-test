# GUI Validation (Worker C)

Date: 2026-02-26  
Run location: repository root (`/Users/cesar514/Documents/agent_programming/cosimi-idai-test`)

## Pass/Fail Matrix

| Check | Command | Status | Evidence |
|---|---|---|---|
| Root Pixi task discoverability | `pixi task list` | PASS | Listed tasks on this machine: `benchmark`, `sim`, `sim-cli`. |
| `sim-cli` path runs from repo root | `pixi run sim-cli` | PASS | Exit `0`; completed `[DONE] success=3/3 ...` with `gui=False`. |
| Root wrapper path works from main folder | `python3 scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7` | PASS | Exit `0`; completed `[DONE] success=1/1 ...`. |
| GUI command path executes | `pixi run sim` | PASS | Exit `0`; completed `[DONE] success=3/3 ...` with `gui=True`. |
| Documented custom-arg forwarding example | `pixi run sim-cli -- --planner r1_weighted_astar --episodes 5 --maze-size 11 --seed 7` | FAIL | `main.py: error: unrecognized arguments: -- ...` (literal `--` is forwarded to argparse). |

## Manual GUI Validation (Visual/Interactive)

Automated CLI runs can confirm exit code and logs, but cannot reliably assert on-screen GUI behavior. Perform these manual checks:

1. From repo root, run: `pixi run sim`.
2. Confirm a PyBullet GUI window opens.
3. Confirm maze walls and ground plane are visible (not blank/black frame).
4. Confirm robot spawns and visibly moves through waypoints.
5. Confirm run ends with terminal line: `[DONE] success=3/3 ...`.
6. Repeat once with a different planner: `python3 scripts/sim_runner.py --planner weighted_astar --episodes 1 --maze-size 11 --seed 7 --gui`.
7. Expected behavior: one episode starts, robot progresses, process exits with `[DONE] success=1/1 ...`.
