# Task 31/36 - Smoke Checks Owner

- Date (UTC): 2026-02-26
- Ownership: `scripts/run_repo_smoke.sh`, `robotics_maze/coordination/agent_reports/task31_smoke.md`
- Goal: Strengthen repository smoke checks for simulation and deck artifacts while keeping runtime practical.

## Changes Made

1. Updated `scripts/run_repo_smoke.sh` from a 3-step flow to a 4-step flow:
   - Step 1/4: Python module compile checks.
   - Step 2/4: Deck artifact checks.
   - Step 3/4: Simulation runner + simulation screenshot artifact checks.
   - Step 4/4: Deterministic robotics benchmark checks.
2. Strengthened deck validation logic:
   - Validates `.pptx` slide XML count (`ppt/slides/slide*.xml`) against mapped slide count.
   - Confirms required archive entry `ppt/presentation.xml` exists.
   - Validates `presentation_assets/link_audit_final.tsv` schema and ensures all rows are reachable with HTTP status in `[200, 399]`.
3. Added practical simulation-focused smoke checks:
   - Executes a minimal headless simulation run via `scripts/sim_runner.py` (`astar`, `1` episode, fixed seed).
   - Asserts expected runtime markers (`[START]`, `[EP 1/1]`, `[DONE] success=1/1`) and positive step count.
   - Parses simulation PNG assets referenced by `slide_image_map.json` and validates PNG signature + IHDR dimensions.

## Smoke Run Result

Command run:

```bash
bash scripts/run_repo_smoke.sh
```

Observed output summary:

```text
[smoke] Step 1/4: compile key python modules
compiled_modules=24
[smoke] Step 2/4: validate deck outputs
deck_slides=41 mapped_images=41 link_rows=48
[smoke] Step 3/4: simulation runner + screenshot artifacts
simulation_episode_steps=49 simulation_png_assets=12 png_dimension_checks=12
[smoke] Step 4/4: deterministic robotics checks
robotics_smoke=ok planners_checked=2 mazes_checked=3
[smoke] PASS
```

Exit code: `0`

## Scope Compliance

- Edited only owned files listed in task instructions.
- Ignored unrelated concurrent edits in the working tree.
