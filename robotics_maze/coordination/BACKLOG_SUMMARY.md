# Backlog Summary: Session-Created GitHub Issues

Last verified: 2026-02-27 (UTC)  
Repository: `Cesar514/cosimo-idai-test`

## Open Issues Created In This Session

| Issue | Title | Status |
|---|---|---|
| [#1](https://github.com/Cesar514/cosimo-idai-test/issues/1) | Test: Validate robotics planner recommendations in-repo + literature grounding (>=10 post-2021 refs) | OPEN |
| [#2](https://github.com/Cesar514/cosimo-idai-test/issues/2) | Test: Validate robotics planner recommendations with pre-2021 literature justifications | OPEN |
| [#5](https://github.com/Cesar514/cosimo-idai-test/issues/5) | Test (Expanded): Validate robotics planner recommendations + >=20 post-2021 references (4-sentence justifications each) | OPEN |
| [#6](https://github.com/Cesar514/cosimo-idai-test/issues/6) | Test (Expanded): Validate robotics planner recommendations + >=20 pre-2021 references (4-sentence justifications each) | OPEN |

## What Each Issue Should Validate

### Issue #1
- Validate all planner recommendations in `robotics_maze/` against repository evidence.
- Classify each method as implemented, partial, docs-only, or missing.
- Provide at least 10 references from 2021+ with relevance summaries.
- Reconcile claims vs implementation reality and propose top remediation steps.

### Issue #2
- Validate all planner recommendations in `robotics_maze/` against repository evidence.
- Classify each method as implemented, partial, docs-only, or missing.
- Provide at least 10 references from 2020 or earlier with relevance summaries.
- Reconcile claims vs implementation reality and propose top remediation steps.

### Issue #5 (Expanded Post-2021)
- Re-run the same verification as #1 with stricter rigor.
- Produce a complete claim-vs-implementation matrix with explicit file-path evidence.
- Provide at least 20 references from 2021+.
- For each reference, include exactly 4 sentences: contribution, relevance, limitation, implementation priority impact.
- Produce prioritized remediation outputs with effort sizing.

### Issue #6 (Expanded Pre-2021)
- Re-run the same verification as #2 with stricter rigor.
- Produce a complete claim-vs-implementation matrix with explicit file-path evidence.
- Provide at least 20 references from 2020 or earlier.
- For each reference, include exactly 4 sentences: contribution, relevance, limitation, implementation priority impact.
- Produce prioritized remediation outputs with effort sizing.

## Backlog Ordering Note

- `#5` is the expanded, stricter version of `#1` (post-2021 track).
- `#6` is the expanded, stricter version of `#2` (pre-2021 track).
- If de-duplicating effort, prioritize `#5` and `#6` first.

## Newly Added Open Issues In This Session (#9-#18)

| Issue | Title | Short Purpose |
|---|---|---|
| [#9](https://github.com/Cesar514/cosimo-idai-test/issues/9) | [Paper/Repro] Freeze benchmark snapshot to prevent manuscript metric drift | Lock a canonical benchmark snapshot and bind manuscript tables to that exact artifact. |
| [#10](https://github.com/Cesar514/cosimo-idai-test/issues/10) | [Math/Stats] Add repeated-run timing protocol and rank-stability analysis | Upgrade benchmarking from single-run timing to repeat-aware, statistically stable comparisons. |
| [#11](https://github.com/Cesar514/cosimo-idai-test/issues/11) | [Literature] Verify all 2021+ references and DOI metadata against primary sources | Audit bibliography metadata and peer-review flags for correctness and traceability. |
| [#12](https://github.com/Cesar514/cosimo-idai-test/issues/12) | [Math/Traceability] Script inferential table generation from benchmark CSV | Create a deterministic script path from benchmark CSV to inferential CSV + LaTeX table outputs. |
| [#13](https://github.com/Cesar514/cosimo-idai-test/issues/13) | [RealSim] Backend parity evaluation: PyBullet vs MuJoCo on matched episodes | Quantify physics-backend sensitivity under matched seeds with paired metrics. |
| [#14](https://github.com/Cesar514/cosimo-idai-test/issues/14) | [RealSim] Implement dynamic-obstacle benchmark extension + replanning metrics | Add dynamic obstacle scenarios and replanning-quality metrics to benchmark coverage. |
| [#15](https://github.com/Cesar514/cosimo-idai-test/issues/15) | [Simulation] URDF fallback robustness tests and structured diagnostics | Test URDF fallback branches and emit machine-readable failure reasons. |
| [#16](https://github.com/Cesar514/cosimo-idai-test/issues/16) | [Benchmark/CI] Enforce canonical 12-planner set with fail-closed checks | Add CI guardrails so planner-set drift fails fast with explicit diagnostics. |
| [#17](https://github.com/Cesar514/cosimo-idai-test/issues/17) | [Paper] Final novelty/framing polish for journal submission | Final editorial pass to tighten bounded novelty claims and framing consistency. |
| [#18](https://github.com/Cesar514/cosimo-idai-test/issues/18) | [Figures] Replace paper figures with publication-grade scripted plots | Replace ad hoc figure generation with deterministic publication-grade plotting pipeline. |

## Prioritization Notes For #9-#18

- **P0 Reproducibility Foundation (do first):** `#9`, `#10`, `#12`, `#16`
- **P1 Runtime/Simulation Robustness (next):** `#13`, `#15`, `#14`
- **P2 Submission Polish (after data is locked):** `#11`, `#18`, `#17`

### Suggested Execution Order
1. `#9` -> freeze snapshot baseline.
2. `#10` -> produce repeat-aware benchmark aggregates.
3. `#12` -> regenerate inferential tables from locked snapshot/aggregates.
4. `#16` -> enforce canonical planner-set contract in CI.
5. `#13` and `#15` in parallel -> backend parity + URDF fallback reliability.
6. `#14` -> dynamic-obstacle extension (after core static benchmark pipeline is stable).
7. `#11` -> final bibliography verification pass before manuscript freeze.
8. `#18` -> deterministic final figures from locked artifacts.
9. `#17` -> final framing polish once numbers/figures/references are fixed.
