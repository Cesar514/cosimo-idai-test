# GUI Setup Integration (Worker B)

## Summary
- Added a Tkinter-based setup dialog in `src/gui_setup.py` that lets the user set:
  - planner name
  - episode count
  - maze size (`width x height`)
  - seed (blank means `None`)
  - GUI mode (maps to existing `--gui` behavior)

## New CLI Flags
- `--gui-setup`
  - Opens the setup dialog before simulation starts.
- `--no-gui-setup`
  - Explicitly skips the setup dialog and runs with CLI arguments/defaults.

## Compatibility and Defaults
- Existing CLI behavior is preserved by default:
  - if neither flag is provided, setup dialog is skipped (same behavior as before).
- Existing flags (`--planner`, `--episodes`, `--maze-size`, `--seed`, `--gui`) still work unchanged.
- When `--gui-setup` is used, dialog selections override the parsed CLI values for runtime execution.

## Non-GUI Environment Handling
- If Tkinter is unavailable or no display is present (headless environment), the app does not crash.
- It logs a warning and continues with the already parsed CLI/default config.
- If the user closes/cancels the dialog, it logs an info message and continues with the CLI/default config.
