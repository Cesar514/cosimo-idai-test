# SOTA Planner Shortlist (2021+) for Maze/Mobile-Robot Navigation

## Scope
- Objective: identify post-2021 planning approaches beyond vanilla A* and rank them for this repository.
- Repository context: current planners are grid-centric and expose `(path, metrics)` (see `robotics_maze/src/alt_planners` and `robotics_maze/src/benchmark.py`).
- Ranking criteria: recent evidence, practical integration fit, expected benchmarking impact, and implementation risk.

## Ranked List (Best Practical Fit First)

| Rank | Approach | Post-2021 evidence | Fit for this repo | Implementation risk |
|---|---|---|---|---|
| 1 | **Learned Local Heuristics for A*** (LoHA* line) | Data-efficient LoHA* workflow (SoCS 2024) reports `<1/10th` data-collection work (expansion-based) for the same amount of training data [4]. | **High**: directly extends existing A*/LPA* style planners on occupancy grids. | Medium |
| 2 | **Cost-aware Hybrid-A* / State Lattice (Smac family)** | Smac planner provides optimized 2D A*/Hybrid-A*/Lattice implementations for ROS2 Nav2 [1], with documented replanning/performance features and kinematic feasibility support [2]. | **High** for next-stage mobile-robot realism (SE2 constraints) once we add heading-aware state. | Medium-High |
| 3 | **Incremental Generalized Hybrid A*** (IGHA*) | IGHA* (accepted to IEEE RA-L, Nov 2025) reports up to **6x fewer expansions** vs optimized HA* baseline in reported settings [3]. | Medium: strong once a Hybrid-A* baseline exists; less immediate for current point-robot grid stack. | High |
| 4 | **Guided RRT* family** (Neural Informed / Hybrid sampling / attention-guided) | Neural Informed RRT* (ICRA 2024) keeps probabilistic completeness and asymptotic optimality while improving benchmark performance [6]; Hybrid-RRT* (2024) reports faster convergence and fewer explored nodes [7]; HAGRRT* (2026) reports further sample/time gains in maze and forest maps [8]. | Medium: good for larger continuous maps and non-grid scaling tests. | Medium-High |
| 5 | **Neural A*** (differentiable search) | ICML 2021 paper reports improved optimality-efficiency trade-off over prior data-driven planners [5]. | Medium: excellent research candidate for grid mazes; requires supervised dataset/training pipeline. | High |
| 6 | **D*Lite + local dynamic-window coupling** | 2024 D*Lite+DWA fusion paper reports improved global-local performance in complex dynamic settings (time/risk metrics) [9]. | Medium-High: aligns with current incremental-planning direction (`r6_lpa_star`) plus simulator loop. | Medium |
| 7 | **Uncertainty-aware MPC local trajectory planning** | 2025 Nav2-oriented MPC preprint models obstacle uncertainty (VAR + Mahalanobis constraints) and reports improved collision avoidance in Gazebo tests [10]. | Medium: valuable once dynamic multi-agent obstacles are core benchmark targets. | High |

## Why This Ranking
- Ranks prioritize **near-term implementability in this repo** over theoretical novelty alone.
- Methods requiring new state spaces (SE2/kinodynamic) are ranked below grid-compatible learned-heuristic upgrades.
- Sampling and MPC methods are strong but currently higher-cost to integrate into the existing benchmark contract.

## Practical Notes for This Repository

### 1) Best next implementation target: LoHA-style planner plugin
- Add `robotics_maze/src/alt_planners/r11_loha_astar.py` with fallback to admissible heuristic when no model is loaded.
- Preserve benchmark compatibility: `(path, metrics)` with at least `status`, `path_cost`, `elapsed_ms`, `expanded_nodes`.
- Extend `robotics_maze/src/benchmark.py` planner discovery and compare against `astar`, `r5_jump_point_search`, `r6_lpa_star`.

### 2) Second target: Hybrid-A* (Smac-inspired)
- Introduce SE2 node state `(row, col, theta_bin)` and motion primitives.
- Keep a 2D projection for existing waypoint-following in `sim.py` until controller is heading-aware.
- Add metrics for turning feasibility (e.g., curvature violations, reverse maneuvers).

### 3) Third target: Guided RRT* for large-map stress tests
- Add separate benchmark mode for continuous coordinates and stochastic planners.
- Run many seeds per map and rank by distribution statistics (median/p95 time, success rate), not single-run time.

## Inference Notes
- Empirical percentages above are reported by the cited papers/docs.
- **Repository-fit ranking is an engineering inference** from those sources plus current code structure in `robotics_maze/src`.

## References
1. Macenski, S., Booker, M., Wallace, J., Fischer, T. (2024, rev. 2025). *Open-Source, Cost-Aware Kinematically Feasible Planning for Mobile and Surface Robotics*. arXiv:2401.13078. https://arxiv.org/abs/2401.13078
2. ROS2 Nav2 docs. *nav2_smac_planner (Humble)*. https://docs.ros.org/en/humble/p/nav2_smac_planner/
3. Talia, S., Salzman, O., Srinivasa, S. (2025, rev. 2025). *Incremental Generalized Hybrid A\**. arXiv:2508.13392 (accepted to IEEE RA-L, per arXiv comments). https://arxiv.org/abs/2508.13392
4. Veerapaneni, R., Park, J., Saleem, M. S., Likhachev, M. (2024). *A Data Efficient Framework for Learning Local Heuristics*. arXiv:2404.06728 (accepted to SoCS 2024, per arXiv comments). https://arxiv.org/abs/2404.06728
5. Yonetani, R., Taniai, T., Barekatain, M., Nishimura, M., Kanezaki, A. (2021). *Path Planning using Neural A\* Search*. ICML 2021, PMLR 139. https://proceedings.mlr.press/v139/yonetani21a.html
6. Huang, Z., Chen, H., Pohovey, J., Driggs-Campbell, K. (2023/2024). *Neural Informed RRT\**. arXiv:2309.14595 (accepted by ICRA 2024, per arXiv comments). https://arxiv.org/abs/2309.14595
7. Ganesan, S., Ramalingam, B., Mohan, R. E. (2024). *A hybrid sampling-based RRT\* path planning algorithm for autonomous mobile robot navigation*. Expert Systems with Applications, 258, 125206. https://doi.org/10.1016/j.eswa.2024.125206
8. Loulou, A., Unel, M. (2026). *Hybrid attention-guided RRT\*: Learning spatial sampling priors for accelerated path planning*. Robotics and Autonomous Systems, 198, 105338. https://doi.org/10.1016/j.robot.2026.105338
9. Gao, Y., Han, Q., Feng, S., Wang, Z., Meng, T., Yang, J. (2024). *Improvement and Fusion of D\* Lite Algorithm and Dynamic Window Approach for Path Planning in Complex Environments*. Machines, 12(8), 525. https://doi.org/10.3390/machines12080525
10. Schöneberg, E., Schröder, M., Görges, D., Schotten, H. D. (2025). *Trajectory Planning with Model Predictive Control for Obstacle Avoidance Considering Prediction Uncertainty*. arXiv:2504.19193 (accepted to IFAC, per arXiv comments). https://arxiv.org/abs/2504.19193
