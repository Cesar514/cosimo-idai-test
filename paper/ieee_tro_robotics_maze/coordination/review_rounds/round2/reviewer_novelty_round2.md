# Reviewer 1 — Novelty & Contribution Framing (Round 2)

## Decision
**major remaining**

## Overall Assessment
Round-2 revisions materially improved framing discipline: the abstract is now complete, claim scope is better bounded to the executed static-grid benchmark regime, and executed-vs-planned boundaries are clearer. However, the manuscript still does not establish a journal-standard novelty delta against the closest benchmark/runtime systems. The core remaining issue is comparative positioning, not writing quality.

## Remaining Revisions Required for Journal-Standard Framing

1. **[Major] Add explicit closest-work delta, not just citation-level positioning.**  
   **Pointers:** `sections/03_related_work.tex:16-17`, `sections/02_introduction.tex:8-14`.  
   **Issue:** The manuscript cites Bench-MR / MotionBenchMaker / composable platforms, but does not show a concrete capability-level comparison demonstrating what is uniquely new here.  
   **Required revision:** Add a compact comparison table (or equivalent structured paragraph) versus the 3--5 closest infrastructure papers on explicit axes (deterministic seed policy, planner I/O normalization, geometric path validation, shared-success comparability policy, backend fallback behavior, artifact traceability). Then state the precise incremental delta in 2--3 sentences.

2. **[Major] Reframe contribution bullets from implementation hygiene to defendable research contributions.**  
   **Pointers:** `sections/02_introduction.tex:8-14`.  
   **Issue:** Current bullets still read primarily as good engineering practice (determinism, adapters, artifact tracking) rather than clearly delimited technical contribution claims.  
   **Required revision:** Rewrite contributions into: (i) one infrastructure-method contribution with explicit mechanism, (ii) one evaluation-protocol contribution with fairness rationale, (iii) one evidence contribution tied to executed results. Move "traceable artifacts" to reproducibility/compliance support language rather than a primary novelty claim.

3. **[Major] Tighten title/opening framing to exactly match demonstrated scope.**  
   **Pointers:** `main.tex:14`, `sections/02_introduction.tex:1-6`.  
   **Issue:** Current title/opening can still be read as broad robotics reproducibility coverage, while evidence is static occupancy-grid maze planning plus deterministic simulation regression checks.  
   **Required revision:** Narrow wording to signal static grid-maze benchmark infrastructure as the demonstrated domain; keep dynamic/kinodynamic generalization explicitly future work.

4. **[Minor] Prune or compress loosely coupled related-work clusters to strengthen novelty signal.**  
   **Pointers:** `sections/03_related_work.tex:7-15`.  
   **Issue:** Broad DRL/multi-robot/uncertainty coverage dilutes the benchmark-infrastructure novelty thread.  
   **Required revision:** Keep only citations directly needed to motivate the benchmark-infrastructure gap and move peripheral domains to one concise bridge sentence.

5. **[Minor] Keep novelty language consistent with current evidentiary ceiling throughout front matter.**  
   **Pointers:** `main.tex:22-34`, `sections/08_conclusion.tex:3-5`.  
   **Issue:** Scope control is substantially improved, but novelty wording should remain consistently "infrastructure contribution for static-grid reproducible comparison" rather than implying broad planner-advancement claims.  
   **Required revision:** Perform one final terminology pass to ensure all contribution and conclusion phrasing uses the same bounded claim template.

## Clearance Condition for Next Round
Upgrade to **cleared** once the manuscript includes an explicit closest-work delta (Item 1), contribution-bullet reframing (Item 2), and scope-aligned title/front-matter positioning (Item 3). Items 4--5 are polish-level but recommended for final journal fit.
