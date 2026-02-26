# R5 Research: Jump Point Search (JPS) on Uniform-Cost Grids

## Summary
Jump Point Search (JPS) is a symmetry-breaking acceleration over A* on uniform-cost grids.  
Instead of expanding every intermediate cell, JPS "jumps" in straight directions until it reaches:
- the goal,
- an obstacle boundary,
- or a **jump point** (a cell with a forced branching opportunity).

This can drastically reduce node expansions in maze-like layouts while preserving optimality under the same cost model.

## Practical Variant Implemented
For this project, I implemented a practical **4-connected (N/E/S/W)** JPS variant:
- unit edge cost,
- Manhattan heuristic,
- forced-neighbor checks for cardinal motion,
- A* over jump points,
- final path expansion back to full cell-by-cell path.

Function: `plan_jps(grid, start, goal)`  
Module: `robotics_maze/src/alt_planners/r5_jump_point_search.py`

## Why This Variant
Canonical JPS is often presented with 8-connected movement and diagonal pruning/jump recursion, which is materially more complex.  
Given current repository maturity and expected planner interface simplicity, this 4-way variant is a strong tradeoff: meaningful pruning gains with lower implementation risk.

## Caveats
- This is **not** full diagonal JPS (no 8-way moves).
- Speedups are map-dependent; in open maps with few obstacles, jump scanning can reduce gains.
- The implementation assumes rectangular, static occupancy grids with `0=free`, non-zero=blocked.

## Return Contract
`plan_jps` returns `(path, metrics)`:
- `path`: full coordinate list from start to goal (inclusive), or `[]` on failure.
- `metrics`: planner status and benchmark fields (`expanded_nodes`, `generated_nodes`, `jump_calls`, `jump_steps`, `forced_stops`, open-list stats, `path_cost`, `elapsed_ms`).

## Expected Use
Use this planner as an alternative baseline to compare against plain A*/IDA* in benchmark harnesses focused on expansion count and wall-clock runtime.
