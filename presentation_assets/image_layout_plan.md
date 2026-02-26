# Image Layout Plan (42-slide deck)

## Readability and Aesthetic Guardrails
- Keep text primary on dense slides: minimum `55%` text area, maximum `45%` image area.
- Use one primary image per slide; only add a secondary visual if it is a small logo/icon (`<=12%` slide width).
- Prefer diagrams/logos for technical slides (7-38); reserve photographic imagery for the robotics section (39-42).
- Use consistent framing on 16:9 (`1920x1080`): safe margins `L/R 120`, `Top 72`, `Bottom 64`.
- For text-over-image slides, apply dark overlay `#0E1A2B` at `18-24%` opacity.

## Master Placement Templates
- `T1 Full-bleed hero`: image `1920x1080`; title block in left third; overlay enabled.
- `T2 60/40 split`: text frame `x120 y160 w1000 h800`; image frame `x1152 y160 w648 h800`.
- `T3 Top band + body`: image band `x120 y180 w1680 h280`; body content below at `y500+`.
- `T4 Center diagram`: diagram frame `x240 y210 w1440 h620`; supporting bullets below/right.
- `T5 Icon rail`: no large image; 1-5 logos/icons in lower or right rail (`96-140 px` each).

## Slide-Range Image Plan

| Slides | Content focus | Placement template | Image density target | Asset direction |
|---|---|---|---|---|
| 1-3 | Title, event scope, agenda | `1: T1`, `2: T2`, `3: T5` | 2 visual-heavy, 1 text-heavy | Use `custom/mcp_mesh.svg` on slide 1 (watermark style), `custom/planning_loop.svg` on slide 2 right panel, logo rail on slide 3 (`openai`, `github`, `git`, `python`). |
| 4-6 | Why now, definition, reference architecture | `4: T3`, `5: T2`, `6: T4` | Balanced | Slide 4 gets a narrow conceptual banner; slide 5 uses `custom/planning_loop.svg`; slide 6 uses a large architecture diagram (no photo). |
| 7-12 | Tool landscape and comparisons | `7: T5`, `8-11: T2`, `12: T5` | Mostly text-forward | Use product logo-led visuals only: `openai`, `github`, `nodedotjs`; one large logo in right panel for slides 8-11, comparison logos as headers on slide 12. |
| 13-16 | Planning mode, pricing, local models | `13: T2`, `14: T2`, `15: T5`, `16: T2` | Text-heavy | Keep pricing slide (15) mostly table with small logos. For 16, use schematic/diagram style rather than photography. |
| 17-20 | Role split and orchestration mechanics | `17: T4`, `18: T4`, `19: T2`, `20: T4` | Diagram-heavy | Use flow/tree diagrams as primary visuals; optional `W1` notation element on 17 and `custom/mcp_mesh.svg` accent on 18-19. |
| 21-30 | Skills + skill spotlights | `21-22: T2/T4`, `23-30: T2` (repeated pattern) | Consistent rhythm | Keep a repeated skill-card visual on right side for slides 23-30 to reduce visual drift. Map icons per skill (see section below). |
| 31-33 | AGENTS.md + MCP trust/safety | `31: T4`, `32: T2`, `33: T2` | Text + governance diagrams | Slide 32 should prominently use `custom/mcp_mesh.svg`; slide 33 uses control/safety icon cards (no photos). |
| 34-38 | Live workflow, debug/testing/research loops | `34: T3`, `35: T4`, `36-38: T2/T4` | Diagram-forward | Use workflow diagrams (`W2`, `W6`) and loop visuals; avoid decorative photos to preserve legibility. |
| 39-42 | Robotics, risk/reward, close | `39: T2`, `40: split risk/reward`, `41: T2`, `42: T1` | Visual-heavy finale | Introduce robotics photos here only: `R2/R3` on 39, `R1 + R6` split on 40, subtle `R7` watermark on 42 close slide. |

## Skill Spotlight Icon Mapping (Slides 23-30)
- Slide 23 (`create-plan`): `custom/planning_loop.svg` in right panel.
- Slide 24 (`github-agents-deploy`): `tooling_logos/github.svg` + `tooling_logos/git.svg`.
- Slide 25 (`openai-docs`): `tooling_logos/openai.svg`.
- Slide 26 (`suggest-improve`): `tooling_logos/python.svg` + checklist-style diagram.
- Slide 27 (`playwright`): `tooling_logos/nodedotjs.svg` + browser-flow mini diagram.
- Slide 28 (`literature-review`): document/search pipeline diagram (native vector, not photo).
- Slide 29 (`scientific-report-editor`): draft-review-publish loop diagram (native vector).
- Slide 30 (`pr-merger`): `tooling_logos/github.svg` + merge flow arrow.

## High-Impact External Image Slots (from `image_manifest_extra.md`)
- Slide 17: `W1` (small notation inset only, avoid full-slide complexity).
- Slide 34: `W2` (top-band crop) for end-to-end workflow context.
- Slide 36: `W6` as the main debug loop visual.
- Slide 39: `R2` (or `R3`) as contextual robotics anchor.
- Slide 40: `R1` (reward/industrial scale) + `R6` (risk/field constraints) in a 50/50 split.
- Slide 42: `R7` faint background watermark behind closing message.

## Final Balance Check Before Export
- No more than two consecutive full-image slides.
- At least one low-image recovery slide every 3-4 slides in dense sections (7-33).
- Keep all captions/attributions in a consistent footer lane; do not overlap body text.
- If a diagram is hard to read at presentation distance, crop tighter or replace with simplified redraw.
