#!/usr/bin/env python3
"""Root-level, simulation-only wrapper for robotics_maze/src/main.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Sequence

DEFAULT_INTERACTIVE_GUI_HOLD_SECONDS = "20"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _normalize_passthrough_args(argv: Sequence[str]) -> list[str]:
    """Drop task-runner separators so CLI args reach the simulation parser cleanly."""
    args = [arg for arg in argv if arg != "--"]
    gui_mode_flags = {"--gui-setup", "--no-gui-setup"}
    last_gui_mode_flag = None
    for arg in args:
        if arg in gui_mode_flags:
            last_gui_mode_flag = arg
    normalized = [arg for arg in args if arg not in gui_mode_flags]
    if last_gui_mode_flag is not None:
        normalized.append(last_gui_mode_flag)
    return normalized


def _apply_interactive_gui_defaults(args: Sequence[str]) -> list[str]:
    normalized = list(args)
    if (
        "--gui" in normalized
        and "--gui-hold-seconds" not in normalized
        and "--no-gui-setup" not in normalized
    ):
        normalized.extend(["--gui-hold-seconds", DEFAULT_INTERACTIVE_GUI_HOLD_SECONDS])

    if (
        "--gui" in normalized
        and "--gui-setup" not in normalized
        and "--no-gui-setup" not in normalized
        and sys.stdin.isatty()
    ):
        normalized.append("--gui-setup")
    return normalized


def run(argv: Sequence[str] | None = None) -> int:
    root = _repo_root()
    target = root / "robotics_maze" / "src" / "main.py"
    raw_args = argv if argv is not None else sys.argv[1:]
    args = _apply_interactive_gui_defaults(_normalize_passthrough_args(raw_args))

    if not target.is_file():
        print(f"[ERROR] Missing simulation entrypoint: {target}", file=sys.stderr)
        return 2

    cmd = [sys.executable, str(target), *args]
    completed = subprocess.run(cmd, cwd=root, check=False)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(run())
