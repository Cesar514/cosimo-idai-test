# Agent Operations Dashboard

Last updated: 2026-02-27
Source: `robotics_maze/coordination/session_event_log.csv`, `robotics_maze/coordination/agent_task_log.csv` + per-task coordination logs.

| Task ID | Agent ID / Nickname | Status | Key Output Files |
|---|---|---|---|
| S1 | `unknown` | completed (historical blocker snapshot logged) | `robotics_maze/coordination/S1.md` |
| B1 | `unknown` | completed | `robotics_maze/pyproject.toml`, `robotics_maze/requirements.txt`, `robotics_maze/src/main.py` |
| B2 | `019c9b76-7e47-7510-bb0a-4e3ae9dcdeb5` | completed | `robotics_maze/src/maze.py`, `robotics_maze/src/geometry.py`, `robotics_maze/coordination/B2.md` |
| B3 | `019c9b76-7f23-7361-bb02-3fa0e144dc98` | completed | `robotics_maze/src/sim.py`, `robotics_maze/src/robot.py`, `robotics_maze/coordination/B3.md` |
| B4 | `unknown` | completed | `robotics_maze/src/planners.py`, `robotics_maze/src/heuristics.py`, `robotics_maze/coordination/B4.md` |
| B5 | `019c9b76-817d-7721-a7b6-c093410d6c13` | completed | `robotics_maze/scripts/fetch_urdfs.py`, `robotics_maze/scripts/fetch_urdfs.sh`, `robotics_maze/urdfs/README.md` |
| B6 | `019c9b76-82b5-77a1-85a3-5f73839e9629` | completed | `robotics_maze/src/benchmark.py`, `robotics_maze/tests/test_core.py`, `robotics_maze/results/benchmark_summary.md` |
| R1 | `unknown` | completed | `robotics_maze/src/alt_planners/r1_weighted_astar.py`, `robotics_maze/research/R1_weighted_astar.md` |
| R2 | `019c9b76-df85-7a72-b361-92555a615212` | completed | `robotics_maze/src/alt_planners/r2_bidirectional_astar.py`, `robotics_maze/research/R2_bidirectional_astar.md` |
| R3 | `unknown` | completed | `robotics_maze/src/alt_planners/r3_theta_star.py`, `robotics_maze/research/R3_theta_star.md` |
| R4 | `unknown` | completed | `robotics_maze/src/alt_planners/r4_idastar.py`, `robotics_maze/research/R4_idastar.md` |
| R5 | `019c9b77-84af-7a03-a93e-41d52db50086` | completed | `robotics_maze/src/alt_planners/r5_jump_point_search.py`, `robotics_maze/research/R5_jump_point_search.md` |
| R6 | `019c9b77-85cf-72c2-97c5-ccb7b56ca040` | completed | `robotics_maze/src/alt_planners/r6_lpa_star.py`, `robotics_maze/research/R6_lpa_star.md` |
| R7 | `unknown` | completed | `robotics_maze/src/alt_planners/r7_beam_search.py`, `robotics_maze/research/R7_beam_search.md` |
| R8 | `019c9b77-87ce-7262-b50d-0b0ecc08b94d` | completed | `robotics_maze/src/alt_planners/r8_fringe_search.py`, `robotics_maze/research/R8_fringe_search.md` |
| R9 | `019c9b77-88d1-77e0-b6ac-590dbfe17c86` | completed | `robotics_maze/src/alt_planners/r9_bidirectional_bfs.py`, `robotics_maze/research/R9_bidirectional_bfs.md` |
| R10 | `019c9b77-89dc-7381-96ae-a4f05f390e37` | completed | `robotics_maze/src/alt_planners/r10_dwa_hybrid.md`, `robotics_maze/research/R10_alt_methods_sota.md` |
| L1 | `Cypress` (id unknown) | completed (logging pass finalized; cycle closed) | `robotics_maze/coordination/L1.md`, `robotics_maze/coordination/session_event_log.csv` |
| T1 | `019c9bd4-81a0-7b72-9eb6-4f5cd62861ca` | completed (post-fix validation pass) | `robotics_maze/testing/run_sim_tests.sh`, `robotics_maze/testing/screenshots/` |
| T2 | `019c9bd4-87c9-7942-8c58-4174b2b32322` | completed | `robotics_maze/testing/benchmark_results_test.csv`, `robotics_maze/testing/benchmark_summary_test.md`, `robotics_maze/testing/benchmark_test_report.md` |
| T3 | `019c9bd4-8db6-7383-9c04-cfb59cd265d0` | completed | `robotics_maze/testing/reports/screenshot_analysis.md`, `robotics_maze/testing/reports/screenshot_debug_todos.md` |
| SC1 | `unknown` | completed | `skills/create-plan/`, `skills/github-agents-deploy/`, `skills/openai-docs/`, `skills/skill-creator/` |
| SC2 | `unknown` | completed | `skills/suggest-improve/`, `skills/playwright/`, `skills/literature-review/`, `skills/scientific-report-editor/`, `skills/pr-merger/` |
| SC3 | `unknown` | completed | `.gitignore`, `robotics_maze/coordination/SC3.md` |
| ROOT_PIXI | `unknown` | completed | `pixi.toml`, `scripts/sim_runner.py`, `robotics_maze/coordination/ROOT_PIXI.md` |
| GUI_SETUP | `Worker B` (id unknown) | completed | `robotics_maze/src/gui_setup.py`, `robotics_maze/coordination/GUI_SETUP.md` |
| GUI_VALIDATION | `Worker C` (id unknown) | completed with known arg-forwarding caveat | `robotics_maze/coordination/GUI_VALIDATION.md` |
| Larry | `019c9bd8-1f91-76a3-bad6-a0a1459985fd` / `Larry` | completed | `robotics_maze/coordination/session_event_log.csv` |
