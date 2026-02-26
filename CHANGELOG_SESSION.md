# Session Changelog (Task 35/36)

Date: 2026-02-26  
Scope: major repository modifications produced in this session, grouped by area.

## Presentation

- Updated `agents.pptx` with integrated custom visuals and simulation screenshots (notably slides 6, 18, 32, 35, 37, 38, 39, 40).
- Added/updated deck automation scripts:
  - `scripts/apply_ppt_assets.py`
  - `scripts/fix_ppt_full.py`
  - `scripts/sim_runner.py` (root wrapper used by deck/runbook flows)
- Added presentation planning and QA artifacts:
  - `presentation_assets/deck_prepatch_audit.md`
  - `presentation_assets/deck_runbook.md`
  - `presentation_assets/deck_style_notes.md`
  - `presentation_assets/deck_style_overrides.json`
  - `presentation_assets/image_coverage_report.md`
  - `presentation_assets/slide_image_map.json`
  - `presentation_assets/slide_references.json`
  - `presentation_assets/references_notes.md`
  - `presentation_assets/speaker_notes.md`
  - `presentation_assets/link_audit.tsv` and `presentation_assets/link_audit_final.tsv`
- Revised `presentation_assets/image_layout_plan.md` with an explicit frontend-design-oriented layout strategy.
- Updated `agents_factual_risk_audit.md` with refreshed high-risk claim priorities and stale-claim cleanup after deck changes.

## Robotics

- Extended runtime configuration in `robotics_maze/src/main.py`:
  - backend selection (`auto`/`pybullet`/`mujoco`)
  - optional GUI setup flow
  - custom URDF validation/fallback
  - GUI hold timing controls
  - broader planner loading (registry + alt planner modules)
- Added Tkinter setup UI via `robotics_maze/src/gui_setup.py`.
- Refactored `robotics_maze/src/sim.py` for stronger execution robustness:
  - backend fallback sequencing between PyBullet and MuJoCo
  - GUI hold loop and camera focus/tracking behavior
  - safer URDF resolution with explicit warnings/fallbacks
  - planner-path normalization fixes for heterogeneous planner outputs
- Upgraded `robotics_maze/src/robot.py` to support differential-drive wheel control when wheel joints are available, with geometry-based wheel/track estimation.
- Enhanced planning and benchmarking:
  - `robotics_maze/src/planners.py`: A* heuristic weighting and tie-break controls
  - `robotics_maze/src/benchmark.py`: ranked summaries, failure counts, delta-vs-top metrics, improved console/markdown output
- Updated screenshot/testing pipeline:
  - `robotics_maze/scripts/generate_mujoco_screenshots.py` (overlay improvements + CLI args)
  - `robotics_maze/scripts/generate_sim_screenshots.py` (CLI args for output/prefix)
  - new `robotics_maze/scripts/capture_regression_screenshots.py`
  - new regression/test artifacts under `robotics_maze/testing/` and `robotics_maze/results/`
- Updated environment/config files for reproducible runs:
  - root `pixi.toml` + `pixi.lock`
  - `robotics_maze/pixi.toml` (added `pybullet` dependency)

## Docs

- Added root-level `README.md` with session status snapshot and runbook pointers.
- Added generated architecture/workflow documentation set under `docs/generated/` (overview + deep dives + indexes).
- Added `robotics_maze/README.md` with root-run instructions, backend switching, URDF usage, and CLI notes.
- Added benchmark/test documentation outputs:
  - `robotics_maze/results/benchmark_summary.md`
  - `robotics_maze/testing/TEST_RUN_LOG.md`
  - `robotics_maze/testing/benchmark_test_report.md`
  - `robotics_maze/testing/reports/screenshot_analysis.md`

## Coordination

- Expanded coordination planning/status artifacts:
  - `robotics_maze/coordination/BACKLOG_SUMMARY.md`
  - `robotics_maze/coordination/GUI_SETUP.md`
  - `robotics_maze/coordination/GUI_VALIDATION.md`
  - `robotics_maze/coordination/ROOT_PIXI.md`
  - `robotics_maze/coordination/SC1.md`, `SC2.md`, `SC3.md`
- Updated `robotics_maze/coordination/B6.md` with benchmark UX completion notes.
- Appended/expanded `robotics_maze/coordination/session_event_log.csv` with session timeline entries (agent completions, bug-fix/test events, and GitHub issue creation records).
- Introduced root `.gitignore` entry to keep local copied skills untracked (`/skills/`), consistent with SC3 notes.

