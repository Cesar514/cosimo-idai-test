#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

export REPO_ROOT="${ROOT_DIR}"
export PYTHONHASHSEED="${PYTHONHASHSEED:-0}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "[smoke] Missing python interpreter: ${PYTHON_BIN}" >&2
  exit 127
fi

echo "[smoke] repo=${ROOT_DIR}"
echo "[smoke] $("${PYTHON_BIN}" --version 2>&1)"
echo "[smoke] PYTHONHASHSEED=${PYTHONHASHSEED}"

echo "[smoke] Step 1/4: compile key python modules"
"${PYTHON_BIN}" - <<'PY'
import os
from pathlib import Path

root = Path(os.environ["REPO_ROOT"])

targets = [
    root / "scripts" / "apply_ppt_assets.py",
    root / "scripts" / "fix_ppt_full.py",
    root / "scripts" / "sim_runner.py",
    root / "robotics_maze" / "src" / "main.py",
    root / "robotics_maze" / "src" / "benchmark.py",
    root / "robotics_maze" / "src" / "planners.py",
    root / "robotics_maze" / "src" / "maze.py",
    root / "robotics_maze" / "src" / "geometry.py",
    root / "robotics_maze" / "src" / "heuristics.py",
    root / "robotics_maze" / "src" / "robot.py",
    root / "robotics_maze" / "src" / "sim.py",
    root / "robotics_maze" / "src" / "gui_setup.py",
]
targets.extend(sorted((root / "robotics_maze" / "src" / "alt_planners").glob("*.py")))

missing = [str(path) for path in targets if not path.is_file()]
if missing:
    raise SystemExit("Missing expected module(s):\n- " + "\n- ".join(missing))

for path in targets:
    source = path.read_text(encoding="utf-8")
    compile(source, str(path), "exec")

print(f"compiled_modules={len(targets)}")
PY

echo "[smoke] Step 2/4: validate deck outputs"
"${PYTHON_BIN}" - <<'PY'
import csv
import json
import os
import re
import zipfile
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(message)


root = Path(os.environ["REPO_ROOT"])
deck_path = root / "agents.pptx"
if not deck_path.is_file():
    fail(f"Missing deck file: {deck_path}")
if deck_path.stat().st_size <= 0:
    fail(f"Deck file is empty: {deck_path}")
if not zipfile.is_zipfile(deck_path):
    fail(f"Deck file is not a valid .pptx zip archive: {deck_path}")

coverage_path = root / "presentation_assets" / "image_coverage_report.md"
coverage_text = coverage_path.read_text(encoding="utf-8")
total_match = re.search(r"Total slides:\s*(\d+)", coverage_text)
coverage_match = re.search(r"Coverage:\s*(\d+)/(\d+)", coverage_text)
if total_match is None or coverage_match is None:
    fail(f"Coverage report is missing expected counters: {coverage_path}")
declared_total = int(total_match.group(1))
declared_covered = int(coverage_match.group(1))
declared_denominator = int(coverage_match.group(2))
if declared_covered != declared_denominator:
    fail(f"Coverage report indicates incomplete coverage: {declared_covered}/{declared_denominator}")

image_map_path = root / "presentation_assets" / "slide_image_map.json"
image_map = json.loads(image_map_path.read_text(encoding="utf-8"))
if not isinstance(image_map, dict) or not image_map:
    fail(f"Invalid or empty image map: {image_map_path}")

try:
    slide_numbers = sorted(int(key) for key in image_map.keys())
except ValueError as exc:
    fail(f"Image map has non-integer slide keys: {exc}")

expected_sequence = list(range(1, slide_numbers[-1] + 1))
if slide_numbers != expected_sequence:
    fail("Image map slide keys must be contiguous and start at 1")

if declared_total != slide_numbers[-1] or declared_denominator != slide_numbers[-1]:
    fail(
        "Deck slide counts are inconsistent between coverage report and image map: "
        f"report_total={declared_total}, report_coverage_total={declared_denominator}, "
        f"image_map_max_slide={slide_numbers[-1]}"
    )

with zipfile.ZipFile(deck_path, "r") as archive:
    zip_entries = set(archive.namelist())
slide_xml_entries = sorted(
    name for name in zip_entries if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
)
if len(slide_xml_entries) != slide_numbers[-1]:
    fail(
        "Deck slide count mismatch between image map and .pptx archive: "
        f"image_map={slide_numbers[-1]}, pptx_slide_xml={len(slide_xml_entries)}"
    )
if "ppt/presentation.xml" not in zip_entries:
    fail("Deck archive is missing required entry: ppt/presentation.xml")

missing_assets: list[str] = []
for slide in slide_numbers:
    mapped_paths = image_map.get(str(slide))
    if not isinstance(mapped_paths, list) or not mapped_paths:
        missing_assets.append(f"slide {slide}: missing image entries")
        continue
    for raw_path in mapped_paths:
        if not isinstance(raw_path, str) or not raw_path.strip():
            missing_assets.append(f"slide {slide}: invalid image path value")
            continue
        candidate = Path(raw_path).expanduser()
        if not candidate.is_absolute():
            candidate = (root / candidate).resolve()
        if candidate.exists():
            continue
        if candidate.suffix.lower() == ".svg" and candidate.with_suffix(".png").exists():
            continue
        missing_assets.append(f"slide {slide}: missing image asset {raw_path}")

if missing_assets:
    fail("Deck image map references missing assets:\n- " + "\n- ".join(missing_assets))

refs_map_path = root / "presentation_assets" / "slide_references.json"
refs_map = json.loads(refs_map_path.read_text(encoding="utf-8"))
if not isinstance(refs_map, dict):
    fail(f"Invalid references map: {refs_map_path}")

fallback_refs = refs_map.get("1", [])
if not isinstance(fallback_refs, list) or not fallback_refs:
    fail("References map must define non-empty fallback refs at key '1'")

bad_refs: list[str] = []
for slide in slide_numbers:
    refs = refs_map.get(str(slide), fallback_refs)
    if not isinstance(refs, list) or not refs:
        bad_refs.append(f"slide {slide}: no references found")
        continue
    for ref in refs:
        if not isinstance(ref, str) or not ref.startswith(("https://", "http://")):
            bad_refs.append(f"slide {slide}: invalid reference URL {ref!r}")

if bad_refs:
    fail("Deck references validation failed:\n- " + "\n- ".join(bad_refs))

link_audit_path = root / "presentation_assets" / "link_audit_final.tsv"
if not link_audit_path.is_file():
    fail(f"Missing link audit artifact: {link_audit_path}")
with link_audit_path.open("r", encoding="utf-8", newline="") as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    fieldnames = set(reader.fieldnames or [])
    required_columns = {"url", "status_code", "final_url", "reachable"}
    if not required_columns.issubset(fieldnames):
        fail(
            "Link audit TSV is missing required columns: "
            + ", ".join(sorted(required_columns - fieldnames))
        )
    rows = list(reader)

if not rows:
    fail(f"Link audit TSV is empty: {link_audit_path}")

link_failures: list[str] = []
for idx, row in enumerate(rows, start=2):
    reachable = str(row.get("reachable", "")).strip().lower()
    status_raw = str(row.get("status_code", "")).strip()
    if reachable not in {"true", "1", "yes"}:
        link_failures.append(
            f"line {idx}: reachable={row.get('reachable')!r} url={row.get('url')!r}"
        )
        continue
    try:
        status_code = int(status_raw)
    except ValueError:
        link_failures.append(f"line {idx}: invalid status_code={status_raw!r}")
        continue
    if status_code < 200 or status_code >= 400:
        link_failures.append(
            f"line {idx}: status_code={status_code} url={row.get('url')!r}"
        )

if link_failures:
    fail("Link audit indicates non-reachable references:\n- " + "\n- ".join(link_failures[:20]))

print(
    "deck_slides="
    f"{slide_numbers[-1]} "
    "mapped_images="
    f"{sum(len(v) for v in image_map.values())} "
    "link_rows="
    f"{len(rows)}"
)
PY

echo "[smoke] Step 3/4: simulation runner + screenshot artifacts"
"${PYTHON_BIN}" - <<'PY'
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(message)


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 24:
        fail(f"PNG file is too small to contain IHDR: {path}")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"Invalid PNG signature: {path}")
    if data[12:16] != b"IHDR":
        fail(f"PNG missing IHDR chunk: {path}")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width <= 0 or height <= 0:
        fail(f"PNG has invalid dimensions ({width}x{height}): {path}")
    return width, height


root = Path(os.environ["REPO_ROOT"])
cmd = [
    sys.executable,
    str(root / "scripts" / "sim_runner.py"),
    "--planner",
    "astar",
    "--episodes",
    "1",
    "--maze-size",
    "9",
    "--seed",
    "42",
    "--physics-backend",
    "auto",
    "--no-gui-setup",
]
completed = subprocess.run(
    cmd,
    cwd=root,
    text=True,
    capture_output=True,
    check=False,
)
combined_output = (completed.stdout or "") + (completed.stderr or "")
if completed.returncode != 0:
    fail(
        "Simulation wrapper smoke run failed: "
        f"exit={completed.returncode}\n{combined_output.strip()}"
    )
if "[START]" not in combined_output:
    fail("Simulation smoke output is missing [START] marker")
if "[EP 1/1]" not in combined_output:
    fail("Simulation smoke output is missing per-episode marker")
if "[DONE] success=1/1" not in combined_output:
    fail("Simulation smoke output did not report full success")

step_match = re.search(r"\[EP 1/1\] status=ok steps=(\d+)", combined_output)
if step_match is None:
    fail("Simulation smoke output is missing parseable step count")
step_count = int(step_match.group(1))
if step_count <= 0:
    fail(f"Simulation smoke run returned non-positive step count: {step_count}")

image_map_path = root / "presentation_assets" / "slide_image_map.json"
image_map = json.loads(image_map_path.read_text(encoding="utf-8"))
if not isinstance(image_map, dict):
    fail(f"Invalid image map payload: {image_map_path}")

tracked_prefixes = (
    (root / "robotics_maze" / "results" / "screenshots").resolve().as_posix() + "/",
    (root / "robotics_maze" / "results" / "screenshots_mujoco").resolve().as_posix() + "/",
    (root / "robotics_maze" / "testing" / "screenshots").resolve().as_posix() + "/",
)
simulation_png_assets: set[Path] = set()
for mapped in image_map.values():
    if not isinstance(mapped, list):
        continue
    for raw_path in mapped:
        if not isinstance(raw_path, str) or not raw_path.strip():
            continue
        candidate = Path(raw_path).expanduser()
        if not candidate.is_absolute():
            candidate = (root / candidate).resolve()
        candidate_posix = candidate.as_posix()
        if candidate.suffix.lower() != ".png":
            continue
        if any(candidate_posix.startswith(prefix) for prefix in tracked_prefixes):
            simulation_png_assets.add(candidate)

if not simulation_png_assets:
    fail("Deck image map does not reference any simulation PNG assets")

dimensions_checked = 0
for png_path in sorted(simulation_png_assets):
    if not png_path.is_file():
        fail(f"Missing simulation PNG asset referenced by deck map: {png_path}")
    png_dimensions(png_path)
    dimensions_checked += 1

print(
    "simulation_episode_steps="
    f"{step_count} "
    "simulation_png_assets="
    f"{len(simulation_png_assets)} "
    "png_dimension_checks="
    f"{dimensions_checked}"
)
PY

echo "[smoke] Step 4/4: deterministic robotics checks"
"${PYTHON_BIN}" - <<'PY'
import importlib.util
import os
import sys
import tempfile
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(message)


root = Path(os.environ["REPO_ROOT"])
benchmark_path = root / "robotics_maze" / "src" / "benchmark.py"
spec = importlib.util.spec_from_file_location("robotics_benchmark_smoke", benchmark_path)
if spec is None or spec.loader is None:
    fail(f"Unable to load benchmark module: {benchmark_path}")
benchmark = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = benchmark
spec.loader.exec_module(benchmark)

grid_a, start_a, goal_a = benchmark.generate_benchmark_maze(
    width=10,
    height=8,
    seed=123,
    algorithm="backtracker",
)
grid_b, start_b, goal_b = benchmark.generate_benchmark_maze(
    width=10,
    height=8,
    seed=123,
    algorithm="backtracker",
)
if grid_a != grid_b or start_a != start_b or goal_a != goal_b:
    fail("Benchmark maze generation is not deterministic for fixed seed and dimensions")

available = benchmark.load_available_planners(include_alt=False)
required = ("astar", "dijkstra")
missing = [name for name in required if name not in available]
if missing:
    fail("Missing baseline planners required for smoke check: " + ", ".join(missing))

selected = {"astar": available["astar"]}
trials_1, _ = benchmark.run_benchmark(
    planners=selected,
    maze_count=3,
    width=10,
    height=10,
    seed=7,
    algorithm="backtracker",
)
trials_2, _ = benchmark.run_benchmark(
    planners=selected,
    maze_count=3,
    width=10,
    height=10,
    seed=7,
    algorithm="backtracker",
)

if len(trials_1) != 3 or len(trials_2) != 3:
    fail("Unexpected number of benchmark trials from deterministic smoke run")
if not all(trial.success for trial in trials_1):
    fail("A* deterministic smoke run reported failed trial(s)")
if not all((trial.path_length or 0) > 0 for trial in trials_1):
    fail("A* deterministic smoke run produced non-positive path length")

signature_1 = [(t.maze_seed, t.success, t.path_length, t.expansions) for t in trials_1]
signature_2 = [(t.maze_seed, t.success, t.path_length, t.expansions) for t in trials_2]
if signature_1 != signature_2:
    fail("Benchmark outputs are not deterministic for fixed seed")

with tempfile.TemporaryDirectory(prefix="repo-smoke-") as tmp_dir:
    _, summary, csv_path, summary_path = benchmark.run_benchmark_and_write_reports(
        planners={"astar": available["astar"], "dijkstra": available["dijkstra"]},
        maze_count=2,
        width=8,
        height=8,
        seed=9,
        algorithm="backtracker",
        output_dir=tmp_dir,
    )

    if len(summary) != 2:
        fail(f"Expected 2 planner summary rows, got {len(summary)}")
    csv_text = csv_path.read_text(encoding="utf-8")
    md_text = summary_path.read_text(encoding="utf-8")
    if "solve_time_ms" not in csv_text or "algorithm" not in csv_text:
        fail("Benchmark CSV output is missing expected columns")
    if "| Rank | Planner |" not in md_text or "Maze algorithm: backtracker" not in md_text:
        fail("Benchmark summary markdown is missing expected content")

print("robotics_smoke=ok planners_checked=2 mazes_checked=3")
PY

echo "[smoke] PASS"
