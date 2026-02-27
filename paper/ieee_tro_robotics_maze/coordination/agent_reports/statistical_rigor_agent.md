# Statistical Rigor Agent Report

Date: 2026-02-26  
Role: Runtime inferential analysis and uncertainty reporting

## Scope Completed
- Updated `paper/ieee_tro_robotics_maze/sections/06_results.tex` with a concise inferential-runtime subsection and aligned cautionary wording.
- Created `paper/ieee_tro_robotics_maze/tables/statistical_comparison_table.tex` (paired inference table).
- Generated `paper/ieee_tro_robotics_maze/figures/runtime_uncertainty.png` (runtime uncertainty box-summary figure).
- Updated `paper/ieee_tro_robotics_maze/coordination/figure_manifest.csv` to register the new figure.
- Created this report.

## Data Source
- `robotics_maze/results/benchmark_results.csv`
- Successful runs only (`success==1`), yielding 12 planners x 50 shared mazes (600 rows total).

## Methods Used (No SciPy/Pandas Dependency)
- Pairing: runtime compared on identical maze keys `(maze_index, maze_seed, width, height, algorithm)`.
- Effect size: paired median delta, \(\Delta=\text{comparator}-\texttt{r1\_weighted\_astar}\), in ms.
- Uncertainty: 95% percentile bootstrap CI from 40,000 paired resamples, fixed RNG seed `20260226`.
- Hypothesis test: exact two-sided paired sign test per comparator.
- Multiplicity: Holm correction over 11 pairwise comparisons.

## Key Outcomes
- `r1_weighted_astar` has the lowest mean runtime (0.4747 ms).
- All 11 pairwise comparisons vs `r1_weighted_astar` remain significant after Holm correction.
- Closest comparator:
  - `r7_beam_search`: median paired delta 0.095 ms, 95% CI [0.057, 0.117], slower/faster = 50/0, adjusted \(p=1.95\times10^{-14}\).
- Largest separations:
  - `r6_lpa_star`: median paired delta 5.991 ms, 95% CI [5.078, 8.016].
  - `r4_idastar`: median paired delta 13.380 ms, 95% CI [7.143, 34.426].

## Claim-Alignment Notes
- Updated Results text now distinguishes consistency/significance from practical magnitude for sub-millisecond deltas.
- Removed previous limitation wording that said formal significance tests were absent.
- Retained external-validity caveats (single maze regime, static fully known maps, Theta* path-length comparability caveat).
