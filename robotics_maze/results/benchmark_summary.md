# Benchmark Summary

- Generated (UTC): 2026-02-27T11:56:29+00:00
- Mazes: 50
- Maze size (cells): 15x15
- Maze algorithm: backtracker
- Seed: 7
- Top planner: r1_weighted_astar
- Comparable mazes: mazes solved by every planner (shared-success set).
- Ranking policy: success rate (desc), comparable solve time (asc), mean expansions (asc), mean solve time (asc), planner name (asc).

| Rank | Planner | Success Rate | Comparable Mazes | Comparable Solve Time (ms) | Delta vs #1 (ms) | Comparable Path Length | Mean Expansions |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | r1_weighted_astar | 100.0% (50/50) | 50 | 0.93 | +0.00 | 142.72 | 187.16 |
| 2 | r5_jump_point_search | 100.0% (50/50) | 50 | 1.15 | +0.22 | 142.72 | 57.26 |
| 3 | r7_beam_search | 100.0% (50/50) | 50 | 1.24 | +0.31 | 142.72 | 198.36 |
| 4 | greedy_best_first | 100.0% (50/50) | 50 | 1.27 | +0.34 | 142.72 | 171.96 |
| 5 | r9_bidirectional_bfs | 100.0% (50/50) | 50 | 1.47 | +0.54 | 142.72 | 201.52 |
| 6 | astar | 100.0% (50/50) | 50 | 1.48 | +0.55 | 142.72 | 189.06 |
| 7 | r8_fringe_search | 100.0% (50/50) | 50 | 1.49 | +0.56 | 142.72 | 190.30 |
| 8 | dijkstra | 100.0% (50/50) | 50 | 1.60 | +0.67 | 142.72 | 200.52 |
| 9 | r2_bidirectional_astar | 100.0% (50/50) | 50 | 3.72 | +2.79 | 142.72 | 468.02 |
| 10 | r3_theta_star | 100.0% (50/50) | 50 | 4.15 | +3.22 | 97.96 | 189.18 |
| 11 | r6_lpa_star | 100.0% (50/50) | 50 | 11.59 | +10.66 | 142.72 | 295.10 |
| 12 | r4_idastar | 100.0% (50/50) | 50 | 74.38 | +73.45 | 142.72 | 7061.34 |
