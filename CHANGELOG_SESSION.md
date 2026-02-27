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

---

# Session Changelog Addendum (Round-2/3 Cycle)

Date: 2026-02-27  
Scope: paper review-cycle integration, benchmark/ranking hardening, artifact refresh, external backlog expansion, and checksum traceability updates.

## Paper

- Integrated round-2/3 review resolutions across manuscript + coordination artifacts:
  - synchronized ranking-policy wording and evidence across method/results/discussion/table surfaces
  - aligned reproducibility entrypoints across root and robotics Pixi configs + protocol table commands
  - removed path-length tie-break from ranking policy and hardened expansion handling when planner metrics are missing
  - closed round-3 minor findings on dependency-pin alignment, fail-closed planner defaults, inferential traceability, and novelty framing polish
- Refreshed round-tracking and status artifacts:
  - `paper/ieee_tro_robotics_maze/coordination/responses_to_reviewers.md`
  - `paper/ieee_tro_robotics_maze/coordination/review_comment_log.csv`
  - `paper/ieee_tro_robotics_maze/coordination/paper_status.md`
  - `paper/ieee_tro_robotics_maze/coordination/claims_traceability.csv`

## Benchmarking

- Updated `robotics_maze/src/benchmark.py` comparison flow for reproducible ranking:
  - enforced fail-closed default benchmark planner set (canonical 12 planners)
  - standardized ranking order: success rate (desc), comparable solve time (asc), mean expansions (asc), mean solve time (asc), planner name (asc)
  - exposed comparable-maze counts + `Delta vs #1 (ms)` in console and markdown summaries
- Refreshed benchmark evidence artifacts consumed by paper outputs:
  - `robotics_maze/results/benchmark_results.csv`
  - `robotics_maze/results/benchmark_summary.md`
  - `paper/ieee_tro_robotics_maze/coordination/inferential_runtime_comparison.csv`

## Artifacts

- Regenerated paper figures and submission package outputs:
  - `paper/ieee_tro_robotics_maze/figures/benchmark_runtime_ms.png`
  - `paper/ieee_tro_robotics_maze/figures/runtime_uncertainty.png`
  - `paper/ieee_tro_robotics_maze/figures/benchmark_expansions.png`
  - `paper/ieee_tro_robotics_maze/figures/benchmark_success_rate.png`
  - `paper/ieee_tro_robotics_maze/submission/ieee_tro_robotics_maze_main.pdf`
  - `paper/ieee_tro_robotics_maze/submission/ieee_tro_robotics_maze_source.zip`
- Updated `paper/ieee_tro_robotics_maze/coordination/figure_manifest.csv` with snapshot-linked provenance for all runtime/result figures.

## GitHub Backlog

- Added external tracking issues `#9`-`#18` in `Cesar514/cosimo-idai-test` (created 2026-02-27), covering:
  - benchmark snapshot freeze and manuscript drift prevention
  - repeated-run timing protocol + rank-stability analysis
  - 2021+ bibliography/DOI verification
  - scripted inferential table generation from benchmark CSV
  - backend parity study (PyBullet vs MuJoCo) and dynamic-obstacle benchmark extension
  - URDF fallback diagnostics tests
  - CI guardrails for canonical planner-set enforcement
  - final novelty/framing editorial polish
  - publication-grade scripted figure regeneration

## Package Checksums

- Recorded refreshed checksum traceability for paper packaging:
  - benchmark snapshot hash used by inferential + figure artifacts: `aad1a3e07fdb0b3921e60f0b8e59ba60d6ea98484ad019fd8191f0acb98f9a30`
  - submission PDF SHA256: `8a2caef1edd77ee1f328661a628cbb2a5c5f2f0c94953ca42afa5115e5182f24`
  - submission source ZIP SHA256: `0456079f8f62ae63e527dd0a8294cb1e7f0678fef7085348b1e32feae61e7c8b`
