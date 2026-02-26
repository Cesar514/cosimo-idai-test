# Session Event Log Schema (`session_event_log.csv`)

## Purpose
Append-only session log for coordination events across robotics maze work (instructions, spawns, status, completions, errors).

## Columns
1. `timestamp_iso`
   - ISO-8601 timestamp when known.
   - Use `unknown` when exact timestamp is not recoverable.
   - If partial timestamp text is provided by source (for example `2026-02-26T19:??:??-05:00`), preserve it as-is.
2. `event_type`
   - Recommended values: `user_instruction`, `agent_spawned`, `agent_status`, `agent_completed`, `agent_error`.
3. `source`
   - Origin of evidence, for example `user`, `subagent`, `coordination/B2.md`.
4. `entity_id`
   - Agent/session identifier if available; else `unknown` or `n/a`.
5. `entity_name`
   - Human-readable actor, for example `B2`, `R6`, `S1`; else `n/a`.
6. `instruction_or_event`
   - Short, plain-language instruction or event summary.
7. `status`
   - State at time of event, for example `received`, `spawned`, `completed`, `blocker`, `missing_log`.
8. `details`
   - Supporting evidence, file paths, caveats, and timestamp quality note when `timestamp_iso=unknown`.

## Usage Rules
1. Append new rows only; do not reorder historical rows.
2. Do not fabricate specifics; prefer `unknown`/`n/a` for missing fields.
3. If `timestamp_iso` is `unknown`, include an explicit `timestamp unknown` note in `details`.
4. Quote CSV fields that contain commas or punctuation-heavy text.
5. Keep entries factual and tied to visible repository evidence or explicit user-provided updates.
