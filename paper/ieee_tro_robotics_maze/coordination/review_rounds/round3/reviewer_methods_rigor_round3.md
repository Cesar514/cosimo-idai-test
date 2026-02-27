# Reviewer A — Methods & Rigor (Round 3)

## Decision
**minor**

## Severity-Tagged Findings

1. **[Minor] Reproduction environments can still drift across entrypoints due inconsistent dependency pinning.**  
   **Pointers:** `pixi.toml:9`, `robotics_maze/pixi.toml:14`.  
   **Issue:** Root and subproject Pixi specs pin different `pybullet` ranges (`>=3.24,<3.26` vs `>=3.2.7`). Re-running commands from different entrypoints can yield different solver/simulator behavior and weakens strict reproducibility.

2. **[Minor] Planner-set reproducibility is not fail-closed.**  
   **Pointers:** `robotics_maze/src/benchmark.py:232-239`, `robotics_maze/src/benchmark.py:250-256`, `robotics_maze/src/benchmark.py:688-702`, `paper/ieee_tro_robotics_maze/sections/05_experiments.tex:25-38`.  
   **Issue:** Planner loading is dynamic (“all discovered planners”), and `_safe_import` swallows `ModuleNotFoundError`, allowing silent planner omission. Current environment resolves 12 planners, but the benchmark does not enforce the manuscript’s 12-planner execution set as a hard check.

3. **[Minor] Inferential-results traceability remains partial.**  
   **Pointers:** `paper/ieee_tro_robotics_maze/sections/06_results.tex:45-47`, `paper/ieee_tro_robotics_maze/coordination/claims_traceability.csv:1-28`.  
   **Issue:** The Results section reports sign-test/Holm and bootstrap-CI claims, but the traceability table does not include dedicated claim rows mapping those inferential numbers to a source artifact/script. This limits auditability of statistical claims.

## Round-3 Summary
Round-2 major blockers in this file set appear resolved (benchmark task harmonization to 50 mazes, ranking-policy alignment, path-length removal from ranking key, and citation/claims artifact cleanup). Remaining items are reproducibility hardening and traceability-completeness refinements, not fundamental method invalidations.
