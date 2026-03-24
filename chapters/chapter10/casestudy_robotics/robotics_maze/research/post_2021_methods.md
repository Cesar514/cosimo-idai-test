# Post-2021 Planning Methods (Alternatives to Vanilla A*)

## Scope
- Objective: compile post-2021 literature (2022+) relevant to maze/mobile-robot planning alternatives to vanilla A*.
- Inclusion focus: search variants beyond vanilla A*, sampling-based planners, swarm/metaheuristics, reinforcement learning, and MPC-based motion planning.
- Output requirement: each reference includes a 4-sentence justification tied to maze or mobile-robot navigation relevance.

## References with 4-Sentence Justifications

### 1) Open-Source, Cost-Aware Kinematically Feasible Planning for Mobile and Surface Robotics (2024)
Reference: Macenski, S., Booker, M., Wallace, J., Fischer, T. (2024). *Open-Source, Cost-Aware Kinematically Feasible Planning for Mobile and Surface Robotics*. arXiv:2401.13078. https://arxiv.org/abs/2401.13078

Justification: This work documents practical Hybrid-A* and state-lattice style planning that directly competes with vanilla grid A* for real mobile robots. It is highly relevant to maze-style benchmarks because it addresses kinematic feasibility, which simple A* often ignores. The paper is also implementation-oriented and maps well to ROS2/Nav2 deployments, making transfer into engineering code straightforward. It is a preprint, but the open-source linkage and detailed planner design make it a strong technical reference.

### 2) Incremental Generalized Hybrid A* (2025)
Reference: Talia, S., Salzman, O., Srinivasa, S. (2025). \"Incremental Generalized Hybrid A*\". arXiv:2508.13392. https://arxiv.org/abs/2508.13392

Justification: IGHA* is relevant because it targets repeated replanning in changing environments, which is common in dynamic mazes and mobile navigation. The method extends hybrid search with incremental updates, reducing wasteful full re-search behavior. That design provides a concrete alternative when vanilla A* is too brittle under frequent map changes. The arXiv record notes RA-L acceptance, so this is near peer-reviewed maturity.

### 3) A Data Efficient Framework for Learning Local Heuristics (2024)
Reference: Veerapaneni, R., Park, J., Saleem, M. S., Likhachev, M. (2024). *A Data Efficient Framework for Learning Local Heuristics*. arXiv:2404.06728. https://arxiv.org/abs/2404.06728

Justification: This paper proposes learned local guidance that changes how heuristic search explores space, rather than relying only on static handcrafted heuristics. It is relevant to maze planning because local structure is often repetitive and can be learned to reduce node expansions. The approach remains close enough to search-based planning to integrate with existing planner stacks and benchmarking harnesses. The paper is a preprint but includes a strong signal of quality through SoCS acceptance.

### 4) Neural Informed RRT* (2023/2024)
Reference: Huang, Z., Chen, H., Pohovey, J., Driggs-Campbell, K. (2023). \"Neural Informed RRT*: Learning-based Path Planning with Point Cloud State Representations under Admissible Ellipsoidal Constraints\". arXiv:2309.14595. https://arxiv.org/abs/2309.14595

Justification: Neural Informed RRT* is directly relevant as a sampling-based alternative to A* for continuous and cluttered mobile-robot spaces. It combines learning with admissible informed constraints, aiming to preserve strong search properties while accelerating convergence. This makes it useful when maze-like environments are large, partially known, or represented as point clouds instead of dense grids. The work is a preprint with ICRA acceptance indicated in the manuscript comments.

### 5) A Hybrid Sampling-Based RRT* Path Planning Algorithm for Autonomous Mobile Robot Navigation (2024)
Reference: Ganesan, S., Ramalingam, B., Mohan, R. E. (2024). \"A hybrid sampling-based RRT* path planning algorithm for autonomous mobile robot navigation\". Expert Systems with Applications, 258, 125206. https://doi.org/10.1016/j.eswa.2024.125206

Justification: This journal paper is relevant because it improves sampling efficiency and path quality in a mature RRT* framework. Hybrid sampling strategies are useful in mazes where narrow passages and dead ends degrade uninformed sampling. The method provides a practical baseline for continuous-space navigation where A* discretization becomes costly or inaccurate. Its peer-reviewed publication in ESWA makes it a strong citation for applied planning alternatives.

### 6) Improved Bidirectional RRT* Algorithm for Robot Path Planning (2023)
Reference: Xin, P., Wang, X., Liu, X., Wang, Y., et al. (2023). \"Improved Bidirectional RRT* Algorithm for Robot Path Planning\". Sensors, 23(2), 1041. https://doi.org/10.3390/s23021041

Justification: Bidirectional growth is relevant for maze domains because it can cut search depth in environments with long detours. This paper provides a concrete post-2021 variant focused on practical gains over baseline RRT* behavior. It is particularly useful for teams comparing graph-search methods to continuous sampling planners under similar map constraints. As a peer-reviewed article with a DOI, it is suitable for inclusion in an implementation-focused literature set.

### 7) Path Planning of a Mobile Robot Based on the Improved RRT Algorithm (2023)
Reference: Li, X., Tong, Y. (2023). *Path Planning of a Mobile Robot Based on the Improved RRT Algorithm*. Applied Sciences, 14(1), 25. https://doi.org/10.3390/app14010025

Justification: This work is relevant because it targets practical RRT enhancements for mobile robots rather than theoretical-only analysis. Improved RRT variants are common alternatives when A* struggles with high-dimensional or nonholonomic constraints. The paper contributes directly to the design space of sampling heuristics and tree expansion rules that can be benchmarked in maze-like scenes. It is a recent peer-reviewed source and therefore useful as a reproducible citation.

### 8) Path Planning of a Mobile Robot Based on the Improved RRT* Algorithm (2024)
Reference: Wang, J., Zheng, E. (2024). *Path Planning of a Mobile Robot Based on the Improved Rapidly Exploring Random Trees Star Algorithm*. Electronics, 13(12), 2340. https://doi.org/10.3390/electronics13122340

Justification: This paper is relevant because it analyzes an improved RRT* pipeline for mobile-robot path planning with attention to path quality. It serves as a post-2021 point of comparison for whether tuning sampling and rewiring can outperform plain A* on complex maps. The method is applicable to maze-like obstacles where global structure is hard to encode in a fixed heuristic. It is peer-reviewed and includes enough algorithmic detail to support implementation replication.

### 9) Multi-Strategy Bidirectional RRT* for Efficient Mobile Robot Path Planning (2025)
Reference: Huang, Y., Jiang, W., Xu, S. (2025). \"A multi strategy bidirectional RRT* algorithm for efficient mobile robot path planning\". Scientific Reports, 15, 13915. https://doi.org/10.1038/s41598-025-13915-2

Justification: This 2025 study is relevant because it combines multiple tree-growth and connection tactics in a single bidirectional RRT* framework. Multi-strategy planners are valuable for maze tasks where one exploration bias fails across all map topologies. The paper adds fresh empirical evidence in a peer-reviewed venue for modern sampling alternatives to A*-centric pipelines. It can be used as a benchmark reference when evaluating search robustness and runtime variability.

### 10) Hybrid Attention-Guided RRT* (2026)
Reference: Loulou, A., Unel, M. (2026). \"Hybrid attention-guided RRT*: Learning spatial sampling priors for accelerated path planning\". Robotics and Autonomous Systems, 198, 105338. https://doi.org/10.1016/j.robot.2026.105338

Justification: This paper is highly relevant because it introduces learned attention priors into RRT* sampling, directly addressing inefficient random exploration. Attention-guided sampling is especially useful in maze-like maps with structured corridors and bottlenecks. It represents a modern bridge between classical sampling guarantees and data-driven guidance. Publication in Robotics and Autonomous Systems provides strong peer-reviewed credibility for this direction.

### 11) Path Planning of Intelligent Mobile Robots with an Improved RRT Algorithm (2025)
Reference: Zhu, W., Qiu, G. (2025). *Path Planning of Intelligent Mobile Robots with an Improved RRT Algorithm*. Applied Sciences, 15(6), 3370. https://doi.org/10.3390/app15063370

Justification: This 2025 work contributes another post-2021 RRT improvement that can be compared against older sampling baselines. It is relevant because practical planner deployments often rely on incremental heuristic refinements rather than entirely new paradigms. The approach broadens the evidence base for how RRT variants behave in mobile-robot navigation settings similar to maze tasks. It is peer-reviewed and easy to trace through its DOI for reproducible citation.

### 12) Dynamic Path Planning via Ant Colony + Dynamic Window (2022)
Reference: Yang, L., Fu, L., Li, P., Mao, J., et al. (2022). *An Effective Dynamic Path Planning Approach for Mobile Robots Based on Ant Colony Fusion Dynamic Windows*. Machines, 10(1), 50. https://doi.org/10.3390/machines10010050

Justification: This paper is relevant because it fuses global swarm-based optimization with local reactive control, which is a common alternative architecture to A*. The combination is useful in dynamic maze scenarios where global and local decisions must be coordinated online. It provides a concrete post-2021 reference for hybrid global-local planning pipelines in mobile robotics. As a peer-reviewed article, it supports comparisons against search-centric baselines.

### 13) D*Lite + DWA Fusion in Complex Environments (2024)
Reference: Gao, Y., Han, Q., Feng, S., Wang, Z., et al. (2024). *Improvement and Fusion of D*Lite Algorithm and Dynamic Window Approach for Path Planning in Complex Environments*. Machines, 12(8), 525. https://doi.org/10.3390/machines12080525

Justification: This paper is strongly relevant because D*Lite provides incremental global replanning while DWA handles local collision avoidance. That architecture is directly suited to maze-like environments with evolving obstacle layouts. It offers a practical alternative to rerunning vanilla A* every time the environment changes. The work is post-2021, peer-reviewed, and aligned with real mobile-robot software constraints.

### 14) Improved ACO + B-Spline for Ackerman Mobile Robot Path Smoothing (2024)
Reference: Huo, F., Zhu, S., Dong, H., Ren, W. (2024). *A new approach to smooth path planning of Ackerman mobile robot based on improved ACO algorithm and B-spline curve*. Robotics and Autonomous Systems, 180, 104655. https://doi.org/10.1016/j.robot.2024.104655

Justification: This work is relevant because it addresses both route discovery and trajectory smoothness, which matter for physically constrained mobile robots. Ackerman steering constraints make vanilla A* paths difficult to execute without substantial post-processing. The improved ACO plus spline formulation provides an explicit alternative pipeline for feasible, smooth motion in cluttered maps. Its publication in a core robotics journal improves citation quality for engineering decisions.

### 15) Intelligently Enhanced Ant Colony Optimization for Global Planning (2025)
Reference: Li, P., Wei, L., Wu, D. (2025). *An Intelligently Enhanced Ant Colony Optimization Algorithm for Global Path Planning of Mobile Robots in Engineering Applications*. Sensors, 25(5), 1326. https://doi.org/10.3390/s25051326

Justification: This paper contributes a recent global-planning ACO variant, offering another non-A* strategy for maze-like pathfinding. It is relevant when deterministic heuristic search becomes brittle under map complexity or multi-objective costs. The algorithmic emphasis on enhanced pheromone and search behavior provides design ideas for adaptive global planners. The source is peer-reviewed and current enough to represent post-2021 state of practice.

### 16) Improved Q-Evaluation ACO for Mobile Robot Path Planning (2025)
Reference: Li, D., Wang, L. (2025). *Research on mobile robot path planning based on improved Q-evaluation ant colony optimization algorithm*. Engineering Applications of Artificial Intelligence, 150, 111890. https://doi.org/10.1016/j.engappai.2025.111890

Justification: This study is relevant because it injects Q-evaluation concepts into ACO to improve path planning decisions. That hybridization reflects a broader trend of combining learning-inspired scoring with classical metaheuristics. It gives a concrete alternative to A* for environments where multi-criteria optimization matters more than strict shortest-path guarantees. Publication in EAAI adds strong applied-AI credibility.

### 17) RL-Based Navigation in Unknown and Complex Environments (2024)
Reference: Raj, R., Kos, A. (2024). *Intelligent mobile robot navigation in unknown and complex environment using reinforcement learning technique*. Scientific Reports, 14, 72857. https://doi.org/10.1038/s41598-024-72857-3

Justification: This paper is relevant because it removes reliance on explicit global graph search and instead learns navigation policies from interaction. Unknown environments are a key regime where vanilla A* often requires frequent remapping and replanning overhead. The work provides empirical reinforcement-learning evidence in settings close to maze exploration with partial information. It is a peer-reviewed 2024 source in a broad, visible journal.

### 18) Deep RL Path Following for Autonomous Mobile Robots (2024)
Reference: Cao, Y., Ni, K., Kawaguchi, T., Hashimoto, S. (2024). *Path Following for Autonomous Mobile Robots with Deep Reinforcement Learning*. Sensors, 24(2), 561. https://doi.org/10.3390/s24020561

Justification: This article is relevant because path-following robustness is a practical bottleneck after global planning in maze-like environments. Deep RL control offers an alternative to purely geometric local planners paired with A*. It is useful for evaluating end-to-end behavior where tracking errors and disturbances dominate runtime performance. The paper is post-2021 and peer-reviewed, so it fits a modern evidence base.

### 19) Optimized Q-Learning for Mobile Robot Local Path Planning (2024)
Reference: Zhou, Q., Lian, Y., Wu, J., Zhu, M., et al. (2024). *An optimized Q-Learning algorithm for mobile robot local path planning*. Knowledge-Based Systems, 300, 111400. https://doi.org/10.1016/j.knosys.2024.111400

Justification: This work is relevant because local planning quality often determines whether a global planner succeeds in cluttered mazes. Optimized Q-learning provides a lightweight learning alternative to fixed-rule local controllers and can complement non-A* global methods. The paper offers recent, application-driven evidence from a strong AI systems journal. It is a credible reference for hybrid planning stacks that mix global and learned local decision layers.

### 20) DRL Local Planning in Dynamic Environments (2024)
Reference: Tao, B., Kim, J.-H. (2024). *Deep reinforcement learning-based local path planning in dynamic environments for mobile robot*. Journal of King Saud University - Computer and Information Sciences, 36(10), 102254. https://doi.org/10.1016/j.jksuci.2024.102254

Justification: This paper is relevant because it addresses dynamic obstacles, a common failure mode for static shortest-path planners like vanilla A*. DRL local planning can adapt online without fully recomputing a global graph each time the scene changes. The method is useful for benchmarking responsiveness and safety tradeoffs in maze-like navigation loops. It is peer-reviewed and recent, making it suitable for post-2021 method coverage.

### 21) DRL Path Planning for Wheeled Mobile Robots in Unknown Environments (2024)
Reference: Wen, T., Wang, X., Zheng, Z., Sun, Z. (2024). *A DRL-based path planning method for wheeled mobile robots in unknown environments*. Computers and Electrical Engineering, 121, 109425. https://doi.org/10.1016/j.compeleceng.2024.109425

Justification: This study is relevant because it targets unknown-environment navigation where model-based search often suffers from missing map information. DRL can internalize exploration and obstacle-avoidance behavior that is difficult to encode with handcrafted heuristics. The paper broadens the set of practical alternatives to A* by focusing on wheeled platforms and deployment constraints. It is a peer-reviewed 2024 publication and therefore a valid high-quality citation.

### 22) MPC for Efficient Avoidance of Ellipsoidal Obstacles (2025)
Reference: Rosenfelder, M., Carius, H., Herrmann-Wicklmayr, M., Eberhard, P., et al. (2025). *Efficient avoidance of ellipsoidal obstacles with model predictive control for mobile robots and vehicles*. Mechatronics, 104, 103386. https://doi.org/10.1016/j.mechatronics.2025.103386

Justification: This paper is relevant because MPC planners can optimize feasible motion directly under dynamic and geometric constraints. Ellipsoidal obstacle handling is useful for realistic mobile navigation where obstacles are not well represented by simple grid blocks. The method serves as a clear alternative to shortest-path graph search by solving constrained trajectory optimization online. Publication in Mechatronics supports strong engineering credibility.

### 23) Polygon Decomposition for Obstacle Representation in MPC Motion Planning (2025)
Reference: Logunov, A., Alhaddad, M., Mironov, K., Yakovlev, K., et al. (2025). *Polygon decomposition for obstacle representation in motion planning with Model Predictive Control*. Engineering Applications of Artificial Intelligence, 145, 110690. https://doi.org/10.1016/j.engappai.2025.110690

Justification: This work is relevant because obstacle representation strongly affects MPC tractability and safety in cluttered environments. Polygon decomposition gives a practical path to scalable optimization-based navigation beyond graph search. It is applicable to maze-style maps where geometric decomposition can reduce solver burden while preserving collision fidelity. The peer-reviewed EAAI publication makes it a reliable citation for optimization-based alternatives.

### 24) MPC with Prediction Uncertainty for Obstacle Avoidance (2025)
Reference: Schöneberg, E., Schröder, M., Görges, D., Schotten, H. D. (2025). *Trajectory Planning with Model Predictive Control for Obstacle Avoidance Considering Prediction Uncertainty*. arXiv:2504.19193. https://arxiv.org/abs/2504.19193

Justification: This paper is relevant because it treats uncertainty explicitly in trajectory planning, which is critical for real mobile robots in non-static scenes. Uncertainty-aware MPC is a strong alternative to A* pipelines that assume deterministic costs and obstacle motion. The method helps evaluate robustness-oriented planning metrics in addition to shortest-path length. It is a preprint, but the manuscript notes IFAC acceptance, which improves confidence in methodological quality.

## Coverage Check
- Total references: **24**
- Year range: **2022-2026**
- Methods covered: learned/incremental search, RRT variants, ACO/metaheuristics, DRL/Q-learning, MPC
