# Deck Style Notes

## Style Pack Identity
- Pack name: Signal Forge Editorial (v2).
- Tone: high-contrast engineering narrative with magazine pacing.
- Visual memory anchor: stencil labels, cobalt signal rails, and warm alarm highlights on cool paper backgrounds.
- Deck fit: supports technical explainers without falling into default enterprise-template aesthetics.

## Typography Direction
- Display marker (`font_label`): `Saira Stencil One` only for compact section markers, badges, and one-word openers.
- Title family (`font_title`): `Chakra Petch` in semibold/bold for section cards and slide titles.
- Body family (`font_body`): `Source Serif 4` for narrative bullets, explainer copy, and image captions.
- Mono family (`font_mono`): `IBM Plex Mono` for CLI snippets, metrics, and coordinate labels.
- Hierarchy rule: one display marker + one title + one body block per viewport; avoid stacked title treatments.
- Tracking rule: apply positive tracking (`0.08em`) on all-caps labels to preserve projector readability.

## Color System
- `bg.canvas` and `bg.card` are the default surfaces.
- `bg.tinted` is reserved for comparison blocks, side rails, and evidence panels.
- `accent.primary` (cobalt) is the anchor accent for path lines, arrows, and key figures.
- `accent.secondary` (teal) marks process/state transitions and neutral callouts.
- `accent.warm` marks caution, tradeoff, or risk statements.
- `accent.hot` is limited to one focal alarm moment per section.
- `accent.signal` is used sparingly for success-path highlights and end-state emphasis.
- Recommended accent ratio per slide: primary `60%`, secondary `20%`, warm `12%`, hot/signal combined `8%` max.

## Composition and Surfaces
- Prefer asymmetric layouts (`55/45`, `60/40`, or offset side-rail compositions) over centered symmetry.
- Introduce one diagonal or stepped edge on dense slides using a colored rail or clipped card.
- Keep base cards neutral (`bg.card`) and layer one atmospheric element (mesh gradient, subtle grain, or signal line) behind key content.
- Use rounded corners (`14-20px`) for KPI/callout cards; keep comparison tables squarer to retain technical tone.

## Motion Ideas
- Section openers: `section_rail_wipe` then title rise (`80ms` delay), no extra animation families.
- Content slides: stagger bullets/chips by `70-90ms`; cap animated entry to six elements.
- Data callouts: apply `kpi_pop` (scale `0.96` to `1.0` + fade) to the first metric only.
- Diagram walkthroughs: animate path strokes left-to-right (`signal_trace`) with no bounce.
- Safety rule: max one motion family per slide, max motion window `<= 900ms`.

## Component Recipes
- KPI tile: white card, cobalt numeral, serif label, thin top border in `line.strong`.
- Evidence panel: tinted surface + mono heading + short serif interpretation block.
- Reference footer: mono at caption size, subdued `text.secondary`, one divider line.
- Screenshot frame: dark outer frame (`bg.inverse`) with inner cool border (`line.default`) for visual consistency.

## Accessibility and QA Guardrails
- Body text contrast target: `>= 7:1` on light surfaces.
- Never place `accent.hot` text directly on `bg.tinted`; use an inverse chip if needed.
- Minimum text size: `14px` for static export, `16px` when animated.
- Validate in both laptop and projector mode before final deck export.
