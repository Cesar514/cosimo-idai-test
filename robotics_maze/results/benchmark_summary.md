# Benchmark Summary

- Generated (UTC): 2026-02-27T00:14:49+00:00
- Mazes: 50
- Maze size (cells): 15x15
- Maze algorithm: backtracker
- Seed: 7
- Top planner: r1_weighted_astar
- Comparable mazes: mazes solved by every planner (shared-success set).
- Ranking policy: success rate (desc), comparable solve time (asc), mean expansions (asc), mean solve time (asc), planner name (asc).

| Rank | Planner | Success Rate | Comparable Mazes | Comparable Solve Time (ms) | Delta vs #1 (ms) | Comparable Path Length | Mean Expansions |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | r1_weighted_astar | 100.0% (50/50) | 50 | 0.35 | +0.00 | 142.72 | 187.16 |
| 2 | r7_beam_search | 100.0% (50/50) | 50 | 0.42 | +0.07 | 142.72 | 198.36 |
| 3 | r5_jump_point_search | 100.0% (50/50) | 50 | 0.45 | +0.10 | 142.72 | 57.26 |
| 4 | greedy_best_first | 100.0% (50/50) | 50 | 0.46 | +0.11 | 142.72 | 171.96 |
| 5 | r8_fringe_search | 100.0% (50/50) | 50 | 0.52 | +0.17 | 142.72 | 190.30 |
| 6 | astar | 100.0% (50/50) | 50 | 0.52 | +0.17 | 142.72 | 189.06 |
| 7 | dijkstra | 100.0% (50/50) | 50 | 0.54 | +0.18 | 142.72 | 200.52 |
| 8 | r9_bidirectional_bfs | 100.0% (50/50) | 50 | 0.54 | +0.19 | 142.72 | 201.52 |
| 9 | r2_bidirectional_astar | 100.0% (50/50) | 50 | 1.25 | +0.90 | 142.72 | 468.02 |
| 10 | r3_theta_star | 100.0% (50/50) | 50 | 1.55 | +1.20 | 97.96 | 189.18 |
| 11 | r6_lpa_star | 100.0% (50/50) | 50 | 3.95 | +3.60 | 142.72 | 295.10 |
| 12 | r4_idastar | 100.0% (50/50) | 50 | 22.56 | +22.20 | 142.72 | 7061.34 |
