# Benchmark Test Report

- Command: `python3 robotics_maze/src/benchmark.py --mazes 12 --width 11 --height 11 --algorithm backtracker --output-dir /tmp/cosimi_t2_bench`
- Run scope: 12 planners x 12 mazes (11x11), maze algorithm `backtracker`, seed base `7`
- Overall reliability: all planners solved all mazes (100% success), no execution errors logged

## Fastest planners (mean solve time)

1. `r1_weighted_astar` - `0.335948 ms`
2. `r7_beam_search` - `0.412813 ms`
3. `r5_jump_point_search` - `0.466132 ms`

## Outliers and anomalies

- Time outliers by IQR (upper bound `2.857457 ms`):
  - `r4_idastar` - `10.984924 ms` (~32.7x slower than fastest)
  - `r6_lpa_star` - `4.183739 ms` (~12.5x slower than fastest)
- `r3_theta_star` produced much shorter mean paths (`32` vs `98` for most planners), which is expected from line-of-sight shortcutting and should be compared with care against grid-constrained path length metrics.
