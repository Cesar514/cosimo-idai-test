# Reviewer 2 — Methods & Technical Correctness (Round 1)

## Overall Assessment
The manuscript has strong implementation depth, but the current methods package has several technical-consistency and reproducibility blockers. The most serious issue is a mismatch between the documented per-episode seed policy and the executable seed path in code. In addition, ranking policy definitions and traceability artifacts are internally inconsistent, which undermines auditability.

## Prioritized Comments

1. **[Critical] Per-episode seed math in the manuscript is inconsistent with executable code.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/sections/04_method.tex:11`; `robotics_maze/src/main.py:515-520`; `robotics_maze/src/maze.py:157-164`.  
   **Issue:** The paper states `s_e = s_0 + (e-1)` and says this is implemented. In code, `main.py` already applies `+(e-1)` and then `DeterministicMazeGenerator.generate()` adds `+episode` again, producing maze seeds `s_0 + 2e - 1`.  
   **Actionable fix:** Make one component own episode indexing (prefer `main.py` only). Update `DeterministicMazeGenerator.generate()` to use provided seed directly when non-`None`. Add a regression test asserting exact episode seeds for a known base seed.

2. **[Major] Ranking policy is contradictory across method text, results table, discussion, and generated artifact.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/sections/04_method.tex:41-45`; `paper/ieee_tro_robotics_maze/tables/main_results_table.tex:3`; `paper/ieee_tro_robotics_maze/sections/07_discussion.tex:3`; `robotics_maze/results/benchmark_summary.md:9`; `robotics_maze/src/benchmark.py:361-369`.  
   **Issue:** The code ranks by success, comparable time, comparable path length, expansions, mean time; manuscript locations state different orders (including expansions before path length).  
   **Actionable fix:** Define one canonical ranking vector in code and auto-render the exact policy text into manuscript artifacts/tables from that source.

3. **[Major] Reproduction entrypoints are inconsistent and include an invalid command path.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/tables/experiment_protocol_table.tex:10`; `robotics_maze/testing/run_sim_tests.sh:1`; `robotics_maze/pixi.toml:20`; `pixi.toml:20`; `paper/ieee_tro_robotics_maze/sections/05_experiments.tex:36-39`.  
   **Issue:** Protocol table shows `python3 .../run_sim_tests.sh` for a Bash script; `robotics_maze/pixi.toml` uses unsupported flag `--num-mazes`; root `pixi` benchmark task runs 30 mazes while reported table is 50 mazes.  
   **Actionable fix:** Publish a single “exact commands to reproduce Table 1/Figures” block and align all task aliases to it; remove invalid flags; include expected output filenames/checksums.

4. **[Major] Timing conclusions rely on single-pass wall-clock measurements despite sub-millisecond separations.**  
   **Pointer:** `robotics_maze/src/benchmark.py:567-574`; `paper/ieee_tro_robotics_maze/sections/06_results.tex:35-46`.  
   **Issue:** Fast planners differ by ~0.1 ms scale; single-run per maze and no hardware control make rank ordering sensitive to runtime noise/environment drift.  
   **Actionable fix:** Add repeated runs per maze-planner pair (with warm-up), report confidence intervals (or bootstrap CIs), and include a rank-stability analysis instead of only point means.

5. **[Major] Path-length tie-break is used even though manuscript states Theta* path lengths are not directly comparable.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/tables/main_results_table.tex:26`; `paper/ieee_tro_robotics_maze/sections/06_results.tex:45`; `robotics_maze/src/benchmark.py:366-369`.  
   **Issue:** Ranking includes path length as a lexicographic key while admitting non-comparability for any-angle planners.  
   **Actionable fix:** Either (a) remove path-length tie-break across mixed planner families, or (b) replace with a normalized geometric metric that is valid for both lattice and any-angle outputs.

6. **[Major] Expansion metric extraction can silently bias comparisons when schema fields are missing/incompatible.**  
   **Pointer:** `robotics_maze/src/benchmark.py:86-102`; `robotics_maze/src/benchmark.py:367-368`.  
   **Issue:** Missing expansion keys default to `0`, which can artificially improve ranking for planners with non-standard metric payloads.  
   **Actionable fix:** Require a strict metrics schema for ranked planners; treat missing expansion counts as invalid/`NaN` and exclude from expansion-based ordering unless explicitly standardized.

7. **[Major] Evidence traceability artifacts are stale and internally contradictory.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/appendix/reproducibility_checklist.tex:18-20`; `paper/ieee_tro_robotics_maze/coordination/citation_compliance_report.md:15-35`; `paper/ieee_tro_robotics_maze/coordination/paper_status.md:10-11`; `paper/ieee_tro_robotics_maze/coordination/claims_traceability.csv:24-28`; contrasted with `paper/ieee_tro_robotics_maze/references.bib:1-20`, `paper/ieee_tro_robotics_maze/coordination/citations_audit.csv:1-20`, `paper/ieee_tro_robotics_maze/coordination/figure_manifest.csv:1-6`, `paper/ieee_tro_robotics_maze/main.tex:37`.  
   **Issue:** Multiple coordination artifacts still claim placeholder bibliography/empty audits though those files are now populated and appendix is included.  
   **Actionable fix:** Regenerate all audit/traceability reports from one script, stamp each with source commit SHA + generation timestamp, and gate manuscript packaging on freshness.

8. **[Minor] Planner-set description is ambiguous about baseline BFS inclusion in benchmarked set.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/sections/04_method.tex:19`; `robotics_maze/src/planners.py:297-338`; `robotics_maze/src/benchmark.py:240`; `paper/ieee_tro_robotics_maze/sections/05_experiments.tex:37-44`.  
   **Issue:** Method text states BFS is a baseline in registry, but benchmark discovery excludes it; phrase “all discovered planners” can be misread as all available baseline variants.  
   **Actionable fix:** Explicitly define “benchmarked planner set” in one table and state why BFS is excluded (or include it for completeness).

9. **[Minor] Figure reproducibility metadata lacks executable provenance.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/coordination/figure_manifest.csv:2-6`.  
   **Issue:** Manifest indicates deterministic generation but records method strings rather than concrete script/command provenance.  
   **Actionable fix:** Add script path + command + source artifact hash per figure in the manifest.

## Reviewer Recommendation (Methods Axis)
Current methods quality is promising but **not yet publication-ready** due to one critical correctness inconsistency (seed policy) and multiple major reproducibility/traceability mismatches. Addressing comments 1–4 should be prioritized before further claim strengthening.
