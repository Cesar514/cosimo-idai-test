# Deck QA Checklist (41 Slides)

Deck: `agents.pptx`  
Deck size baseline: `41` slides (as documented in `speaker_notes.md` on 2026-02-26)

## Pass/Fail Gates
- `Title consistency`: Every slide title matches the final outline text and casing pattern; intentional exceptions are explicitly approved.
- `Image presence`: Every slide has at least one visible, non-broken visual asset.
- `References footer`: Every slide has a footer citation band with three columns following `citation_style_spec.md`.
- `Factual-risk hotspots`: High/medium-risk claim slides are re-validated against primary sources and date-stamped.
- `Demo readiness`: Demo-critical slides have rehearsed flow, working commands, and fallback artifacts.

## Global Sign-off
- [ ] 41/41 slide titles checked against final outline.
- [ ] 41/41 slides have image(s) present and correctly positioned.
- [ ] 41/41 slides have references footer in correct format and contrast.
- [ ] All `High` factual-risk slides re-validated in the last 24 hours.
- [ ] Final QA command flow completed in sequence (no skipped gates).
- [ ] `scripts/run_repo_smoke.sh` exits `0` and prints `[smoke] PASS`.
- [ ] `link_audit_final.tsv` unresolved row count is `0`.
- [ ] Hotspot completeness check returns no reference/audit gaps.
- [ ] Full demo flow rehearsed once on target machine.
- [ ] Offline/backup path tested for every demo-critical step.

## Final QA Run Metadata
- QA owner:
- Run timestamp (local):
- Repo commit (optional):
- Result: `PASS` / `FAIL`
- Notes:

## Final QA Command Flow (Run in Order)

### Gate 1 - Structural + Coverage Smoke
- [ ] Run:
```bash
bash scripts/run_repo_smoke.sh
```
- [ ] Confirm output includes:
  - `deck_slides=41 mapped_images=41`
  - `[smoke] PASS`

### Gate 2 - In-deck Image + Reference Footer Presence
- [ ] Run:
```bash
python3 - <<'PY'
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Inches

prs = Presentation("agents.pptx")
footer_threshold = prs.slide_height - Inches(0.9)
missing_images = []
missing_refs = []

for index, slide in enumerate(prs.slides, start=1):
    has_picture = any(shape.shape_type == MSO_SHAPE_TYPE.PICTURE for shape in slide.shapes)
    if not has_picture:
        missing_images.append(index)

    has_footer_refs = False
    for shape in slide.shapes:
        if not getattr(shape, "has_text_frame", False) or not shape.has_text_frame:
            continue
        if shape.top < footer_threshold:
            continue
        text = (shape.text_frame.text or "").lower()
        if "http" in text or "refs:" in text:
            has_footer_refs = True
            break
    if not has_footer_refs:
        missing_refs.append(index)

print(f"missing_images={missing_images}")
print(f"missing_reference_footers={missing_refs}")
PY
```
- [ ] Confirm:
  - `missing_images=[]`
  - `missing_reference_footers=[]`

### Gate 3 - Reference Link Audit Artifact
- [ ] Run:
```bash
awk -F '\t' 'NR==1 || $4 != "true" {print $0}' presentation_assets/link_audit_final.tsv
awk -F '\t' 'NR>1 && $4 != "true" {print $0}' presentation_assets/link_audit_final.tsv | wc -l
```
- [ ] Confirm:
  - First command prints header only.
  - Second command prints `0`.

### Gate 4 - Factual-risk Hotspot Completeness
- [ ] Run:
```bash
python3 - <<'PY'
import json
from pathlib import Path

hotspots = [4, 7, 10, 12, 13, 15, 33, 34, 39, 40]
refs = json.loads(Path("presentation_assets/slide_references.json").read_text(encoding="utf-8"))
audit = Path("agents_factual_risk_audit.md").read_text(encoding="utf-8")

ref_issues = [(slide, len(refs.get(str(slide), []))) for slide in hotspots if len(refs.get(str(slide), [])) != 3]
missing_audit_sections = [slide for slide in hotspots if f"## Slide {slide}:" not in audit]

print(f"hotspot_ref_rows_not_equal_3={ref_issues}")
print(f"hotspot_missing_audit_sections={missing_audit_sections}")
PY
```
- [ ] Confirm:
  - `hotspot_ref_rows_not_equal_3=[]`
  - `hotspot_missing_audit_sections=[]`

### Gate 5 - Manual Factual Spot-check
- [ ] Re-open slides `4, 7, 10, 12, 13, 15, 33, 34, 39, 40`.
- [ ] Confirm date-sensitive claims are "as of Feb 26, 2026" (or softened wording).
- [ ] If any edit is needed, rerun Gates 1-4 before final sign-off.

## Per-slide QA Tracker
Legend: mark `Title`, `Image`, `Refs`, and `Demo` with `[x]` when complete.

| Slide | Title | Risk | Title | Image | Refs | Demo |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Multi-agentic Workflows | Low | [ ] | [ ] | [ ] | N/A |
| 2 | Event Details and Scope | Low | [ ] | [ ] | [ ] | N/A |
| 3 | Agenda (60 Minutes) | Low | [ ] | [ ] | [ ] | N/A |
| 4 | Why 2026 Is Different | High | [ ] | [ ] | [ ] | N/A |
| 5 | What Multi-agent Workflow Means | Medium | [ ] | [ ] | [ ] | N/A |
| 6 | Reference Architecture | Medium | [ ] | [ ] | [ ] | N/A |
| 7 | Tool Landscape (As of Feb 26, 2026) | High | [ ] | [ ] | [ ] | N/A |
| 8 | Codex CLI: High-Leverage Features | Medium | [ ] | [ ] | [ ] | N/A |
| 9 | GitHub Copilot Coding Agent | Medium | [ ] | [ ] | [ ] | N/A |
| 10 | Google Jules | High | [ ] | [ ] | [ ] | N/A |
| 11 | Gemini CLI in Multi-agent Stacks | Medium | [ ] | [ ] | [ ] | N/A |
| 12 | Codex vs Gemini CLI vs Claude: Choice Matters | High | [ ] | [ ] | [ ] | N/A |
| 13 | Using GPT-5.2 Pro (Why It Helps) | High | [ ] | [ ] | [ ] | N/A |
| 14 | Planning Mode: Codex and Gemini | Medium | [ ] | [ ] | [ ] | N/A |
| 15 | Subscription Prices Snapshot (US, Feb 26, 2026) | High | [ ] | [ ] | [ ] | N/A |
| 16 | Local Models: When and Why to Use Them | Medium | [ ] | [ ] | [ ] | N/A |
| 17 | Role Split: Planner vs Implementer vs Reviewer | Low | [ ] | [ ] | [ ] | N/A |
| 18 | Codex Spawn Tree: Agents, Subagents, Max Depth | Medium | [ ] | [ ] | [ ] | N/A |
| 19 | Codex Agent Types and Why This Is Marvelous | Low | [ ] | [ ] | [ ] | N/A |
| 20 | Hardcore Orchestration Pattern | Medium | [ ] | [ ] | [ ] | N/A |
| 21 | skills.md / SKILL.md Patterns | Low | [ ] | [ ] | [ ] | N/A |
| 22 | How to Create a Skill (skill-creator Workflow) | Low | [ ] | [ ] | [ ] | N/A |
| 23 | Skill Spotlight: create-plan | Low | [ ] | [ ] | [ ] | N/A |
| 24 | Skill Spotlight: github-agents-deploy | Medium | [ ] | [ ] | [ ] | N/A |
| 25 | Skill Spotlight: openai-docs | Medium | [ ] | [ ] | [ ] | N/A |
| 26 | Skill Spotlight: suggest-improve | Low | [ ] | [ ] | [ ] | N/A |
| 27 | Skill Spotlight: playwright | Medium | [ ] | [ ] | [ ] | N/A |
| 28 | Skill Spotlight: literature-review | Low | [ ] | [ ] | [ ] | N/A |
| 29 | Skill Spotlight: scientific-report-editor | Low | [ ] | [ ] | [ ] | N/A |
| 30 | Skill Spotlight: pr-merger | Low | [ ] | [ ] | [ ] | N/A |
| 31 | AGENTS.md as Behavioral Control Plane | Medium | [ ] | [ ] | [ ] | N/A |
| 32 | MCP Basics: Why It Matters | Medium | [ ] | [ ] | [ ] | N/A |
| 33 | MCP in Practice: Trust and Safety | High | [ ] | [ ] | [ ] | N/A |
| 34 | Live Walkthrough: Blank Repo to PoC | High | [ ] | [ ] | [ ] | [ ] |
| 35 | Cesar's Real Workflow (Control Loop) | Medium | [ ] | [ ] | [ ] | [ ] |
| 36 | Debug Loop with Agents | Medium | [ ] | [ ] | [ ] | [ ] |
| 37 | Testing Workflows with Agents | Medium | [ ] | [ ] | [ ] | [ ] |
| 38 | Research and Writing Workflows | Low | [ ] | [ ] | [ ] | N/A |
| 39 | Experimental Robotics: Real World as Tools | High | [ ] | [ ] | [ ] | [ ] |
| 40 | High Risk, High Reward in Robot Agent Systems | High | [ ] | [ ] | [ ] | [ ] |
| 41 | Ralph Wiggum Technique (Actual Definition) | Medium | [ ] | [ ] | [ ] | [ ] |

## Title Consistency Checks
- Confirm each title exactly matches the final order in `speaker_notes.md`.
- Keep punctuation and casing consistent (`Title Case` default, deliberate lowercase preserved where intended).
- Explicitly approve known intentional tone/style outliers before final export.

## Image Presence Checks
- Confirm every slide has at least one visible image/icon/diagram after final alignment.
- Check for broken links, empty placeholders, pixelated exports, and accidental cropping.
- Verify image-to-claim fit (visual supports the specific claim on the slide, not generic decoration).

## References Footer Checks
- Footer appears on all slides with top divider, three equal citation columns, and readable contrast.
- Use normalized URLs and truncate with middle ellipsis only when needed.
- If a slide has fewer than three sources, leave unused column(s) blank to preserve alignment.

## Factual-risk Hotspots (Must Re-validate)
- Slides `4, 7, 10, 12, 13, 15, 33, 34, 39, 40`.
- Re-check all “as-of” claims with explicit date labels (for example `Feb 26, 2026`).
- Verify pricing/product-tier claims on slide 15 against current public pricing pages on presentation day.
- Re-verify tool capability comparisons (slides 7, 10, 12, 13) against primary vendor docs.
- Re-verify safety/governance claims (slides 33, 39, 40) against primary frameworks/papers.

## Demo Readiness Checklist
- [ ] Demo machine environment verified (`repo`, dependencies, auth, network, display scaling).
- [ ] Command/script list finalized and copied to presenter notes.
- [ ] Dry run completed without edits on slides `34-37`.
- [ ] Robotics/video assets for slides `39-40` open locally with no buffering.
- [ ] Backup plan prepared: prerecorded run, static screenshots, and narration fallback.
- [ ] Recovery checkpoints defined (where to resume if a step fails live).
