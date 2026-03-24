# Benchmark Test Report

- Source snapshot: `robotics_maze/results/benchmark_summary.md` (Generated UTC `2026-02-27T00:14:49+00:00`)
- Scope: 12 planners, 50 mazes, 15x15 cells, maze algorithm `backtracker`, seed `7`
- Ranking policy: success rate (desc), comparable solve time (asc), mean expansions (asc), mean solve time (asc), planner name (asc)
- Reliability: all planners solved 50/50 mazes (100.0%) on the shared-success set

## Key ranking (comparable solve time on shared-success set)

1. `r1_weighted_astar` - `0.35 ms` (delta `+0.00 ms`)
2. `r7_beam_search` - `0.42 ms` (delta `+0.07 ms`)
3. `r5_jump_point_search` - `0.45 ms` (delta `+0.10 ms`)

## Key metrics and spread

- Mid-pack reference: `astar` (`0.52 ms`), `dijkstra` (`0.54 ms`), `r9_bidirectional_bfs` (`0.54 ms`)
- Slowest planners: `r6_lpa_star` (`3.95 ms`, `+3.60 ms`) and `r4_idastar` (`22.56 ms`, `+22.20 ms`)
- Expansion efficiency: `r5_jump_point_search` has the lowest mean expansions (`57.26`) while ranking #3 in solve time
- Path-length caveat: `r3_theta_star` reports shorter comparable paths (`97.96` vs `142.72` for most planners) due to line-of-sight shortcutting

## Traceability

- Snapshot metadata: `benchmark_summary.md` lines 3-10
- Ranking and metrics: `benchmark_summary.md` lines 12-25
