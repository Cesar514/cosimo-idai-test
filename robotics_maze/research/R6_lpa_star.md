# R6 Research Note: LPA* / D* Lite for Repeated Replanning

## Why this family
- **Lifelong Planning A\*** (LPA\*) keeps `g` and `rhs` values across replans, so it can update only locally affected vertices after map changes instead of re-running A\* from scratch.
- **D\* Lite** uses the same core idea with a goal-rooted formulation that is especially effective when the robot start moves over time.
- Both are best when edge-cost changes are sparse between replans (typical for partially discovered maps or dynamic obstacles).

## Practical behavior in dynamic maps
- If only a few cells change occupancy, LPA\* typically expands far fewer nodes than fresh A\*.
- Priority-queue work scales with affected inconsistency, not full map size, when updates are local.
- This makes the method suitable for looped simulation where each step triggers small obstacle edits or incremental sensing updates.

## R6 implementation choice
- Implemented `plan_lpa_star(grid, start, goal)` as a **forward LPA\*** variant with persistent module-level cache.
- Supports incremental replanning when:
  - grid dimensions are unchanged
  - `start` and `goal` are unchanged
  - occupancy updates are applied between calls
- Explicit approximation boundary:
  - if shape or endpoints change, planner performs a full reset and recomputes from scratch.
  - this keeps behavior clear and robust while still giving practical incremental wins for repeated same-endpoint replans.

## Returned metrics (for benchmarking)
- `reused_tree`, `full_reset`, `reset_reason`
- `changed_cells`
- `expanded_nodes`, `queue_pushes`, `queue_pops`
- `path_cost`, `path_length`, `time_ms`, `status`

## Strength summary
- **Main strength:** fast repeated replanning under local map updates.
- **Secondary strength:** deterministic and benchmark-friendly counters.
- **Known limitation:** moving-start scenarios are better served by a D\* Lite-style key-shift (`k_m`) extension.

## Canonical references
- Koenig, Likhachev, Furcy (2004): *Lifelong Planning A\**.
- Koenig, Likhachev (2002): *D\* Lite*.
