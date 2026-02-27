# cosimi-idai-test

Agentic engineering demo workspace with three active tracks:

- `robotics_maze/`: maze generation, planners, simulation, benchmarking
- `presentation_assets/` + `agents.pptx`: deck assets and factual audit material
- `robotics_maze/coordination/`: multi-agent planning, logs, and per-task reports

Last updated: 2026-02-27 (UTC)

## Quick Start

Run from repository root:

```bash
pixi install
pixi task list
```

Current root Pixi tasks:

- `sim`
- `benchmark`

## Run Commands

Default GUI simulation task:

```bash
pixi run sim
```

Default benchmark task (`50` mazes, `seed 7`):

```bash
pixi run benchmark
```

Equivalent direct benchmark command:

```bash
python robotics_maze/src/benchmark.py --mazes 50 --width 15 --height 15 --algorithm backtracker --seed 7 --output-dir robotics_maze/results
```

Custom simulation examples:

```bash
python scripts/sim_runner.py --planner astar --episodes 3 --maze-size 15 --seed 42
python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 15 --seed 42 --gui --physics-backend pybullet
python scripts/sim_runner.py --planner astar --episodes 3 --maze-size 15 --seed 42 --physics-backend mujoco
```

## Validation Commands

```bash
bash robotics_maze/testing/run_sim_tests.sh
bash scripts/run_repo_smoke.sh
pytest robotics_maze/tests/test_core.py
```

## Key Outputs

- Benchmark CSV: `robotics_maze/results/benchmark_results.csv`
- Benchmark summary: `robotics_maze/results/benchmark_summary.md`
- Coordination dashboard: `robotics_maze/coordination/AGENT_DASHBOARD.md`
- Coordination event log: `robotics_maze/coordination/session_event_log.csv`
- Test run log: `robotics_maze/testing/TEST_RUN_LOG.md`
