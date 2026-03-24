# Reviewer B — Novelty & Contribution Framing (Round 3)

## Decision
**minor**

## Severity-Tagged Findings

1. **[Minor] "Closest work" set is partly adjacent rather than closest benchmark-infrastructure prior art.**  
   **Pointers:** `sections/03_related_work.tex:4`, `tables/closest_work_delta_table.tex:23-29`.  
   **Issue:** The table mixes direct benchmark-framework comparators (Bench-MR, MotionBenchMaker, CoBRA) with broader platform papers (FogROS2-LS, Arena 4.0). That can weaken novelty defensibility by inviting pushback on comparator selection.  
   **Recommended fix:** Keep direct benchmark/runtime comparators in the "closest" table; move FogROS2-LS/Arena 4.0 to a short "adjacent systems" note.

2. **[Minor] Discussion devotes substantial space to speculative hypotheses, which dilutes current contribution framing.**  
   **Pointers:** `sections/07_discussion.tex:51-71`, `sections/08_conclusion.tex:5`.  
   **Issue:** H1--H4 are detailed enough to read like proposal content rather than bounded interpretation of executed results. This slightly blurs the paper's present-scope contribution signal.  
   **Recommended fix:** Compress H1--H4 into a concise future-work paragraph (or move detailed validation plans to appendix/supplement).

3. **[Nit] Delta wording could be framed as integration novelty (combination and auditable execution) rather than per-row implied component novelty.**  
   **Pointers:** `tables/closest_work_delta_table.tex:9-25`, `sections/03_related_work.tex:8`.  
   **Issue:** Current phrasing may be read as each component being newly introduced, while the stronger claim is the repository-level integration and traceable execution policy.  
   **Recommended fix:** Add one sentence explicitly stating that novelty is in the integrated, reproducible stack and bounded protocol, not in inventing each individual mechanism.

## Round-3 Summary
Core Round-2 novelty blockers are resolved: contribution bullets are bounded, closest-work delta is explicit, and scope control is clear in abstract/conclusion. Remaining items are polish-level framing refinements.
