# Benchmark Test Report Refresh

- Timestamp (UTC): 2026-02-27T10:30:27Z
- Updated file: `robotics_maze/testing/benchmark_test_report.md`
- Source of truth: `robotics_maze/results/benchmark_summary.md`

## What was refreshed

1. Replaced stale benchmark scope (`12` mazes, `11x11`) with latest snapshot metadata (`50` mazes, `15x15`, `backtracker`, seed `7`).
2. Synced key ranking to latest shared-success comparable solve-time table:
   - #1 `r1_weighted_astar` `0.35 ms`
   - #2 `r7_beam_search` `0.42 ms` (`+0.07 ms`)
   - #3 `r5_jump_point_search` `0.45 ms` (`+0.10 ms`)
3. Updated spread notes to current slowest planners:
   - `r6_lpa_star` `3.95 ms` (`+3.60 ms`)
   - `r4_idastar` `22.56 ms` (`+22.20 ms`)
4. Added explicit traceability section in the report pointing to source line ranges.

## Trace links used

- Snapshot metadata: `benchmark_summary.md` lines 3-10
- Ranking/metrics table: `benchmark_summary.md` lines 12-25
