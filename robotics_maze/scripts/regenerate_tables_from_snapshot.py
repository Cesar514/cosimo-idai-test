"""Regenerate paper LaTeX tables from a designated benchmark snapshot.

Usage:
    python robotics_maze/scripts/regenerate_tables_from_snapshot.py
    python robotics_maze/scripts/regenerate_tables_from_snapshot.py --snapshot paper_v1
    python robotics_maze/scripts/regenerate_tables_from_snapshot.py --snapshot paper_v1 --output-dir /tmp/tables
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parents[2]
_SNAPSHOTS_DIR = _REPO_ROOT / "robotics_maze" / "results" / "snapshots"
_PAPER_TABLES_DIR = _REPO_ROOT / "paper" / "ieee_tro_robotics_maze" / "tables"
_SNAPSHOT_MANIFEST = (
    _REPO_ROOT / "paper" / "ieee_tro_robotics_maze" / "coordination" / "snapshot_manifest.json"
)

# Bootstrap parameters that must stay fixed across runs for reproducibility.
_BOOTSTRAP_RESAMPLES = 40_000
_BOOTSTRAP_SEED = 0
_BASELINE_PLANNER = "r1_weighted_astar"

# Display-name mapping used in the LaTeX tables.
_PLANNER_DISPLAY = {
    "astar": "A*",
    "dijkstra": "Dijkstra",
    "greedy_best_first": "Greedy Best-First",
    "r1_weighted_astar": "R1 Weighted A*",
    "r2_bidirectional_astar": "R2 Bidirectional A*",
    "r3_theta_star": r"R3 Theta*",
    "r4_idastar": "R4 IDA*",
    "r5_jump_point_search": "R5 Jump Point Search",
    "r6_lpa_star": "R6 LPA*",
    "r7_beam_search": "R7 Beam Search",
    "r8_fringe_search": "R8 Fringe Search",
    "r9_bidirectional_bfs": "R9 Bidirectional BFS",
}


# ---------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------

def _sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_snapshot_csv(snapshot_id: str) -> tuple[list[dict], str]:
    """Return (rows, csv_sha256) for the given snapshot ID."""
    csv_path = _SNAPSHOTS_DIR / snapshot_id / "benchmark_results.csv"
    if not csv_path.exists():
        sys.exit(f"ERROR: Snapshot CSV not found: {csv_path}")
    digest = _sha256_of_file(csv_path)
    rows: list[dict] = []
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(row)
    return rows, digest


def _verify_snapshot_hash(snapshot_id: str, csv_sha256: str) -> None:
    """Verify CSV hash matches the snapshot_meta.json record."""
    meta_path = _SNAPSHOTS_DIR / snapshot_id / "snapshot_meta.json"
    if not meta_path.exists():
        return  # No metadata to verify against; skip.
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    recorded = meta.get("csv_sha256", "")
    if recorded and recorded != csv_sha256:
        sys.exit(
            f"ERROR: Snapshot '{snapshot_id}' CSV hash mismatch.\n"
            f"  Recorded in snapshot_meta.json : {recorded}\n"
            f"  Actual file hash               : {csv_sha256}\n"
            "The snapshot CSV may have been modified."
        )


# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------

def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    m = _mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def _median(values: list[float]) -> float:
    if not values:
        return math.nan
    s = sorted(values)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def _percentile(values: list[float], pct: float) -> float:
    """Linear interpolation percentile (matches numpy default)."""
    if not values:
        return math.nan
    s = sorted(values)
    n = len(s)
    idx = pct / 100.0 * (n - 1)
    lo = int(idx)
    hi = lo + 1
    frac = idx - lo
    if hi >= n:
        return s[-1]
    return s[lo] * (1 - frac) + s[hi] * frac


def _iqr(values: list[float]) -> tuple[float, float]:
    return _percentile(values, 25), _percentile(values, 75)


# ---------------------------------------------------------------------------
# Bootstrap confidence interval
# ---------------------------------------------------------------------------

def _bootstrap_median_delta_ci(
    baseline_times: list[float],
    comparator_times: list[float],
    n_resamples: int = _BOOTSTRAP_RESAMPLES,
    seed: int = _BOOTSTRAP_SEED,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """Percentile bootstrap CI for median of (comparator - baseline) paired differences."""
    rng = random.Random(seed)
    n = len(baseline_times)
    diffs = [c - b for b, c in zip(baseline_times, comparator_times)]
    bootstrap_medians: list[float] = []
    for _ in range(n_resamples):
        sample = [diffs[rng.randrange(n)] for _ in range(n)]
        bootstrap_medians.append(_median(sample))
    bootstrap_medians.sort()
    lo_idx = int(math.floor((alpha / 2) * n_resamples))
    hi_idx = int(math.ceil((1 - alpha / 2) * n_resamples)) - 1
    hi_idx = min(hi_idx, n_resamples - 1)
    return bootstrap_medians[lo_idx], bootstrap_medians[hi_idx]


# ---------------------------------------------------------------------------
# Paired sign test + Holm correction
# ---------------------------------------------------------------------------

def _sign_test_p(diffs: list[float]) -> float:
    """Exact two-sided paired sign test p-value."""
    n_pos = sum(1 for d in diffs if d > 0)
    n_neg = sum(1 for d in diffs if d < 0)
    n = n_pos + n_neg
    if n == 0:
        return 1.0
    # Binomial(n, 0.5); exact two-sided
    k = min(n_pos, n_neg)
    # Sum P(X <= k) * 2 using exact binomial PMF via logarithms
    log_half_n = n * math.log(0.5)

    def _log_comb(a: int, b: int) -> float:
        if b < 0 or b > a:
            return -math.inf
        if b == 0 or b == a:
            return 0.0
        # Stirling via lgamma
        return math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)

    p_one_tail = sum(
        math.exp(_log_comb(n, i) + log_half_n) for i in range(k + 1)
    )
    return min(1.0, 2.0 * p_one_tail)


def _holm_correct(p_values: list[float]) -> list[float]:
    """Holm-Bonferroni correction. Returns adjusted p-values in original order."""
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted = [0.0] * m
    cummax = 0.0
    for rank, idx in enumerate(order):
        adj = p_values[idx] * (m - rank)
        cummax = max(cummax, adj)
        adjusted[idx] = min(1.0, cummax)
    return adjusted


# ---------------------------------------------------------------------------
# Build per-planner summary from raw CSV rows
# ---------------------------------------------------------------------------

def _parse_rows(csv_rows: list[dict]) -> dict[str, list[dict]]:
    """Group rows by planner, parsing numeric fields."""
    grouped: dict[str, list[dict]] = {}
    for raw in csv_rows:
        p = raw["planner"]
        row = {
            "planner": p,
            "maze_index": int(raw["maze_index"]),
            "success": int(raw["success"]) != 0,
            "solve_time_ms": float(raw["solve_time_ms"]),
            "path_length": int(raw["path_length"]) if raw["path_length"] else None,
            "expansions": int(raw["expansions"]) if raw["expansions"] else None,
        }
        grouped.setdefault(p, []).append(row)
    return grouped


def _shared_success_indices(grouped: dict[str, list[dict]]) -> set[int]:
    """Maze indices solved successfully by ALL planners."""
    per_maze: dict[int, set[str]] = {}
    success_per_maze: dict[int, set[str]] = {}
    for planner, rows in grouped.items():
        for row in rows:
            idx = row["maze_index"]
            per_maze.setdefault(idx, set()).add(planner)
            if row["success"]:
                success_per_maze.setdefault(idx, set()).add(planner)
    planners = set(grouped.keys())
    shared = {
        idx
        for idx, solved in success_per_maze.items()
        if solved == planners and per_maze.get(idx) == planners
    }
    return shared


def _build_main_stats(
    grouped: dict[str, list[dict]], shared_indices: set[int]
) -> list[dict]:
    """Compute per-planner statistics for the main results table."""
    stats: list[dict] = []
    for planner, rows in grouped.items():
        n_total = len(rows)
        n_success = sum(1 for r in rows if r["success"])
        times_all = [r["solve_time_ms"] for r in rows]
        shared_rows = [r for r in rows if r["maze_index"] in shared_indices]
        times_shared = [r["solve_time_ms"] for r in shared_rows]
        path_lengths = [r["path_length"] for r in rows if r["success"] and r["path_length"] is not None]
        shared_path_lengths = [r["path_length"] for r in shared_rows if r["path_length"] is not None]
        expansions = [r["expansions"] for r in rows if r["success"] and r["expansions"] is not None]

        stats.append(
            {
                "planner": planner,
                "n_total": n_total,
                "n_success": n_success,
                "mean_time_ms": _mean(times_all),
                "std_time_ms": _std(times_all),
                "median_time_ms": _median(times_all),
                "q25_time_ms": _percentile(times_all, 25),
                "q75_time_ms": _percentile(times_all, 75),
                "mean_shared_time_ms": _mean(times_shared),
                "mean_path_length": _mean([float(x) for x in path_lengths]),
                "mean_shared_path_length": _mean([float(x) for x in shared_path_lengths]),
                "mean_expansions": _mean([float(x) for x in expansions]),
            }
        )

    # Rank: success rate desc, shared time asc, expansions asc, overall time asc, name asc
    def _rank_key(s: dict) -> tuple:
        sr = s["n_success"] / s["n_total"] if s["n_total"] else 0.0
        cmp_time = s["mean_shared_time_ms"] if not math.isnan(s["mean_shared_time_ms"]) else math.inf
        exp = s["mean_expansions"] if not math.isnan(s["mean_expansions"]) else math.inf
        return (-sr, cmp_time, exp, s["mean_time_ms"], s["planner"])

    stats.sort(key=_rank_key)
    for rank, s in enumerate(stats, start=1):
        s["rank"] = rank
    return stats


def _build_stat_comparison(
    grouped: dict[str, list[dict]],
    baseline_planner: str = _BASELINE_PLANNER,
) -> list[dict]:
    """Compute paired comparison statistics against the baseline planner."""
    if baseline_planner not in grouped:
        sys.exit(f"ERROR: Baseline planner '{baseline_planner}' not found in snapshot CSV.")

    baseline_rows_by_idx = {r["maze_index"]: r for r in grouped[baseline_planner]}
    planners = [p for p in sorted(grouped.keys()) if p != baseline_planner]

    raw_p_values: list[float] = []
    entries: list[dict] = []
    for comp in planners:
        comp_rows_by_idx = {r["maze_index"]: r for r in grouped[comp]}
        common_indices = sorted(
            set(baseline_rows_by_idx.keys()) & set(comp_rows_by_idx.keys())
        )
        if not common_indices:
            continue
        base_times = [baseline_rows_by_idx[i]["solve_time_ms"] for i in common_indices]
        comp_times = [comp_rows_by_idx[i]["solve_time_ms"] for i in common_indices]
        diffs = [c - b for b, c in zip(base_times, comp_times)]
        median_delta = _median(diffs)
        ci_lo, ci_hi = _bootstrap_median_delta_ci(base_times, comp_times)
        slower = sum(1 for d in diffs if d > 0)
        faster = sum(1 for d in diffs if d < 0)
        p_val = _sign_test_p(diffs)
        raw_p_values.append(p_val)
        entries.append(
            {
                "planner": comp,
                "median_delta_ms": median_delta,
                "ci_lo_ms": ci_lo,
                "ci_hi_ms": ci_hi,
                "slower": slower,
                "faster": faster,
                "p_value": p_val,
                "n_pairs": len(common_indices),
            }
        )

    holm_p = _holm_correct(raw_p_values)
    for entry, adj in zip(entries, holm_p):
        entry["holm_p"] = adj

    # Sort by median_delta ascending (matching current table order)
    entries.sort(key=lambda e: e["median_delta_ms"])
    return entries


# ---------------------------------------------------------------------------
# LaTeX table rendering
# ---------------------------------------------------------------------------

def _sci_notation(value: float) -> str:
    """Format a small p-value in LaTeX scientific notation, e.g. 1.95e-14."""
    if value >= 0.001:
        return f"{value:.3f}"
    exp = int(math.floor(math.log10(abs(value)))) if value > 0 else 0
    mantissa = value / (10 ** exp)
    return rf"\({mantissa:.2f}\times10^{{{exp}}}\)"


def _theta_star_footnote(planner: str) -> str:
    return r"$^\dagger$" if planner == "r3_theta_star" else ""


def render_main_results_table(stats: list[dict], maze_count: int) -> str:
    lines: list[str] = [
        r"\begin{table*}[t]",
        r"\centering",
        (
            r"\caption{Main benchmark results on "
            + str(maze_count)
            + r" generated \(15\times15\) backtracker mazes. "
            r"Rows are ranked by success rate (descending), then comparable mean solve time on shared-success mazes, "
            r"mean expansions, and overall mean solve time (ascending), with planner name as deterministic tie-break. "
            r"Time is reported as mean \(\pm\) standard deviation over mazes; median and interquartile range (IQR) "
            r"are included to expose skew. Lower is better for time, path length, and expansions.}"
        ),
        r"\label{tab:main_results}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{4.2pt}",
        r"\begin{tabular}{clccccc}",
        r"\toprule",
        r"Rank & Planner & Success & Time (ms) $\downarrow$ & Median [IQR] (ms) $\downarrow$ & Path Length $\downarrow$ & Expansions $\downarrow$ \\",
        r"\midrule",
    ]

    for s in stats:
        rank = s["rank"]
        display = _PLANNER_DISPLAY.get(s["planner"], s["planner"])
        success_str = f"{s['n_success']}/{s['n_total']}"
        path_len = s["mean_shared_path_length"] if not math.isnan(s["mean_shared_path_length"]) else s["mean_path_length"]
        path_str = f"{path_len:.2f}" + _theta_star_footnote(s["planner"])
        lines.append(
            f"{rank:<2} & {display:<22} & {success_str} "
            f"& {s['mean_time_ms']:.2f} $\\pm$ {s['std_time_ms']:.2f}"
            f"   & {s['median_time_ms']:.2f} [{s['q25_time_ms']:.2f}, {s['q75_time_ms']:.2f}]"
            f"   & {path_str:<17}"
            f"& {s['mean_expansions']:.2f}  \\\\"
        )

    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        "",
        r"{\raggedright\footnotesize $^\dagger$Theta* uses any-angle motion, so path-length values are not directly comparable to cardinal-grid planners.\par}",
        r"\end{table*}",
    ]
    return "\n".join(lines) + "\n"


def render_statistical_comparison_table(entries: list[dict]) -> str:
    lines: list[str] = [
        r"\begin{table*}[t]",
        r"\centering",
        (
            r"\caption{Exploratory paired runtime comparisons against "
            r"\texttt{r1\_weighted\_astar} on the same mazes (single run per planner-maze pair). "
            r"Positive \(\Delta\) means the comparator is slower. "
            r"Confidence intervals are percentile bootstrap intervals from 40{,}000 paired resamples (fixed seed). "
            r"\(p\)-values are exact two-sided paired sign tests with Holm correction across "
            + str(len(entries))
            + r" comparisons.}"
        ),
        r"\label{tab:runtime_statistical_comparison}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{4.0pt}",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"Comparator & Median \(\Delta\) (ms) & 95\% CI for \(\Delta\) (ms) & Slower/Faster (of "
        + str(entries[0]["n_pairs"] if entries else 0)
        + r") & Holm-adjusted \(p\) \\",
        r"\midrule",
    ]

    for e in entries:
        display = _PLANNER_DISPLAY.get(e["planner"], e["planner"])
        delta_str = f"{e['median_delta_ms']:.3f}"
        ci_str = f"[{e['ci_lo_ms']:.3f}, {e['ci_hi_ms']:.3f}]"
        sf_str = f"{e['slower']}/{e['faster']}"
        p_str = _sci_notation(e["holm_p"])
        lines.append(f"{display:<22} & {delta_str:<7} & {ci_str:<20} & {sf_str:<6} & {p_str} \\\\")

    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table*}",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def regenerate_tables(snapshot_id: str, output_dir: Path) -> None:
    print(f"Loading snapshot: {snapshot_id}")
    csv_rows, csv_sha256 = load_snapshot_csv(snapshot_id)
    _verify_snapshot_hash(snapshot_id, csv_sha256)
    print(f"  CSV SHA256 : {csv_sha256}")
    print(f"  Rows loaded: {len(csv_rows)}")

    grouped = _parse_rows(csv_rows)
    planners_found = sorted(grouped.keys())
    print(f"  Planners   : {', '.join(planners_found)}")

    shared_indices = _shared_success_indices(grouped)
    maze_count_csv = len({r["maze_index"] for rows in grouped.values() for r in rows})
    print(f"  Mazes      : {maze_count_csv}  |  Shared-success: {len(shared_indices)}")

    stats = _build_main_stats(grouped, shared_indices)
    comparison = _build_stat_comparison(grouped)

    output_dir.mkdir(parents=True, exist_ok=True)

    main_tex = output_dir / "main_results_table.tex"
    main_tex.write_text(render_main_results_table(stats, maze_count_csv), encoding="utf-8")
    print(f"  Written    : {main_tex}")

    stat_tex = output_dir / "statistical_comparison_table.tex"
    stat_tex.write_text(render_statistical_comparison_table(comparison), encoding="utf-8")
    print(f"  Written    : {stat_tex}")

    print("Done.")


def _resolve_snapshot_id() -> str:
    if _SNAPSHOT_MANIFEST.exists():
        manifest = json.loads(_SNAPSHOT_MANIFEST.read_text(encoding="utf-8"))
        return str(manifest["designated_snapshot"])
    # Default fallback
    return "paper_v1"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate paper LaTeX tables from a frozen benchmark snapshot."
    )
    parser.add_argument(
        "--snapshot",
        default=None,
        help=(
            "Snapshot ID (sub-directory name under robotics_maze/results/snapshots/). "
            "Defaults to the designated_snapshot in paper coordination snapshot_manifest.json."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Directory where regenerated .tex files are written. "
            "Defaults to paper/ieee_tro_robotics_maze/tables/."
        ),
    )
    args = parser.parse_args()

    snapshot_id = args.snapshot or _resolve_snapshot_id()
    output_dir = Path(args.output_dir) if args.output_dir else _PAPER_TABLES_DIR
    regenerate_tables(snapshot_id, output_dir)


if __name__ == "__main__":
    main()
