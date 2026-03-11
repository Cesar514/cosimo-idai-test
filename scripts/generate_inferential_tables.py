#!/usr/bin/env python3
"""Generate inferential runtime comparison tables from a benchmark CSV.

Produces:
  1. ``coordination/inferential_runtime_comparison.csv``  – paired bootstrap CIs,
     sign-test p-values, and Holm-adjusted p-values for every non-baseline planner.
  2. ``tables/statistical_comparison_table.tex``  – IEEEtran-ready LaTeX table.

Usage example (from repo root)::

    python scripts/generate_inferential_tables.py \\
        --input  robotics_maze/results/benchmark_results.csv \\
        --output-csv  paper/ieee_tro_robotics_maze/coordination/inferential_runtime_comparison.csv \\
        --output-tex  paper/ieee_tro_robotics_maze/tables/statistical_comparison_table.tex \\
        --baseline r1_weighted_astar \\
        --seed 42 \\
        --bootstrap-resamples 40000

Reproducibility guarantee
--------------------------
Fixed ``--seed`` ensures identical bootstrap samples on every run.
Running the script on the same benchmark CSV snapshot always produces
byte-identical output files.

Metadata written to stdout (seed, bootstrap count, timestamp).
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timezone
from math import comb
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Optional numpy import (required for bootstrap resampling)
# ---------------------------------------------------------------------------
try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:  # pragma: no cover
    _HAS_NUMPY = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_benchmark_csv(path: Path) -> list[dict[str, Any]]:
    """Load benchmark CSV rows, coercing numeric columns."""
    rows: list[dict[str, Any]] = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                row["solve_time_ms"] = float(row["solve_time_ms"])
                row["maze_index"] = int(row["maze_index"])
                row["success"] = int(row["success"])
            except (KeyError, ValueError) as exc:
                raise ValueError(
                    f"Malformed row in {path}: {exc!r}  row={dict(row)}"
                ) from exc
            rows.append(row)
    return rows


def _build_paired_deltas(
    rows: list[dict[str, Any]],
    baseline: str,
) -> dict[str, list[float]]:
    """Return {planner: [delta_ms_per_maze]} for all non-baseline planners.

    delta = comparator_time - baseline_time  (positive ⟹ comparator is slower)
    Only mazes where BOTH the baseline and the comparator succeeded are included.
    """
    # Index baseline times by maze_index
    baseline_times: dict[int, float] = {}
    for row in rows:
        if row["planner"] == baseline and row["success"] == 1:
            baseline_times[row["maze_index"]] = row["solve_time_ms"]

    # Group comparator times by planner → maze_index
    comparator_times: dict[str, dict[int, float]] = {}
    for row in rows:
        if row["planner"] == baseline:
            continue
        if row["success"] != 1:
            continue
        comparator_times.setdefault(row["planner"], {})[row["maze_index"]] = (
            row["solve_time_ms"]
        )

    paired_deltas: dict[str, list[float]] = {}
    for planner, times in comparator_times.items():
        common_mazes = sorted(set(times) & set(baseline_times))
        paired_deltas[planner] = [
            times[m] - baseline_times[m] for m in common_mazes
        ]
    return paired_deltas


def _sanity_checks(
    paired_deltas: dict[str, list[float]],
    rows: list[dict[str, Any]],
    baseline: str,
    expected_planners: int | None,
    expected_mazes: int | None,
) -> None:
    """Raise ValueError on failed sanity checks."""
    all_planners = {r["planner"] for r in rows}
    if baseline not in all_planners:
        raise ValueError(
            f"Baseline planner '{baseline}' not found in CSV. "
            f"Available planners: {sorted(all_planners)}"
        )
    if not paired_deltas:
        raise ValueError(
            "No comparator planners found after pairing. "
            "Check that the CSV contains planners other than the baseline."
        )

    # Planner count check
    actual_planner_count = len(paired_deltas) + 1  # +1 for baseline itself
    if expected_planners is not None and actual_planner_count != expected_planners:
        raise ValueError(
            f"Expected {expected_planners} planners (including baseline), "
            f"found {actual_planner_count}."
        )

    # Paired maze count check
    maze_counts = {p: len(d) for p, d in paired_deltas.items()}
    min_mazes = min(maze_counts.values()) if maze_counts else 0
    max_mazes = max(maze_counts.values()) if maze_counts else 0
    if min_mazes != max_mazes:
        unequal = {p: c for p, c in maze_counts.items() if c != max_mazes}
        raise ValueError(
            f"Unequal paired maze counts across planners: {unequal}. "
            "All comparators must share the same set of paired mazes."
        )
    if expected_mazes is not None and min_mazes != expected_mazes:
        raise ValueError(
            f"Expected {expected_mazes} paired mazes per comparator, "
            f"found {min_mazes}."
        )
    if min_mazes < 1:
        raise ValueError(
            "No paired mazes found. Check that baseline and comparators "
            "share common maze_index values with success=1."
        )


def _bootstrap_median_ci(
    deltas: list[float],
    n_resamples: int,
    rng: "np.random.Generator",
) -> tuple[float, float, float]:
    """Return (median, ci95_low, ci95_high) via percentile bootstrap."""
    arr = np.asarray(deltas, dtype=np.float64)
    samples = rng.choice(arr, size=(n_resamples, len(arr)), replace=True)
    boot_medians = np.median(samples, axis=1)
    ci_low = float(np.percentile(boot_medians, 2.5))
    ci_high = float(np.percentile(boot_medians, 97.5))
    median = float(np.median(arr))
    return median, ci_low, ci_high


def _sign_test_two_sided(deltas: list[float]) -> float:
    """Exact two-sided paired sign test p-value (ties excluded)."""
    slower = sum(1 for d in deltas if d > 0)
    faster = sum(1 for d in deltas if d < 0)
    n = slower + faster
    if n == 0:
        return 1.0
    k_min = min(slower, faster)
    p = 2.0 * sum(comb(n, i) * (0.5 ** n) for i in range(k_min + 1))
    return min(p, 1.0)


def _holm_correction(p_values: list[float]) -> list[float]:
    """Holm-Bonferroni correction.  Returns adjusted p-values in original order."""
    m = len(p_values)
    if m == 0:
        return []
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    adjusted = [0.0] * m
    running_max = 0.0
    for rank, (orig_idx, pval) in enumerate(indexed, start=1):
        adj = min(1.0, pval * (m - rank + 1))
        running_max = max(running_max, adj)
        adjusted[orig_idx] = running_max
    return adjusted


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

_CSV_FIELDNAMES = [
    "planner",
    "median_delta_ms",
    "ci95_low_ms",
    "ci95_high_ms",
    "slower_count",
    "faster_count",
    "sign_test_p_two_sided",
    "holm_adjusted_p",
    "bootstrap_resamples",
    "baseline_planner",
]


def _write_inferential_csv(
    results: list[dict[str, Any]],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=_CSV_FIELDNAMES)
        writer.writeheader()
        for row in results:
            writer.writerow({k: row[k] for k in _CSV_FIELDNAMES})


def _planner_display_name(planner: str) -> str:
    """Human-readable display name for a planner identifier."""
    _MAP = {
        "r1_weighted_astar": "R1 Weighted A*",
        "r2_bidirectional_astar": "R2 Bidirectional A*",
        "r3_theta_star": "R3 Theta*",
        "r4_idastar": "R4 IDA*",
        "r5_jump_point_search": "R5 Jump Point Search",
        "r6_lpa_star": "R6 LPA*",
        "r7_beam_search": "R7 Beam Search",
        "r8_fringe_search": "R8 Fringe Search",
        "r9_bidirectional_bfs": "R9 Bidirectional BFS",
        "astar": "A*",
        "dijkstra": "Dijkstra",
        "greedy_best_first": "Greedy Best-First",
    }
    return _MAP.get(planner, planner.replace("_", " ").title())


def _fmt_p(p: float) -> str:
    """Format p-value for LaTeX in scientific notation."""
    if p >= 0.001:
        return f"{p:.3f}"
    import math
    exp = int(math.floor(math.log10(p))) if p > 0 else -308
    mantissa = p / (10 ** exp)
    return rf"\({mantissa:.2f}\times10^{{{exp}}}\)"


def _write_latex_table(
    results: list[dict[str, Any]],
    output_path: Path,
    baseline: str,
    n_mazes: int,
    n_resamples: int,
) -> None:
    """Write the statistical comparison LaTeX table."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    baseline_tex = baseline.replace("_", r"\_")
    lines: list[str] = [
        r"\begin{table*}[t]",
        r"\centering",
        (
            r"\caption{Exploratory paired runtime comparisons against "
            rf"\texttt{{{baseline_tex}}} on the same {n_mazes} mazes "
            r"(single run per planner-maze pair). "
            r"Positive \(\Delta\) means the comparator is slower. "
            "Confidence intervals are percentile bootstrap intervals from "
            rf"{n_resamples:,}".replace(",", r"{,}")
            + r" paired resamples (fixed seed). "
            r"\(p\)-values are exact two-sided paired sign tests with Holm "
            rf"correction across {len(results)} comparisons."
            + "}"
        ),
        r"\label{tab:runtime_statistical_comparison}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{4.0pt}",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"Comparator & Median \(\Delta\) (ms) & 95\% CI for \(\Delta\) (ms) "
        r"& Slower/Faster (of " + str(n_mazes) + r") & Holm-adjusted \(p\) \\",
        r"\midrule",
    ]

    for row in results:
        name = _planner_display_name(row["planner"])
        med = row["median_delta_ms"]
        ci_lo = row["ci95_low_ms"]
        ci_hi = row["ci95_high_ms"]
        slower = int(row["slower_count"])
        faster = int(row["faster_count"])
        holm_p = row["holm_adjusted_p"]

        # Format with 3 decimal places regardless of magnitude
        med_str = f"{med:.3f}"
        ci_str = f"[{ci_lo:.3f}, {ci_hi:.3f}]"

        p_str = _fmt_p(holm_p)
        lines.append(
            f"{name:<24} & {med_str:<6} & {ci_str:<22} "
            f"& {slower}/{faster} & {p_str} \\\\"
        )

    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table*}",
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def run_pipeline(
    input_path: Path,
    output_csv: Path,
    output_tex: Path,
    baseline: str,
    seed: int,
    n_resamples: int,
    expected_planners: int | None,
    expected_mazes: int | None,
) -> list[dict[str, Any]]:
    """Execute the full bootstrap/sign-test/Holm pipeline.

    Returns the list of result dicts (one per comparator planner).
    """
    if not _HAS_NUMPY:
        raise ImportError(
            "numpy is required for bootstrap resampling. "
            "Install it with:  pip install numpy"
        )

    rows = _read_benchmark_csv(input_path)
    paired_deltas = _build_paired_deltas(rows, baseline)
    _sanity_checks(paired_deltas, rows, baseline, expected_planners, expected_mazes)

    rng = np.random.default_rng(seed)
    raw_p_values: list[float] = []
    intermediate: list[dict[str, Any]] = []

    # Sort planners for deterministic ordering
    for planner in sorted(paired_deltas):
        deltas = paired_deltas[planner]
        median, ci_low, ci_high = _bootstrap_median_ci(deltas, n_resamples, rng)
        sign_p = _sign_test_two_sided(deltas)
        slower = sum(1 for d in deltas if d > 0)
        faster = sum(1 for d in deltas if d < 0)
        raw_p_values.append(sign_p)
        intermediate.append(
            {
                "planner": planner,
                "median_delta_ms": median,
                "ci95_low_ms": ci_low,
                "ci95_high_ms": ci_high,
                "slower_count": slower,
                "faster_count": faster,
                "sign_test_p_two_sided": sign_p,
                "bootstrap_resamples": n_resamples,
                "baseline_planner": baseline,
            }
        )

    holm_ps = _holm_correction(raw_p_values)
    for record, adj_p in zip(intermediate, holm_ps):
        record["holm_adjusted_p"] = adj_p

    n_mazes = len(next(iter(paired_deltas.values())))

    _write_inferential_csv(intermediate, output_csv)
    _write_latex_table(intermediate, output_tex, baseline, n_mazes, n_resamples)
    return intermediate


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    _repo_root = Path(__file__).resolve().parents[1]
    default_input = _repo_root / "robotics_maze" / "results" / "benchmark_results.csv"
    default_csv = (
        _repo_root
        / "paper"
        / "ieee_tro_robotics_maze"
        / "coordination"
        / "inferential_runtime_comparison.csv"
    )
    default_tex = (
        _repo_root
        / "paper"
        / "ieee_tro_robotics_maze"
        / "tables"
        / "statistical_comparison_table.tex"
    )
    parser = argparse.ArgumentParser(
        description=(
            "Generate inferential runtime comparison CSV and LaTeX table "
            "from a benchmark results CSV."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input,
        help="Path to benchmark_results.csv produced by the benchmark harness.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=default_csv,
        help="Destination path for inferential_runtime_comparison.csv.",
    )
    parser.add_argument(
        "--output-tex",
        type=Path,
        default=default_tex,
        help="Destination path for statistical_comparison_table.tex.",
    )
    parser.add_argument(
        "--baseline",
        default="r1_weighted_astar",
        help="Planner name used as the paired baseline.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="RNG seed for bootstrap resampling (fixed for reproducibility).",
    )
    parser.add_argument(
        "--bootstrap-resamples",
        type=int,
        default=40000,
        help="Number of bootstrap resamples for confidence intervals.",
    )
    parser.add_argument(
        "--expect-planners",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Expected total planner count (including baseline). "
            "Raises an error if the CSV contains a different count."
        ),
    )
    parser.add_argument(
        "--expect-mazes",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Expected number of paired mazes per comparator. "
            "Raises an error if the CSV contains a different count."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    generated_at = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
    print(f"[generate_inferential_tables] started at {generated_at} UTC")
    print(f"  input:              {args.input}")
    print(f"  output-csv:         {args.output_csv}")
    print(f"  output-tex:         {args.output_tex}")
    print(f"  baseline:           {args.baseline}")
    print(f"  seed:               {args.seed}")
    print(f"  bootstrap-resamples:{args.bootstrap_resamples}")

    try:
        results = run_pipeline(
            input_path=args.input,
            output_csv=args.output_csv,
            output_tex=args.output_tex,
            baseline=args.baseline,
            seed=args.seed,
            n_resamples=args.bootstrap_resamples,
            expected_planners=args.expect_planners,
            expected_mazes=args.expect_mazes,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"  comparators processed: {len(results)}")
    print(f"Wrote: {args.output_csv}")
    print(f"Wrote: {args.output_tex}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
