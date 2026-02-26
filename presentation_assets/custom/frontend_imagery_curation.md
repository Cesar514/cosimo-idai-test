# Frontend-Design Imagery Curation Pack

Purpose: provide high-quality, non-generic visual directions and prompt-ready concepts for slides that need custom diagrams/illustrations.

## Visual DNA
- Tone: technical editorial, confident, high-clarity.
- Composition: asymmetry, diagonal energy, layered translucent cards.
- Palette anchor: `#0B5FFF` primary, `#00A3A3` secondary, `#FF7A18` sparingly for risk/highlight.
- Rendering preference: clean vector or semi-vector illustration; avoid plastic 3D stock aesthetic.
- Background discipline: off-white or deep navy fields with subtle grain, never flat default gray.

## Concept Library (Prompt-Ready)

| ID | Target slides | Prompt seed | Composition notes | Export spec |
|---|---|---|---|---|
| `C01` | 1, 32 | `Abstract protocol mesh diagram, glowing node network, technical editorial style, clean vector gradients, off-white field, depth via layered translucent planes, no text labels.` | Keep one dominant center node and 6-8 satellites; leave left third visually quiet for title copy. | `SVG` preferred, plus `PNG 2400x1350` transparent variant. |
| `C02` | 5, 6, 16, 17 | `Planner-worker-reviewer orchestration map, three swimlanes, directional arrows, precise modern infographics, strong hierarchy, no clutter.` | Lanes should run left-to-right with 12-15 degree arrow accents; emphasize handoff points with ring nodes. | `SVG 1920x1080` with editable stroke layers. |
| `C03` | 13, 15, 21 | `Stacked capability cards for software skills, clean UI card system, technical presentation graphic, crisp icon placeholders.` | 3-4 cards max; card depths should step in Z-order from top-right to bottom-left. | `SVG` and flattened `PNG 1600x900`. |
| `C04` | 31, 32, 33 | `Trust boundary security gate illustration, policy shield, access checkpoints, audit trail nodes, minimal futuristic blueprint style.` | Central gate shape with three surrounding control cards (auth, policy, audit). | `SVG 1920x1080`, dark and light variants. |
| `C05` | 35, 37 | `Debug feedback loop diagram, detect isolate verify cycle, engineering ops visual, crisp arrows, timeline ticks.` | Clockwise loop with three major checkpoints and one metric ribbon at bottom. | `SVG`; optional `PNG 2000x1125`. |
| `C06` | 25, 28, 29, 36 | `Research to report pipeline, search screen synthesize publish, document-centric workflow diagram, clean editorial infographic.` | Use 4-stage horizontal flow; allow swap-in icons for docs/search/review/publish. | `SVG` with reusable icon symbols. |
| `C07` | 24, 30, 38 | `Pull request merge gate flow, branch to review to merge to monitor path, software delivery diagram, polished vector.` | Keep one “happy path” bold; supporting alternate path in lighter stroke. | `SVG 1920x1080` plus transparent branch-only export. |
| `C08` | 42 | `Robotics horizon matte backdrop, abstract robotic silhouette, atmospheric but restrained, suitable as closing slide watermark.` | Keep right-side weight; left two-thirds low-contrast and calm for final message. | `PNG 2400x1350` + optional `SVG` silhouette layer. |
| `C09` | 40 | `Risk and reward diptych, industrial robotics contrast, left optimistic production floor, right constrained field conditions, cinematic documentary tone.` | Frame as two equal panels with matching horizon lines for direct comparison. | `PNG 2400x1350`, center-safe crop tested. |
| `C10` | 12 | `Technical product badge set, monochrome icon plaques with one accent outline, presentation-ready consistency.` | Build 4-6 equal-size badges with identical corner radius and shadow weight. | `SVG sprite sheet` + individual `SVG` exports. |
| `C11` | 4, 34 | `Dataflow signal ribbon, abstract process stream, layered lines and nodes, horizontal cinematic strip.` | Designed for top-band crops; avoid dense labels. | `SVG 1920x320` and `PNG 1920x320`. |

## Placement Pairing Rules
- `C01`, `C08`: pair with `T1` or `T8` templates only.
- `C02`, `C04`, `C05`, `C06`, `C07`: pair with `T2` or `T4` depending on text density.
- `C09`: use only with `T7` split layout.
- `C10`: use `T5` icon rail or matrix slot.
- `C11`: use `T3` top-band slides.

## Quality Gate Before Import
- Confirm visual still reads at projected size from 2-3 meters.
- Remove micro-labels below 18 pt equivalent.
- Keep no more than two accent colors per image.
- Ensure empty space aligns with expected text block position.
- Export and test both light and dark slide backgrounds where applicable.
