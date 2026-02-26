# Deck Execution Runbook

Deck: `agents.pptx`  
Audience: engineering and technical leadership  
Target duration: 60 minutes talk + 10-15 minutes Q&A  
Last updated: 2026-02-26

## 1) Presenter Intent

- Deliver a practical, evidence-backed workflow, not a tool promo.
- Keep one core throughline: role clarity + checkpoints + artifacts.
- Treat live demos as optional acceleration, not a single point of failure.

## 2) Preflight Checklist (T-30 to T-5)

### T-30 to T-20: Environment
- Confirm `agents.pptx` opens locally and in presenter mode.
- Disable notifications on presenting machine.
- Set display scaling to avoid font/layout shifts.
- Keep a second desktop/space with terminal + fallback artifacts open.

### T-20 to T-10: Demo Readiness
- In repo root, run baseline smoke validation:
  - `bash scripts/run_repo_smoke.sh`
- Confirm smoke output includes:
  - `deck_slides=41 mapped_images=41`
  - `robotics_smoke=ok planners_checked=2 mazes_checked=3`
- Keep these artifacts already open in tabs/windows:
  - `robotics_maze/results/benchmark_summary.md`
  - `robotics_maze/testing/TEST_RUN_LOG.md`
  - `robotics_maze/testing/reports/screenshot_analysis.md`
  - `robotics_maze/coordination/session_event_log.csv`
  - `agents_factual_risk_audit.md`

### T-10 to T-5: Room/Flow
- Execute the final QA command flow in Section 3 and record pass/fail plus timestamp.
- Start a visible countdown timer for yourself.
- Confirm microphone, clicker, and HDMI reliability.
- Decide in advance whether to run full live demo or fallback-first mode.

## 3) Final QA Flow (Repeatable Commands)

Run from repo root. Do not present if any gate fails.

### Gate 1: Structural + Coverage Smoke
```bash
bash scripts/run_repo_smoke.sh
```
Pass criteria:
- Script exits with `0`.
- Output includes `[smoke] PASS`.

### Gate 2: In-deck Image + Reference Footer Presence
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

print(f"slides={len(prs.slides)}")
print(f"missing_images={missing_images}")
print(f"missing_reference_footers={missing_refs}")
PY
```
Pass criteria:
- `missing_images=[]`
- `missing_reference_footers=[]`

### Gate 3: Reference Link Audit Artifact
```bash
awk -F '\t' 'NR==1 || $4 != "true" {print $0}' presentation_assets/link_audit_final.tsv
awk -F '\t' 'NR>1 && $4 != "true" {print $0}' presentation_assets/link_audit_final.tsv | wc -l
```
Pass criteria:
- First command prints header only.
- Second command returns `0`.

### Gate 4: Factual-risk Hotspot Completeness
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
Pass criteria:
- `hotspot_ref_rows_not_equal_3=[]`
- `hotspot_missing_audit_sections=[]`

### Gate 5: Manual Factual Spot-check (Required)
- Re-open slides `4, 7, 10, 12, 13, 15, 33, 34, 39, 40`.
- Confirm each date-sensitive claim is explicitly framed as "as of Feb 26, 2026" or intentionally softened in speaker notes.
- If any claim has drifted from source pages, update references and rerun Gates 1-4.

## 4) Timing Plan (60 Minutes)

| Time | Slides | Goal | Delivery Notes |
|---|---:|---|---|
| 00:00-04:00 | 1-3 | Frame scope and agenda | Set expectations: practical patterns, real constraints, evidence. |
| 04:00-09:00 | 4-6 | Why now + architecture | Keep architecture narration left-to-right and concise. |
| 09:00-20:00 | 7-16 | Tool landscape + model routing | Anchor claims as "as of 2026-02-26" for date-sensitive content. |
| 20:00-28:00 | 17-21 | Role split + orchestration + skills concept | Emphasize contracts, handoffs, and audit artifacts. |
| 28:00-39:00 | 22-30 | Skill spotlights | Move briskly; pause only on workflows you actually use weekly. |
| 39:00-45:00 | 31-33 | Governance + MCP trust/safety | Reinforce approval gates and least privilege controls. |
| 45:00-53:00 | 34 | Live walkthrough | Timebox to 8 minutes max; do not debug deeply on stage. |
| 53:00-59:00 | 35-40 | Real workflow + robotics risk/reward | Keep this grounded with concrete constraints and failure modes. |
| 59:00-60:00 | 41 | Close | End on deterministic loop principle and transition to Q&A. |

### Compression Rules if Behind Time
- If >5 minutes behind by slide 22, skip detailed narration on slides 28-30.
- If >8 minutes behind by slide 31, run slide 34 in fallback mode (artifact walkthrough only).
- If >10 minutes behind by slide 35, summarize slides 39-40 in one minute and move to Q&A.

## 5) Demo Checkpoints

| Checkpoint | When | Pass Criteria | If Failed |
|---|---|---|---|
| CP1: Deck Integrity | Before slide 1 | Deck renders correctly, fonts/images stable | Switch to PDF export immediately. |
| CP2: Tooling Credibility | End slide 16 | You have terminal session + artifacts pre-opened | Commit to artifact-backed demo path before slide 34. |
| CP3: Live Demo Gate | Start slide 34 | Commands run within expected latency and outputs are readable | Abort live typing after one failed attempt; switch to prepared outputs. |
| CP4: Robotics Evidence | Slides 39-40 | You can show benchmark/test evidence in <30 seconds | Use pre-opened `benchmark_summary.md` and screenshot QA report. |

## 6) Failure Fallback Matrix

| Failure Mode | Immediate Pivot Line | Backup Asset/Action |
|---|---|---|
| Internet outage | "I will continue in offline evidence mode." | Use local markdown artifacts and deck only. |
| CLI/auth failure | "I will show the exact outputs captured earlier in this repo." | Open benchmark/test/report files directly. |
| Live command hangs | "I will timebox this and move to recorded outputs." | Stop command, show precomputed logs/results. |
| GitHub/MCP service unavailable | "The orchestration model remains the same; I will show local traces." | Use `session_event_log.csv` + coordination docs. |
| Simulation backend mismatch | "This environment may fall back to MuJoCo; results are still reproducible." | Show test log noting fallback behavior. |
| Deck rendering glitch | "Switching to visual-safe mode." | Present from PDF or alternate machine. |

## 7) Q&A Pivot Bank

Use this pattern: direct answer (20-30s), then pivot to evidence (slide/file), then invite a deeper follow-up.

- "Which agent is best overall?"
  - Pivot: There is no universal best; choose by governance needs, autonomy level, and edit style.
  - Evidence: slides 12, 17, 31-33.

- "How do you control hallucination risk?"
  - Pivot: Use role contracts, independent review, and artifact-based verification before merge/release.
  - Evidence: slides 17, 20, 31, 36-37.

- "Is this too expensive at scale?"
  - Pivot: Cost is controlled via model routing and role-based tiering.
  - Evidence: slides 13, 15.

- "What if tools/APIs change quickly?"
  - Pivot: Timestamp claims, keep a factual risk audit, and revalidate date-sensitive slides before each delivery.
  - Evidence: slide 7, slide 15, `agents_factual_risk_audit.md`.

- "How do we adopt this next week with a small team?"
  - Pivot: Start with planner/implementer/reviewer split and one enforced checkpoint per PR.
  - Evidence: slides 17, 20, 30.

- "Can this work in safety-critical robotics?"
  - Pivot: Only with staged autonomy, strict approval gates, and conservative rollout from sim to real.
  - Evidence: slides 39-40, 33.

## 8) Presenter Command Card (Optional Live Use)

```bash
# Repo root
python3 scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7
pixi run benchmark
```

If either command fails once on stage, switch to artifacts and continue. Do not debug live beyond 60-90 seconds.

## 9) Post-Talk Capture (5 Minutes)

- Save ad-hoc questions and objections raised in Q&A.
- Mark which fallback paths were used and why.
- Update this runbook + speaker notes before next delivery.
