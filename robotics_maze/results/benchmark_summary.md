# Benchmark Summary

- Generated (UTC): 2026-02-26T22:31:51+00:00
- Mazes: 50
- Maze size (cells): 15x15
- Maze algorithm: backtracker
- Seed: 7
- Top planner: r1_weighted_astar
- Ranking policy: success rate (desc), mean solve time (asc), mean expansions (asc), mean path length (asc).

| Rank | Planner | Success Rate | Mean Solve Time (ms) | Delta vs #1 (ms) | Mean Path Length | Mean Expansions |
|---:|---|---:|---:|---:|---:|---:|
| 1 | r1_weighted_astar | 100.0% (50/50) | 0.47 | +0.00 | 142.72 | 187.16 |
| 2 | r7_beam_search | 100.0% (50/50) | 0.57 | +0.10 | 142.72 | 198.36 |
| 3 | greedy_best_first | 100.0% (50/50) | 0.64 | +0.16 | 142.72 | 171.96 |
| 4 | r5_jump_point_search | 100.0% (50/50) | 0.64 | +0.16 | 142.72 | 57.26 |
| 5 | r9_bidirectional_bfs | 100.0% (50/50) | 0.69 | +0.21 | 142.72 | 201.52 |
| 6 | r8_fringe_search | 100.0% (50/50) | 0.73 | +0.25 | 142.72 | 190.30 |
| 7 | astar | 100.0% (50/50) | 0.73 | +0.26 | 142.72 | 189.06 |
| 8 | dijkstra | 100.0% (50/50) | 0.74 | +0.27 | 142.72 | 200.52 |
| 9 | r2_bidirectional_astar | 100.0% (50/50) | 1.74 | +1.26 | 142.72 | 468.02 |
| 10 | r3_theta_star | 100.0% (50/50) | 1.95 | +1.47 | 45.40 | 189.18 |
| 11 | r6_lpa_star | 100.0% (50/50) | 7.13 | +6.65 | 142.72 | 295.10 |
| 12 | r4_idastar | 100.0% (50/50) | 27.27 | +26.80 | 142.72 | 7061.34 |
