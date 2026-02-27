# Reviewer 2 — Methods & Rigor (Round 2)

## Decision
**major remaining**

## Remaining Blockers (Round-1 major/critical not fully cleared)

1. **[Major] Reproduction entrypoints are still inconsistent across executable paths.**  
   **Pointers:** `paper/ieee_tro_robotics_maze/sections/05_experiments.tex:27-30`, `pixi.toml:20`, `robotics_maze/pixi.toml:20`.  
   **Why still open:** The manuscript reports a 50-maze benchmark snapshot, while task aliases still target 30 mazes; one alias still uses invalid `--num-mazes`.

2. **[Major] Ranking policy is still contradictory between manuscript claims and shipped benchmark artifact metadata.**  
   **Pointers:** `paper/ieee_tro_robotics_maze/sections/04_method.tex:46-50`, `paper/ieee_tro_robotics_maze/tables/main_results_table.tex:3`, `paper/ieee_tro_robotics_maze/sections/07_discussion.tex:3`, `robotics_maze/results/benchmark_summary.md:9`.  
   **Why still open:** Manuscript sections are internally harmonized, but `benchmark_summary.md` still states a different ranking key order.

3. **[Major] Sub-millisecond timing claims still rely on single-run per maze-planner measurements.**  
   **Pointers:** `paper/ieee_tro_robotics_maze/sections/05_experiments.tex:43-46`, `paper/ieee_tro_robotics_maze/sections/06_results.tex:45-47`.  
   **Why still open:** Inferential tests were added, but the protocol still executes each maze-planner pair once and does not document repeat-run/hardware-control procedures needed for stable sub-ms effect interpretation.

4. **[Major] Path-length tie-break remains active despite explicit non-comparability for Theta*.**  
   **Pointers:** `robotics_maze/src/benchmark.py:365-368`, `paper/ieee_tro_robotics_maze/tables/main_results_table.tex:26`, `paper/ieee_tro_robotics_maze/sections/06_results.tex:55`.  
   **Why still open:** The ranking still uses comparable path length as a lexicographic key while the manuscript explicitly states any-angle path lengths are not directly comparable to cardinal-grid planners.

5. **[Major] Expansion extraction still defaults missing schema fields to zero, which can bias ranking.**  
   **Pointers:** `robotics_maze/src/benchmark.py:86-103`, `robotics_maze/src/benchmark.py:217`, `robotics_maze/src/benchmark.py:368`.  
   **Why still open:** Missing/incompatible metrics can map to `0` expansions and then feed ranking keys.

6. **[Major] Traceability/compliance artifacts remain stale and internally contradictory.**  
   **Pointers:** `paper/ieee_tro_robotics_maze/coordination/citation_compliance_report.md:15-19`, `paper/ieee_tro_robotics_maze/coordination/citation_compliance_report.md:31`, `paper/ieee_tro_robotics_maze/coordination/citation_compliance_report.md:35`, `paper/ieee_tro_robotics_maze/coordination/paper_status.md:11`, `paper/ieee_tro_robotics_maze/coordination/claims_traceability.csv:24-27`.  
   **Why still open:** Coordination files simultaneously report both “0 references/non-compliant” and “70 references/citation gate pass,” plus outdated pending placeholder claims.

## Cleared Since Round 1 (major/critical scope)
- Front matter blocker is resolved: `paper/ieee_tro_robotics_maze/main.tex:16-39`.
- Manuscript-side ranking-order mismatch across Method/Table/Discussion is resolved: `paper/ieee_tro_robotics_maze/sections/04_method.tex:46-50`, `paper/ieee_tro_robotics_maze/tables/main_results_table.tex:3`, `paper/ieee_tro_robotics_maze/sections/07_discussion.tex:3`.
- Invalid shell invocation in protocol table is resolved: `paper/ieee_tro_robotics_maze/tables/experiment_protocol_table.tex:10`.
- Inferential runtime table and uncertainty reporting were added: `paper/ieee_tro_robotics_maze/sections/06_results.tex:44-47`, `paper/ieee_tro_robotics_maze/tables/statistical_comparison_table.tex:1-23`.
