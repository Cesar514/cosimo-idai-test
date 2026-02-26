# Reference Quality Upgrade Notes (Task 26/36)

Scope:
- Updated `presentation_assets/slide_references.json` for slides `1`-`41`.
- Preserved exactly `3` URLs per slide.
- Replaced weak/non-primary references where possible.

Primary-source upgrades applied:
- Replaced Wikimedia file-page links with stronger primary sources (official docs/specs/papers) across workflow, skills, testing, and robotics slides.
- Replaced `github.com/features/copilot` with GitHub Docs coding-agent documentation (slides `3`, `4`).
- Replaced `anthropic.com/news/model-context-protocol` with the MCP specification page (slide `4`).
- Replaced `chatgpt.com/plus/pricing` with OpenAI pricing (`openai.com/api/pricing`) and replaced Copilot plans marketing URL with GitHub Docs subscription-plans documentation (slide `15`).

New primary references introduced:
- Anthropic Claude Code docs: `https://docs.anthropic.com/en/docs/claude-code/overview` (slide `12`).
- OMG BPMN 2.0.2 spec: `https://www.omg.org/spec/BPMN/2.0.2/` (slide `17`).
- PubMed help documentation: `https://pubmed.ncbi.nlm.nih.gov/help/` (slide `28`).
- NIST AI RMF reused as safety/governance anchor where applicable (slide `33`, retained on `40`).

Quality checks:
- Verified all slide entries in `slide_references.json` still contain exactly three references.
- Confirmed removal of low-authority patterns targeted in this pass (`commons.wikimedia`, GitHub feature marketing links, Anthropic news link, `chatgpt.com/plus/pricing`).
- Deck reference file currently covers `41` slides (matching current deck order in `speaker_notes.md`).

## Link Reachability Audit (Task 19/36)

Audit method:
- Ran automated URL checks over all unique references in `presentation_assets/slide_references.json` using `curl -L` with browser-like headers.
- Stored detailed check output in `presentation_assets/link_audit_final.tsv`.

Findings before replacement:
- `3` OpenAI URLs returned `403` in this environment:
  - `https://platform.openai.com/docs/models`
  - `https://platform.openai.com/docs/api-reference/responses/retrieve`
  - `https://openai.com/api/pricing/`

Replacements applied:
- Slide `13`:
  - `https://platform.openai.com/docs/models` -> `https://developers.openai.com/docs/models/`
  - `https://platform.openai.com/docs/api-reference/responses/retrieve` -> `https://developers.openai.com/docs/api-reference/responses/get`
  - `https://openai.com/api/pricing/` -> `https://developers.openai.com/docs/pricing`
- Slide `15`:
  - `https://openai.com/api/pricing/` -> `https://developers.openai.com/docs/pricing`

Final result:
- `48/48` unique URLs are now reachable (`200`), `0` failures.

## Terminology Correction (Task 18/36)

Scope:
- Slide `41` narrative currently uses "Ralph Wiggum Technique (Actual Definition)".

Finding (as of Feb 26, 2026):
- "Ralph Wiggum technique" is in active community use (open-source tooling/docs), but it is an informal nickname, not a standard formal term in software engineering literature.
- For a factual, publication-safe narrative, use neutral terminology and treat "Ralph Wiggum" as an alias only.

Recommended replacement phrasing:
- Slide title: `Fresh-Context Agent Loop (Externalized State)`
- Optional subtitle: `Community alias: "Ralph Wiggum loop"`
- Narrative anchor: `Repeat a bounded agent run; persist state in files/git; accept progress only when quality gates pass.`

Reference set for the slide narrative:
- `https://www.gnu.org/software/bash/manual/html_node/Looping-Constructs`
- `https://git-scm.com/docs/git`
- `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets`
- `https://www.12factor.net/processes`

Community-term provenance (optional mention, not primary technical anchor):
- `https://github.com/vercel-labs/ralph-loop-agent`
- `https://wiggum.dev/concepts/the-loop/`

## References Auditor (Task 15/36) - 2026-02-26

Audit scope:
- Validated `presentation_assets/slide_references.json`.
- Confirmed slide coverage is contiguous from `1` to `41` with no missing keys.
- Confirmed every slide contains exactly `3` references.

Weak-citation flags (kept, but should be reviewed in a later hardening pass):
- Slides `5`, `37`, `39`, `40`: arXiv links are preprints, which are weaker than peer-reviewed or standards-body sources for factual claims.
- Slide `10`: `https://jules.google/docs/changelog/2025-10-03/` is a changelog entry and may age quickly.
- Slides `11`, `12`: `https://github.com/google-gemini/gemini-cli` is mutable repository documentation; versioned docs/releases are usually stronger citations.
- Slide `15`: `https://developers.google.com/program/plans-and-pricing` is a broad pricing page and may be indirect for product-specific claims.
- Slides `35`, `41`: `https://git-scm.com/docs/git` is top-level and broad; command-specific Git docs would be more precise.
