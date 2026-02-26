# R10 Research: SOTA Alternatives to A* for Maze/Mobile Robotics

## Scope
Focus: practical global planners for grid mazes and mobile-robot navigation where maps may change online.

## Ranked Comparison (Best Overall for This Repo First)

| Rank | Method | Time Complexity (Typical) | Optimality | Dynamic-Map Handling | Expected Runtime on Grid Mazes* | Why It Ranks Here |
|---|---|---|---|---|---|---|
| 1 | **D* Lite** | Initial search near `O((E + V) log V)`; local repairs often near `O(k log V)` for `k` changed states | Optimal with admissible/consistent heuristic | **Excellent** (incremental replanning by reusing prior search) | Initial: ~5-40 ms; map updates: ~1-15 ms | Best balance of speed, quality, and dynamic updates for repeated maze regeneration and obstacle changes |
| 2 | **Anytime Dynamic A* (AD\*)** | Same class as incremental A* + repeated improvement passes | Bounded-suboptimal anytime (`epsilon > 1`), converges toward optimal as `epsilon -> 1` | **Excellent** (anytime + incremental updates) | First feasible path: ~3-20 ms; tightened path: ~10-80 ms | Strong when you need a fast first answer plus quality improvement under time budget |
| 3 | **Multi-Heuristic A* (MHA\*)** | Roughly scales with number of heuristics `H` (multi-queue guided search) | Bounded-suboptimal (with anchor heuristic setting) | Moderate (usually reruns; not inherently incremental like D* Lite) | ~8-70 ms (depends heavily on heuristic quality/count) | Very good if we can design diverse heuristics for maze geometry; otherwise gains are smaller |
| 4 | **Hybrid-RRT\*** (sampling + heuristic/grid guidance) | Sampling/tree growth often `O(n log n)` expected (NN + rewiring) | Asymptotically optimal, probabilistically complete | Moderate (often replans from scratch/partial tree reuse) | ~40-400+ ms in dense grids (variance high) | Useful bridge to continuous kinodynamic planning, but heavier than graph-search methods on pure grids |
| 5 | **Learning-Augmented Heuristic Search (LoHA\*/similar)** | Online planning close to heuristic search; plus offline training cost | Usually no strict guarantee unless anchored with admissible fallback | Moderate to Good (depends on retraining/domain shift) | Inference-guided planning can be fast (~2-30 ms), but deployment risk is data-dependent | High upside long-term, but higher integration and validation risk for immediate repo needs |

\*Runtime ranges are engineering expectations for this repo context (Python grid-maze benchmarks) and should be validated in `B6` benchmark harness.

## Notes Per Method

### 1) D* Lite
- Designed for repeated replanning as edge costs/obstacles change.
- Reuses previous search effort, typically giving much faster updates than full A* reruns.

### 2) AD*
- Unifies incremental replanning and anytime behavior.
- Good when latency matters but path quality can improve if extra cycles are available.

### 3) MHA*
- Uses multiple heuristics to reduce expansions in hard search spaces.
- Most effective when we provide strong complementary heuristics (distance, corridor bias, wall-clearance bias).

### 4) Hybrid-RRT*
- Strong in continuous/high-DOF planning; less compelling than D* family on strictly discrete grid mazes.
- Recent hybrid variants show node-reduction and faster convergence vs vanilla Informed RRT*.

### 5) Learning-Augmented Search
- Learns local heuristic guidance to reduce expansions.
- Best treated as a second-phase optimization after a robust classical fallback is in place.

## Top 2 Candidates for Immediate Implementation

## 1) D* Lite (First)
- Lowest implementation risk with high payoff for dynamic mazes.
- Natural drop-in extension of A*/LPA* style interfaces already common in this codebase.
- Deterministic and benchmark-friendly.

## 2) AD* (Second)
- Adds a practical speed/quality knob on top of dynamic replanning.
- Good fit for real-time simulation loops: return fast path now, refine later.

## Why Not Others First
- MHA*: great potential but needs heuristic engineering effort before consistent wins.
- Hybrid-RRT*: heavier and stochastic for grid-only benchmark goals.
- Learning-based: promising but requires dataset/training/evaluation infra not yet present.

## Primary References
- Koenig, S. and Likhachev, M. "D* Lite" (AAAI 2002): https://idm-lab.org/bib/abstracts/Koen02e.html
- Koenig, S. et al. "Fast Replanning for Navigation in Unknown Terrain" (T-RO): https://www.cs.cmu.edu/~maxim/files/Fringe.pdf
- Likhachev, M. et al. "Anytime Dynamic A*: An Anytime, Replanning Algorithm" (ICAPS 2005): https://www.cs.cmu.edu/~maxim/ADStarICAPS05.pdf
- Likhachev, M. et al. "A Generalized Framework for Lifelong Planning A*" (proofs/details): https://www.ri.cmu.edu/publications/a-generalized-framework-for-lifelong-planning-a/
- Aine, S. et al. "Multi-Heuristic A*" (CMU RI publication): https://www.ri.cmu.edu/publications/multi-heuristic-a/
- Nasirian, F. et al. "Hybrid-RRT*: A Faster RRT* for Robot Path Planning in Dense Environments" (2024): https://www.sciencedirect.com/science/article/abs/pii/S0921889024001468
- Cao, S. et al. "Local Heuristics for Accelerating A* in 2D Continuous Space Path Planning (LoHA*)" (2024): https://arxiv.org/abs/2411.03650
