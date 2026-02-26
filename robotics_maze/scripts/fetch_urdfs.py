#!/usr/bin/env python3
"""Fetch optional mobile robot URDF sources for local simulation use.

This script only populates robotics_maze/urdfs/external. Simulation code should
continue to use pybullet_data as the default when external assets are missing.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
from typing import Dict, Iterable, Optional, Sequence
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEST = PROJECT_ROOT / "urdfs" / "external"


@dataclass(frozen=True)
class Source:
    name: str
    repo: str
    ref: str
    paths: tuple[str, ...]
    license_note: str
    usage_note: str


SOURCES: Dict[str, Source] = {
    "turtlebot3": Source(
        name="turtlebot3",
        repo="https://github.com/ROBOTIS-GIT/turtlebot3.git",
        ref="main",
        paths=("turtlebot3_description/urdf", "turtlebot3_description/meshes"),
        license_note="Apache-2.0 (check upstream LICENSE for exact terms).",
        usage_note=(
            "Most files are directly loadable URDF; some models still rely on ROS "
            "conventions."
        ),
    ),
    "husky": Source(
        name="husky",
        repo="https://github.com/husky/husky.git",
        ref="noetic-devel",
        paths=("husky_description/urdf", "husky_description/meshes"),
        license_note="BSD-3-Clause style terms (check upstream LICENSE).",
        usage_note=(
            "Primary model is xacro-driven in upstream ROS package; conversion to a "
            "plain URDF may be needed for direct PyBullet loading."
        ),
    ),
}


def run(cmd: Sequence[str], *, cwd: Optional[Path] = None) -> None:
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def repo_slug(repo_url: str) -> str:
    url = repo_url[:-4] if repo_url.endswith(".git") else repo_url
    marker = "github.com/"
    idx = url.find(marker)
    if idx < 0:
        raise ValueError(f"Unsupported repository URL: {repo_url}")
    return url[idx + len(marker) :]


def safe_extract(tar: tarfile.TarFile, destination: Path) -> None:
    base = destination.resolve()
    for member in tar.getmembers():
        candidate = (base / member.name).resolve()
        if candidate != base and base not in candidate.parents:
            raise RuntimeError(f"Unsafe tar member path: {member.name}")
    tar.extractall(destination)


def copy_if_exists(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst)


def copy_selected_paths(repo_root: Path, source: Source, destination: Path) -> None:
    for relative in source.paths:
        src = repo_root / relative
        if not src.exists():
            raise FileNotFoundError(f"Expected path not found: {src}")
        copy_if_exists(src, destination / relative)

    for optional in ("LICENSE", "LICENSE.txt", "README.md"):
        copy_if_exists(repo_root / optional, destination / optional)


def fetch_with_git(source: Source, destination: Path) -> None:
    temp_dir = Path(tempfile.mkdtemp(prefix=f"fetch-urdf-{source.name}-"))
    try:
        run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                source.ref,
                "--filter=blob:none",
                "--sparse",
                source.repo,
                str(temp_dir),
            ]
        )
        run(
            [
                "git",
                "-C",
                str(temp_dir),
                "sparse-checkout",
                "set",
                *source.paths,
                "LICENSE",
                "LICENSE.txt",
                "README.md",
            ]
        )
        copy_selected_paths(temp_dir, source, destination)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def fetch_with_archive(source: Source, destination: Path) -> None:
    slug = repo_slug(source.repo)
    archive_url = f"https://codeload.github.com/{slug}/tar.gz/refs/heads/{source.ref}"

    with tempfile.TemporaryDirectory(prefix=f"fetch-urdf-{source.name}-") as temp_dir:
        temp_path = Path(temp_dir)
        archive_path = temp_path / "source.tar.gz"
        extract_root = temp_path / "extract"
        extract_root.mkdir(parents=True, exist_ok=True)

        with urlopen(archive_url) as response, archive_path.open("wb") as out_file:
            shutil.copyfileobj(response, out_file)

        with tarfile.open(archive_path, "r:gz") as tar:
            safe_extract(tar, extract_root)

        extracted_dirs = [p for p in extract_root.iterdir() if p.is_dir()]
        if not extracted_dirs:
            raise RuntimeError(f"Archive did not contain a source folder: {archive_url}")

        copy_selected_paths(extracted_dirs[0], source, destination)


def write_metadata(destination: Path, source: Source, transport: str) -> None:
    metadata = {
        "source": source.name,
        "repository": source.repo,
        "ref": source.ref,
        "transport": transport,
        "fetched_at_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat(),
        "license_note": source.license_note,
        "usage_note": source.usage_note,
    }
    (destination / "SOURCE.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch optional external URDF sources for mobile robots."
    )
    parser.add_argument(
        "sources",
        nargs="*",
        metavar="SOURCE",
        help=f"Sources to fetch (default: all): {', '.join(SOURCES)}",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        help=f"Target directory (default: {DEFAULT_DEST})",
    )
    parser.add_argument(
        "--transport",
        choices=("auto", "git", "archive"),
        default="auto",
        help="Fetch method: git clone, tarball archive, or auto fallback.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing source folders.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available sources and exit.",
    )
    return parser.parse_args(argv)


def resolve_sources(raw_sources: Iterable[str]) -> list[Source]:
    requested = list(raw_sources)
    if not requested:
        return [SOURCES[name] for name in SOURCES]

    unknown = [name for name in requested if name not in SOURCES]
    if unknown:
        raise ValueError(
            f"Unknown source(s): {', '.join(unknown)}. Valid options: {', '.join(SOURCES)}"
        )
    return [SOURCES[name] for name in requested]


def choose_transport(requested: str) -> str:
    if requested != "auto":
        return requested
    return "git" if shutil.which("git") else "archive"


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)

    if args.list:
        print("Available URDF sources:")
        for key, source in SOURCES.items():
            print(f"- {key}: {source.repo}@{source.ref}")
            print(f"  license: {source.license_note}")
            print(f"  note: {source.usage_note}")
        return 0

    try:
        selected_sources = resolve_sources(args.sources)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    destination_root = args.dest.resolve()
    destination_root.mkdir(parents=True, exist_ok=True)

    for source in selected_sources:
        destination = destination_root / source.name
        if destination.exists():
            if not args.force:
                print(f"skip {source.name}: {destination} already exists (use --force)")
                continue
            shutil.rmtree(destination)
        destination.mkdir(parents=True, exist_ok=True)

        transport = choose_transport(args.transport)
        try:
            if transport == "git":
                fetch_with_git(source, destination)
            else:
                fetch_with_archive(source, destination)
        except Exception:
            if args.transport == "auto" and transport == "git":
                print(
                    f"git fetch failed for {source.name}; retrying with archive download..."
                )
                fetch_with_archive(source, destination)
                transport = "archive"
            else:
                raise

        write_metadata(destination, source, transport)
        print(f"fetched {source.name} -> {destination}")

    print(
        "Done. These assets are optional; keep pybullet_data as default when "
        "external URDF folders are missing."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
