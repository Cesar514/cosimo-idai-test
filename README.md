# cosimi-idai-test

Multi-track workspace for an agentic engineering demo with three active streams:

- Robotics maze planning/simulation code (`robotics_maze/`)
- Presentation production assets and audit artifacts (`agents.pptx`, `presentation_assets/`)
- Multi-agent coordination and reporting outputs (`robotics_maze/coordination/`)

Last updated: 2026-02-26 (UTC)

## Repository Components

| Component | What it contains | Key paths |
|---|---|---|
| Robotics runtime | Maze generation, planners, simulator backends, CLI entrypoints | `robotics_maze/src/` |
| Planner research + alternatives | Alternative planner implementations and research notes | `robotics_maze/src/alt_planners/`, `robotics_maze/research/` |
| Benchmark outputs | Planner trial CSV and aggregated summary markdown | `robotics_maze/results/benchmark_results.csv`, `robotics_maze/results/benchmark_summary.md` |
| Testing outputs | Deterministic test logs and screenshot QA artifacts | `robotics_maze/testing/` |
| Multi-agent coordination | Task board, per-agent logs, event timeline/log schema, issue backlog summary | `robotics_maze/coordination/` |
| Task-level handoff reports | Per-task execution summaries from agents | `robotics_maze/coordination/agent_reports/` |
| Presentation track | Deck plus image/reference maps, style notes, factual audit | `agents.pptx`, `presentation_assets/`, `agents_factual_risk_audit.md` |
| Root automation scripts | Simulation wrapper, deck update scripts, repo smoke checks | `scripts/` |
| Generated architecture docs | Auto-generated architecture/process documentation | `docs/generated/` |

## Environment Setup

Run from repository root:

```bash
pixi install
pixi task list
```

Current root Pixi tasks:

- `sim`
- `benchmark`

## Core Commands

### Simulation

Run the default GUI simulation task:

```bash
pixi run sim
```

Run headless or custom runs directly through the wrapper:

```bash
python scripts/sim_runner.py --planner astar --episodes 3 --maze-size 15 --seed 42
```

Force a specific backend:

```bash
python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 15 --seed 42 --gui --physics-backend pybullet
python scripts/sim_runner.py --planner astar --episodes 3 --maze-size 15 --seed 42 --physics-backend mujoco
```

### Benchmarking

Run the default benchmark task:

```bash
pixi run benchmark
```

Run benchmark directly with explicit parameters/output folder:

```bash
python robotics_maze/src/benchmark.py --mazes 30 --width 15 --height 15 --algorithm backtracker --seed 7 --output-dir robotics_maze/results
```

### Tests and Validation

Run deterministic simulation/test workflow and screenshot capture:

```bash
bash robotics_maze/testing/run_sim_tests.sh
```

Run root-level smoke checks (module compile + deck validation + deterministic robotics checks):

```bash
bash scripts/run_repo_smoke.sh
```

Run Python tests:

```bash
pytest robotics_maze/tests/test_core.py
```

## Multi-Agent Outputs

Primary coordination outputs are under `robotics_maze/coordination/`:

- Task plan and ownership: `TASK_BOARD.md`
- Event log (append-only): `session_event_log.csv`
- Event log schema: `session_event_log_schema.md`
- Agent rollup/status board: `AGENT_DASHBOARD.md`
- Session backlog/issues rollup: `BACKLOG_SUMMARY.md`
- Per-agent execution logs: `B1.md`-`B6.md`, `R1.md`-`R10.md`, `S1.md`, `L1.md`, and support logs (`SC1.md`, `SC2.md`, `SC3.md`)
- Per-task reports: `agent_reports/task*.md`

Issue-validation backlog (tracked in GitHub and summarized locally):

- `#1`, `#2`, `#5`, `#6` in `Cesar514/cosimo-idai-test`

## Key Artifacts To Check First

1. `robotics_maze/coordination/session_event_log.csv`
2. `robotics_maze/coordination/AGENT_DASHBOARD.md`
3. `robotics_maze/results/benchmark_summary.md`
4. `robotics_maze/testing/TEST_RUN_LOG.md`
5. `presentation_assets/image_coverage_report.md`
6. `agents_factual_risk_audit.md`

## Repository Layout

```text
.
├── README.md
├── agents.pptx
├── agents_factual_risk_audit.md
├── docs/generated/
├── presentation_assets/
├── robotics_maze/
│   ├── src/
│   ├── research/
│   ├── results/
│   ├── testing/
│   └── coordination/
├── scripts/
└── pixi.toml
```
