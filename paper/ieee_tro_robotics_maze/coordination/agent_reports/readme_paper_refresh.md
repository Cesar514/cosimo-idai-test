# README Paper Refresh Report

## Scope
- Owned file updated: `paper/ieee_tro_robotics_maze/README.md`
- Requested report file created: `paper/ieee_tro_robotics_maze/coordination/agent_reports/readme_paper_refresh.md`

## What Changed
- Replaced minimal template README with a practical paper README.
- Added concrete build commands from `paper/ieee_tro_robotics_maze/Makefile`:
  - `make pdf`
  - `make clean`
  - effective compiler command: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
- Documented key manuscript inputs from `main.tex` and referenced section/table/appendix/figure files.
- Documented evidence/provenance input paths used by the manuscript:
  - `../../robotics_maze/results/benchmark_results.csv`
  - `../../robotics_maze/results/benchmark_summary.md`
  - `coordination/inferential_runtime_comparison.csv`
  - `coordination/figure_manifest.csv`
- Added artifact path map for:
  - `main.pdf`
  - `submission/ieee_tro_robotics_maze_main.pdf`
  - `submission/ieee_tro_robotics_maze_source.zip`
  - `coordination/paper_status.md`
- Added latest submission artifact hash table (size, UTC modified time, SHA-256).

## Source Values Used (No Invented Values)
- Build commands/flags: `paper/ieee_tro_robotics_maze/Makefile`
- Manuscript structure/inputs: `paper/ieee_tro_robotics_maze/main.tex`
- Benchmark regeneration command reference: `robotics_maze/results/README.md`
- Submission artifacts and metadata:
  - `paper/ieee_tro_robotics_maze/submission/ieee_tro_robotics_maze_main.pdf`
  - `paper/ieee_tro_robotics_maze/submission/ieee_tro_robotics_maze_source.zip`

## Recorded Submission Hashes
- `submission/ieee_tro_robotics_maze_main.pdf`
  - size: `1026654`
  - modified (UTC): `2026-02-26 23:52:59 +0000`
  - sha256: `8a2caef1edd77ee1f328661a628cbb2a5c5f2f0c94953ca42afa5115e5182f24`
- `submission/ieee_tro_robotics_maze_source.zip`
  - size: `990176`
  - modified (UTC): `2026-02-27 00:20:17 +0000`
  - sha256: `0456079f8f62ae63e527dd0a8294cb1e7f0678fef7085348b1e32feae61e7c8b`
