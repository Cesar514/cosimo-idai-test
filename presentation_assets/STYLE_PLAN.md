# Technical Deck Visual Style System

## 1) Design Intent
- Build for clarity and endurance across 40+ slides: high contrast, predictable structure, minimal style drift.
- Visual tone: precise, technical, modern.
- Default mode: light background with dark text for readability in mixed lighting.

## 2) Core Tokens

### 2.1 Color System
Use only these named tokens in the deck theme.

| Token | Hex | Usage |
|---|---|---|
| `bg.canvas` | `#F4F7FB` | Default slide background |
| `bg.card` | `#FFFFFF` | Cards, content blocks, table fills |
| `bg.inverse` | `#0E1A2B` | Dark section dividers, final slide |
| `text.primary` | `#0F172A` | Primary text |
| `text.secondary` | `#475569` | Supporting text, captions |
| `text.inverse` | `#F8FAFC` | Text on dark backgrounds |
| `accent.primary` | `#0B5FFF` | Links, key numbers, active highlights |
| `accent.secondary` | `#00A3A3` | Secondary emphasis, process steps |
| `accent.warm` | `#FF7A18` | One-off emphasis, warnings in visuals |
| `status.success` | `#0E9F6E` | Positive outcomes |
| `status.warning` | `#D97706` | Caution states |
| `status.error` | `#DC2626` | Risks, blockers |
| `line.default` | `#D1D9E6` | Dividers, gridlines, borders |

Color rules:
- Keep `accent.primary` as the dominant accent (about 70% of accent usage).
- Never use more than 2 accent colors on one slide.
- Maintain minimum contrast ratio 4.5:1 for body text.

### 2.2 Typography
Font pair:
- Sans: `IBM Plex Sans` (fallback: `Aptos`, `Segoe UI`)
- Mono: `IBM Plex Mono` (fallback: `Consolas`)

Type scale (size/line height):

| Role | Style |
|---|---|
| Deck title | 56 / 62, Semibold |
| Section title | 40 / 46, Semibold |
| Slide title | 32 / 38, Semibold |
| Subtitle | 24 / 30, Medium |
| Body large | 22 / 30, Regular |
| Body | 18 / 26, Regular |
| Caption | 14 / 20, Regular |
| Code | 16 / 24, Mono Regular |

Type rules:
- Max 2 font weights per slide (plus mono if needed).
- Limit line length to 60-75 characters for body text blocks.
- Sentence case for titles (not ALL CAPS).

### 2.3 Spacing and Rhythm
Use an 8 px base grid.

| Token | Value |
|---|---|
| `space.1` | 8 |
| `space.2` | 16 |
| `space.3` | 24 |
| `space.4` | 32 |
| `space.5` | 40 |
| `space.6` | 48 |
| `space.8` | 64 |
| `space.10` | 80 |

Layout frame for 16:9 slides (1920x1080):
- Left/right safe margin: 120 px
- Top margin: 72 px
- Bottom margin: 64 px
- Content baseline spacing between major blocks: 32 px minimum

## 3) Slide Layout Rules
Create and reuse master layouts only:
1. Title slide
2. Agenda/outline
3. Section divider
4. One-column content
5. Two-column content (60/40 and 50/50 variants)
6. Data visualization focus
7. Comparison matrix
8. Full-bleed image + annotation
9. Closing / Q&A

Composition rules:
- One message per slide; title states the takeaway, not the topic.
- Maximum 6 bullets per content slide, one line each when possible.
- Keep at least 32 px between title block and body content.
- Align all objects to master guides; avoid manual off-grid placement.

## 4) Image and Diagram Treatment
- Prefer authentic technical visuals (product UI, diagrams, data) over generic stock photography.
- Image corners: 12 px radius when inside cards; square for full-bleed.
- Add a subtle overlay (`#0E1A2B` at 15-25% opacity) when text sits on images.
- Use consistent stroke style for diagrams: 2 px, `line.default`.
- Annotation callouts: `bg.card`, 1 px `line.default`, 10 px padding, 6 px corner radius.

## 5) Data Visualization Rules
- Chart title communicates insight, not metric label.
- Default series mapping:
  - Series 1: `accent.primary`
  - Series 2: `accent.secondary`
  - Series 3: `accent.warm`
  - Baseline/reference: `line.default`
- Remove nonessential chart chrome (heavy borders, excessive ticks, 3D effects).
- Use direct labels when possible; legend only if required.

## 6) Deck-Scale Consistency Rules (40+ Slides)
- Repeat a small set of patterns; do not invent new layout styles after slide 10.
- Section dividers every 5-8 slides for pacing.
- Keep footer system consistent: slide number + short section label.
- Run a final QA pass for alignment, font sizes, color usage, and contrast.

## 7) Implementation Checklist
- Configure theme colors using token names above.
- Configure theme fonts (`IBM Plex Sans`, `IBM Plex Mono`).
- Build master layouts once; lock guides and recurring placeholders.
- Create reusable components: callout box, KPI card, code snippet block, chart style.
- Validate on projector and laptop display before final delivery.
