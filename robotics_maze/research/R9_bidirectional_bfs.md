# R9 Research: Bidirectional BFS as a Uniform-Cost Baseline

## Summary
Bidirectional BFS is a strong baseline for unweighted, 4-connected grid mazes because it is:
- Optimal (returns shortest path in edge count).
- Complete (finds a path when one exists).
- Heuristic-free (no tuning, no admissibility concerns).

For unit-cost grids, it often cuts search effort from roughly `O(b^d)` (single-source BFS behavior) to about `O(b^(d/2))` from each side, where:
- `b` = effective branching factor,
- `d` = shortest-path depth.

## Why It Is a Good Baseline Against A*
As a benchmark baseline, bidirectional BFS gives a clean reference for:
- True shortest-path cost without heuristic influence.
- Search efficiency when heuristic guidance is weak or misleading.
- Robustness across maps because behavior does not depend on heuristic quality.

This makes it useful as a control method when evaluating A* variants and heuristic designs.

## When It Beats A*
Bidirectional BFS tends to outperform A* (runtime / expansions) when:
- The heuristic is weak relative to maze structure (e.g., Manhattan in tortuous labyrinths with many forced detours).
- Start and goal are far apart in a mostly unweighted, uniform environment.
- There are many equivalent shortest corridors where heuristic tie-breaking gives little directional advantage.
- You need predictable performance without heuristic sensitivity.

In these cases, two-front exploration can meet near the middle and reduce total expansions substantially.

## When It Does Not Beat A*
Bidirectional BFS usually loses to A* when:
- The heuristic is informative and consistent (e.g., open layouts where Manhattan closely tracks true cost).
- The map has strong directional geometry toward goal, so A* remains narrowly focused.
- Memory pressure is high: bidirectional BFS stores visited sets and parents for two searches.
- The graph is weighted (non-uniform costs): plain BFS is no longer cost-optimal and must be replaced by cost-aware methods.

## Practical Positioning
Recommended role in this project:
- Use as a deterministic, optimal uniform-cost baseline for benchmarking.
- Compare A* speedups against it to quantify heuristic value.
- Keep it in the planner suite for regression checks and heuristic-agnostic sanity validation.
