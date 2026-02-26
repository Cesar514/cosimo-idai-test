# R7 Research: Beam Search for Fast Approximate Pathfinding

## What It Is
Beam Search is a bounded best-first strategy. Instead of keeping all frontier
states (like A*), it keeps only the top `k` states (`beam_width`) by a ranking
function. In this implementation, ranking is:

`f(n) = g(n) + h(n)` with Manhattan `h(n)` and deterministic tie-breakers.

## Why It Is Fast
- It caps frontier growth to at most `beam_width` each depth.
- It reduces memory pressure compared to A*.
- It often reaches a decent path quickly in large open grids.

## Main Tradeoff: Speed vs Optimality
- Small `beam_width`:
  - Faster and lower memory.
  - Higher risk of pruning the best corridor.
  - More failures in narrow/maze-like maps.
- Large `beam_width`:
  - Slower, more memory.
  - Better success rate and path quality.
  - Approaches A*-like behavior as width increases.

Beam Search is **not optimality-guaranteed** and **not complete** under tight
beam limits, because good paths can be pruned early.

## Complexity (Qualitative)
Let `b` be branching factor, `d` solution depth, `k` beam width.
- Time (rough): `O(d * k * b + d * k log k)` from expansion + ranking/sort.
- Space (rough): `O(k + visited)` for active beam plus accepted states.

In practice, runtime scales close to linearly with `k` on fixed maps.

## Metrics Returned by `plan_beam_search`
- `found`: whether goal was reached.
- `path_length`: number of moves if found.
- `runtime_ms`: wall-clock runtime in milliseconds.
- `expanded_nodes`: number of beam nodes expanded.
- `generated_nodes`: improved candidate states generated.
- `visited_nodes`: unique states with best-known g-score.
- `max_frontier_size`: largest beam size used (<= `beam_width`).
- `beam_width`, `failure_reason`, `optimality_guaranteed`.

## Practical Recommendation
- Start with `beam_width=32` as a fast baseline.
- Increase to `64` or `128` when mazes are narrow or highly deceptive.
- Use A* when optimality must be guaranteed.
