# Pre-2021 Planning Literature (Alternatives to Vanilla A*)

## Scope
- Goal: compile pre-2021 references relevant to maze/mobile-robot planning alternatives to vanilla A*.
- Inclusion window: publication year <= 2020.
- Emphasis: methods that are practical for grid mazes, mobile robot navigation, dynamic replanning, or local collision avoidance.
- Justification format per reference: exactly 4 sentences (contribution, relevance, limitation, implementation-priority impact).

## References and 4-Sentence Justifications

### 1) Khatib (1986) - Artificial Potential Fields
**Citation:** Khatib, O. (1986). *Real-Time Obstacle Avoidance for Manipulators and Mobile Robots*. International Journal of Robotics Research, 5(1), 90-98. https://doi.org/10.1177/027836498600500106
- Contribution: This paper introduced the artificial potential field framework for real-time reactive obstacle avoidance with direct control-level integration.
- Relevance: It remains a foundational non-graph alternative when the robot must react continuously in maze corridors or partially observed environments.
- Limitation: The method is known to suffer from local minima and oscillations near obstacle boundaries without additional escape heuristics.
- Implementation-priority impact: It is medium priority as a lightweight local safety layer paired with a stronger global planner.

### 2) Borenstein and Koren (1991) - VFH
**Citation:** Borenstein, J., & Koren, Y. (1991). *The Vector Field Histogram - Fast Obstacle Avoidance for Mobile Robots*. IEEE Transactions on Robotics and Automation, 7(3), 278-288. https://doi.org/10.1109/70.88137
- Contribution: VFH proposed a histogram-grid representation that converts local obstacle structure into steerable motion commands.
- Relevance: The approach is directly applicable to maze-style navigation where rapid local decisions are needed in narrow passages.
- Limitation: It is a local planner and does not guarantee global path optimality or completeness by itself.
- Implementation-priority impact: It is medium priority for improving short-horizon obstacle avoidance once a global planner provides waypoints.

### 3) Fox, Burgard, and Thrun (1997) - Dynamic Window Approach
**Citation:** Fox, D., Burgard, W., & Thrun, S. (1997). *The Dynamic Window Approach to Collision Avoidance*. IEEE Robotics & Automation Magazine, 4(1), 23-33. https://doi.org/10.1109/100.580977
- Contribution: DWA framed local planning in velocity space under dynamic constraints to choose collision-free commands in real time.
- Relevance: It is highly relevant for mobile robots that must track maze paths while respecting acceleration and turning limits.
- Limitation: DWA can be short-sighted in cluttered regions unless coupled to a robust global planner.
- Implementation-priority impact: It is high priority for realistic control-layer integration after global path generation is stable.

### 4) Stentz (1994) - Original D*
**Citation:** Stentz, A. (1994). *Optimal and Efficient Path Planning for Partially-Known Environments*. Proceedings of ICRA 1994. https://doi.org/10.1109/ROBOT.1994.351061
- Contribution: This work introduced D* for incremental replanning in partially known environments with changing edge costs.
- Relevance: D* directly targets the repeated replanning pattern seen when maze knowledge updates online.
- Limitation: The original formulation is algorithmically more complex and less pedagogically clean than later D* Lite formulations.
- Implementation-priority impact: It is medium priority as historical grounding, with D* Lite usually preferred for implementation.

### 5) Stentz (1995) - Focused D*
**Citation:** Stentz, A. (1995). *The Focussed D* Algorithm for Real-Time Replanning*. Proceedings of IJCAI 1995, 1652-1659. https://www.ri.cmu.edu/publications/the-focussed-d-algorithm-for-real-time-replanning/
- Contribution: Focused D* improved practical replanning speed by focusing repairs on affected search regions.
- Relevance: The paper is central for mobile robots operating in unknown terrain where map updates are frequent.
- Limitation: The algorithmic description is less straightforward to adapt than modern incremental-search variants.
- Implementation-priority impact: It is medium priority as a benchmark reference to justify choosing simpler descendants.

### 6) Koenig and Likhachev (2002) - D* Lite
**Citation:** Koenig, S., & Likhachev, M. (2002). *D* Lite*. AAAI 2002, 476-483. https://cdn.aaai.org/AAAI/2002/AAAI02-072.pdf
- Contribution: D* Lite recast dynamic replanning into a simpler incremental heuristic-search structure with formal guarantees.
- Relevance: It is one of the strongest alternatives to repeated A* reruns for maze environments that evolve over time.
- Limitation: Performance gains diminish when environment changes are global or extremely frequent relative to planning cycles.
- Implementation-priority impact: It is high priority because it offers strong theoretical guarantees with practical engineering tractability.

### 7) Koenig, Likhachev, and Furcy (2004) - Lifelong Planning A*
**Citation:** Koenig, S., Likhachev, M., & Furcy, D. (2004). *Lifelong Planning A**. Artificial Intelligence, 155(1-2), 93-146. https://doi.org/10.1016/j.artint.2003.12.001
- Contribution: LPA* provided a generalized incremental-search framework that reuses prior search effort across related problems.
- Relevance: It fits repeated maze episodes where only small map sections change between planning queries.
- Limitation: Benefits are limited when each new query is effectively unrelated to prior search structure.
- Implementation-priority impact: It is high priority for benchmark suites that repeatedly replan on structurally similar grids.

### 8) Likhachev, Gordon, and Thrun (2003) - ARA*
**Citation:** Likhachev, M., Gordon, G. J., & Thrun, S. (2003). *ARA*: Anytime A* with Provable Bounds on Sub-Optimality*. Advances in Neural Information Processing Systems 16 (NIPS 2003). https://papers.nips.cc/paper/2382-ara-anytime-a-with-provable-bounds-on-sub-optimality
- Contribution: ARA* introduced a bounded-suboptimal anytime search that quickly returns a feasible path and refines it over time.
- Relevance: It is useful when robots in mazes need fast initial plans with optional refinement under tighter time budgets.
- Limitation: Quality depends on weight-schedule tuning, and poor schedules can reduce practical gains.
- Implementation-priority impact: It is medium-high priority for real-time settings with variable compute budgets.

### 9) Likhachev et al. (2005) - Anytime Dynamic A*
**Citation:** Likhachev, M., Ferguson, D., Gordon, G., Stentz, A., & Thrun, S. (2005). *Anytime Dynamic A*: An Anytime, Replanning Algorithm*. ICAPS 2005, 262-271. https://www.ri.cmu.edu/publications/anytime-dynamic-a-an-anytime-replanning-algorithm/
- Contribution: AD* combined incremental replanning and anytime refinement into one framework for dynamic environments.
- Relevance: This is particularly relevant for mobile robots that must both react to map changes and improve path quality online.
- Limitation: The algorithm introduces additional complexity and parameterization compared with single-purpose planners.
- Implementation-priority impact: It is high priority when both responsiveness and progressive optimality are required.

### 10) Ferguson and Stentz (2006) - Field D*
**Citation:** Ferguson, D., & Stentz, A. (2006). *Using Interpolation to Improve Path Planning: The Field D* Algorithm*. Journal of Field Robotics, 23(2), 79-101. https://doi.org/10.1002/rob.20109
- Contribution: Field D* introduced interpolation-based updates that reduce grid-heading artifacts and produce smoother paths.
- Relevance: It is useful in maze maps where cell-center paths are too jagged for realistic robot motion.
- Limitation: Interpolation increases implementation complexity and still depends on discretized map structure.
- Implementation-priority impact: It is medium-high priority when path smoothness matters for downstream controllers.

### 11) Dolgov et al. (2008) - Hybrid A* for Autonomous Driving
**Citation:** Dolgov, D., Thrun, S., Montemerlo, M., & Diebel, J. (2008). *Practical Search Techniques in Path Planning for Autonomous Driving*. STAIR-08. https://ai.stanford.edu/~ddolgov/dolgov08gppSTAIR.html
- Contribution: This work documented practical Hybrid A* style search techniques that incorporate vehicle kinematic feasibility.
- Relevance: It is highly relevant when moving from point-robot mazes to realistic differential-drive or car-like robots.
- Limitation: It requires richer state representations and motion primitives that are heavier than pure 2D grid planning.
- Implementation-priority impact: It is high priority for upgrading from grid-optimality toward physically executable paths.

### 12) Daniel et al. (2010) - Theta*
**Citation:** Daniel, K., Nash, A., Koenig, S., & Felner, A. (2010). *Theta*: Any-Angle Path Planning on Grids*. Journal of Artificial Intelligence Research, 39, 533-579. https://doi.org/10.1613/jair.2994
- Contribution: Theta* enabled any-angle planning on grids by combining heuristic search with line-of-sight parent updates.
- Relevance: It is a strong maze-navigation option when shorter, less zig-zaggy paths are desired without continuous-space planning.
- Limitation: It is not guaranteed to return true shortest continuous paths and depends on efficient visibility checks.
- Implementation-priority impact: It is high priority as a practical quality upgrade over standard grid-constrained search.

### 13) Nash, Koenig, and Tovey (2010) - Lazy Theta*
**Citation:** Nash, A., Koenig, S., & Tovey, C. (2010). *Lazy Theta*: Any-Angle Path Planning and Path Length Analysis in 3D*. AAAI 2010. https://idm-lab.org/bib/abstracts/Koen10j.html
- Contribution: Lazy Theta* reduced expensive line-of-sight computations by delaying checks while preserving path-quality behavior.
- Relevance: It is relevant for larger maze grids or 3D voxel maps where visibility checks dominate runtime.
- Limitation: It still inherits Theta*-family dependence on geometric visibility routines and map discretization quality.
- Implementation-priority impact: It is medium-high priority when Theta* quality is desired but LOS cost is a bottleneck.

### 14) Harabor and Grastien (2011) - Jump Point Search
**Citation:** Harabor, D., & Grastien, A. (2011). *Online Graph Pruning for Pathfinding on Grid Maps*. AAAI 2011, 1114-1119. https://doi.org/10.1609/aaai.v25i1.7994
- Contribution: Jump Point Search introduced symmetry-breaking pruning rules that dramatically accelerate optimal grid search.
- Relevance: It is directly applicable to uniform-cost maze grids where many expansions in vanilla search are redundant.
- Limitation: Gains are reduced on weighted or irregular grids and when movement models deviate from JPS assumptions.
- Implementation-priority impact: It is high priority for benchmark speedups on classic occupancy-grid maze tasks.

### 15) Aine et al. (2016) - Multi-Heuristic A*
**Citation:** Aine, S., Swaminathan, S., Narayanan, V., Hwang, V., & Likhachev, M. (2016). *Multi-Heuristic A**. International Journal of Robotics Research, 35(1), 224-243. https://www.ri.cmu.edu/publications/multi-heuristic-a-2/
- Contribution: MHA* showed how multiple heuristic queues can be combined with guarantees to improve search guidance.
- Relevance: It is valuable for maze/mobile planning where one heuristic cannot capture corridor, clearance, and progress tradeoffs simultaneously.
- Limitation: It requires heuristic set design and tuning, which can add engineering complexity.
- Implementation-priority impact: It is medium priority once baseline planners are stable and heuristic diversity can be exploited.

### 16) Kavraki et al. (1996) - Probabilistic Roadmaps
**Citation:** Kavraki, L. E., Svestka, P., Latombe, J.-C., & Overmars, M. H. (1996). *Probabilistic Roadmaps for Path Planning in High-Dimensional Configuration Spaces*. IEEE Transactions on Robotics and Automation, 12(4), 566-580. https://doi.org/10.1109/70.508439
- Contribution: PRM introduced a two-phase sampling roadmap paradigm that became a cornerstone of motion planning.
- Relevance: It provides a non-grid alternative when maze-like constraints appear in higher-dimensional robot configuration spaces.
- Limitation: Single-query or highly dynamic scenarios can make roadmap construction overhead less favorable.
- Implementation-priority impact: It is medium priority for offline or repeated-query settings with richer robot kinematics.

### 17) Kuffner and LaValle (2000) - RRT-Connect
**Citation:** Kuffner, J. J., & LaValle, S. M. (2000). *RRT-Connect: An Efficient Approach to Single-Query Path Planning*. ICRA 2000, 995-1001. https://doi.org/10.1109/ROBOT.2000.844730
- Contribution: RRT-Connect introduced bidirectional tree growth with aggressive connect steps for fast feasible-path discovery.
- Relevance: It is useful for quickly finding traversable paths in cluttered spaces where grid search becomes expensive.
- Limitation: It prioritizes feasibility over optimality and often requires post-smoothing or optimization.
- Implementation-priority impact: It is medium priority for fast-first-path baselines in continuous-state planner tracks.

### 18) Karaman and Frazzoli (2011) - RRT*
**Citation:** Karaman, S., & Frazzoli, E. (2011). *Sampling-based Algorithms for Optimal Motion Planning*. International Journal of Robotics Research, 30(7), 846-894. https://doi.org/10.1177/0278364911406761
- Contribution: This paper established asymptotic optimality results and introduced RRT* and PRM* as principled optimal variants.
- Relevance: It is core literature for continuous-space alternatives when maze benchmarks expand beyond grid abstractions.
- Limitation: Convergence to high-quality solutions can be slow in narrow passages and high dimensions.
- Implementation-priority impact: It is medium-high priority for optimal continuous planning experiments and comparisons.

### 19) Gammell, Srinivasa, and Barfoot (2014) - Informed RRT*
**Citation:** Gammell, J. D., Srinivasa, S. S., & Barfoot, T. D. (2014). *Informed RRT*: Optimal Sampling-based Path Planning Focused via Direct Sampling of an Admissible Ellipsoidal Heuristic*. IROS 2014. https://doi.org/10.1109/IROS.2014.6942976
- Contribution: Informed RRT* focused sampling inside the subset that can improve current solutions, accelerating convergence.
- Relevance: It is a strong alternative for maze-like continuous domains where uninformed global sampling is inefficient.
- Limitation: It still depends on an initial feasible solution and can struggle in highly non-Euclidean cost landscapes.
- Implementation-priority impact: It is medium-high priority if RRT* is adopted and faster convergence is required.

### 20) Gammell, Srinivasa, and Barfoot (2015) - BIT*
**Citation:** Gammell, J. D., Srinivasa, S. S., & Barfoot, T. D. (2015). *Batch Informed Trees (BIT*): Sampling-based Optimal Planning via the Heuristically Guided Search of Implicit Random Geometric Graphs*. ICRA 2015, 3067-3074. https://doi.org/10.1109/ICRA.2015.7139620
- Contribution: BIT* unified ideas from graph search and sampling-based planning to improve anytime optimal planning efficiency.
- Relevance: It is relevant for larger maze/mobile planning problems where both optimality trend and runtime matter.
- Limitation: Implementation complexity is higher than basic RRT-family methods and requires careful data-structure handling.
- Implementation-priority impact: It is medium priority for advanced benchmarking after simpler planners are validated.

### 21) Strub and Gammell (2020) - AIT*
**Citation:** Strub, M. P., & Gammell, J. D. (2020). *Adaptively Informed Trees (AIT*): Fast Asymptotically Optimal Path Planning through Adaptive Heuristics*. arXiv:2002.06599. https://arxiv.org/abs/2002.06599
- Contribution: AIT* introduced adaptive heuristic estimation within informed sampling to improve convergence behavior.
- Relevance: It is relevant to maze/mobile robotics as a modern pre-2021 bridge between classical informed search and learned guidance.
- Limitation: The cited source is a preprint and evidence maturity is weaker than fully archival journal versions.
- Implementation-priority impact: It is medium-low priority unless the project specifically targets cutting-edge informed sampling research.

## Coverage Check
- Total references: **21**
- All references are pre-2021: **Yes**
- Each reference includes a 4-sentence justification: **Yes**
