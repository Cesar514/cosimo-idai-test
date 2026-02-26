#!/usr/bin/env python3
"""Capture deterministic simulation screenshots for regression checks.

This script writes all generated PNGs into robotics_maze/testing/screenshots
by default and is intended for CI/local regression automation.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "testing" / "screenshots"


@dataclass(frozen=True)
class CaptureStep:
    name: str
    script: Path
    filename_prefix: str
    expected_suffixes: tuple[str, ...]
    optional: bool

    def expected_filenames(self) -> tuple[str, ...]:
        return tuple(f"{self.filename_prefix}{suffix}" for suffix in self.expected_suffixes)


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate regression screenshot artifacts into testing/screenshots."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where regression screenshots will be stored.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove existing PNG files from the output directory first.",
    )
    parser.add_argument(
        "--require-mujoco",
        action="store_true",
        help="Fail the run if MuJoCo screenshot capture fails.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned commands and deterministic output filenames without running generators.",
    )
    return parser.parse_args(argv)


def _run_step(
    *,
    step: CaptureStep,
    output_dir: Path,
    require_mujoco: bool,
    strict_expected_only: bool,
) -> tuple[bool, list[Path]]:
    if not step.script.is_file():
        message = f"[WARN] missing screenshot script: {step.script}"
        if step.optional and not require_mujoco:
            print(message)
            return True, []
        print(message)
        return False, []

    cmd = [
        sys.executable,
        str(step.script),
        "--output-dir",
        str(output_dir),
        "--filename-prefix",
        step.filename_prefix,
    ]

    print(f"[INFO] running: {' '.join(cmd)}")
    completed = subprocess.run(cmd, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.stderr:
        print(completed.stderr.rstrip(), file=sys.stderr)

    if completed.returncode != 0:
        if step.optional and not require_mujoco:
            print(
                f"[WARN] optional step failed: {step.name} (exit={completed.returncode})"
            )
            return True, []
        print(f"[ERROR] step failed: {step.name} (exit={completed.returncode})")
        return False, []

    expected_names = step.expected_filenames()
    expected_paths = [output_dir / name for name in expected_names]
    missing = [path for path in expected_paths if not path.is_file()]
    if missing:
        message = (
            f"missing deterministic screenshots for prefix '{step.filename_prefix}': "
            f"{', '.join(str(path.name) for path in missing)}"
        )
        if step.optional and not require_mujoco:
            print(f"[WARN] {message}")
            return True, []
        print(f"[ERROR] {message}")
        return False, []

    if strict_expected_only:
        actual = sorted(path.name for path in output_dir.glob(f"{step.filename_prefix}*.png"))
        expected = sorted(expected_names)
        unexpected = [name for name in actual if name not in expected]
        if unexpected:
            message = (
                f"unexpected screenshot names for prefix '{step.filename_prefix}': "
                f"{', '.join(unexpected)}"
            )
            if step.optional and not require_mujoco:
                print(f"[WARN] {message}")
                return True, expected_paths
            print(f"[ERROR] {message}")
            return False, []

    return True, expected_paths


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    steps = [
        CaptureStep(
            name="MuJoCo screenshots",
            script=ROOT / "scripts" / "generate_mujoco_screenshots.py",
            filename_prefix="mujoco_",
            expected_suffixes=(
                "sim_mujoco_1_astar.png",
                "sim_mujoco_2_weighted_astar.png",
                "sim_mujoco_3_fringe_search.png",
            ),
            optional=True,
        ),
        CaptureStep(
            name="Fallback screenshots",
            script=ROOT / "scripts" / "generate_sim_screenshots.py",
            filename_prefix="fallback_",
            expected_suffixes=(
                "sim_snapshot_1_astar.png",
                "sim_snapshot_2_weighted_astar.png",
                "sim_snapshot_3_fringe_search.png",
            ),
            optional=False,
        ),
    ]

    if args.dry_run:
        print(f"[DRY-RUN] output directory: {output_dir.resolve()}")
        print("[DRY-RUN] deterministic screenshot plan:")
        for step in steps:
            cmd = [
                sys.executable,
                str(step.script),
                "--output-dir",
                str(output_dir),
                "--filename-prefix",
                step.filename_prefix,
            ]
            print(f"[DRY-RUN] step: {step.name}")
            print(f"[DRY-RUN] command: {' '.join(cmd)}")
            for name in step.expected_filenames():
                print(f"[DRY-RUN] output: {output_dir / name}")
        return 0

    if not args.no_clean:
        for png in output_dir.glob("*.png"):
            png.unlink()

    all_generated: list[Path] = []
    for step in steps:
        ok, generated = _run_step(
            step=step,
            output_dir=output_dir,
            require_mujoco=args.require_mujoco,
            strict_expected_only=not args.no_clean,
        )
        if not ok:
            return 1
        all_generated.extend(generated)

    if not all_generated:
        print("[ERROR] no screenshots were generated.")
        return 1

    print("[INFO] generated screenshots:")
    seen: set[Path] = set()
    ordered_unique: list[Path] = []
    for image in all_generated:
        resolved = image.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered_unique.append(resolved)

    for image in ordered_unique:
        print(image)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
