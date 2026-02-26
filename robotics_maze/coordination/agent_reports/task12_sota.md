# Task 12/36 Report: SOTA Planner Research (2021+)

## Status
- Completed on: **2026-02-26**
- Ownership files delivered:
  - `robotics_maze/research/sota_planners_2021_plus.md`
  - `robotics_maze/coordination/agent_reports/task12_sota.md`

## Deliverable Summary
- Produced a ranked, citation-backed shortlist of **7** post-2021 planning approaches beyond vanilla A*.
- Added repository-specific integration notes tied to current planner and benchmark contracts.
- Included explicit references (papers/docs) and separated literature claims from engineering inferences.

## Top Ranked Outcomes (for this repo)
1. Learned Local Heuristics for A* (LoHA* line)
2. Cost-aware Hybrid-A* / State Lattice (Smac family)
3. Incremental Generalized Hybrid A* (IGHA*)
4. Guided RRT* family (Neural Informed / Hybrid / attention-guided)
5. Neural A* (differentiable search)
6. D*Lite + DWA fusion
7. Uncertainty-aware MPC local planning

## Practical Recommendation
- Start with a LoHA-style planner plugin (`r11_loha_astar`) to preserve the current grid benchmark setup while adding a post-2021 SOTA direction with moderate integration risk.

## Notes
- Ranking emphasizes practical fit for this repository’s current architecture.
- Some methods are highly capable but ranked lower due to required SE2/kinodynamic state expansion or heavier training/runtime dependencies.
