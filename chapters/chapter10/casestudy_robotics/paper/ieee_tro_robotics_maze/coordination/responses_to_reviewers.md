# Round 1 Responses to Reviewers (Revision Integrator)

## Scope note
Round 1 revisions now include both non-statistical fixes and a dedicated statistical-rigor pass.
Round 2 integration additionally applied benchmark code and coordination-artifact updates to clear previously open technical blockers.

## Reviewer 3 (Rigor, Writing, Compliance)

| ID | Status | Response and action |
|---|---|---|
| R3-1 | Resolved | Completed front matter in `main.tex`: concrete author metadata, publication-quality abstract, and non-placeholder IEEE keywords. |
| R3-2 | Resolved | Added paired exact sign tests with Holm correction and paired bootstrap confidence intervals in `sections/06_results.tex` and `tables/statistical_comparison_table.tex`; discussion claims now reference inferential evidence. |
| R3-3 | Partially resolved | Expanded timing protocol text in `sections/05_experiments.tex` (timing API, per-pair execution model, descriptive interpretation caution). No repeated-run data generation in this pass. |
| R3-4 | Resolved | Harmonized ranking policy text to executable ordering in `sections/04_method.tex`, `tables/main_results_table.tex`, `tables/experiment_protocol_table.tex`, and `sections/07_discussion.tex`. |
| R3-5 | Resolved | Updated `appendix/reproducibility_checklist.tex` to remove stale placeholder statements and align with current repository artifacts. |
| R3-6 | Resolved | Reframed Discussion claims as descriptive snapshot evidence, not inferential superiority (`sections/07_discussion.tex`). |
| R3-7 | Resolved | Corrected invalid command to `bash robotics_maze/testing/run_sim_tests.sh` in `tables/experiment_protocol_table.tex`. |
| R3-8 | Resolved | Reduced manuscript-process figure prominence by removing the workflow figure from main experiments text and keeping only the scientific pipeline figure (`sections/05_experiments.tex`). |
| R3-9 | Resolved | Added runtime uncertainty figure (`figures/runtime_uncertainty.png`) and integrated it in `sections/06_results.tex`. |

## Reviewer 2 (Methods and Technical Correctness)

| ID | Status | Response and action |
|---|---|---|
| R2-1 | Resolved | Method text now explicitly matches executable seed behavior in `sections/04_method.tex` (documented `s_main` and effective `s_gen` policy). |
| R2-2 | Resolved | Ranking policy now matches executable behavior across code, generated summary artifact, and manuscript text/tables. |
| R2-3 | Resolved | Reproduction entrypoints synchronized in `pixi.toml`, `robotics_maze/pixi.toml`, and protocol tables (valid command flags and 50-maze workload). |
| R2-4 | Partially resolved | Inferential analysis remains exploratory because each planner-maze pair is measured once; explicit caveat added in `sections/06_results.tex` and table caption. |
| R2-5 | Resolved | Path-length tie-break removed from executable ranking policy; path length retained as descriptive metric only. |
| R2-6 | Resolved | `benchmark.py` no longer defaults missing expansion schema fields to zero for ranking statistics. |
| R2-7 | Resolved | Coordination artifacts refreshed (`citation_compliance_report.md`, `claims_traceability.csv`, `paper_status.md`). |
| R2-8 | Resolved | Clarified benchmarked planner set and explicit BFS exclusion rationale in `sections/05_experiments.tex`. |
| R2-9 | Resolved | Figure manifest updated with explicit provenance details and artifact references in `coordination/figure_manifest.csv`. |

## Reviewer 1 (Novelty and Framing)

| ID | Status | Response and action |
|---|---|---|
| R1-1 | Resolved | Added complete abstract in `main.tex`. |
| R1-2 | Resolved | Contribution bullets in `sections/02_introduction.tex` are reframed as bounded infrastructure/protocol/evidence contributions. |
| R1-3 | Resolved | Added explicit closest-work delta comparison in `tables/closest_work_delta_table.tex` and integrated it in `sections/03_related_work.tex`. |
| R1-4 | Partially resolved | Experiments and Discussion now explicitly bound claims to the executed static benchmark regime. |
| R1-5 | Resolved | Title and front-matter wording now explicitly scope claims to static grid-maze benchmark infrastructure. |
| R1-6 | Resolved | Related Work narrowed to infrastructure-adjacent literature and concise positioning. |
| R1-7 | Resolved | Introduction now frames traceability artifacts as reproducibility support, not primary novelty. |
| R1-8 | Resolved | Executed-vs-planned boundary reinforced in `sections/05_experiments.tex` and aligned discussion language. |
| R1-9 | Resolved | Manuscript-process figure removed from main experiments section. |
| R1-10 | Resolved | Placeholder keywords replaced with concrete indexing terms in `main.tex`. |

## Consolidated status
- Resolved in this round: seed-policy wording alignment, ranking-policy consistency across code/artifacts/text, benchmark entrypoint consistency, path-length ranking bias removal, expansion-metric hardening, novelty reframing, and coordination-artifact freshness.
- Partially resolved: timing rigor remains limited by single-run per planner-maze timing; this is now explicitly labeled exploratory and queued for repeated-run future work.
