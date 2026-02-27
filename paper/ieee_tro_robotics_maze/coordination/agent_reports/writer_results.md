# Results Writer Report

## Scope
- Owned files edited:
  - `paper/ieee_tro_robotics_maze/sections/06_results.tex`
  - `paper/ieee_tro_robotics_maze/tables/main_results_table.tex`
  - `paper/ieee_tro_robotics_maze/coordination/agent_reports/writer_results.md`

## Inputs Used
- `robotics_maze/results/benchmark_summary.md`
- `robotics_maze/results/benchmark_results.csv`
- `robotics_maze/results/README.md` (to confirm benchmark protocol and metric definitions)

## What Was Added
- Replaced placeholder Results section with:
  - overall outcome statement (12 planners, 600/600 successes, no runtime errors),
  - runtime ranking interpretation,
  - search-effort trade-off interpretation,
  - explicit uncertainty/limitations paragraph.
- Added standalone table file `tables/main_results_table.tex` and included it from `06_results.tex`.

## Main Quantitative Claims Embedded
- Fastest mean runtime: `r1_weighted_astar` at 0.47 ms.
- Near-fastest cluster: 0.64--0.74 ms across six planners.
- Fastest-per-maze count: `r1_weighted_astar` fastest on 49/50 mazes.
- Small winner margins among fast methods: best-vs-second median gap 0.066 ms; 32/50 mazes within 0.1 ms.
- Expansion trade-off: `r5_jump_point_search` at 57.26 expansions vs `astar` at 189.06 (about 69.7% lower).
- Slow outliers: `r6_lpa_star` 7.13 ms; `r4_idastar` 27.27 ms with high variance (std 26.63 ms; IQR 3.85--51.48).

## Uncertainty and Limitation Language Added
- Single benchmark regime (50 mazes, one size, one generator, one seed schedule).
- Wall-clock timings with sub-ms deltas for top planners; cautioned interpretation.
- No repeated-run variance decomposition or formal significance testing.
- Static, fully known mazes only; transfer to dynamic/partial-observability not claimed.
- Theta* path-length comparability caveat explicitly stated due any-angle motion model.
