# cosimi-idai-test

Agentic engineering demo workspace with three active tracks:

- `robotics_maze/`: maze generation, planners, simulation, benchmarking
- `presentation_assets/` + `agents.pptx`: deck assets and factual audit material
- `robotics_maze/coordination/`: multi-agent planning, logs, and per-task reports

Last updated: 2026-02-27 (UTC)

## Key Outputs

- Benchmark CSV: `robotics_maze/results/benchmark_results.csv`
- Benchmark summary: `robotics_maze/results/benchmark_summary.md`
- Coordination dashboard: `robotics_maze/coordination/AGENT_DASHBOARD.md`
- Coordination event log: `robotics_maze/coordination/session_event_log.csv`
- Test run log: `robotics_maze/testing/TEST_RUN_LOG.md`

## Execution Narrative

- Paper writing plan used: `paper/ieee_tro_robotics_maze/coordination/PAPER_WRITING_PLAN_USED.md`
- Full prompt/step/result slideshow: `docs/generated/repo_prompt_step_results_slideshow.md`
- Full chat-order prompt ledger: `docs/generated/session_chat_prompt_ledger.md`

## Plan and Agent Distribution

Primary plan document:

- `paper/ieee_tro_robotics_maze/coordination/PAPER_WRITING_PLAN_USED.md`

Prompt-log-derived artifacts (cleaned and centralized):

- `artifacts_prompts/PAPER_WRITING_PLAN_USED.md`
- `artifacts_prompts/session_chat_prompt_ledger.md`
- `artifacts_prompts/repo_prompt_step_results_slideshow.md`
- `artifacts_prompts/session_prompt_raw_from_history.md`

Logged agent distribution (from coordination artifacts):

```mermaid
flowchart TD
    A[Session Orchestration]
    A --> B[Robotics Build Agents<br/>B1-B6 (6)]
    A --> C[Alternative Method Research<br/>R1-R10 (10)]
    A --> D[Supervisor + Logger<br/>S1 + L1 (2)]
    A --> E[Test and Screenshot Loop<br/>T1-T3 (3)]
    A --> F[Skills Copy Agents<br/>SC1-SC3 (3)]
    A --> G[Runtime and GUI Tracks<br/>ROOT_PIXI + GUI_SETUP + GUI_VALIDATION (3)]
    A --> H[Monitoring Agent<br/>Larry (1)]
    A --> I[Paper Review Roles<br/>researcher/reviewer/math/verifier/literature/figure/integrator]
    A --> J[Privacy Audit Sweep<br/>20 agents]
```

## Useful Artifact Map

Paper and submission:

- `paper/ieee_tro_robotics_maze/README.md`
- `paper/ieee_tro_robotics_maze/coordination/paper_status.md`
- `paper/ieee_tro_robotics_maze/submission/ieee_tro_robotics_maze_main.pdf`
- `paper/ieee_tro_robotics_maze/submission/ieee_tro_robotics_maze_source.zip`

Prompt and process documentation:

- `artifacts_prompts/session_chat_prompt_ledger.md`
- `artifacts_prompts/repo_prompt_step_results_slideshow.md`
- `artifacts_prompts/session_prompt_raw_from_history.md`
- `artifacts_prompts/privacy_audit/MASTER_SUMMARY.md`

Robotics implementation and experiments:

- `robotics_maze/README.md`
- `robotics_maze/src/`
- `robotics_maze/results/benchmark_summary.md`
- `robotics_maze/testing/TEST_RUN_LOG.md`
- `robotics_maze/testing/screenshots/`

Coordination and operations:

- `robotics_maze/coordination/AGENT_DASHBOARD.md`
- `robotics_maze/coordination/session_event_log.csv`
- `robotics_maze/coordination/BACKLOG_SUMMARY.md`

Presentation and references:

- `agents.pptx`
- `presentation_assets/slide_references.json`
- `presentation_assets/slide_image_map.json`
- `presentation_assets/deck_runbook.md`

Skills mirrored for reproducibility:

- `skills/README_LOCAL_SKILLS.md`
- `skills/`

## Contact

For any more questions, feel free to email: `cac214@bham.ac.uk`

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


## Contact

For any more questions, feel free to email: `cac214@bham.ac.uk`