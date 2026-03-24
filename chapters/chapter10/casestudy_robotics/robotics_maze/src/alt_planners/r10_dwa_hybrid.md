# R10 Integration Notes: DWA Hybrid with SOTA Global Replanners

## Goal
Recommend immediately implementable global planner upgrades to pair with local DWA control in maze navigation.

## Recommended Immediate Pair

## 1) D* Lite + DWA (Primary)
- Global: D* Lite on occupancy grid.
- Local: DWA tracks next global waypoint segment.
- Trigger global repair when occupancy updates invalidate upcoming path cells.

Why first:
- Best dynamic-map behavior with deterministic runtime.
- Closest to existing A*/LPA* design patterns.

## 2) AD* + DWA (Secondary)
- Global: AD* with `epsilon_start > 1` for fast first path.
- Local: DWA executes current prefix while AD* refines in background.
- When map changes, AD* repairs incrementally and can still improve quality over time.

Why second:
- Adds latency/quality control useful for simulation stress tests.

## Suggested Planner Contract

Use one shared interface so B4/B6 can benchmark fairly:

`planner(grid, start, goal, changed_cells=None, time_budget_ms=None, **kwargs) -> (path, metrics)`

Minimum `metrics` keys:
- `runtime_ms`
- `expanded_nodes`
- `path_cost`
- `replans`
- `status` (`ok`, `unreachable`, `timeout`)

## DWA Hybrid Loop (Planner-Agnostic)
1. Receive latest occupancy updates.
2. If path invalid or stale, call global planner with changed cells.
3. Select lookahead waypoint on global path.
4. Run DWA for one control horizon toward lookahead.
5. Repeat until goal reached or declared unreachable.

## Implementation Priority
1. Implement `r10_dstar_lite.py` first.
2. Implement `r10_adstar.py` second.
3. Add both to B6 benchmark matrix against A* baseline and LPA* (R6).

## Risks / Mitigations
- Risk: frequent full replans due poor invalidation logic.
- Mitigation: track affected path indices and only repair when necessary.

- Risk: DWA oscillation near tight corners.
- Mitigation: waypoint smoothing + minimum progress threshold + short-term heading bias.
