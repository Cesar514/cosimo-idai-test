# Figure Agent Benchmark Report

## Scope
- Owned outputs generated:
  - `paper/ieee_tro_robotics_maze/figures/benchmark_runtime_ms.png`
  - `paper/ieee_tro_robotics_maze/figures/benchmark_expansions.png`
  - `paper/ieee_tro_robotics_maze/figures/benchmark_success_rate.png`
- Coordination file updates:
  - `paper/ieee_tro_robotics_maze/coordination/figure_manifest.csv`

## Input Data
- Source CSV: `robotics_maze/results/benchmark_results.csv`
- CSV rows: `600`
- Planners: `12`
- Mazes: `50`
- CSV SHA-256: `26f120507a37a3fbb72fdcf89cf8e63d2693b7c3f73ecb25f77fc09c1f7d64e7`

## Generated Figures
- `benchmark_runtime_ms.png`
  - Size: `2600x1700`
  - DPI metadata: `~300`
  - SHA-256: `1584ade9d3761eaeafc58b6766bb6e714126452b15d40f1aeb8fceda6e74c7a2`
- `benchmark_expansions.png`
  - Size: `2600x1700`
  - DPI metadata: `~300`
  - SHA-256: `55f87186ed43658474019818e13f61aa9e6b8a05e7338e8b8741501b52aa9f28`
- `benchmark_success_rate.png`
  - Size: `2600x1700`
  - DPI metadata: `~300`
  - SHA-256: `4502ccf34b5a05bbf2df79df973ce733d91c2f568816de225dc256595aa4f1b7`

## Deterministic Generation Notes
- Renderer implementation used only Python stdlib + Pillow (`PIL`), with no stochastic calls.
- Ranking and planner ordering were computed from CSV using the same policy as `robotics_maze/src/benchmark.py`:
  - `success_rate` (desc)
  - comparable solve time (asc; shared-success mean if available, else mean solve time)
  - comparable path length (asc; shared-success mean if available, else mean path length)
  - mean expansions (asc)
  - mean solve time (asc)
  - planner name (asc)
- All 12 planners solved all 50 mazes, so comparable set included all mazes.
- Fixed plotting parameters:
  - Canvas: `2600x1700`, white background
  - DPI metadata: `300`
  - Fixed font fallback order: Times New Roman, then Arial
  - Fixed color palette and margins
  - Runtime axis: logarithmic with ticks `[0.5, 1, 2, 5, 10, 20, 30]`
  - Expansions axis: logarithmic with ticks `[50, 100, 200, 500, 1000, 2000, 5000, 8000]`
  - Success axis: linear `[0, 20, 40, 60, 80, 100]`
- Re-running the same deterministic script with the same input CSV reproduces identical pixel outputs and hashes.

## Ranked Planner Order Used In All Three Figures
1. `r1_weighted_astar`
2. `r7_beam_search`
3. `greedy_best_first`
4. `r5_jump_point_search`
5. `r9_bidirectional_bfs`
6. `r8_fringe_search`
7. `astar`
8. `dijkstra`
9. `r2_bidirectional_astar`
10. `r3_theta_star`
11. `r6_lpa_star`
12. `r4_idastar`
