# IEEE T-RO Paper Orchestration Plan: Robotics Maze System + Benchmark (2021+ Literature Only)

## Summary
Produce a **full submission package** in LaTeX (IEEE journal format aligned to T-RO expectations) for the robotics maze setup, covering:
1. What is implemented and validated now.
2. What remains to implement, with aggressive forward-looking hypotheses.
3. A strict literature base of **at least 40 references, all from 2021+**, with **>=80% peer-reviewed** sources.

The process is multi-agent, reviewer-driven, and evidence-traceable, with journal-style internal review rounds before final packaging.

## Scope and Boundaries
- In scope: manuscript, bibliography, figures/tables, appendices, reproducibility package, internal reviewer comments/responses.
- In scope: current implemented artifacts from this repo (simulation, planners, benchmark outputs, screenshots, coordination evidence).
- In scope: explicit “still-to-implement” roadmap with speculative hypotheses.
- Out of scope: fabricating any new results, fabricated citations, or undocumented claims.
- Evidence policy: use current repository results + formal gap analysis; no new experiments required in this cycle.

## Target Deliverable Set
Create a new paper workspace at `paper/ieee_tro_robotics_maze` with:
1. `main.tex` (IEEE journal template).
2. `sections/*.tex` (full manuscript sections).
3. `references.bib` (40+ references, all 2021+).
4. `figures/*` (reproducible plots/diagrams and selected simulation visuals).
5. `tables/*` and LaTeX tables in sections.
6. `appendix/*.tex` for reproducibility and additional analyses.
7. `review_rounds/*.md` and `responses_to_reviewers.md`.
8. `submission/` package (PDF, source bundle, checklist artifacts).

## Agent Topology (22 Roles, Rolling Concurrency)
Use rolling orchestration (thread-safe, no dangling tasks), with each agent writing to `paper/ieee_tro_robotics_maze/coordination/agent_reports/`.

| Agent Group | Count | Responsibility |
|---|---:|---|
| Orchestrator/Supervisor | 1 | Task routing, dependency ordering, completion matrix |
| Literature Researchers | 5 | Find and screen 2021+ papers for planning, navigation, benchmarking, reproducibility |
| Citation Verifiers | 2 | DOI/venue/year verification, dedupe, peer-review ratio enforcement |
| Methods Writers | 2 | System architecture, planner taxonomy, implementation details |
| Math Agents | 2 | Complexity notation, optimization formulations, algorithm pseudocode consistency |
| Results/Analysis Writers | 2 | Benchmark interpretation, limitations, threat-to-validity |
| Figure/Table Agents | 3 | Figure extraction, redraw, caption quality, table consistency |
| Reproducibility/Verifier Agents | 2 | Claim-to-evidence map, reproducibility appendix, artifact checks |
| Reviewer Agents (journal-style) | 3 | Major/minor comments from novelty, methods, and rigor perspectives |
| Critic/Rebuttal Agents | 2 | Consolidate critique, propose revisions, track resolved vs unresolved |

## Manuscript Structure (Decision-Complete)
Use this exact section spine:
1. Abstract.
2. Introduction and contributions.
3. Related work (2021+ only).
4. System architecture and implementation details.
5. Planner set and mathematical formulation.
6. Experimental protocol and benchmark design.
7. Results and comparative analysis.
8. Limitations and threats to validity.
9. Future implementation roadmap with aggressive hypotheses.
10. Conclusion.
11. Reproducibility appendix.
12. Reviewer-response appendix (internal cycle artifact).

## Aggressive Speculation Policy (Locked)
Aggressive speculation is allowed only in a dedicated section:
- Title: “Forward-Looking Hypotheses and High-Risk Directions”.
- Must use explicit labels: `Hypothesis`, `Rationale`, `Expected Benefit`, `Validation Plan`, `Risk`.
- Must not include fabricated empirical numbers.
- Must not be mixed into “Results” phrasing.

## Literature and Citation Pipeline
1. Seed from current repo research docs (`post_2021_methods.md`, `sota_planners_2021_plus.md`) to initialize a candidate list.
2. Expand to >=60 candidate papers, then filter to >=40 final citations.
3. Enforce hard checks:
   - Year >= 2021 for every entry.
   - >=80% peer-reviewed journal/conference.
   - <=20% preprint/tech report.
   - No duplicate DOI/title.
4. Build final `references.bib` from verified identifiers only.
5. Maintain `citations_audit.csv` with status fields for provenance.

## Important Interfaces / Artifacts (Public Project Interfaces)
These are required machine-readable interfaces for downstream agents:
1. `coordination/claims_traceability.csv`
   - Columns: `claim_id, claim_text, section, evidence_file, evidence_locator, evidence_type, status`.
2. `coordination/citations_audit.csv`
   - Columns: `cite_key, title, year, venue, peer_reviewed, doi_or_url, verification_status, included`.
3. `coordination/review_comment_log.csv`
   - Columns: `round, reviewer_role, severity, location, comment, owner_agent, resolution_status`.
4. `coordination/figure_manifest.csv`
   - Columns: `figure_id, source_path, generation_method, caption_status, section, reproducible`.
5. `coordination/paper_status.md`
   - Live gate summary: bibliography, build, claims, review resolution.

## Execution Phases (for Implementing Agent)
1. **Bootstrap**: initialize IEEE journal paper scaffold and coordination files.
2. **Evidence Harvest**: pull implemented facts from repo benchmark/results/coordination artifacts into traceability table.
3. **Literature Expansion**: build 2021+ corpus and run citation audits to lock final 40+ set.
4. **Draft Pass A**: write full sections with placeholders only where explicitly allowed.
5. **Math/Method Pass**: formalize notation, complexity statements, and pseudocode consistency.
6. **Figure/Table Pass**: produce publication-quality figures and quantitative tables with reproducible provenance.
7. **Internal Review Round 1**: journal-style reviewer comments (major/minor).
8. **Revision Round 1**: resolve all major comments; log each resolution.
9. **Internal Review Round 2**: second reviewer cycle with stricter acceptance gates.
10. **Submission Packaging**: build PDF, source bundle, appendices, and final audit report.

## Quality Gates and Test Scenarios
1. **Build Gate**: `latexmk` build succeeds; PDF generated; no missing bibliography keys.
2. **Citation Gate**: `references.bib` has >=40 entries; all entries year >=2021; peer-reviewed ratio >=80%.
3. **Claims Gate**: every contribution claim has a traceability row linking to concrete evidence.
4. **Figure Gate**: every figure referenced in text exists, has caption, and appears in manifest.
5. **Review Gate**: zero unresolved “major” review comments before final packaging.
6. **Integrity Gate**: no fabricated results; speculative content confined to dedicated future-work section.

## Acceptance Criteria
- Full IEEE-style LaTeX manuscript compiles successfully.
- 40+ verified references, all 2021+, with strict quality mix satisfied.
- Implemented vs not-yet-implemented content is clearly separated and correctly labeled.
- Two internal reviewer rounds completed with resolution log.
- Final submission package includes manuscript, bibliography, appendices, and reviewer-response artifact.

## Assumptions and Defaults
- Venue style: IEEE journal template tuned for T-RO expectations.
- Paper framing: System + Benchmark Study.
- Evidence source: current repository outputs plus gap analysis.
- Authorship: Cesar as primary author; remaining coauthors as placeholders.
- Speculation mode: aggressive but explicitly labeled hypotheses only, no fabricated empirical outcomes.
- Tooling availability: TeX toolchain (`latexmk`, `pdflatex`, `biber`, `bibtex`) is present and usable.
