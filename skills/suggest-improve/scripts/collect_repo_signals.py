#!/usr/bin/env python3
"""
Collect lightweight, read-only repository signals to support a quality/optimization review.

This script is intentionally conservative:
- Avoids modifying the repo
- Avoids executing repo-defined scripts (tests/lints/builds) by default
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


DEFAULT_IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "out",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".turbo",
    ".cache",
    ".parcel-cache",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "__pycache__",
    ".idea",
    ".vscode",
    "target",
    "vendor",
}


def _run(cmd: list[str], cwd: Path) -> str | None:
    try:
        out = subprocess.check_output(cmd, cwd=str(cwd), stderr=subprocess.STDOUT, text=True)
        return out.strip()
    except Exception:
        return None


def _safe_read_text(path: Path, max_bytes: int = 512_000) -> str | None:
    try:
        data = path.read_bytes()
    except Exception:
        return None
    if len(data) > max_bytes:
        data = data[:max_bytes]
    try:
        return data.decode("utf-8", errors="replace")
    except Exception:
        return None


def _iter_files(repo_root: Path, ignore_dirs: set[str], max_files: int | None) -> Iterable[Path]:
    seen = 0
    for dirpath, dirnames, filenames in os.walk(repo_root):
        if max_files is not None and seen >= max_files:
            return

        # Prune ignored dirs in-place
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        for filename in filenames:
            if max_files is not None and seen >= max_files:
                return
            seen += 1
            yield Path(dirpath) / filename


def _ext(path: Path) -> str:
    # Treat "Dockerfile" etc as extensionless
    suf = path.suffix.lower()
    return suf[1:] if suf.startswith(".") else ""


@dataclass(frozen=True)
class GitInfo:
    is_repo: bool
    branch: str | None
    head_sha: str | None
    status_porcelain_count: int | None
    remote_origin: str | None


@dataclass(frozen=True)
class PackageJsonInfo:
    path: str
    name: str | None
    private: bool | None
    type: str | None
    scripts: list[str]
    dependencies_count: int | None
    dev_dependencies_count: int | None


@dataclass(frozen=True)
class RepoSignals:
    repo_root: str
    platform: dict[str, str]
    git: GitInfo
    file_counts_total: int
    file_counts_by_ext: list[dict[str, Any]]
    largest_files: list[dict[str, Any]]
    todo_like_counts: dict[str, int]
    configs_present: list[str]
    package_json: list[PackageJsonInfo]


def _collect_git(repo_root: Path) -> GitInfo:
    is_repo = (_run(["git", "rev-parse", "--is-inside-work-tree"], repo_root) == "true")
    if not is_repo:
        return GitInfo(
            is_repo=False,
            branch=None,
            head_sha=None,
            status_porcelain_count=None,
            remote_origin=None,
        )
    branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_root)
    head_sha = _run(["git", "rev-parse", "HEAD"], repo_root)
    status = _run(["git", "status", "--porcelain"], repo_root)
    status_count = None if status is None else (0 if status == "" else len(status.splitlines()))
    remote_origin = _run(["git", "remote", "get-url", "origin"], repo_root)
    return GitInfo(
        is_repo=True,
        branch=branch,
        head_sha=head_sha,
        status_porcelain_count=status_count,
        remote_origin=remote_origin,
    )


def _collect_package_json(repo_root: Path) -> list[PackageJsonInfo]:
    infos: list[PackageJsonInfo] = []
    for path in sorted(repo_root.glob("**/package.json")):
        # Skip common vendor dirs quickly
        if any(part in DEFAULT_IGNORE_DIRS for part in path.parts):
            continue
        raw = _safe_read_text(path)
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue
        scripts = sorted(list((data.get("scripts") or {}).keys()))
        deps = data.get("dependencies") or {}
        dev_deps = data.get("devDependencies") or {}
        infos.append(
            PackageJsonInfo(
                path=str(path.relative_to(repo_root)),
                name=data.get("name"),
                private=data.get("private"),
                type=data.get("type"),
                scripts=scripts,
                dependencies_count=len(deps) if isinstance(deps, dict) else None,
                dev_dependencies_count=len(dev_deps) if isinstance(dev_deps, dict) else None,
            )
        )
    return infos


def _find_configs(repo_root: Path) -> list[str]:
    candidates = [
        "README.md",
        "README.MD",
        "README.txt",
        "README",
        "CONTRIBUTING.md",
        "CODEOWNERS",
        ".editorconfig",
        ".prettierrc",
        ".prettierrc.json",
        ".prettierrc.yml",
        ".prettierrc.yaml",
        "prettier.config.js",
        ".eslintrc",
        ".eslintrc.json",
        ".eslintrc.js",
        ".eslintrc.cjs",
        "eslint.config.js",
        "eslint.config.mjs",
        "eslint.config.cjs",
        "tsconfig.json",
        "tsconfig.base.json",
        "biome.json",
        "biome.jsonc",
        ".ruff.toml",
        "ruff.toml",
        "pyproject.toml",
        "mypy.ini",
        "pytest.ini",
        "tox.ini",
        ".github/workflows",
        ".gitlab-ci.yml",
        "azure-pipelines.yml",
        "Makefile",
        "justfile",
    ]
    present: list[str] = []
    for c in candidates:
        p = repo_root / c
        if p.exists():
            present.append(c + ("/" if p.is_dir() else ""))
    return present


def _count_todo_like(paths: Iterable[Path], repo_root: Path) -> dict[str, int]:
    markers = ["TODO", "FIXME", "HACK", "XXX"]
    counts = {m: 0 for m in markers}

    for path in paths:
        # Skip binaries and very large files
        try:
            st = path.stat()
        except Exception:
            continue
        if st.st_size > 2_000_000:
            continue
        raw = _safe_read_text(path, max_bytes=256_000)
        if raw is None:
            continue
        # Rough binary heuristic
        if "\x00" in raw:
            continue
        upper = raw.upper()
        for m in markers:
            counts[m] += upper.count(m)

    return counts


def _format_bytes(n: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    f = float(n)
    for u in units:
        if f < 1024 or u == units[-1]:
            if u == "B":
                return f"{int(f)} {u}"
            return f"{f:.1f} {u}"
        f /= 1024
    return f"{n} B"


def _to_md(signals: RepoSignals) -> str:
    lines: list[str] = []
    lines.append("# Repo Signals")
    lines.append("")
    lines.append("## Environment")
    lines.append(f"- OS: {signals.platform.get('system')} {signals.platform.get('release')}")
    lines.append(f"- Python: {signals.platform.get('python')}")
    lines.append("")
    lines.append("## Git")
    if not signals.git.is_repo:
        lines.append("- Not a git repo (or git unavailable).")
    else:
        lines.append(f"- Branch: {signals.git.branch}")
        lines.append(f"- HEAD: {signals.git.head_sha}")
        lines.append(f"- Dirty files: {signals.git.status_porcelain_count}")
        if signals.git.remote_origin:
            lines.append(f"- origin: `{signals.git.remote_origin}`")
    lines.append("")
    lines.append("## Files")
    lines.append(f"- Total files scanned: {signals.file_counts_total}")
    lines.append("- Top extensions:")
    for row in signals.file_counts_by_ext[:15]:
        lines.append(f"  - .{row['ext'] or '(none)'}: {row['count']}")
    lines.append("")
    lines.append("## Largest files (top 15)")
    for lf in signals.largest_files[:15]:
        lines.append(f"- {lf['size_human']}: `{lf['path']}`")
    lines.append("")
    lines.append("## TODO-like markers (rough count)")
    for k, v in signals.todo_like_counts.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Tooling / configs present")
    for c in signals.configs_present:
        lines.append(f"- `{c}`")
    lines.append("")
    if signals.package_json:
        lines.append("## package.json")
        for pkg in signals.package_json[:10]:
            lines.append(f"- `{pkg.path}`")
            if pkg.name:
                lines.append(f"  - name: `{pkg.name}`")
            if pkg.scripts:
                lines.append("  - scripts:")
                for s in pkg.scripts[:25]:
                    lines.append(f"    - `{s}`")
            lines.append(
                "  - deps:"
                f" dependencies={pkg.dependencies_count}, devDependencies={pkg.dev_dependencies_count}"
            )
        if len(signals.package_json) > 10:
            lines.append(f"- (plus {len(signals.package_json) - 10} more package.json files)")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Collect lightweight repo signals (read-only).")
    parser.add_argument("repo_root", nargs="?", default=".", help="Repository root (default: .)")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Optional cap on files scanned (useful for very large repos)",
    )
    parser.add_argument(
        "--ignore-dir",
        action="append",
        default=[],
        help="Additional directory name to ignore (repeatable)",
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    ignore_dirs = set(DEFAULT_IGNORE_DIRS) | set(args.ignore_dir or [])

    files = list(_iter_files(repo_root, ignore_dirs=ignore_dirs, max_files=args.max_files))

    by_ext: dict[str, int] = {}
    largest: list[tuple[int, Path]] = []
    for p in files:
        ex = _ext(p)
        by_ext[ex] = by_ext.get(ex, 0) + 1
        try:
            st = p.stat()
        except Exception:
            continue
        largest.append((st.st_size, p))
    largest.sort(key=lambda t: t[0], reverse=True)

    signals = RepoSignals(
        repo_root=str(repo_root),
        platform={
            "system": platform.system(),
            "release": platform.release(),
            "python": sys.version.split()[0],
        },
        git=_collect_git(repo_root),
        file_counts_total=len(files),
        file_counts_by_ext=[
            {"ext": ext, "count": count}
            for ext, count in sorted(by_ext.items(), key=lambda kv: kv[1], reverse=True)
        ],
        largest_files=[
            {
                "path": str(path.relative_to(repo_root)),
                "size_bytes": size,
                "size_human": _format_bytes(size),
            }
            for size, path in largest[:50]
        ],
        todo_like_counts=_count_todo_like(files, repo_root=repo_root),
        configs_present=_find_configs(repo_root),
        package_json=_collect_package_json(repo_root),
    )

    if args.format == "json":
        print(json.dumps(asdict(signals), indent=2, sort_keys=True))
    else:
        print(_to_md(signals))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
