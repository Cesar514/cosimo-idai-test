#!/usr/bin/env python3
"""Check physics backend availability and print recommended runtime flags."""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

BACKEND_CHOICES = ("auto", "pybullet", "mujoco")
DEFAULT_GUI_HOLD_SECONDS = 8.0


@dataclass(frozen=True)
class ModuleProbe:
    name: str
    available: bool
    version: str | None
    detail: str | None


def _probe_module(module_name: str) -> ModuleProbe:
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return ModuleProbe(
            name=module_name,
            available=False,
            version=None,
            detail="not installed",
        )

    import_check = subprocess.run(
        [sys.executable, "-c", f"import importlib; importlib.import_module('{module_name}')"],
        check=False,
        capture_output=True,
        text=True,
    )
    if import_check.returncode != 0:  # pragma: no cover - environment dependent.
        error_text = (import_check.stderr or import_check.stdout).strip().splitlines()
        message = error_text[-1] if error_text else "import failed"
        return ModuleProbe(
            name=module_name,
            available=False,
            version=None,
            detail=message,
        )

    try:
        version = importlib.metadata.version(module_name)
    except importlib.metadata.PackageNotFoundError:
        version = None

    origin = spec.origin
    detail = str(Path(origin).resolve()) if isinstance(origin, str) else "import ok"
    return ModuleProbe(
        name=module_name,
        available=True,
        version=str(version) if version is not None else None,
        detail=detail,
    )


def _resolve_backend_order(
    backend: str, *, pybullet_available: bool, mujoco_available: bool
) -> tuple[str, ...]:
    if backend == "auto":
        if pybullet_available:
            return ("pybullet", "mujoco")
        if mujoco_available:
            return ("mujoco",)
        return ()

    if backend == "pybullet":
        if pybullet_available:
            return ("pybullet", "mujoco")
        if mujoco_available:
            return ("mujoco",)
        return ()

    if mujoco_available:
        return ("mujoco", "pybullet")
    if pybullet_available:
        return ("pybullet",)
    return ()


def _render_probe(probe: ModuleProbe) -> str:
    state = "yes" if probe.available else "no"
    version = probe.version or "n/a"
    detail = probe.detail or "n/a"
    return f"{probe.name:<13} available={state:<3} version={version:<12} detail={detail}"


def _print_recommendations(*, pybullet_available: bool, mujoco_available: bool) -> None:
    print("\nRecommended runtime flags:")
    print("  default_headless: --no-gui-setup --physics-backend auto")
    if pybullet_available:
        print(
            "  gui_visual: --gui --physics-backend pybullet "
            f"--gui-hold-seconds {DEFAULT_GUI_HOLD_SECONDS:g} --no-gui-setup"
        )
    elif mujoco_available:
        print("  mujoco_only: --no-gui-setup --physics-backend mujoco")
        print("  note: GUI views require PyBullet in this project.")
    else:
        print(
            "  fallback_only: --no-gui-setup --physics-backend auto "
            "(deterministic kinematic fallback)"
        )

    if platform.system() == "Linux" and mujoco_available:
        mujoco_gl = os.environ.get("MUJOCO_GL")
        if mujoco_gl:
            print(f"  env_hint: MUJOCO_GL already set to '{mujoco_gl}'")
        elif not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
            print("  env_hint: set MUJOCO_GL=egl for headless Linux runs")


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check whether pybullet/mujoco are importable and show runtime flags "
            "recommended for robotics_maze/src/main.py."
        )
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    _parse_args(argv)
    pybullet_probe = _probe_module("pybullet")
    pybullet_data_probe = _probe_module("pybullet_data")
    mujoco_probe = _probe_module("mujoco")

    pybullet_available = pybullet_probe.available and pybullet_data_probe.available
    mujoco_available = mujoco_probe.available

    print("Physics backend probe:")
    print(f"  {_render_probe(pybullet_probe)}")
    print(f"  {_render_probe(pybullet_data_probe)}")
    print(f"  {_render_probe(mujoco_probe)}")
    print(f"\nEffective backend availability: pybullet={int(pybullet_available)} mujoco={int(mujoco_available)}")

    print("\nResolution order by --physics-backend:")
    for backend in BACKEND_CHOICES:
        order = _resolve_backend_order(
            backend,
            pybullet_available=pybullet_available,
            mujoco_available=mujoco_available,
        )
        rendered_order = " -> ".join(order) if order else "kinematic_fallback_only"
        print(f"  {backend:<8} {rendered_order}")

    _print_recommendations(
        pybullet_available=pybullet_available,
        mujoco_available=mujoco_available,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
