# Task 22/36 - Deck Runbook/QA Owner

Date: 2026-02-26

## Ownership
- `presentation_assets/deck_runbook.md`
- `presentation_assets/DECK_QA_CHECKLIST.md`
- `robotics_maze/coordination/agent_reports/task22_runbook.md`

## Goal
- Improve final deck QA flow for image, reference, and factual checks.
- Add repeatable command blocks for pre-presentation verification.

## Changes Delivered
- Updated `presentation_assets/deck_runbook.md` with a dedicated `Final QA Flow (Repeatable Commands)` section.
- Added five explicit QA gates:
  - structural smoke (`scripts/run_repo_smoke.sh`)
  - in-deck image/footer verification (`python-pptx` check)
  - reference link audit artifact validation (`link_audit_final.tsv`)
  - factual-risk hotspot completeness check (`slide_references.json` + `agents_factual_risk_audit.md`)
  - mandatory manual factual spot-check on high-risk slides
- Updated `presentation_assets/DECK_QA_CHECKLIST.md`:
  - added global sign-off items for command-gate execution
  - added QA run metadata capture fields
  - added ordered, copy/paste command flow with pass criteria

## Validation Run (Executed)
- `bash scripts/run_repo_smoke.sh`
  - Result: PASS
  - Key output: `deck_slides=41 mapped_images=41`, `robotics_smoke=ok planners_checked=2 mazes_checked=3`
- In-deck image/footer command:
  - Result: `missing_images=[]`, `missing_reference_footers=[]`
- Link audit unresolved count:
  - Command: `awk -F '\t' 'NR>1 && $4 != "true" {print $0}' presentation_assets/link_audit_final.tsv | wc -l`
  - Result: `0`
- Hotspot completeness command:
  - Result: `hotspot_ref_rows_not_equal_3=[]`, `hotspot_missing_audit_sections=[]`

## Notes
- No files outside task ownership were modified.
