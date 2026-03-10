"""CI check: verify that paper LaTeX tables match the designated benchmark snapshot.

Exits with code 0 if tables are consistent, non-zero on any mismatch or error.

Usage:
    python robotics_maze/scripts/check_snapshot_tables.py
    python robotics_maze/scripts/check_snapshot_tables.py --snapshot paper_v1
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PAPER_TABLES_DIR = _REPO_ROOT / "paper" / "ieee_tro_robotics_maze" / "tables"
_SNAPSHOTS_DIR = _REPO_ROOT / "robotics_maze" / "results" / "snapshots"
_SNAPSHOT_MANIFEST = (
    _REPO_ROOT / "paper" / "ieee_tro_robotics_maze" / "coordination" / "snapshot_manifest.json"
)

_CHECKED_TABLES = (
    "main_results_table.tex",
    "statistical_comparison_table.tex",
)


def _sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _verify_snapshot_csv_hash(snapshot_id: str) -> str:
    """Verify snapshot CSV integrity against snapshot_meta.json; return actual hash."""
    csv_path = _SNAPSHOTS_DIR / snapshot_id / "benchmark_results.csv"
    if not csv_path.exists():
        print(f"ERROR: Snapshot CSV not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    actual_hash = _sha256_of_file(csv_path)

    meta_path = _SNAPSHOTS_DIR / snapshot_id / "snapshot_meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        recorded = meta.get("csv_sha256", "")
        if recorded and recorded != actual_hash:
            print(
                f"ERROR: Snapshot '{snapshot_id}' CSV has been modified!\n"
                f"  Expected (snapshot_meta.json): {recorded}\n"
                f"  Actual file hash             : {actual_hash}",
                file=sys.stderr,
            )
            sys.exit(1)

    manifest_hash = ""
    if _SNAPSHOT_MANIFEST.exists():
        manifest = json.loads(_SNAPSHOT_MANIFEST.read_text(encoding="utf-8"))
        manifest_hash = manifest.get("csv_sha256", "")
    if manifest_hash and manifest_hash != actual_hash:
        print(
            f"ERROR: Snapshot '{snapshot_id}' CSV hash does not match snapshot_manifest.json!\n"
            f"  snapshot_manifest.json : {manifest_hash}\n"
            f"  Actual file hash       : {actual_hash}",
            file=sys.stderr,
        )
        sys.exit(1)

    return actual_hash


def _resolve_snapshot_id(cli_snapshot: str | None) -> str:
    if cli_snapshot:
        return cli_snapshot
    if _SNAPSHOT_MANIFEST.exists():
        manifest = json.loads(_SNAPSHOT_MANIFEST.read_text(encoding="utf-8"))
        return str(manifest["designated_snapshot"])
    return "paper_v1"


def _regenerate_into(snapshot_id: str, output_dir: Path) -> None:
    """Call regenerate_tables_from_snapshot.py in a subprocess to avoid import side-effects."""
    import subprocess

    regen_script = _REPO_ROOT / "robotics_maze" / "scripts" / "regenerate_tables_from_snapshot.py"
    result = subprocess.run(
        [
            sys.executable,
            str(regen_script),
            "--snapshot", snapshot_id,
            "--output-dir", str(output_dir),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(
            f"ERROR: regenerate_tables_from_snapshot.py failed:\n{result.stderr}",
            file=sys.stderr,
        )
        sys.exit(result.returncode)


def _compare_tables(snapshot_id: str) -> bool:
    """Regenerate tables and diff against paper tables. Returns True if all match."""
    ok = True
    with tempfile.TemporaryDirectory(prefix="snapshot_check_") as tmp_str:
        tmp_dir = Path(tmp_str)
        _regenerate_into(snapshot_id, tmp_dir)

        for table_name in _CHECKED_TABLES:
            paper_path = _PAPER_TABLES_DIR / table_name
            regen_path = tmp_dir / table_name

            if not paper_path.exists():
                print(
                    f"MISSING: {paper_path} does not exist. "
                    "Run regenerate_tables_from_snapshot.py to create it.",
                    file=sys.stderr,
                )
                ok = False
                continue

            if not regen_path.exists():
                print(f"MISSING: regenerated file not found: {regen_path}", file=sys.stderr)
                ok = False
                continue

            paper_text = paper_path.read_text(encoding="utf-8")
            regen_text = regen_path.read_text(encoding="utf-8")

            if paper_text == regen_text:
                print(f"  OK   : {table_name}")
            else:
                ok = False
                print(f"  FAIL : {table_name} — content differs from snapshot regeneration.")
                _print_diff(paper_text, regen_text, table_name)

    return ok


def _print_diff(paper: str, regen: str, name: str) -> None:
    """Print a compact unified diff between two strings."""
    import difflib

    paper_lines = paper.splitlines(keepends=True)
    regen_lines = regen.splitlines(keepends=True)
    diff = list(
        difflib.unified_diff(
            paper_lines,
            regen_lines,
            fromfile=f"paper/{name}",
            tofile=f"snapshot_regen/{name}",
            n=3,
        )
    )
    if diff:
        print("".join(diff[:60]), file=sys.stderr)
        if len(diff) > 60:
            print(f"  ... ({len(diff) - 60} more diff lines omitted)", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "CI check: verify paper LaTeX tables match the designated benchmark snapshot. "
            "Exits non-zero if any table differs from what the snapshot would produce."
        )
    )
    parser.add_argument(
        "--snapshot",
        default=None,
        help=(
            "Snapshot ID to check against. "
            "Defaults to the designated_snapshot in snapshot_manifest.json."
        ),
    )
    args = parser.parse_args()

    snapshot_id = _resolve_snapshot_id(args.snapshot)
    print(f"Checking tables against snapshot: {snapshot_id}")

    csv_hash = _verify_snapshot_csv_hash(snapshot_id)
    print(f"  Snapshot CSV SHA256: {csv_hash}")
    print(f"  Tables to check    : {', '.join(_CHECKED_TABLES)}")

    all_ok = _compare_tables(snapshot_id)

    if all_ok:
        print("PASS: All paper tables match the designated snapshot.")
        sys.exit(0)
    else:
        print(
            "\nFAIL: One or more paper tables do not match the snapshot.\n"
            "To fix: run  python robotics_maze/scripts/regenerate_tables_from_snapshot.py",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
