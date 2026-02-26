# Task 03 - URDF Visibility Owner

## Scope
- Owned files: `robotics_maze/src/sim.py`, `robotics_maze/urdfs/README.md`.
- Goal covered: default real-robot URDF load path, explicit fallback when primary URDF is unavailable, and camera framing behavior that keeps robot elevation in view.

## Changes Made
1. `robotics_maze/src/sim.py`
- Kept Husky as the primary default URDF (`husky/husky.urdf`) and `r2d2.urdf` as fallback.
- Made fallback explicit by emitting a warning when Husky is missing/unloadable and fallback is used:
  - `Default robot URDF fallback engaged: ... Using 'r2d2.urdf'.`
- Added primary-failure detail to terminal runtime error when both defaults fail.
- Improved camera framing to keep robot visible vertically:
  - added `_camera_target_z` state,
  - added `_get_robot_position()`,
  - updated camera application to target `(x, y, z)` instead of fixed `z=0.0`,
  - added `_camera_target_z_for_robot()` and used it during initial focus + tracking updates.

2. `robotics_maze/urdfs/README.md`
- Documented runtime default order explicitly:
  1. `husky/husky.urdf` (primary)
  2. `r2d2.urdf` (explicit fallback)
- Documented that failure of both defaults raises runtime error.

## Validation Command
```bash
python3 - <<'PY'
from __future__ import annotations
import contextlib
import io
import tempfile
from pathlib import Path

from robotics_maze.src import sim


class FakePyBullet:
    class error(Exception):
        pass

    def __init__(self, fail_primary: bool = False):
        self.fail_primary = fail_primary
        self.loaded = []

    def loadURDF(self, urdf_path, *args, **kwargs):
        self.loaded.append(urdf_path)
        if self.fail_primary and urdf_path == sim.DEFAULT_ROBOT_URDF:
            raise self.error("primary missing")
        return 101


def make_default_tree(root: Path, include_husky: bool) -> None:
    if include_husky:
        (root / "husky").mkdir(parents=True, exist_ok=True)
        (root / "husky" / "husky.urdf").write_text("<robot name='husky'/>", encoding="utf-8")
    (root / "r2d2.urdf").write_text("<robot name='r2d2'/>", encoding="utf-8")


class FakePyBulletData:
    def __init__(self, data_path: str):
        self._path = data_path

    def getDataPath(self) -> str:
        return self._path


def run_default_primary_check() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        make_default_tree(root, include_husky=True)
        old_p, old_data = sim.p, sim.pybullet_data
        fake_p = FakePyBullet(fail_primary=False)
        sim.p = fake_p
        sim.pybullet_data = FakePyBulletData(str(root))
        try:
            inst = object.__new__(sim.PyBulletMazeSim)
            inst.client_id = 1
            _, name = inst._load_default_robot((0, 0, 0.2), (0, 0, 0, 1))
            assert name == "husky", name
            assert fake_p.loaded[0] == sim.DEFAULT_ROBOT_URDF, fake_p.loaded
            print(f"default_load={name}")
        finally:
            sim.p, sim.pybullet_data = old_p, old_data


def run_fallback_warning_check() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        make_default_tree(root, include_husky=False)
        old_p, old_data = sim.p, sim.pybullet_data
        fake_p = FakePyBullet(fail_primary=False)
        sim.p = fake_p
        sim.pybullet_data = FakePyBulletData(str(root))
        out = io.StringIO()
        try:
            inst = object.__new__(sim.PyBulletMazeSim)
            inst.client_id = 1
            with contextlib.redirect_stdout(out):
                _, name = inst._load_default_robot((0, 0, 0.2), (0, 0, 0, 1))
            assert name == "r2d2", name
            text = out.getvalue()
            assert "Default robot URDF fallback engaged" in text, text
            print("fallback_warning=ok")
        finally:
            sim.p, sim.pybullet_data = old_p, old_data


def run_camera_z_check() -> None:
    value = sim._camera_target_z_for_robot(0.2)
    assert value > 0.2, value
    inst = object.__new__(sim.PyBulletMazeSim)
    inst.gui = True
    inst._camera_bounds_xy = (0.0, 10.0, 0.0, 10.0)
    inst._camera_target_xy = (5.0, 5.0)
    inst._camera_target_z = 0.28
    inst._get_robot_position = lambda: (9.5, 9.5, 0.2)
    captured = {}
    inst._apply_camera = lambda *, target_x, target_y, target_z: captured.update(
        {"x": target_x, "y": target_y, "z": target_z}
    )
    inst._update_camera_tracking()
    assert captured["z"] > 0.28, captured
    print(f"camera_target_z={captured['z']:.3f}")


run_default_primary_check()
run_fallback_warning_check()
run_camera_z_check()
print("validation=ok")
PY
```

## Validation Output
```text
default_load=husky
fallback_warning=ok
camera_target_z=0.300
validation=ok
```

## Notes
- `python3 -m py_compile robotics_maze/src/sim.py` also passes.
- Attempting `pixi run` validation in this environment failed while building `pybullet==3.2.7`, so verification used a deterministic mock-based command.
