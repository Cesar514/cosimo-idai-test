# Task 34/36 - Deck Validator Owner

Date: 2026-02-26

## Ownership
- `scripts/validate_deck_assets.py`
- `robotics_maze/coordination/agent_reports/task34_deck_validator.md`

## Goal
- Add/refresh a validator for deck artifacts that checks:
  - slide count alignment
  - image coverage
  - reference coverage

## Deliverable Summary
- Added `scripts/validate_deck_assets.py`.
- Validator implementation details:
  - Reads slide count from `agents.pptx` directly via PPTX XML (`ppt/presentation.xml`).
  - Cross-checks slide count alignment across:
    - `agents.pptx`
    - `presentation_assets/speaker_notes.md`
    - `presentation_assets/slide_image_map.json`
    - `presentation_assets/slide_references.json`
  - Validates image coverage:
    - contiguous slide keys matching expected deck range
    - at least one image path per slide
    - mapped image paths exist on disk
  - Validates reference coverage:
    - contiguous slide keys matching expected deck range
    - exactly `3` references per slide (configurable)
    - URL format (`http://` or `https://`)
  - Emits gate-level status lines:
    - `slide_count_alignment=PASS|FAIL`
    - `image_coverage=PASS|FAIL`
    - `reference_coverage=PASS|FAIL`

## Validation Run (Executed)
Command:
```bash
python3 scripts/validate_deck_assets.py
```

Output:
```text
deck_asset_validator
deck_slide_count=41
speaker_notes_slide_count=41
image_map_slide_keys=41
image_map_entries=41
references_map_slide_keys=41
references_map_entries=123
slide_count_alignment=PASS
image_coverage=PASS
reference_coverage=PASS
status=PASS
```
