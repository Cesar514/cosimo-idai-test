# Literature Pool 2 (Agent 2, 2021+)

## Scope Notes
- Candidate count: **36** (all year >= 2021).
- Emphasis: benchmarking/reproducibility, robotics software stacks, hybrid planning, RL local planning, uncertainty-aware motion planning.
- DOI-overlap with `robotics_maze/research/post_2021_methods.md`: **0** (checked via DOI extraction).
- Preprints: **0** (all entries are peer-reviewed journal or conference records).

## Benchmarking, Evaluation, and Reproducibility

1. **Bench-MR: A Motion Planning Benchmark for Wheeled Mobile Robots**
   - DOI: `10.1109/lra.2021.3068913`
   - URL: https://doi.org/10.1109/lra.2021.3068913
   - Year: `2021`
   - Venue: `IEEE Robotics and Automation Letters`
   - `peer_reviewed`: `true`
   - Relevance: Provides a standardized wheeled-mobile-robot planning benchmark with consistent maps and metrics for fair cross-method comparison.

2. **MotionBenchMaker: A Tool to Generate and Benchmark Motion Planning Datasets**
   - DOI: `10.1109/lra.2021.3133603`
   - URL: https://doi.org/10.1109/lra.2021.3133603
   - Year: `2022`
   - Venue: `IEEE Robotics and Automation Letters`
   - `peer_reviewed`: `true`
   - Relevance: Introduces an automated dataset-generation tool for motion-planning benchmarks, improving repeatability and coverage analysis.

3. **Autonomous Ground Navigation in Highly Constrained Spaces: Lessons Learned From the Benchmark Autonomous Robot Navigation Challenge at ICRA 2022 [Competitions]**
   - DOI: `10.1109/mra.2022.3213466`
   - URL: https://doi.org/10.1109/mra.2022.3213466
   - Year: `2022`
   - Venue: `IEEE Robotics & Automation Magazine`
   - `peer_reviewed`: `true`
   - Relevance: Distills practical lessons from the BARN challenge, including evaluation pitfalls and benchmark protocol considerations.

4. **SRPB: a benchmark for the quantitative evaluation of a social robot navigation**
   - DOI: `10.1109/mmar58394.2023.10242422`
   - URL: https://doi.org/10.1109/mmar58394.2023.10242422
   - Year: `2023`
   - Venue: `2023 27th International Conference on Methods and Models in Automation and Robotics (MMAR)`
   - `peer_reviewed`: `true`
   - Relevance: Presents a quantitative social-navigation benchmark useful for evaluating local planner behavior under social constraints.

5. **CoBRA: A Composable Benchmark for Robotics Applications**
   - DOI: `10.1109/icra57147.2024.10610776`
   - URL: https://doi.org/10.1109/icra57147.2024.10610776
   - Year: `2024`
   - Venue: `2024 IEEE International Conference on Robotics and Automation (ICRA)`
   - `peer_reviewed`: `true`
   - Relevance: Proposes a composable benchmarking framework that supports modular, reproducible robotics evaluation pipelines.

6. **OpenBench: A New Benchmark and Baseline for Semantic Navigation in Smart Logistics**
   - DOI: `10.1109/icra55743.2025.11127476`
   - URL: https://doi.org/10.1109/icra55743.2025.11127476
   - Year: `2025`
   - Venue: `2025 IEEE International Conference on Robotics and Automation (ICRA)`
   - `peer_reviewed`: `true`
   - Relevance: Adds a semantic-navigation benchmark plus baseline methods for logistics scenarios, useful for reproducible SOTA comparisons.

7. **Demonstrating Arena 5.0: A Photorealistic ROS2 Simulation Framework for Developing and Benchmarking Social Navigation**
   - DOI: `10.15607/rss.2025.xxi.092`
   - URL: https://doi.org/10.15607/rss.2025.xxi.092
   - Year: `2025`
   - Venue: `Robotics: Science and Systems XXI`
   - `peer_reviewed`: `true`
   - Relevance: Delivers a photorealistic ROS2 simulation benchmark environment, improving sim-to-stack reproducibility for social navigation.

8. **Parameter Optimization for Manipulator Motion Planning using a Novel Benchmark Set**
   - DOI: `10.1109/icra48891.2023.10160694`
   - URL: https://doi.org/10.1109/icra48891.2023.10160694
   - Year: `2023`
   - Venue: `2023 IEEE International Conference on Robotics and Automation (ICRA)`
   - `peer_reviewed`: `true`
   - Relevance: Uses a dedicated benchmark set for systematic motion-planner parameter optimization and controlled performance analysis.

## Robotics Software Stacks and Frameworks

9. **PIC4rl-gym: a ROS2 Modular Framework for Robots Autonomous Navigation with Deep Reinforcement Learning**
   - DOI: `10.1109/icccr56747.2023.10193996`
   - URL: https://doi.org/10.1109/icccr56747.2023.10193996
   - Year: `2023`
   - Venue: `2023 3rd International Conference on Computer, Control and Robotics (ICCCR)`
   - `peer_reviewed`: `true`
   - Relevance: Defines a ROS2 modular framework that couples autonomous navigation with DRL components for stack-level experimentation.

10. **FogROS2-LS: A Location-Independent Fog Robotics Framework for Latency Sensitive ROS2 Applications**
   - DOI: `10.1109/icra57147.2024.10610759`
   - URL: https://doi.org/10.1109/icra57147.2024.10610759
   - Year: `2024`
   - Venue: `2024 IEEE International Conference on Robotics and Automation (ICRA)`
   - `peer_reviewed`: `true`
   - Relevance: Extends ROS2 with location-independent fog execution for latency-sensitive applications, relevant to reproducible deployment studies.

11. **A modular functional framework for the design and evaluation of multi-robot navigation**
   - DOI: `10.1016/j.robot.2021.103849`
   - URL: https://doi.org/10.1016/j.robot.2021.103849
   - Year: `2021`
   - Venue: `Robotics and Autonomous Systems`
   - `peer_reviewed`: `true`
   - Relevance: Offers a modular architecture for multi-robot navigation design/evaluation, supporting reusable and testable stack composition.

12. **A ROS2-Based Framework for Industrial Automation Systems**
   - DOI: `10.1109/icccr54399.2022.9790247`
   - URL: https://doi.org/10.1109/icccr54399.2022.9790247
   - Year: `2022`
   - Venue: `2022 2nd International Conference on Computer, Control and Robotics (ICCCR)`
   - `peer_reviewed`: `true`
   - Relevance: Presents a ROS2-based industrial automation framework that documents integration patterns transferable to navigation stacks.

13. **Arena 4.0: a Comprehensive Ros2 Development and Benchmarking Platform for Human-Centric Navigation Using Generative-Model-Based Environment Generation**
   - DOI: `10.1109/icra55743.2025.11127635`
   - URL: https://doi.org/10.1109/icra55743.2025.11127635
   - Year: `2025`
   - Venue: `2025 IEEE International Conference on Robotics and Automation (ICRA)`
   - `peer_reviewed`: `true`
   - Relevance: Introduces Arena 4.0 as a ROS2-centric development and benchmarking platform for human-centric navigation workflows.

14. **Exploring ROS2 Based Robot Navigation: Parameter Tuning Using the NAV2 Package**
   - DOI: `10.1115/detc2025-168734`
   - URL: https://doi.org/10.1115/detc2025-168734
   - Year: `2025`
   - Venue: `Volume 5: 21st IEEE/ASME International Conference on Mechatronic and Embedded Systems and Applications (MESA); 49th Mechanisms and Robotics Conference (MR)`
   - `peer_reviewed`: `true`
   - Relevance: Studies NAV2 parameter tuning in ROS2, directly relevant to reproducible software-stack configuration and benchmarking.

## Hybrid Planning

15. **Path Planning Method for Mobile Robot Based on a Hybrid Algorithm**
   - DOI: `10.1007/s10846-023-01985-1`
   - URL: https://doi.org/10.1007/s10846-023-01985-1
   - Year: `2023`
   - Venue: `Journal of Intelligent & Robotic Systems`
   - `peer_reviewed`: `true`
   - Relevance: Hybridizes planning components for mobile robots, making it a useful baseline against single-paradigm global planners.

16. **Improved Exponential and Cost-Weighted Hybrid Algorithm for Mobile Robot Path Planning**
   - DOI: `10.3390/s25082579`
   - URL: https://doi.org/10.3390/s25082579
   - Year: `2025`
   - Venue: `Sensors`
   - `peer_reviewed`: `true`
   - Relevance: Combines exponential and cost-weighted strategies to improve multi-objective mobile-robot path planning performance.

17. **Hybrid Boustrophedon and Direction-Biased Region Transitions for Mobile Robot Coverage Path Planning: A Region-Based Multi-Cost Framework**
   - DOI: `10.3390/app152312666`
   - URL: https://doi.org/10.3390/app152312666
   - Year: `2025`
   - Venue: `Applied Sciences`
   - `peer_reviewed`: `true`
   - Relevance: Uses hybrid region-transition logic for coverage path planning, relevant for tasks beyond shortest-path routing.

18. **A Hybrid Mobile Robot Path Planning Scheme Based on Modified Gray Wolf Optimization and Situation Assessment**
   - DOI: `10.1155/2022/4167170`
   - URL: https://doi.org/10.1155/2022/4167170
   - Year: `2022`
   - Venue: `Journal of Robotics`
   - `peer_reviewed`: `true`
   - Relevance: Blends modified gray-wolf optimization with situational assessment, representing heuristic-hybrid global planning design.

19. **Hybrid path planning algorithm for mobile robot based on A* algorithm fused with DWA**
   - DOI: `10.1109/iciba56860.2023.10165386`
   - URL: https://doi.org/10.1109/iciba56860.2023.10165386
   - Year: `2023`
   - Venue: `2023 IEEE 3rd International Conference on Information Technology, Big Data and Artificial Intelligence (ICIBA)`
   - `peer_reviewed`: `true`
   - Relevance: Explicitly fuses A* global search with DWA local control, closely matching hybrid stack designs used in practice.

20. **WiTHy A*: Winding-Constrained Motion Planning for Tethered Robot using Hybrid A***
   - DOI: `10.1109/icra57147.2024.10611175`
   - URL: https://doi.org/10.1109/icra57147.2024.10611175
   - Year: `2024`
   - Venue: `2024 IEEE International Conference on Robotics and Automation (ICRA)`
   - `peer_reviewed`: `true`
   - Relevance: Applies Hybrid A* with winding constraints for tethered robots, extending hybrid planning to constrained domains.

## RL-Based Local Planning

21. **DRL-DCLP: A Deep Reinforcement Learning-Based Dimension-Configurable Local Planner for Robot Navigation**
   - DOI: `10.1109/lra.2025.3544927`
   - URL: https://doi.org/10.1109/lra.2025.3544927
   - Year: `2025`
   - Venue: `IEEE Robotics and Automation Letters`
   - `peer_reviewed`: `true`
   - Relevance: Introduces a dimension-configurable DRL local planner, a strong modern reference for adaptable local navigation policies.

22. **Navigation system with SLAM-based trajectory topological map and reinforcement learning-based local planner**
   - DOI: `10.1080/01691864.2021.1938671`
   - URL: https://doi.org/10.1080/01691864.2021.1938671
   - Year: `2021`
   - Venue: `Advanced Robotics`
   - `peer_reviewed`: `true`
   - Relevance: Integrates SLAM/topological mapping with an RL local planner, showing practical coupling between mapping and local control.

23. **RL-DOVS: Reinforcement Learning for Autonomous Robot Navigation in Dynamic Environments**
   - DOI: `10.3390/s22103847`
   - URL: https://doi.org/10.3390/s22103847
   - Year: `2022`
   - Venue: `Sensors`
   - `peer_reviewed`: `true`
   - Relevance: Targets dynamic environments with RL-based navigation, useful as a baseline for moving-obstacle local planning.

24. **Crowd-Aware Mobile Robot Navigation Based on Improved Decentralized Structured RNN via Deep Reinforcement Learning**
   - DOI: `10.3390/s23041810`
   - URL: https://doi.org/10.3390/s23041810
   - Year: `2023`
   - Venue: `Sensors`
   - `peer_reviewed`: `true`
   - Relevance: Focuses on crowd-aware DRL local navigation, relevant to socially compliant local planner benchmarking.

25. **Deep Reinforcement Learning-Based Mapless Navigation for Mobile Robot in Unknown Environment With Local Optima**
   - DOI: `10.1109/lra.2024.3511437`
   - URL: https://doi.org/10.1109/lra.2024.3511437
   - Year: `2025`
   - Venue: `IEEE Robotics and Automation Letters`
   - `peer_reviewed`: `true`
   - Relevance: Addresses mapless navigation and local-optima failure modes, a key weakness in learned local planners.

26. **Combining Motion Planner and Deep Reinforcement Learning for UAV Navigation in Unknown Environment**
   - DOI: `10.1109/lra.2023.3334978`
   - URL: https://doi.org/10.1109/lra.2023.3334978
   - Year: `2024`
   - Venue: `IEEE Robotics and Automation Letters`
   - `peer_reviewed`: `true`
   - Relevance: Combines a conventional planner with DRL in unknown environments, illustrating hybrid learned-local planning workflows.

27. **Learning Crowd-Aware Robot Navigation from Challenging Environments via Distributed Deep Reinforcement Learning**
   - DOI: `10.1109/icra46639.2022.9812011`
   - URL: https://doi.org/10.1109/icra46639.2022.9812011
   - Year: `2022`
   - Venue: `2022 International Conference on Robotics and Automation (ICRA)`
   - `peer_reviewed`: `true`
   - Relevance: Uses distributed DRL for crowd-aware navigation, providing reproducible multi-agent local-planning evidence.

## Uncertainty-Aware Motion Planning

28. **Vision-Based Uncertainty-Aware Motion Planning Based on Probabilistic Semantic Segmentation**
   - DOI: `10.1109/lra.2023.3322899`
   - URL: https://doi.org/10.1109/lra.2023.3322899
   - Year: `2023`
   - Venue: `IEEE Robotics and Automation Letters`
   - `peer_reviewed`: `true`
   - Relevance: Propagates probabilistic segmentation uncertainty into planning decisions, linking perception uncertainty to trajectory safety.

29. **Safe motion planning with environment uncertainty**
   - DOI: `10.1016/j.robot.2022.104203`
   - URL: https://doi.org/10.1016/j.robot.2022.104203
   - Year: `2022`
   - Venue: `Robotics and Autonomous Systems`
   - `peer_reviewed`: `true`
   - Relevance: Provides a direct safe-motion-planning treatment under environmental uncertainty for baseline uncertainty-aware comparisons.

30. **RADIUS: Risk-Aware, Real-Time, Reachability-Based Motion Planning**
   - DOI: `10.15607/rss.2023.xix.083`
   - URL: https://doi.org/10.15607/rss.2023.xix.083
   - Year: `2023`
   - Venue: `Robotics: Science and Systems XIX`
   - `peer_reviewed`: `true`
   - Relevance: Presents risk-aware reachability-based planning with real-time guarantees, relevant for safety-critical uncertain settings.

31. **IBBT: Informed Batch Belief Trees for Motion Planning Under Uncertainty**
   - DOI: `10.1109/icra57147.2024.10610244`
   - URL: https://doi.org/10.1109/icra57147.2024.10610244
   - Year: `2024`
   - Venue: `2024 IEEE International Conference on Robotics and Automation (ICRA)`
   - `peer_reviewed`: `true`
   - Relevance: Introduces informed batch belief trees for uncertainty-aware planning, useful for long-horizon stochastic tasks.

32. **Planning with SiMBA: Motion Planning under Uncertainty for Temporal Goals using Simplified Belief Guides**
   - DOI: `10.1109/icra48891.2023.10160897`
   - URL: https://doi.org/10.1109/icra48891.2023.10160897
   - Year: `2023`
   - Venue: `2023 IEEE International Conference on Robotics and Automation (ICRA)`
   - `peer_reviewed`: `true`
   - Relevance: Handles temporal goals under uncertainty via simplified belief guides, bridging task constraints and stochastic planning.

33. **Uncertainty-Aware Trajectory Planning: Using Uncertainty Quantification and Propagation in Traversability Prediction of Planetary Rovers**
   - DOI: `10.1109/mra.2023.3341289`
   - URL: https://doi.org/10.1109/mra.2023.3341289
   - Year: `2024`
   - Venue: `IEEE Robotics & Automation Magazine`
   - `peer_reviewed`: `true`
   - Relevance: Details uncertainty quantification/propagation for rover trajectory planning, offering a practical UQ-to-planning pipeline.

34. **Chance-Constrained Multi-Robot Motion Planning Under Gaussian Uncertainties**
   - DOI: `10.1109/lra.2023.3337700`
   - URL: https://doi.org/10.1109/lra.2023.3337700
   - Year: `2024`
   - Venue: `IEEE Robotics and Automation Letters`
   - `peer_reviewed`: `true`
   - Relevance: Formulates chance-constrained multi-robot planning under Gaussian uncertainty, directly relevant to safe coordination.

35. **Sparse Integration Schemes for Chance-Constrained Motion Primitive Path Planning**
   - DOI: `10.1109/lra.2022.3173045`
   - URL: https://doi.org/10.1109/lra.2022.3173045
   - Year: `2022`
   - Venue: `IEEE Robotics and Automation Letters`
   - `peer_reviewed`: `true`
   - Relevance: Improves tractability of chance-constrained primitive planning through sparse integration schemes.

36. **Trajectory Optimization of Chance-Constrained Nonlinear Stochastic Systems for Motion Planning Under Uncertainty**
   - DOI: `10.1109/tro.2022.3197072`
   - URL: https://doi.org/10.1109/tro.2022.3197072
   - Year: `2023`
   - Venue: `IEEE Transactions on Robotics`
   - `peer_reviewed`: `true`
   - Relevance: Gives a rigorous trajectory-optimization treatment of nonlinear stochastic chance constraints in motion planning.
