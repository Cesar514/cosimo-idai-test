# GitHub Issue Templates - Reference Verification

This file provides ready-to-post issue bodies for reference verification work split by publication date.

## Template 1: Post-2021 Reference Verification

**Issue Title**

`[Research][Refs][Post-2021] Verify and curate >=20 references for planner claims (2021+)`

**Issue Body (copy/paste)**

```md
## Summary
Verify and curate the post-2021 (2021 and newer) literature backing our maze/mobile-robot planning claims, then update repository research notes with trustworthy citations.

## Context
- Primary working file: `robotics_maze/research/sota_planners_2021_plus.md`
- Related context files: `robotics_maze/research/R10_alt_methods_sota.md`, `robotics_maze/src/alt_planners/`
- We need current, high-quality references that support algorithm choices and ranking claims.

## Scope
- Include only references with publication year >= 2021.
- Cover diverse source types: peer-reviewed papers, conference proceedings, journals, and authoritative project docs where relevant.
- Validate metadata for each reference: title, authors, year, venue/source, URL/DOI, and claim supported.

## Required Deliverables
- A vetted list of at least 20 post-2021 references.
- A short evidence table mapping each reference to at least one repository claim it supports.
- A `Justification` section written as exactly 4 sentences explaining why this post-2021 set is sufficient, credible, and relevant.
- A summary of dropped/rejected references with concise reasons (duplicate, weak source, outdated claim fit, broken link, etc.).

## Execution Checklist
- [ ] Collected candidate references from scholarly and authoritative sources.
- [ ] Removed duplicates and low-quality/non-verifiable sources.
- [ ] Confirmed year filter (>= 2021) for every retained reference.
- [ ] Verified each URL/DOI is reachable at time of check.
- [ ] Linked every retained reference to at least one concrete claim in our research notes.
- [ ] Added exactly 4-sentence `Justification` section.

## Acceptance Criteria
- [ ] Retained reference count is >= 20.
- [ ] All retained references are post-2021.
- [ ] Every retained reference includes complete bibliographic metadata and a working link/DOI.
- [ ] The `Justification` section has exactly 4 sentences.
- [ ] Output is committed to repository markdown files under `robotics_maze/research/`.
```

## Template 2: Pre-2021 Reference Verification

**Issue Title**

`[Research][Refs][Pre-2021] Verify and curate >=20 foundational references for planner baseline claims`

**Issue Body (copy/paste)**

```md
## Summary
Verify and curate foundational pre-2021 references that support baseline planner concepts, historical context, and canonical algorithm claims used in this repository.

## Context
- Primary context files: `robotics_maze/research/R1_weighted_astar.md` through `R10_alt_methods_sota.md`
- Supporting code context: `robotics_maze/src/alt_planners/`
- We need a strong historical/reference backbone for classical methods and baseline comparisons.

## Scope
- Include only references with publication year < 2021.
- Prioritize canonical and widely cited works for A*, D* Lite, LPA*, IDA*, BFS variants, and related planning baselines.
- Validate metadata for each reference: title, authors, year, venue/source, URL/DOI, and claim supported.

## Required Deliverables
- A vetted list of at least 20 pre-2021 references.
- A claim-to-reference mapping table showing which baseline assertion each citation supports.
- A `Justification` section written as exactly 4 sentences explaining why this pre-2021 set is sufficient, credible, and historically representative.
- A short note on any expected canonical references that were excluded and why.

## Execution Checklist
- [ ] Collected foundational references from trusted archives, proceedings, journals, and official docs.
- [ ] Removed duplicates, unverifiable citations, and weak secondary sources.
- [ ] Confirmed year filter (< 2021) for every retained reference.
- [ ] Verified each URL/DOI is reachable at time of check.
- [ ] Linked every retained reference to at least one specific baseline claim.
- [ ] Added exactly 4-sentence `Justification` section.

## Acceptance Criteria
- [ ] Retained reference count is >= 20.
- [ ] All retained references are pre-2021.
- [ ] Every retained reference includes complete bibliographic metadata and a working link/DOI.
- [ ] The `Justification` section has exactly 4 sentences.
- [ ] Output is committed to repository markdown files under `robotics_maze/research/`.
```
