# R1 Research: Weighted A* for Grid Mazes

## Core Idea
Weighted A* uses:

`f(n) = g(n) + w * h(n)`, with `w >= 1`

- `g(n)`: cost from start to node `n`
- `h(n)`: heuristic estimate to goal (Manhattan distance for 4-connected grids)
- `w`: heuristic inflation factor (speed-quality knob)

When `w = 1`, it is standard A*. As `w` increases, search becomes greedier and typically expands fewer nodes.

## Practical Behavior in Mazes
- Usually much faster than A* on large/open mazes or when start-goal distance is large.
- Often returns near-optimal paths for moderate weights (for example `1.2` to `2.0`).
- Can degrade path quality in narrow corridor mazes or trap-heavy maps where greediness causes detours.

## Complexity
Using a binary heap on a grid graph:
- Time (worst case): `O(E log V)` (same asymptotic class as A*)
- Space (worst case): `O(V)`

In practice, constant factors are often lower than A* because fewer nodes are expanded when heuristic guidance is informative.

## Quality vs Speed Tradeoff
- Lower `w` (close to `1.0`): closer to optimal path cost, more expansions.
- Higher `w`: fewer expansions and lower runtime, but higher suboptimality risk.
- Typical tuning strategy: start with `w=1.5`, then adjust per benchmark target (latency budget vs path quality).

## When It Outperforms A*
Weighted A* typically outperforms A* when:
- Real-time replanning speed matters more than strict optimality.
- Maps are large and mostly navigable (heuristic strongly correlates with true distance).
- You run many episodes and can accept small path-cost inflation for major runtime reduction.
