# R3 Research Note: Theta* for Maze Navigation

## Summary
Theta* is an any-angle extension of A* that keeps A*'s best-first search but relaxes the parent relation using line-of-sight (LOS) checks. Instead of forcing each successor to use the current node as its parent, Theta* tries to connect the successor directly to the current node's parent when visible. This reduces zig-zagging and typically shortens paths in open regions.

## Why Theta* for Mazes
- A* on an 8-connected grid is easy to implement and robust but still grid-constrained.
- Theta* keeps discrete search over free cells but outputs fewer heading changes by skipping intermediate turning points.
- It is a practical middle ground between pure graph A* and full continuous trajectory optimization.

## Core Update Rule
For each expansion from `s` to neighbor `s'`:
- Standard A* candidate: `g(s) + c(s, s')`
- Theta* candidate: if `LOS(parent(s), s')` then `g(parent(s)) + c(parent(s), s')`
- Choose lower-cost option.

This parent lifting is what performs implicit smoothing during the search itself.

## LOS Optimization Details
- Use a supercover grid traversal so every cell touched by the line segment is tested.
- Include a diagonal pinch check: if two corner-touching blocked cells would be squeezed between, LOS is rejected.
- Cache LOS results by node pair to avoid repeated geometric checks in large open spaces.

## Assumptions
- Grid uses `(row, col)` indexing.
- Free cell is falsy (`0`/`False`); blocked is truthy (`1`/`True`).
- Grid is rectangular.
- 8-connected motion with Euclidean step cost (`1` cardinal, `sqrt(2)` diagonal).
- Out-of-bounds behaves as blocked.
- Point-robot approximation (no footprint inflation in this planner layer).

## Complexity Notes
- Search backbone remains A*-like: worst-case node expansions still tied to grid size.
- LOS checks add per-edge overhead versus plain A*.
- LOS caching recovers substantial runtime when many nodes share visibility queries.

## When Smoothing Helps Most
- Open courtyards or long hallways where many waypoints are collinear/near-collinear.
- Maps where A* produces frequent staircase patterns around sparse obstacles.
- Long-distance goals with few narrow chokepoints.

## When Gains Are Limited
- Very dense mazes with frequent occlusion (LOS fails often).
- Tight one-cell corridors where paths are already constrained.
- Situations requiring robot-footprint-aware clearance (needs inflation or post-checking).

## Metrics to Track
- `expanded_nodes`: search effort.
- `los_checks`, `los_successes`, `los_cache_hits`: LOS workload and payoff.
- `path_cost`, `path_nodes`: solution quality/compactness.
- `smoothed_segments`: number of multi-cell straight jumps in final path.
- `wall_time_ms`: end-to-end runtime.
