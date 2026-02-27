# Benchmark Summary

- Generated (UTC): 2026-02-27T10:31:02+00:00
- Mazes: 1
- Maze size (cells): 9x9
- Maze algorithm: backtracker
- Seed: 7
- Top planner: r1_weighted_astar
- Comparable mazes: mazes solved by every planner (shared-success set).
- Ranking policy: success rate (desc), comparable solve time (asc), mean expansions (asc), mean solve time (asc), planner name (asc).

| Rank | Planner | Success Rate | Comparable Mazes | Comparable Solve Time (ms) | Delta vs #1 (ms) | Comparable Path Length | Mean Expansions |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | r1_weighted_astar | 100.0% (1/1) | 1 | 0.24 | +0.00 | 108.00 | 135.00 |
| 2 | r7_beam_search | 100.0% (1/1) | 1 | 0.29 | +0.06 | 108.00 | 140.00 |
| 3 | r5_jump_point_search | 100.0% (1/1) | 1 | 0.30 | +0.06 | 108.00 | 39.00 |
| 4 | greedy_best_first | 100.0% (1/1) | 1 | 0.30 | +0.06 | 108.00 | 133.00 |
| 5 | dijkstra | 100.0% (1/1) | 1 | 0.32 | +0.08 | 108.00 | 141.00 |
| 6 | astar | 100.0% (1/1) | 1 | 0.34 | +0.10 | 108.00 | 136.00 |
| 7 | r9_bidirectional_bfs | 100.0% (1/1) | 1 | 0.35 | +0.11 | 108.00 | 140.00 |
| 8 | r8_fringe_search | 100.0% (1/1) | 1 | 0.36 | +0.13 | 108.00 | 137.00 |
| 9 | r2_bidirectional_astar | 100.0% (1/1) | 1 | 0.68 | +0.44 | 108.00 | 281.00 |
| 10 | r3_theta_star | 100.0% (1/1) | 1 | 0.92 | +0.69 | 76.00 | 136.00 |
| 11 | r6_lpa_star | 100.0% (1/1) | 1 | 0.99 | +0.75 | 108.00 | 137.00 |
| 12 | r4_idastar | 100.0% (1/1) | 1 | 7.69 | +7.45 | 108.00 | 2988.00 |
