# Bibliography + Related Work Lead Report

## Scope
Owned files updated:
- `paper/ieee_tro_robotics_maze/references.bib`
- `paper/ieee_tro_robotics_maze/coordination/citations_audit.csv`
- `paper/ieee_tro_robotics_maze/sections/03_related_work.tex`
- `paper/ieee_tro_robotics_maze/sections/02_introduction.tex`
- `paper/ieee_tro_robotics_maze/sections/04_method.tex`

## 1) Merge + Dedupe Result
Input pools:
- `lit_pool_1.bib`: 35 entries
- `lit_pool_2.bib`: 36 entries
- Raw total: 71 entries

Dedupe policy:
- Primary key: normalized DOI
- Fallback key: normalized title + year
- Keep first occurrence in pool order (`lit_pool_1` then `lit_pool_2`)

Dedupe outcome:
- Removed duplicates: 1 (duplicate DOI `10.1109/lra.2024.3511437`)
- Final merged entries in `references.bib`: **70**

Key-collision handling (distinct papers sharing same cite key):
- `Xiao_2022` (second distinct entry) renamed to `Xiao_2022_2`
- `Hu_2025` (second distinct entry) renamed to `Hu_2025_2`

## 2) Constraint Compliance
Hard constraints:
- Minimum entries >= 40: **PASS** (`70`)
- Every entry year >= 2021: **PASS** (minimum year = `2021`)
- Peer-reviewed share >= 80%: **PASS** (`70/70 = 100.0%`)

Peer-reviewed heuristic used in audit CSV:
- `peer_reviewed=yes` when entry type is `article` or `inproceedings` (or `incollection`) and journal/booktitle exists.

Year distribution in merged bibliography:
- 2021: 13
- 2022: 19
- 2023: 16
- 2024: 13
- 2025: 9

## 3) citations_audit.csv Population
`coordination/citations_audit.csv` fully rebuilt from the included merged set.

Columns populated per row:
- `cite_key`
- `title`
- `year`
- `venue`
- `peer_reviewed`
- `doi_or_url`
- `verification_status` (`verified_doi` used when DOI present)
- `included` (`yes` for all retained entries)

Row totals:
- Total rows: 70
- `included=yes`: 70
- `peer_reviewed=yes`: 70

## 4) Related Work Drafting
`sections/03_related_work.tex` replaced from placeholder to full grouped synthesis with citations across:
- Surveys/taxonomies
- Single-robot planning + mapless RL navigation
- Multi-robot exploration/coordination
- Uncertainty/risk-aware planning
- Benchmarks and runtime frameworks

The section now positions this manuscript clearly as an infrastructure/reproducibility contribution rather than a new planner proposal.

## 5) Intro/Method Citation Compliance Fixes
### Introduction (`02_introduction.tex`)
Removed non-compliant/absent keys:
- `hart1968formal`
- `dijkstra1959note`
- `macenski2024smac`
- `coumans2019pybullet`
- `todorov2012mujoco`

Replaced with compliant 2021+ keys present in merged bibliography, including:
- `S_nchez_Ib_ez_2021`, `Karur_2021`, `Xiao_2022`, `Liu_2023`
- `Baumann_2021`, `He_2022`, `Chen_2024`, `Shcherbyna_2025`

### Method (`04_method.tex`)
- Added compliant benchmark references: `Heiden_2021`, `Chamzas_2022`, `Mayer_2024`.
- No pre-2021 citations remain.

## 6) Citation-Key Integrity Check
Audit across `02_introduction.tex`, `03_related_work.tex`, `04_method.tex`:
- Unique cited keys: 49
- Missing keys (used in sections but absent from `references.bib`): **0**
- Cited keys with year < 2021: **0**

Status: **All requested bibliography and citation compliance checks are satisfied.**

## 7) Build Verification
- Ran `latexmk -C` followed by `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
- Final build completed and emitted `main.pdf`.
- Citation warnings observed during intermediate passes were resolved after BibTeX regeneration.
