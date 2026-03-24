# R4 Research: IDA* for Memory-Constrained Pathfinding

## Why IDA*
Iterative Deepening A* (IDA*) combines the heuristic guidance of A* with DFS-like memory usage:
- A* keeps a large open set in memory (`O(|V|)` worst case).
- IDA* keeps the current DFS path plus recursion state (`O(d)` where `d` is solution depth).
- This makes IDA* attractive when maps are large but RAM is limited.

## Core Mechanics
1. Start with `threshold = h(start, goal)`.
2. Run depth-first search with pruning on `f(n) = g(n) + h(n)`.
3. If a node has `f(n) > threshold`, cut it and return that `f(n)` as a candidate next threshold.
4. If goal not reached, increase threshold to the minimum exceeded `f(n)` and repeat.
5. Stop when goal is found or no next threshold exists.

## Heuristic and Grid Assumptions
- 2D occupancy grid.
- 4-connected motion, unit edge cost.
- Manhattan distance is admissible and consistent under these assumptions.
- Deterministic tie-breaking improves repeatability for benchmarking.

## Complexity and Tradeoffs
- Memory: `O(d)` (main practical benefit).
- Time: often higher than A* due to repeated re-expansion across iterations.
- Best case: few threshold increases with informative heuristic.
- Worst case: many iterations and heavy re-traversal when heuristic is weak.

## Performance Expectations in Labyrinths
Labyrinths frequently contain:
- long corridors,
- choke points,
- dead-end branches,
- low direct-line visibility.

Expected behavior:
- Memory stays low and stable even as map size grows (strong IDA* advantage).
- Runtime can degrade versus A* in twisty labyrinths because each new threshold can replay substantial corridor prefixes.
- If the maze geometry causes Manhattan distance to underestimate heavily (e.g., walls force detours), expect more threshold increments and more re-expansions.
- In sparse, corridor-like maps with near-monotone progress to goal, IDA* can be competitive.

Practical expectation for benchmarking:
- IDA* should be treated as a memory-efficient alternative baseline.
- In complex labyrinths, expect slower wall-clock time than a well-implemented A* but lower peak memory pressure.
