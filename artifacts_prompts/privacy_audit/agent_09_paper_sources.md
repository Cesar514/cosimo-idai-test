# Privacy Audit Report: `paper/ieee_tro_robotics_maze/` Manuscript Sources

## Scope
- Audited sources:
  - `paper/ieee_tro_robotics_maze/main.tex`
  - `paper/ieee_tro_robotics_maze/sections/*.tex`
  - `paper/ieee_tro_robotics_maze/tables/*.tex`
  - `paper/ieee_tro_robotics_maze/appendix/*.tex`
  - `paper/ieee_tro_robotics_maze/references.bib`
  - `paper/ieee_tro_robotics_maze/figures/*.png` (metadata/embedded-text check)
- Focus:
  - Private identity leakage
  - Absolute/local filesystem path leakage
  - Secrets/credential-like leakage
  - Caption-level leakage in manuscript figures/tables
- Constraints followed:
  - No manuscript source files modified.

## Method
- Pattern scans across scoped `.tex` and `.bib` files for:
  - emails/contacts, ORCID, phone/address-like markers
  - credential patterns (`token`, `secret`, `password`, API key signatures)
  - absolute paths (`/Users/...`, `/home/...`, Windows drive paths, localhost)
- Focused extraction of path-like `\texttt{.../...}` references.
- Caption review (`\caption{...}`) for private/path leakage.
- Figure checks:
  - metadata review via `sips -g all`
  - embedded-string scan via `strings` + pattern matching.

## Findings

### 1. Explicit personal identity + location in author block
- **Location:** `paper/ieee_tro_robotics_maze/main.tex:16-17`
- **Content:** author full name and geographic location (`California, USA`).
- **Risk:** **Low-to-Medium** (context dependent).
  - Low risk for camera-ready publication.
  - Medium risk if this draft is expected to be anonymized (double-blind).

### 2. Repository-internal relative path disclosure throughout manuscript text
- **Representative locations:**
  - `paper/ieee_tro_robotics_maze/sections/02_introduction.tex:4,6`
  - `paper/ieee_tro_robotics_maze/sections/04_method.tex:3,5,6,24,36`
  - `paper/ieee_tro_robotics_maze/sections/05_experiments.tex:11,26,30,31,55,58`
  - `paper/ieee_tro_robotics_maze/tables/experiment_protocol_table.tex:10`
  - `paper/ieee_tro_robotics_maze/appendix/reproducibility_checklist.tex:11-21`
- **Observed pattern:** repository-relative references such as `robotics_maze/src/...`, `robotics_maze/results/...`, `coordination/...`, `scripts/...`, `testing/...`.
- **Risk:** **Low**.
  - No host/user absolute paths found.
  - This is mostly intentional reproducibility traceability, but it does expose internal project layout and coordination artifact names.

### 3. Captions are clean for private/path leakage
- Reviewed figure/table captions in sections, tables, and appendix.
- No caption includes:
  - user-home absolute paths
  - credentials/tokens
  - emails/contact details

### 4. Bibliography links are public DOI links only
- `references.bib` contains URL fields pointing to `http://dx.doi.org/...` entries.
- No local-file fields (`file={...}`), no reference-manager local metadata, and no contact credentials observed.
- **Risk:** **None/expected** for scholarly bibliography metadata.

### 5. Figure files: no meaningful private metadata found
- `sips -g all` surfaced standard image properties (dimensions, color space, format), no author/comment fields.
- No convincing credential/path/identity strings found in PNG embedded-text checks.
- **Risk:** **Low/none detected**.

## Negative Checks (what was *not* found)
- Emails in scoped manuscript text/bib: **0**
- Credential/token/password/API-key signatures: **0**
- Absolute local filesystem paths in manuscript text/bib (`/Users`, `/home`, `C:\\...`, `localhost`): **0**
- Non-DOI external links (e.g., GitHub/Drive/Slack): **0** in scoped manuscript sources

## Risk Assessment
- Overall: **Low**.
- Main actionable concern is contextual: author/location disclosure may conflict with anonymized-review requirements, depending on submission stage.

## Recommendations
- If this is for double-blind review, remove or anonymize `main.tex:16-17` identity/location line.
- If minimizing internal structure exposure is desired, reduce `coordination/...` references in manuscript-visible text (especially appendix checklist evidence columns).
- Keep current practice of avoiding absolute user paths and credentials.

## Final Verdict
- **Pass with minor hygiene notes**: no secrets or absolute local path leakage detected; only intentional identity and repository-structure disclosures were found.
