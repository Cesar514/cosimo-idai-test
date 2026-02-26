# Image Layout Plan (42-slide deck, frontend-design revision)

## Visual Direction: Kinetic Blueprint Editorial
- Core look: clean technical canvases with bold, directional diagram energy.
- Memory hook: diagonal signal traces and layered translucent cards, not generic stock photos.
- Accent discipline: keep imagery mostly in `accent.primary` + one secondary accent (`accent.secondary` or `accent.warm`) per slide.
- Texture policy: subtle grain/noise (`4-6%`) only on hero and divider slides to avoid flat backgrounds.

## Hard Guardrails (Readability First)
- Text-safe area: keep all body text inside `x120..1100` on split slides and `x120..1800` on full-width text slides.
- Image-safe area: do not place critical visual detail within 48 px of image frame edges.
- Dense technical sections (slides 7-38): maintain minimum `58%` text footprint.
- Hero/finale sections (slides 1-3, 39-42): image area can expand to `55-65%`.
- Text-over-image overlay: `#0E1A2B` at `18-24%` for light scenes, `12-16%` for dark scenes.
- Maximum one dominant visual per slide; secondary visuals must be icon-scale only (`<=12%` width).

## Placement Templates v2 (1920x1080)

| Template | Layout intent | Coordinates |
|---|---|---|
| `T1 Hero Offset` | Big visual with anchored headline | Image `x0 y0 w1920 h1080`; text block `x120 y132 w860 h700` |
| `T2 Editorial Split 60/40` | Text left, visual right with generous gutter | Text `x120 y160 w1000 h800`; image `x1152 y150 w648 h820` |
| `T3 Signal Band` | Thin cinematic strip plus dense body | Band `x120 y170 w1680 h260`; body starts `y480` |
| `T4 Diagram Stage` | System map central with supporting copy | Diagram `x220 y200 w1480 h620`; notes `x220 y845 w1480 h160` |
| `T5 Icon Rail` | Logo/icon rhythm without heavy imagery | Rail zone `x1280 y200 w520 h640`; icons `96-140 px` |
| `T6 Dual Card Cascade` | Two visual cards at different vertical levels | Card A `x1030 y170 w710 h360`; Card B `x1140 y560 w600 h300` |
| `T7 Risk/Reward Diptych` | Equal split for contrast narratives | Left `x120 y180 w810 h760`; Right `x990 y180 w810 h760` |
| `T8 Watermark Close` | Soft background motif behind final message | Watermark `x900 y120 w920 h840` at `10-16%` opacity |

## Slide-by-Slide Imagery and Placement

| Slide | Narrative focus | Template | Primary visual | Placement and crop notes |
|---|---|---|---|---|
| 1 | Title / opening claim | `T1` | `custom/mcp_mesh.svg` + `C01` texture | Scale mesh to `132%`, center-right bias, keep central node off headline area. |
| 2 | Event scope | `T2` | `custom/planning_loop.svg` | Use right panel with top-right crop; leave ring center visible for quick recognition. |
| 3 | Agenda | `T5` | `openai`, `github`, `git`, `python` logos | Place as vertical rail with alternating card fills (`bg.card`/`bg.canvas`) for visual cadence. |
| 4 | Why now | `T3` | `C11` data-flow ribbon | Use high-contrast top band only; no full-frame image on this slide. |
| 5 | Definition framing | `T2` | `C02` orchestration lanes | Keep lanes simplified to three bands, arrows angled 12-15 degrees for motion feel. |
| 6 | Reference architecture | `T4` | `C02` orchestration lanes (expanded) | Center large architecture diagram, labels outside path intersections for legibility. |
| 7 | Tool landscape intro | `T5` | Brand icon rail (`openai`, `github`, `nodedotjs`) | Intro slide stays text-led; icons as supporting right rail only. |
| 8 | Tool comparison A | `T2` | `openai` logo card + subtle mesh background | Right panel card with low-opacity mesh behind logo (`8-10%`). |
| 9 | Tool comparison B | `T2` | `github` logo card | Use monochrome card with a single `accent.primary` keyline. |
| 10 | Tool comparison C | `T2` | `nodedotjs` logo card | Keep card background light and avoid extra decorative elements. |
| 11 | Tool comparison D | `T2` | `docker` or `kubernetes` logo card | Use same card geometry as slides 8-10 for rhythm consistency. |
| 12 | Comparison synthesis | `T5` | `C10` icon badge set | Build compact matrix of 4-6 badges aligned to category headings. |
| 13 | Planning mode | `T2` | `custom/planning_loop.svg` + `C03` inset | Loop as main visual, with one small step-card inset for phase labels. |
| 14 | Pricing model | `T5` | Lightweight logo chips only | Keep imagery minimal; emphasize table and numbers. |
| 15 | Local models | `T2` | `C03` skill/model card scaffold | Right card stack with clear hierarchy; no photos. |
| 16 | Runtime topology | `T4` | `C02` topology variant | Show host/local/cloud nodes as rounded cards linked by directional edges. |
| 17 | Role split | `T4` | `W1` BPMN inset + `C02` lanes | BPMN used as small legend tile in top-right, not the main diagram. |
| 18 | Orchestration mechanics | `T4` | `W2` workflow (tight crop) | Crop to 2-3 key swimlanes and redraw labels at deck typography scale. |
| 19 | Handoff rules | `T2` | `W3` SIPOC-inspired card | Convert to simplified vector look; remove unnecessary chart chrome. |
| 20 | Escalation paths | `T4` | `W4` value-stream decomposition | Keep one highlighted path in `accent.warm` for “critical escalation.” |
| 21 | Skills architecture | `T2` | `C03` card scaffold | Reusable skill card motif starts here and persists through slide 30. |
| 22 | Skill taxonomy | `T4` | `W5`-style simplified map | Reduce to one central flow with three branches; avoid dense map text. |
| 23 | Skill spotlight: create-plan | `T2` | `custom/planning_loop.svg` | Right panel, lower-half crop to keep arrowheads visible near slide center. |
| 24 | Skill spotlight: github-agents-deploy | `T2` | `github` + `git` + `C07` arrows | Two icon cards with one merge-flow arrow layer behind. |
| 25 | Skill spotlight: openai-docs | `T2` | `openai` logo + `C06` doc pipeline | Keep doc pipeline very light (`line.default` strokes) behind logo chip. |
| 26 | Skill spotlight: suggest-improve | `T2` | `python` logo + checklist card | Emphasize before/after card comparison with a single accent highlight. |
| 27 | Skill spotlight: playwright | `T2` | `nodedotjs` + browser path mini-diagram | Keep browser path compact (`<=40%` of right panel height). |
| 28 | Skill spotlight: literature-review | `T2` | `C06` research pipeline | Three-stage visual: search -> screen -> synthesize. |
| 29 | Skill spotlight: scientific-report-editor | `T2` | `C06` publish loop variant | Use loop with document, review, and camera/checkpoint nodes. |
| 30 | Skill spotlight: pr-merger | `T2` | `github` + `C07` merge gate | Right panel merge gate with one bold “approved” branch in primary accent. |
| 31 | AGENTS.md governance | `T4` | `C04` trust boundary gate | Place gate centrally with short policy labels around perimeter. |
| 32 | MCP trust model | `T2` | `custom/mcp_mesh.svg` + `C04` overlay | Mesh at right; add shield/gate overlay at lower-right quadrant. |
| 33 | Safety controls | `T2` | `C04` control cards | Use three stacked control cards (auth, policy, audit). |
| 34 | Live workflow overview | `T3` | `W2` top-band crop + `C11` accents | Use W2 strip in top band, keep body text dominant. |
| 35 | Debug/test loop | `T4` | `C05` debug feedback loop | Central loop with three checkpoints: detect, isolate, verify. |
| 36 | Research loop | `T2` | `W6` + `C06` hybrid | W6 loop on right with lightweight doc/search icons at loop nodes. |
| 37 | Iteration rhythm | `T4` | `C05` loop variant | Show timeboxed loop phases with clockwise priority markers. |
| 38 | Deploy and observe | `T2` | `C07` merge-to-monitor path | Use one path from PR merge to production monitor card. |
| 39 | Robotics section opener | `T2` | `R2` (fallback `R3`) | Crop to arm silhouette on right; overlay at `16-18%` for text contrast. |
| 40 | Risk vs reward | `T7` | `R1` left + `R6` right | Left side cooler grade for reward, right side warmer/desaturated for risk. |
| 41 | Practical takeaway | `T2` | `custom/robotics_arm.svg` + soft `R7` inset | Keep illustration dominant; `R7` only as faint secondary watermark. |
| 42 | Closing / call to action | `T8` | `R7` watermark + `C08` horizon matte | Large faint watermark on right; leave left two-thirds clean for closing text. |

## Rhythm and Recovery Checks
- Never run more than two visually heavy slides in sequence.
- Keep recovery slides at 7, 12, 14, 21, 33 where visuals are intentionally lighter.
- In slides 23-30, keep right-panel visual geometry identical and only swap iconography/content.
- In slides 39-42, progressively increase image scale and reduce annotation density toward the close.

## Attribution Lane
- Reserve footer lane `y1028..1068` for source/credit text on any slide using `R*` or `W*` assets.
- Use compact format: `Title - Author - Source - License`.
- For CC BY-SA assets modified in-slide, mark derivative note in speaker notes.
