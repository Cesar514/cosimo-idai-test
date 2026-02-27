# Reviewer 1 — Novelty & Contribution Framing (Round 1)

## Overall Assessment
The manuscript presents a potentially useful **engineering benchmark stack** for deterministic grid-maze experiments, but the current novelty framing is not yet convincing for an IEEE robotics journal standard. The main issue is not implementation effort; it is the gap between what is claimed as contribution and what is demonstrated as new knowledge versus existing benchmarking/runtime frameworks.

## Prioritized Comments

1. **[Major] Novelty framing is currently unassessable at the manuscript entry point due to a missing abstract.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/main.tex`, `Abstract` block, lines 22–24.  
   **Why this matters:** The abstract is where novelty, gap, and core contribution scope must be stated succinctly. Its absence prevents a proper first-pass novelty assessment.

2. **[Major] Claimed contributions are mostly implementation-quality practices; the manuscript does not yet isolate a clear scientific/methodological novelty over existing benchmark platforms.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/sections/02_introduction.tex`, `Introduction` contribution list, lines 8–14; `paper/ieee_tro_robotics_maze/sections/03_related_work.tex`, `Benchmarks and runtime frameworks`, lines 16–17.  
   **Why this matters:** Determinism, adapter layers, path validation, and artifact traceability are valuable, but these are often expected in modern benchmark infrastructure. The paper needs a sharper “what is new here beyond prior systems” argument.

3. **[Major] Positioning versus closest prior benchmarking systems is asserted but not demonstrated.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/sections/03_related_work.tex`, lines 16–17; `paper/ieee_tro_robotics_maze/sections/04_method.tex`, `Benchmark Protocol and Ranking`, lines 33–47.  
   **Why this matters:** The manuscript cites Bench-MR / MotionBenchMaker / composable platforms, but does not provide an explicit comparative analysis (feature-level or empirical) to justify incremental vs distinct contribution.

4. **[Major] Contribution scope is broader than supporting evidence; current experiments are too narrow to sustain stronger general claims.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/sections/05_experiments.tex`, `Planner benchmark (executed)`, lines 34–51; `paper/ieee_tro_robotics_maze/sections/06_results.tex`, lines 4–5 and 44–47; `paper/ieee_tro_robotics_maze/sections/07_discussion.tex`, lines 40–47.  
   **Why this matters:** Evidence is from one maze family, one size, one seed schedule, static setting, and saturated success (100% for all planners). This supports a narrow benchmark snapshot, not broader claims about robotics navigation benchmarking.

5. **[Major] Overclaim risk from title/positioning relative to demonstrated scope.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/main.tex`, title line 14; `paper/ieee_tro_robotics_maze/sections/07_discussion.tex`, lines 7–10 and 12–15.  
   **Why this matters:** The title and framing suggest broad multi-backend robotics reproducibility contributions, while demonstrated quantitative evidence remains limited to static grid-maze planner timing/expansion comparisons.

6. **[Minor] Related-work breadth is high but includes several domains not directly tied to the tested contribution, which weakens novelty focus.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/sections/03_related_work.tex`, lines 7–15.  
   **Why this matters:** Extensive DRL mapless, multi-robot exploration, and uncertainty planning discussion is only loosely connected to the actually evaluated system, making the core novelty thread harder to follow.

7. **[Minor] “Traceable research artifacts” is framed as a core contribution, but this reads as reproducibility hygiene rather than novelty.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/sections/02_introduction.tex`, contribution item 4, lines 13–14.  
   **Why this matters:** In a T-RO-style review, artifact traceability is expected; it can strengthen credibility, but typically does not by itself constitute a primary scientific contribution.

8. **[Minor] Executed-vs-planned boundary is clearer in experiments than in the headline contribution framing, creating scope ambiguity.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/sections/02_introduction.tex`, lines 8–14; `paper/ieee_tro_robotics_maze/sections/05_experiments.tex`, lines 66–81; `paper/ieee_tro_robotics_maze/sections/08_conclusion.tex`, lines 5–5.  
   **Why this matters:** The paper responsibly labels future studies later, but the earlier contribution framing can still be read as stronger than currently executed evidence.

9. **[Nit] Manuscript-production workflow figure may dilute technical contribution emphasis in the experiments section.**  
   **Pointer:** `paper/ieee_tro_robotics_maze/sections/05_experiments.tex`, lines 11–12 and 24–31.  
   **Why this matters:** For novelty framing, space is better focused on technical benchmark design and differentiators.

10. **[Nit] Placeholder keywords indicate an unfinished contribution framing front matter.**  
    **Pointer:** `paper/ieee_tro_robotics_maze/main.tex`, `IEEEkeywords`, lines 26–28.  
    **Why this matters:** Keywords are part of positioning and discoverability; placeholders weaken the paper’s contribution signaling.

## Reviewer Recommendation (Novelty Axis)
Current novelty signal is **below acceptance threshold** for a strict IEEE robotics-journal bar in its present framing. The work appears promising as a reproducible benchmark/system paper, but novelty must be reframed around a sharply defined, demonstrated delta versus closest infrastructure baselines and a contribution scope that exactly matches executed evidence.
