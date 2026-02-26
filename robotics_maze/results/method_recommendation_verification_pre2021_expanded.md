# Method Recommendation Verification — Pre-2021 Expanded
**Repository:** `Cesar514/cosimo-idai-test` — `robotics_maze/`  
**Audit date:** 2026-02-26  
**Scope:** All robotics planner recommendations in `robotics_maze/`; implementation status per method against repository evidence; foundational literature grounding (≥20 references, year ≤ 2020).

---

## 1. Method Verification Matrix

Each row names a recommended or implemented planner, its evidence file(s) in the repository, and its verified implementation status.

| ID  | Method | Research File | Implementation File | Benchmark Integration | Status |
|-----|--------|--------------|--------------------|-----------------------|--------|
| B-1 | A\* (baseline) | `research/R1_weighted_astar.md` (background) | `src/planners.py` → `astar()` | `src/benchmark.py` registry | ✅ Fully implemented |
| B-2 | Dijkstra (baseline) | — | `src/planners.py` → `dijkstra()` | `src/benchmark.py` registry | ✅ Fully implemented |
| B-3 | Greedy Best-First (baseline) | — | `src/planners.py` → `greedy_best_first()` | `src/benchmark.py` registry | ✅ Fully implemented |
| R1  | Weighted A\* | `research/R1_weighted_astar.md` | `src/alt_planners/r1_weighted_astar.py` → `plan_weighted_astar()` | Available for benchmark harness | ✅ Fully implemented |
| R2  | Bidirectional A\* | `research/R2_bidirectional_astar.md` | `src/alt_planners/r2_bidirectional_astar.py` | Available for benchmark harness | ✅ Fully implemented |
| R3  | Theta\* (any-angle) | `research/R3_theta_star.md` | `src/alt_planners/r3_theta_star.py` → `plan_theta_star()` | Available for benchmark harness | ✅ Fully implemented |
| R4  | IDA\* | `research/R4_idastar.md` | `src/alt_planners/r4_idastar.py` | Available for benchmark harness | ✅ Fully implemented |
| R5  | Jump Point Search (JPS) | `research/R5_jump_point_search.md` | `src/alt_planners/r5_jump_point_search.py` → `plan_jps()` | Available for benchmark harness | ✅ Fully implemented |
| R6  | LPA\* (Lifelong Planning A\*) | `research/R6_lpa_star.md` | `src/alt_planners/r6_lpa_star.py` → `plan_lpa_star()` | Available for benchmark harness | ✅ Fully implemented |
| R7  | Beam Search | `research/R7_beam_search.md` | `src/alt_planners/r7_beam_search.py` → `plan_beam_search()` | Available for benchmark harness | ✅ Fully implemented |
| R8  | Fringe Search | `research/R8_fringe_search.md` | `src/alt_planners/r8_fringe_search.py` | Available for benchmark harness | ✅ Fully implemented |
| R9  | Bidirectional BFS | `research/R9_bidirectional_bfs.md` | `src/alt_planners/r9_bidirectional_bfs.py` | Available for benchmark harness | ✅ Fully implemented |
| R10a | D\* Lite (top recommended) | `research/R10_alt_methods_sota.md`, `src/alt_planners/r10_dwa_hybrid.md` | **Not present** | Not benchmarked | ⚠️ Recommended but not implemented |
| R10b | Anytime Dynamic A\* (AD\*) | `research/R10_alt_methods_sota.md`, `src/alt_planners/r10_dwa_hybrid.md` | **Not present** | Not benchmarked | ⚠️ Recommended but not implemented |
| R10c | Multi-Heuristic A\* (MHA\*) | `research/R10_alt_methods_sota.md` | **Not present** | Not benchmarked | ⚠️ Recommended but not implemented |
| R10d | Hybrid-RRT\* | `research/R10_alt_methods_sota.md` | **Not present** | Not benchmarked | ⚠️ Recommended but not implemented |
| R10e | Learning-Augmented Search (LoHA\*) | `research/R10_alt_methods_sota.md` | **Not present** | Not benchmarked | ⚠️ Recommended but not implemented |

**Summary:** 12 of 17 tracked methods are fully implemented. All 5 unimplemented methods come from the SOTA recommendations in `R10_alt_methods_sota.md`. The core-baseline set (B-1 through B-3) and all R1–R9 alternative planners have runnable Python code with documented interfaces. R10 remains at the design/notes stage.

---

## 2. Foundational Literature (≥ 20 References, Year ≤ 2020)

Each entry provides: **(1)** core contribution, **(2)** relevance to this repository's recommendations, **(3)** limitation or caveat for this context, **(4)** practical implication for the implementation roadmap.

---

### [1] Hart, P.E., Nilsson, N.J., & Raphael, B. (1968). A Formal Basis for the Heuristic Determination of Minimum Cost Paths. *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100–107.

**(1) Core contribution:** Introduced A\* and proved that with an admissible heuristic it finds the optimal-cost path while expanding the fewest nodes among all algorithms that use the same heuristic, establishing the theoretical foundation for best-first graph search. **(2) Relevance:** Every planner in this repository — baselines (`src/planners.py`) and alternatives R1–R8 — either is A\* or derives directly from it by modifying cost function, heuristic inflation, or frontier representation; this paper defines the correctness conditions (admissibility, consistency) that all implementations implicitly rely on. **(3) Limitation:** The original formulation assumes a finite, explicitly enumerated graph and a static, perfectly known environment; the maze grids in this project satisfy these constraints, but extension to dynamic maps (required by R10a D\* Lite) requires additional theory beyond this paper. **(4) Practical implication:** Implementers should audit every planner's heuristic for admissibility before trust in optimality is claimed in benchmark reports; in particular, the weighted A\* (R1) and beam search (R7) implementations intentionally relax this guarantee and must be documented as suboptimal.

---

### [2] Dijkstra, E.W. (1959). A Note on Two Problems in Connexion with Graphs. *Numerische Mathematik*, 1(1), 269–271.

**(1) Core contribution:** Presented the first provably correct shortest-path algorithm for graphs with non-negative edge weights using a priority-queue expansion strategy, which became the zero-heuristic special case of A\* and the canonical optimal-search baseline. **(2) Relevance:** `src/planners.py` registers `dijkstra` as an explicit baseline with `heuristic=0`; its role in the benchmark harness (`src/benchmark.py`) is to provide the expansion-count upper bound that makes heuristic speedups legible and reproducible. **(3) Limitation:** Dijkstra's algorithm does not scale gracefully to the large or dynamically updated maps anticipated by R6 (LPA\*) and R10a (D\* Lite), because it performs a full re-expansion from scratch on every map change without reusing prior search state. **(4) Practical implication:** Benchmark reports should always include Dijkstra as the no-heuristic reference point so that the node-expansion savings attributable purely to heuristic guidance can be measured independently of path-cost differences.

---

### [3] Korf, R.E. (1985). Depth-First Iterative-Deepening: An Optimal Admissible Tree Search. *Artificial Intelligence*, 27(1), 97–109.

**(1) Core contribution:** Introduced IDA\*, combining iterative deepening's O(d) memory footprint with A\*'s f-value threshold to guarantee optimal paths while using only stack-depth memory instead of an explicit open set. **(2) Relevance:** R4 (`src/alt_planners/r4_idastar.py`) is a direct implementation of IDA\* for 4-connected grid mazes; the research note `research/R4_idastar.md` explicitly references this paper's memory-efficiency motivation for deployment on large maps. **(3) Limitation:** IDA\* suffers from repeated re-expansion of nodes in each threshold iteration; in the corridor-heavy labyrinth mazes generated by this project's `src/maze.py`, the narrow path structure can cause multiple threshold increments and dramatically higher wall-clock times compared to A\*. **(4) Practical implication:** IDA\* should be profiled specifically on high-density mazes to quantify the re-expansion penalty; if peak memory is not a concern on target hardware, A\* or Fringe Search (R8) will likely dominate in all benchmark metrics and IDA\* should be relegated to a memory-constrained deployment scenario.

---

### [4] Pohl, I. (1969). Bi-Directional Search. *Machine Intelligence*, 6, 127–140.

**(1) Core contribution:** Formalized bidirectional search and proved that meeting in the middle can, in the best case, halve the depth of each frontier and reduce total node expansions from O(b^d) to approximately O(b^(d/2)), where b is the branching factor and d is solution depth. **(2) Relevance:** Both R2 (`src/alt_planners/r2_bidirectional_astar.py`) and R9 (`src/alt_planners/r9_bidirectional_bfs.py`) are bidirectional implementations whose theoretical advantage claims trace directly back to this paper's complexity analysis. **(3) Limitation:** The O(b^(d/2)) reduction is an idealized bound that assumes symmetric costs and near-symmetric frontier growth; real maze grids with asymmetric obstacle distributions or narrow corridors frequently cause one frontier to stall, reducing the practical speedup. **(4) Practical implication:** When comparing R2 and R9 to A\* in benchmarks, expansion-count ratios should be reported per maze topology class (corridor-heavy vs. open) to determine whether bidirectional benefits are consistent across this project's maze generator outputs.

---

### [5] Koenig, S., & Likhachev, M. (2002). D\* Lite. *Proceedings of AAAI 2002*, 476–483.

**(1) Core contribution:** Introduced D\* Lite as an incremental replanning algorithm that searches backward from the goal using LPA\* key mechanics, reusing prior search state so that only locally inconsistent vertices are re-expanded after map changes, achieving fast replanning with a fraction of A\*'s per-update cost. **(2) Relevance:** D\* Lite is the top-ranked recommendation in `research/R10_alt_methods_sota.md` and the primary target for `src/alt_planners/r10_dstar_lite.py`, which does not yet exist; the paper provides the exact data structures (`rhs`, `g`, priority key formula) needed to implement this planner. **(3) Limitation:** D\* Lite's key formula and consistency definitions assume a consistent heuristic and directed graph; implementing it correctly in the existing forward-oriented planner registry (`src/planners.py`) requires either a registry wrapper that inverts the search direction or a standalone module that bypasses the shared `_best_first_search` helper. **(4) Practical implication:** R10a (D\* Lite) should be implemented as a new standalone file (`r10_dstar_lite.py`) rather than adapted from the shared `_best_first_search` function, and its incremental replanning benefit should be validated by benchmarking replanning latency under random single-cell obstacle additions, not just fresh-path planning speed.

---

### [6] Koenig, S., Likhachev, M., & Furcy, D. (2004). Lifelong Planning A\*. *Artificial Intelligence*, 155(1–2), 93–146.

**(1) Core contribution:** Defined Lifelong Planning A\* (LPA\*), a general incremental heuristic search framework that maintains `g` and `rhs` values per vertex, propagates only locally inconsistent changes after cost updates, and guarantees replanning produces optimal paths at each query without a full re-expansion. **(2) Relevance:** R6 (`src/alt_planners/r6_lpa_star.py`) is a direct implementation of forward LPA\* with a module-level persistent cache; the research note `research/R6_lpa_star.md` explicitly cites this paper and its authors as the foundational reference. **(3) Limitation:** The module-level cache approach in `r6_lpa_star.py` couples state to the Python process lifetime, making parallel or multi-episode benchmark runs share (and potentially corrupt) incremental state; the implementation note acknowledges this and resets state when grid shape or endpoints change. **(4) Practical implication:** The benchmark harness should isolate LPA\* replanning scenarios into a dedicated episode sequence that keeps start/goal fixed while injecting controlled obstacle changes, to accurately measure the incremental speedup rather than always triggering the full-reset code path.

---

### [7] Harabor, D., & Grastien, A. (2011). Online Graph Pruning for Pathfinding on Grid Maps. *Proceedings of AAAI 2011*, 1114–1119.

**(1) Core contribution:** Introduced Jump Point Search (JPS), a symmetry-breaking technique that prunes search on uniform-cost grids by "jumping" over structurally identical cells and expanding only jump points — intersections where branching decisions matter — reducing expanded nodes dramatically without sacrificing optimality. **(2) Relevance:** R5 (`src/alt_planners/r5_jump_point_search.py`) implements a 4-connected JPS variant; the research note `research/R5_jump_point_search.md` acknowledges this paper and notes that the repository uses a cardinal-only variant instead of full 8-connected JPS to reduce implementation risk. **(3) Limitation:** JPS provides the largest node-reduction gains on open uniform-cost grids; in corridor-heavy mazes — the primary map type generated by `src/maze.py` — obstacle density limits jump length, reducing JPS's advantage and potentially making it slower than A\* due to jump-scan overhead. **(4) Practical implication:** JPS benchmark results should be stratified by maze openness (wall density quartile) to determine at what obstacle density JPS transitions from faster to slower than baseline A\*, which will inform whether it belongs in the primary planner suite or as a map-type-conditional alternative.

---

### [8] Nash, A., Daniel, K., Koenig, S., & Felner, A. (2007). Theta\*: Any-Angle Path Planning on Grids. *Proceedings of AAAI 2007*, 1177–1183.

**(1) Core contribution:** Presented Theta\*, an extension of A\* that uses line-of-sight checks to bypass intermediate grid vertices and return paths with fewer heading changes and shorter Euclidean lengths than grid-constrained A\*, while remaining complete and near-optimal. **(2) Relevance:** R3 (`src/alt_planners/r3_theta_star.py`) implements Theta\* with an 8-connected grid and supercover LOS checks; the research note `research/R3_theta_star.md` describes path smoothing metrics (`smoothed_segments`, `los_successes`) that directly track the benefit claimed in this paper. **(3) Limitation:** Theta\*'s LOS-check overhead is proportional to the number of visible parent-to-successor pairs, which can become significant in large open mazes; the repository note acknowledges LOS caching as a mitigation, but caching correctness must be validated when the grid is modified between queries. **(4) Practical implication:** Theta\* should be evaluated not only on node-expansion count but on output path waypoint count and Euclidean path cost, because those metrics — rather than raw speed — constitute its primary advantage over A\* and justify its higher per-node cost in a robotics controller context.

---

### [9] Bjornsson, Y., Enzenberger, M., Holte, R.C., & Schaeffer, J. (2005). Fringe Search: Beating A\* at Pathfinding on Game Maps. *Proceedings of CIG 2005*.

**(1) Core contribution:** Introduced Fringe Search, a threshold-based heuristic search that replaces A\*'s global priority queue with two simple lists (`now`/`later`) separated by a per-pass threshold, reducing heap-operation overhead on wide uniform frontiers while preserving optimality with a consistent heuristic. **(2) Relevance:** R8 (`src/alt_planners/r8_fringe_search.py`) is a direct implementation; `research/R8_fringe_search.md` explicitly attributes the algorithm to this paper and describes its expected performance characteristics on the maze benchmark. **(3) Limitation:** Fringe Search's advantage is greatest when many frontier nodes share similar f-values — i.e., uniform-cost grids with wide fronts — but the corridor-heavy mazes in this project produce narrow, linear frontiers where strict best-first ordering (A\*) may expand far fewer nodes and eliminate Fringe Search's list-scan overhead. **(4) Practical implication:** The benchmark should report both `runtime_ms` and `expanded_nodes` for Fringe Search versus A\* across maze sizes; if Fringe Search is faster but expands more nodes, it confirms the queue-overhead hypothesis and justifies it only as a throughput optimizer, not a search-efficiency optimizer.

---

### [10] Likhachev, M., Gordon, G., & Thrun, S. (2003). ARA\*: Anytime Replanning with Provable Bounds on Sub-Optimality. *Advances in Neural Information Processing Systems (NIPS) 16*.

**(1) Core contribution:** Introduced Anytime Repairing A\* (ARA\*), which starts with an inflated heuristic (w > 1) to return a fast suboptimal solution and then progressively decreases w, reusing prior search effort to improve solution quality toward optimality within any available time budget. **(2) Relevance:** ARA\* is the direct predecessor of AD\* (R10b recommendation) and establishes the anytime quality-improvement framework referenced in `research/R10_alt_methods_sota.md`; its epsilon-suboptimality bound is the theoretical guarantee that makes R1 Weighted A\* conceptually safe when combined with anytime iteration. **(3) Limitation:** ARA\*'s efficiency depends on the ability to reuse the search tree across epsilon-decreasing iterations; this requires persistent data structures not present in the current stateless planner interface (`src/planners.py`), meaning ARA\* cannot simply be dropped into the existing registry without architectural changes. **(4) Practical implication:** When implementing R10b (AD\*), the registry planner signature should be extended with optional state-carry-over arguments so anytime planners can preserve internal search state between calls within a single simulation episode.

---

### [11] Likhachev, M., Ferguson, D., Gordon, G., Stentz, A., & Thrun, S. (2005). Anytime Dynamic A\*: An Anytime, Replanning Algorithm. *Proceedings of ICAPS 2005*, 262–271.

**(1) Core contribution:** Presented Anytime Dynamic A\* (AD\*), which combines ARA\*'s anytime quality-improvement passes with D\* Lite's incremental map-update capability, enabling a planner that can both improve solution quality over time and efficiently repair plans after local map changes without full re-expansion. **(2) Relevance:** AD\* is the second-ranked recommendation in `research/R10_alt_methods_sota.md` and the target of `src/alt_planners/r10_adstar.py`, which does not yet exist; the integration notes in `src/alt_planners/r10_dwa_hybrid.md` propose using AD\* with `epsilon_start > 1` for fast first paths in simulation loops. **(3) Limitation:** AD\* requires maintaining both an anytime inflation state (current epsilon) and a D\* Lite-style consistency state simultaneously, making it the most complex algorithm targeted by R10; implementation errors in the key-update or epsilon-decrease logic can silently produce suboptimal or incorrect paths. **(4) Practical implication:** AD\* should be implemented and validated in two phases: first verify correctness as ARA\* (static maps, epsilon decreasing), then add the D\* Lite incremental layer; this staged approach aligns with the R10 risk mitigation note and reduces debugging surface area.

---

### [12] Fox, D., Burgard, W., & Thrun, S. (1997). The Dynamic Window Approach to Collision Avoidance. *IEEE Robotics and Automation Magazine*, 4(1), 23–33.

**(1) Core contribution:** Introduced the Dynamic Window Approach (DWA), a local reactive planner that samples velocity commands from the robot's dynamic feasibility window and scores them by a combination of goal heading, obstacle clearance, and speed, providing real-time collision-free navigation without full trajectory optimization. **(2) Relevance:** `src/alt_planners/r10_dwa_hybrid.md` explicitly recommends pairing global planners (D\* Lite, AD\*) with DWA as the local controller, and DWA is named as the "DWA Hybrid" strategy proposed for R10 integration; this paper is the primary algorithmic reference for that local component. **(3) Limitation:** DWA operates on a kinematic/dynamic model of the robot; the current project's grid-based planning layer (`src/maze.py`, `src/planners.py`) is purely discrete and does not expose velocity or acceleration constraints, meaning DWA integration requires a velocity-space adapter layer not yet present in the codebase. **(4) Practical implication:** Before implementing the DWA local controller, the robot model in `src/robot.py` and the simulation loop in `src/sim.py` must be audited to confirm whether continuous velocity commands can be issued, or whether DWA must operate as a waypoint-selection heuristic on top of the discrete grid planner.

---

### [13] LaValle, S.M. (1998). Rapidly-Exploring Random Trees: A New Tool for Path Planning. *Technical Report TR 98-11*, Iowa State University.

**(1) Core contribution:** Introduced RRT, a sampling-based tree-growing algorithm that builds a space-filling exploration tree by incrementally extending toward random samples, offering probabilistic completeness and natural handling of high-dimensional configuration spaces without requiring an explicit graph representation. **(2) Relevance:** Hybrid-RRT\* is the fourth-ranked recommendation in `research/R10_alt_methods_sota.md` as a bridge to continuous kinodynamic planning; this paper provides the original RRT foundation from which RRT\* (asymptotic optimality) and Hybrid-RRT\* (grid-guided sampling) are derived. **(3) Limitation:** RRT and its variants are stochastic, making benchmark reproducibility difficult without fixed seeds; the project's existing benchmark harness (`src/benchmark.py`) assumes deterministic planners, and RRT would require special handling to produce stable aggregate metrics. **(4) Practical implication:** Hybrid-RRT\* should be given the lowest implementation priority among R10 candidates for this grid-only project; if continuous motion planning is a future goal, a dedicated stochastic benchmark mode with seeded randomness should be designed before integrating RRT variants.

---

### [14] Kavraki, L.E., Svestka, P., Latombe, J.C., & Overmars, M.H. (1996). Probabilistic Roadmaps for Path Planning in High-Dimensional Configuration Spaces. *IEEE Transactions on Robotics and Automation*, 12(4), 566–580.

**(1) Core contribution:** Presented Probabilistic Roadmaps (PRM), a sampling-based approach that constructs a roadmap of randomly sampled collision-free configurations, enabling efficient multi-query path planning in high-dimensional spaces by amortizing sampling cost across repeated queries. **(2) Relevance:** While not directly implemented in this repository, PRM establishes the sampling-based planning paradigm that underlies Hybrid-RRT\* (R10d recommendation) and contextualizes why sampling methods are noted in `R10_alt_methods_sota.md` as secondary to graph-search methods for the discrete grid domain. **(3) Limitation:** PRM's strength is multi-query planning in continuous high-DOF spaces; the repository's maze environment is a 2D discrete grid where a connected component graph is already implicitly available, making PRM's roadmap construction overhead entirely unnecessary. **(4) Practical implication:** PRM is not a candidate for direct implementation in the current project scope; its relevance is strictly as background context for understanding why the R10 ranking places sampling methods below graph-search methods for grid maze navigation.

---

### [15] Stentz, A. (1994). Optimal and Efficient Path Planning for Partially-Known Environments. *Proceedings of ICRA 1994*, 3310–3317.

**(1) Core contribution:** Introduced D\* (Dynamic A\*), the first practical incremental replanning algorithm for robot navigation in unknown or changing environments, propagating cost changes backward from affected areas to update paths efficiently without complete re-expansion from the start. **(2) Relevance:** D\* Lite (R10a recommendation, `research/R10_alt_methods_sota.md`) is the simplified and more implementable successor to original D\*; understanding D\* provides the historical context for why D\* Lite (Koenig & Likhachev 2002) retains goal-rooted search and why the repository's R6 LPA\* planner also shares the `rhs`/`g` inconsistency-repair model. **(3) Limitation:** Original D\* uses a complex `RAISE`/`LOWER` state machine that is harder to implement correctly than D\* Lite; the repository correctly targets D\* Lite rather than original D\* for R10a, which should be maintained as the implementation target. **(4) Practical implication:** When documenting R10a (D\* Lite), the implementation notes should explicitly compare to original D\* to help future contributors understand why D\* Lite's simpler two-key priority formula was chosen and what correctness guarantees are maintained.

---

### [16] Russell, S., & Norvig, P. (2009). *Artificial Intelligence: A Modern Approach* (3rd ed.). Prentice Hall.

**(1) Core contribution:** Provided the most widely used unified textbook treatment of heuristic search, covering A\*, IDA\*, bidirectional search, and beam search with formal definitions, optimality proofs, and worked examples that serve as the canonical reference for algorithm correctness and terminology across the AI/robotics community. **(2) Relevance:** Multiple research notes in this repository (`R1`, `R2`, `R4`, `R7`) implicitly use AIMA-style notation and correctness conditions; using a shared textbook as a reference ensures that terms like "admissible," "consistent," and "complete" carry the same meaning across all planners and documentation. **(3) Limitation:** AIMA presents algorithms in pseudocode targeting conceptual clarity rather than Python performance; direct translation without profiling-driven optimizations (lazy deletion, closed-set pruning, tie-breaking) can leave significant speedup on the table for production grid planners. **(4) Practical implication:** Any new planner documentation should cite both the primary algorithmic paper and AIMA for the property-definition framework, so that correctness claims are grounded in a stable, widely reviewed source and reviewers can quickly verify the claimed properties.

---

### [17] Pearl, J. (1984). *Heuristics: Intelligent Search Strategies for Computer Problem Solving*. Addison-Wesley.

**(1) Core contribution:** Provided the formal mathematical framework for heuristic search including the conditions under which A\* is optimal and optimally efficient, introduced the notion of informed search and heuristic quality metrics, and gave the theoretical basis for why better heuristics reduce node expansions even when exact optimality is preserved. **(2) Relevance:** The `src/heuristics.py` module and the heuristic parameter interface across all planners (`heuristic: str | HeuristicFn | None`) reflect Pearl's framework for pluggable heuristics; the discussion of heuristic dominance in this book explains why Manhattan outperforms Chebyshev for 4-connected grids and why Euclidean is admissible for 8-connected variants. **(3) Limitation:** Pearl's results primarily address single-query optimal search on static graphs; the dynamic-map scenarios targeted by R6 (LPA\*) and R10a (D\* Lite) require extensions to the consistency and monotonicity conditions that are not fully developed in this 1984 treatment. **(4) Practical implication:** `src/heuristics.py` should document which heuristics are admissible and consistent for which motion models (4-connected vs. 8-connected, unit-cost vs. Euclidean-cost) using Pearl's formal definitions, so that planner authors can correctly choose heuristics and benchmark reports can clearly state optimality claims.

---

### [18] Kaindl, H., & Kainz, G. (1997). Bidirectional Heuristic Search Reconsidered. *Journal of Artificial Intelligence Research*, 7, 283–317.

**(1) Core contribution:** Re-examined bidirectional heuristic search and proved that naïve bidirectional A\* can fail to find optimal paths without careful meeting-condition management, identifying the termination conditions and path-cost update rules required for correctness, which were absent or informal in many prior bidirectional implementations. **(2) Relevance:** R2 (`src/alt_planners/r2_bidirectional_astar.py`) implements bidirectional A\* with explicit `best_cost` path-update logic and a documented termination condition; this paper's correctness analysis directly validates or challenges the design choices made in R2's meeting-condition implementation. **(3) Limitation:** The paper's correctness proofs assume consistent heuristics and specific priority-queue management; if the R2 implementation uses any approximate or inadmissible heuristic variant, the optimality guarantees analyzed in this paper may not hold, and the returned path could be suboptimal without detection. **(4) Practical implication:** The R2 implementation should include an explicit unit test that verifies path cost against unidirectional A\* on a small known maze, serving both as a regression guard and as a correctness check that the bidirectional meeting logic matches the termination conditions described in this paper.

---

### [19] Aine, S., Swaminathan, S., Narayanan, V., Hwang, V., & Likhachev, M. (2016). Multi-Heuristic A\*. *The International Journal of Robotics Research*, 35(1–3), 224–243.

**(1) Core contribution:** Introduced Multi-Heuristic A\* (MHA\*), a framework that runs multiple inadmissible heuristics in parallel queues anchored by one admissible heuristic, guaranteeing bounded suboptimality while allowing aggressive inadmissible guidance to significantly reduce node expansions in complex search spaces. **(2) Relevance:** MHA\* is the third-ranked recommendation in `research/R10_alt_methods_sota.md` with the note that it requires "heuristic engineering effort before consistent wins"; this paper provides the specific bounded-suboptimality proof and the anchor-heuristic contract that must be satisfied for any MHA\* implementation to be correct. **(3) Limitation:** MHA\*'s benefits over A\* depend directly on having multiple diverse and informative heuristics for the specific domain; the current repository only implements a Manhattan heuristic, meaning MHA\* would provide minimal benefit without first designing corridor-bias, wall-clearance, or topology-aware heuristics for the maze domain. **(4) Practical implication:** MHA\* should only be added to the planner suite after domain-specific heuristics (e.g., maze-corridor alignment, dead-end penalty) have been prototyped and shown to reduce expansions individually; investing in heuristic engineering before MHA\* architecture avoids implementing a framework before its key inputs exist.

---

### [20] LaValle, S.M. (2006). *Planning Algorithms*. Cambridge University Press.

**(1) Core contribution:** Provided a comprehensive unified treatment of motion planning including grid-based search, sampling-based planning (RRT, PRM), potential field methods, kinodynamic planning, and multi-robot coordination, establishing the algorithmic foundations and complexity bounds for all major planning paradigms used in modern robotics. **(2) Relevance:** The range of R1–R10 planners in this repository collectively cover graph search (A\*, D\* Lite, IDA\*), sampling (Hybrid-RRT\*), and local reactive methods (DWA); LaValle provides the common theoretical framework that allows these approaches to be compared on a shared dimension of completeness, optimality, and computational complexity. **(3) Limitation:** Planning Algorithms focuses on correctness and theoretical efficiency; it does not address Python-specific implementation considerations, benchmark harness design, or the practical performance characteristics of grid planners at the sizes (15×15 to 100×100) targeted by this project's benchmark harness. **(4) Practical implication:** When writing the method comparison section of `results/benchmark_summary.md`, the completeness and optimality columns should use LaValle's definitions so that properties claimed for each planner are formally grounded and consistent across all entries in the benchmark summary table.

---

### [21] Pohl, I. (1970). Heuristic Search Viewed as Path Finding in a Graph. *Artificial Intelligence*, 1(3–4), 193–204.

**(1) Core contribution:** Provided a graph-theoretic formalization of heuristic search, proved conditions for A\*'s optimality and efficiency using path-cost dominance arguments, and introduced bidirectional heuristic front-to-front search as a practical acceleration technique that influenced most subsequent bidirectional A\* variants. **(2) Relevance:** This paper establishes the theoretical basis for both unidirectional A\* (used in baselines B-1 and R1) and bidirectional heuristic search (R2), and it is the earliest formal reference connecting heuristic guidance to efficiency guarantees used in the `research/R2_bidirectional_astar.md` motivation section. **(3) Limitation:** Front-to-front bidirectional heuristic search as described requires computing heuristic estimates between the two frontiers, which is computationally expensive; R2 in this repository avoids this by using one-sided Manhattan estimates rather than front-to-front heuristics, which simplifies implementation but weakens the theoretical optimality guarantees analyzed here. **(4) Practical implication:** Documentation for R2 should note that it uses a simplified (not front-to-front) bidirectional heuristic, and benchmark comparisons should acknowledge this difference when citing efficiency claims from Pohl (1970).

---

### [22] Felner, A., Korf, R.E., & Hanan, S. (2004). Additive Pattern Database Heuristics. *Journal of Artificial Intelligence Research*, 22, 279–318.

**(1) Core contribution:** Introduced additive pattern databases (PDBs), a method for constructing highly informative admissible heuristics by decomposing the problem into subgroups and summing their individual pattern database estimates, significantly improving A\* performance in puzzle and planning domains by providing tighter lower bounds. **(2) Relevance:** The `src/heuristics.py` module currently provides only Manhattan and basic Euclidean heuristics; PDB-style heuristics represent the strongest admissible improvement direction for the grid planner benchmarks in this project, and understanding PDB construction informs the heuristic engineering work required before MHA\* (R10c) can deliver its promised benefit. **(3) Limitation:** PDB construction for grid mazes requires defining meaningful subproblems (e.g., row-projection, column-projection, or corridor-topology abstractions); maze connectivity varies between generated instances, making fixed offline PDBs potentially misaligned with runtime maze structures. **(4) Practical implication:** As a near-term alternative to full PDB construction, maze-topology-aware heuristics (e.g., estimating minimum corridor crossings from connectivity analysis) could be added to `src/heuristics.py` as a medium-effort improvement that benefits all informed search planners (A\*, JPS, Theta\*, MHA\*) simultaneously.

---

### [23] Koenig, S., & Likhachev, M. (2005). Fast Replanning for Navigation in Unknown Terrain. *IEEE Transactions on Robotics*, 21(3), 354–363.

**(1) Core contribution:** Provided an extended and rigorously analyzed version of D\* Lite, including a detailed proof of correctness for the key-update formula, optimality under dynamic obstacles, and empirical evidence on replanning efficiency for robot navigation in terrain revealed incrementally during execution. **(2) Relevance:** This T-RO paper complements the original AAAI 2002 D\* Lite paper and is the version most cited for implementation guidance; the `research/R10_alt_methods_sota.md` file links to the Koenig & Likhachev T-RO work as a primary reference, and any implementation of R10a should use this paper's pseudocode as the authoritative specification. **(3) Limitation:** The paper's empirical evaluation uses specific robot and terrain configurations that differ from the discrete maze generation model in this project; replanning speedup ratios should be re-measured empirically using the project's `src/benchmark.py` harness rather than extrapolated from the paper's navigation scenarios. **(4) Practical implication:** The R10a (D\* Lite) implementation should include a dedicated replanning benchmark scenario that injects random obstacle changes between planning calls and measures the ratio of re-expanded nodes versus full A\* re-runs, directly reproducing the experimental methodology described in this paper for comparability.

---

## 3. Reconciliation Report

### 3.1 Unsupported Claims

| Claim Location | Claim | Status | Finding |
|---|---|---|---|
| `research/R10_alt_methods_sota.md` — Rank 1 | D\* Lite expected runtime: "Initial: ~5–40 ms; map updates: ~1–15 ms" | ⚠️ Unvalidated | No implementation exists (`r10_dstar_lite.py` absent); runtime ranges are design estimates, not measured values |
| `research/R10_alt_methods_sota.md` — Rank 2 | AD\* first feasible path: "~3–20 ms; tightened path: ~10–80 ms" | ⚠️ Unvalidated | AD\* not implemented; runtime ranges are design estimates only |
| `research/R10_alt_methods_sota.md` — Rank 3 | MHA\* runtime: "~8–70 ms" | ⚠️ Unvalidated | MHA\* not implemented; no domain-specific heuristics exist to generate meaningful MHA\* results |
| `research/R10_alt_methods_sota.md` — Rank 4 | Hybrid-RRT\* runtime: "~40–400+ ms in dense grids" | ⚠️ Unvalidated | Hybrid-RRT\* not implemented; estimate is speculative |
| `src/alt_planners/r10_dwa_hybrid.md` | DWA-Hybrid loop described as immediately implementable | ⚠️ Overstated | `src/sim.py` operates on discrete grid; no velocity-command interface exists to support DWA local control |
| `research/R5_jump_point_search.md` | "Can drastically reduce node expansions in maze-like layouts" | ⚠️ Partially supported | JPS benefits are map-topology-dependent; no benchmark data yet confirms this claim for this project's maze type |
| `research/R9_bidirectional_bfs.md` | "Cuts search effort to O(b^(d/2))" | ℹ️ Theoretical only | This is a best-case bound; no empirical verification for this project's generated mazes |

### 3.2 Prioritized Fix List

| Priority | ID | Fix | Effort | Rationale |
|---|---|---|---|---|
| **P1** | R10a | Implement `src/alt_planners/r10_dstar_lite.py` using Koenig & Likhachev (2002, 2005) pseudocode; add to benchmark harness | **L** | Top-ranked recommendation with zero implementation; highest expected payoff for dynamic maze scenarios |
| **P2** | R10b | Implement `src/alt_planners/r10_adstar.py` in two phases: ARA\* first, then incremental layer | **L** | Second-ranked recommendation; completes the anytime planning capability identified as a key gap |
| **P3** | Benchmark | Run full benchmark (`src/benchmark.py`) over R1–R9 on ≥100 mazes; generate `results/benchmark_summary.md`; replace all estimated runtime ranges in research notes with measured values | **M** | All runtime claims in `R10_alt_methods_sota.md` are unvalidated estimates; empirical data needed before R10 design decisions are finalized |
| **P4** | R10a–b | Add replanning benchmark scenario (single episode with N random obstacle injections) to `src/benchmark.py` to measure D\* Lite / AD\* incremental speedup vs. A\* re-runs | **M** | Justifies incremental planner investment with measurable data; required before claiming replanning benefit in any report |
| **P5** | DWA | Audit `src/sim.py` and `src/robot.py` for velocity-command interface; document gap between discrete grid planner and DWA local controller requirements | **S** | `r10_dwa_hybrid.md` overstates DWA readiness; gap assessment prevents wasted implementation effort |
| **P6** | R5 (JPS) | Stratify JPS benchmark results by maze wall-density quartile; add finding to `research/R5_jump_point_search.md` | **S** | JPS open-grid advantage is unverified for corridor-heavy mazes; quick post-benchmark analysis with existing implementation |
| **P7** | Heuristics | Extend `src/heuristics.py` with at least one maze-topology-aware heuristic (e.g., corridor-crossing estimate); document admissibility bounds | **M** | Prerequisite for MHA\* (R10c) and improves all informed planners; medium effort with broad benefit |
| **P8** | R10c | Implement MHA\* only after P7 (heuristic engineering) is complete; use Aine et al. (2016) anchor-heuristic contract | **L** | Premature without diverse heuristics; defer until P7 confirms measurable single-heuristic improvement |
| **P9** | R2 / R9 | Add unit tests comparing R2 (Bidirectional A\*) and R9 (Bidirectional BFS) path costs to unidirectional A\*/Dijkstra on known mazes to verify meeting-condition correctness | **S** | Correctness gap identified in Kaindl & Kainz (1997) analysis; small test effort, high safety value |
| **P10** | Docs | Update all research notes to replace unsupported runtime-estimate ranges with "TBD — see `results/benchmark_summary.md`" placeholders until P3 is complete | **S** | Prevents misleading performance claims from propagating to downstream design decisions |

### 3.3 Implementation Completeness Summary

- **Fully implemented and benchmarkable:** B-1 (A\*), B-2 (Dijkstra), B-3 (GBFS), R1–R9 (9 alternative planners)
- **Designed but not implemented:** R10a (D\* Lite), R10b (AD\*), R10c (MHA\*), R10d (Hybrid-RRT\*), R10e (Learning-Augmented)
- **Architectural prerequisite missing:** DWA local controller (requires velocity interface in `src/sim.py`)
- **Benchmark data missing:** All runtime claims in `R10_alt_methods_sota.md`; JPS open-grid advantage verification; bidirectional optimality regression tests

---

*Verification audit completed. All file-path references verified against repository state as of 2026-02-26.*
