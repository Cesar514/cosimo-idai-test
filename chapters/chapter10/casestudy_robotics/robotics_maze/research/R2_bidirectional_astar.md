# R2 Research: Bidirectional A* for Grid Mazes

## Summary
Bidirectional A* runs two informed searches at once:
- Forward search: `start -> goal`
- Backward search: `goal -> start`

For 2D maze grids with unit edge cost and 4-neighbor motion, this often reduces expansions compared to one-way A* because each frontier covers a smaller radius before meeting.

## Practical Algorithm Choice
Implemented variant:
- Heuristic: Manhattan distance.
- Motion model: 4-connected (`N, E, S, W`), unit cost per step.
- Meet condition: update best path when the two searches touch at a node or across one edge.
- Stop condition: stop when both frontier minima cannot beat the current best path (`best_cost`).

Returned outputs:
- `path`: list of `(row, col)` from start to goal.
- `metrics`: status, runtime, expansions, generated nodes, path length/cost, and meet bridge.

## Complexity
- Time: `O((V + E) log V)` worst-case (heap operations).
- Space: `O(V)` for frontier + g-score + parent maps.
- In open mazes, practical runtime is usually much lower than one-way A* due to reduced search depth from both sides.

## Tradeoffs
1. Faster in many symmetric/open mazes
- Two frontiers can significantly cut expansions.
- Extra bookkeeping adds overhead, so small mazes may see little benefit.

2. More state management than A*
- Must track two g-maps, two parent maps, and bridge candidates.
- More room for implementation bugs than unidirectional A*.

3. Heuristic dependence
- Manhattan is strong for axis-aligned 4-neighbor grids.
- Benefit drops when heuristic is weak (dense obstacles, convoluted corridors).

4. Unit-cost assumption in this implementation
- Current planner assumes each move costs `1`.
- Weighted terrain needs generalized edge costs and careful admissible heuristics.

## Failure Modes and Mitigations
1. Invalid or blocked endpoints
- Mode: start/goal out of bounds or on obstacles.
- Mitigation: early validation with clear status (`out_of_bounds`, `blocked_start_or_goal`).

2. Disconnected maze / no feasible path
- Mode: frontiers never connect.
- Mitigation: terminate with `status = no_path` and empty path.

3. Non-rectangular or malformed grid inputs
- Mode: indexing errors or undefined behavior if rows differ in length.
- Mitigation: caller should provide rectangular grids; add shape checks if integrating in production runner.

4. Representation mismatch for obstacles
- Mode: map encoding differs from expected conventions.
- Mitigation: normalize map data before planning; current implementation supports common numeric and simple string encodings.

5. Large maze memory pressure
- Mode: two frontier/state maps can grow large.
- Mitigation: cap maze size for real-time loop, or switch to memory-bounded alternatives (IDA*, frontier search variants).
