# Citation Footer Style Spec (16:9 PPT, 3 URLs/slide)

## 1) Purpose
Create a consistent, low-noise citation footer for up to 3 source URLs per slide that stays readable on projector screens without competing with main content.

## 2) Footer Zone (Widescreen 16:9)
- Slide size reference: 1920x1080 px (`13.333" x 7.5"`).
- Footer citation band:
  - X: `120 px` from left (`60 pt`)
  - Width: `1680 px` (`840 pt`)
  - Height: `40 px` (`20 pt`) default, expandable to `56 px` (`28 pt`) when wrapping to 2 lines
  - Y anchor: bottom-aligned with `16 px` (`8 pt`) inner bottom padding from slide edge
- Add top divider line for separation:
  - Stroke: `1 px`, color `line.default` (`#D1D9E6`)

## 3) Three-Source Layout
- Use exactly 3 equal columns inside the citation band.
- Column gap: `24 px` (`12 pt`)
- Effective column width: `(1680 - 2*24) / 3 = 544 px` (`272 pt`)
- Each column contains one citation in this format:
  - `[n] short-url-or-title`
  - Example: `[1] openai.com/research/agentic-systems`

## 4) Typography
- Font family: `IBM Plex Sans` (fallback `Aptos`, `Segoe UI`)
- Font size: `9 pt` (minimum allowed: `8.5 pt`; never below)
- Line spacing: `11 pt` fixed (single line feel, compact but readable)
- Weight:
  - Index token `[1]`: Semibold
  - URL text: Regular
- Character spacing: normal (`0`)

## 5) Color + Contrast
- Default light-slide citation text color: `text.secondary` (`#475569`)
- Index token `[n]` color: `text.primary` (`#0F172A`) at `85%` opacity equivalent
- Optional clickable link emphasis (only on hover/click contexts, not visual clutter): `accent.primary` (`#0B5FFF`) with no underline in static layout
- Dark slide variant:
  - Text: `text.inverse` (`#F8FAFC`) at `82-88%` opacity equivalent
  - Divider: `#334155`

## 6) Wrapping Rules
- Max lines per citation: `2`
- Preferred line break points (in order):
  1. After `/`
  2. Before `?`
  3. After `&`
  4. After `-` or `_`
- Disable character-level hard breaks when possible to avoid splitting domains (`example.co` should stay intact).

## 7) Truncation Rules (Robust)
Apply normalization before truncation:
1. Strip protocol: `https://`, `http://`
2. Strip trailing slash
3. Remove tracking query params (`utm_*`, `fbclid`, `gclid`)

Then truncate only if needed:
- Single-line fit target: about `70-78` characters per column at `9 pt`
- Two-line hard cap: `150` characters per citation after normalization
- Truncation style: middle ellipsis, preserving domain + final path slug
  - Example: `docs.example.com/product/.../api-reference-v2`

## 8) Spacing + Alignment
- Citation band inner padding:
  - Top: `6 px` (`3 pt`)
  - Bottom: `6 px` (`3 pt`)
- Text vertical alignment: middle within band
- Keep at least `8 px` clear space above citation band from any content object
- Do not overlap with slide number/footer label; if both exist:
  - Row 1 (upper): citations
  - Row 2 (lower): slide number + section label

## 9) Behavior for Missing/Extra Sources
- If 1-2 sources only: keep 3-column grid; leave unused columns blank (preserves rhythm).
- If more than 3 sources exist: show top 3 most authoritative links and append a short note in column 3:
  - `+N additional sources in speaker notes`

## 10) Copy-Paste Authoring Template
Use this exact line pattern in each column text box:
- `[1] domain.tld/path`
- `[2] domain.tld/path`
- `[3] domain.tld/path`

Authoring checklist per slide:
1. Normalize URLs (remove protocol/tracking params).
2. Confirm each citation fits in <=2 lines.
3. Apply middle-ellipsis truncation if overflow remains.
4. Verify contrast against background variant (light/dark).
