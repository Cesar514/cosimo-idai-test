# Reviewer 3 (Rigor, Writing, and Compliance) - Round 1

## Scope
Review focus: statistical rigor, limitation handling, writing quality, figure/table integration, and citation compliance with the 2021+ constraint.

## Summary Verdict
- Statistical rigor: **major revisions needed** (descriptive statistics are present, but inferential support is missing for core comparative claims).
- Limitation handling: **partially adequate** (good limitation text exists, but some claims still overreach relative to evidence).
- Writing quality: **major revisions needed** (front matter is incomplete for submission).
- Figure/table integration: **moderate issues** (core links exist, but some figure/table choices and protocol details need correction).
- Citation compliance (2021+): **pass on current manuscript and bibliography** (no cited pre-2021 entries found).

## Prioritized Findings

1. **BLOCKER - Submission front matter is incomplete.**  
   **Locations:** `paper/ieee_tro_robotics_maze/main.tex:16-18`, `paper/ieee_tro_robotics_maze/main.tex:22-24`, `paper/ieee_tro_robotics_maze/main.tex:26-28`  
   **Issue:** Author block contains placeholders, abstract is empty, and keywords are placeholders (`keyword1, keyword2, keyword3`).  
   **Why it matters:** This is non-compliant with journal submission basics and prevents substantive scientific evaluation by editors/reviewers.

2. **MAJOR - Comparative performance claims are not supported by inferential statistics.**  
   **Locations:** `paper/ieee_tro_robotics_maze/sections/06_results.tex:35-42`, `paper/ieee_tro_robotics_maze/sections/07_discussion.tex:7-10`, `paper/ieee_tro_robotics_maze/tables/main_results_table.tex:11-22`  
   **Issue:** The manuscript makes rank/speed claims (e.g., fastest planner, 35% faster language) from descriptive summaries only, while top-tier runtime differences are small and overlapping in spread.  
   **Required action:** Add per-maze paired inferential analysis (e.g., Wilcoxon signed-rank or bootstrap paired CI), effect sizes, and multiplicity control across planner comparisons.

3. **MAJOR - Timing methodology is under-specified for sub-millisecond claims.**  
   **Locations:** `paper/ieee_tro_robotics_maze/sections/05_experiments.tex:46-51`, `paper/ieee_tro_robotics_maze/sections/06_results.tex:45`  
   **Issue:** Wall-clock runtime is central, but the manuscript does not report timing API, hardware/OS details, CPU governor/load controls, warm-up strategy, or repeated-run protocol per maze-planner pair.  
   **Why it matters:** Without measurement protocol detail, very small runtime deltas are not reproducibly interpretable.

4. **MAJOR - Ranking policy is described inconsistently across sections.**  
   **Locations:** `paper/ieee_tro_robotics_maze/sections/04_method.tex:41-45`, `paper/ieee_tro_robotics_maze/tables/main_results_table.tex:3`, `paper/ieee_tro_robotics_maze/sections/07_discussion.tex:3`  
   **Issue:** Method equation states path length precedes expansions in tie-breaking, while table/discussion text states expansions precede path length.  
   **Required action:** Harmonize one canonical ranking order and restate it identically in Method, Results table caption, and Discussion.

5. **MAJOR - Appendix checklist includes stale/incorrect compliance statements.**  
   **Locations:** `paper/ieee_tro_robotics_maze/appendix/reproducibility_checklist.tex:18-20`  
   **Issue:** Appendix claims references/citation audit/figure manifest are still placeholder-level, which conflicts with current repository files.  
   **Why it matters:** This undermines trust in reproducibility and compliance reporting.

6. **MEDIUM - Limitation text exists but is not fully reflected in claim strength.**  
   **Locations:** `paper/ieee_tro_robotics_maze/sections/06_results.tex:44-47`, `paper/ieee_tro_robotics_maze/sections/07_discussion.tex:7-10`  
   **Issue:** The manuscript acknowledges external-validity limits, yet discussion language still frames findings as robust without inferential backing.  
   **Required action:** Reframe outcome language as benchmark-snapshot evidence unless stronger statistics are added.

7. **MEDIUM - Protocol table uses an invalid command form for the simulation regression script.**  
   **Locations:** `paper/ieee_tro_robotics_maze/tables/experiment_protocol_table.tex:10`, `robotics_maze/testing/run_sim_tests.sh:1`  
   **Issue:** Table lists `python3 robotics_maze/testing/run_sim_tests.sh`, but the target is a bash script.  
   **Required action:** Replace with `bash robotics_maze/testing/run_sim_tests.sh` (or executable invocation) for reproducibility accuracy.

8. **MEDIUM - Figure portfolio includes a process-management figure with weak scientific payoff in main text.**  
   **Locations:** `paper/ieee_tro_robotics_maze/sections/05_experiments.tex:11-12`, `paper/ieee_tro_robotics_maze/sections/05_experiments.tex:27-29`  
   **Issue:** The agentic-workflow figure documents manuscript production flow rather than algorithmic behavior or experimental outcomes.  
   **Recommendation:** Move this figure to supplement/appendix unless directly tied to a scientific reproducibility argument in main claims.

9. **MINOR - Results figures omit uncertainty visualization despite central reliance on runtime comparisons.**  
   **Locations:** `paper/ieee_tro_robotics_maze/sections/06_results.tex:14-15`, `paper/ieee_tro_robotics_maze/sections/06_results.tex:22-23`  
   **Issue:** Runtime/expansion plots display means only; variability is only in table text.  
   **Recommendation:** Add error bars, boxplots, or violin overlays to align figures with statistical interpretation.

## Citation Compliance (2021+ Constraint)
- **Pass**: `references.bib` entries are year 2021-2025 only (no `<2021` entries detected).
- **Pass**: all in-text cite keys found in manuscript sections resolve to entries in `references.bib`.
- **Compliance caveat**: narrative compliance reporting should be synchronized with current appendix/checklist statements to avoid internal contradictions.
