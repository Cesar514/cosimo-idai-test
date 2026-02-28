# Media/Binary Metadata Privacy Audit (Agent 16)

## Scope
- Repository root: `/Users/cesar514/Documents/agent_programming/cosimi-idai-test`
- Target types scanned: `jpg`, `jpeg`, `png`, `gif`, `webp`, `tif`, `tiff`, `bmp`, `heic`, `heif`, `avif`, `svg`, `pdf`
- Candidate files found: `50`

## Tooling Used
- `pdfinfo` for PDF document metadata
- `mdls` for Spotlight-exposed metadata fields
- `sips -g all` for raster image property checks
- `xattr` for macOS extended attributes on media files
- `strings` + pattern grep for fallback embedded-text checks in binary formats

## Availability Constraints
- `exiftool` not installed
- ImageMagick `identify` not installed

## Findings

### 1. PDF internal metadata
Two PDFs expose generator metadata only:
- `paper/ieee_tro_robotics_maze/submission/ieee_tro_robotics_maze_main.pdf`
  - `Creator: TeX`
  - `Producer: pdfTeX-1.40.28`
- `paper/ieee_tro_robotics_maze/main.pdf`
  - `Creator: TeX`
  - `Producer: pdfTeX-1.40.28`

No explicit personal author name, email, or filesystem path was found in these PDF metadata fields.

### 2. Raster image metadata (PNG/JPG/etc.)
- No author/creator/comment/software/private path strings were surfaced by `sips`, `mdls`, or `strings` heuristics.
- One benign color profile marker was observed:
  - `skills/skill-creator/assets/skill-creator.png` -> `profile: sRGB IEC61966-2.1`

### 3. SVG metadata/text pass
- No `dc:creator`, `cc:Agent`, `sodipodi`, `inkscape`, email, or absolute-path-like strings were found via text search.

### 4. macOS extended attributes (filesystem-level, not embedded file payload)
Most media files include `com.apple.provenance`.
A subset also contains:
- `com.apple.quarantine`
- `com.apple.lastuseddate#PS`

Files with `com.apple.quarantine`:
- `robotics_maze/testing/screenshots/fallback_sim_snapshot_3_fringe_search.png`
- `robotics_maze/testing/screenshots/mujoco_sim_mujoco_2_weighted_astar.png`
- `robotics_maze/testing/screenshots/fallback_sim_snapshot_2_weighted_astar.png`
- `robotics_maze/testing/screenshots/mujoco_sim_mujoco_3_fringe_search.png`
- `paper/ieee_tro_robotics_maze/submission/ieee_tro_robotics_maze_main.pdf`
- `paper/ieee_tro_robotics_maze/main.pdf`

Observed quarantine format sample: `0082;...;Preview;` (indicates macOS quarantine metadata with Preview as agent).

## Risk Assessment (Likely Private Strings)
- **Embedded media/PDF metadata risk:** Low in this scan.
- **Filesystem metadata risk (xattrs):** Moderate operational privacy signal on macOS workstations (download/view provenance and access timestamps), but these are not typical in-file EXIF/XMP author fields.

## Limitations
- Without `exiftool`, deep EXIF/XMP/IPTC extraction is incomplete for some image formats.
- `strings` is heuristic and may miss compressed/encoded metadata blocks.
- `mdls`/`xattr` results are host-filesystem dependent and macOS-specific.
- This audit is practical/common-path only; it does not perform full binary parsing of every possible metadata namespace.
