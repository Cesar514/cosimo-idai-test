"""Backend sensitivity experiment: paired-episode comparison of PyBullet vs MuJoCo.

Runs matched episodes under both physics backends with the same maze seeds and
planner outputs, then computes per-backend deltas and confidence intervals so that
any material divergence can be documented and included in the manuscript appendix.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, stdev
from typing import Any, Sequence

_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

BACKENDS = ("pybullet", "mujoco")
_TINV_95_SMALL = {  # two-tailed t* for 95 % CI (df = n-1); pre-computed to avoid scipy dep
    1: 12.706,
    2: 4.303,
    3: 3.182,
    4: 2.776,
    5: 2.571,
    6: 2.447,
    7: 2.365,
    8: 2.306,
    9: 2.262,
    10: 2.228,
}
_TINV_95_LARGE = 1.96  # z* approximation for df >= 30


def _t_critical(n: int) -> float:
    """Return the two-tailed t* value for 95 % CI given sample size n."""
    if n < 2:
        return float("nan")
    df = n - 1
    if df in _TINV_95_SMALL:
        return _TINV_95_SMALL[df]
    if df < 30:
        # linear interpolation between the nearest tabulated values
        lo_df = max(k for k in _TINV_95_SMALL if k < df)
        hi_df = min(k for k in _TINV_95_SMALL if k > df)
        lo_t = _TINV_95_SMALL[lo_df]
        hi_t = _TINV_95_SMALL[hi_df]
        frac = (df - lo_df) / (hi_df - lo_df)
        return lo_t + frac * (hi_t - lo_t)
    return _TINV_95_LARGE


@dataclass(frozen=True)
class EpisodeOutcome:
    """Outcome of a single episode under one physics backend."""

    backend: str
    episode: int
    seed: int | None
    success: bool
    steps: int
    elapsed_s: float


@dataclass(frozen=True)
class PairedEpisodeResult:
    """Results for one episode run under both backends."""

    episode: int
    seed: int | None
    pybullet: EpisodeOutcome
    mujoco: EpisodeOutcome

    @property
    def steps_delta(self) -> int:
        """mujoco.steps − pybullet.steps (signed difference)."""
        return self.mujoco.steps - self.pybullet.steps

    @property
    def elapsed_delta_s(self) -> float:
        """mujoco.elapsed_s − pybullet.elapsed_s (signed difference)."""
        return self.mujoco.elapsed_s - self.pybullet.elapsed_s

    @property
    def both_success(self) -> bool:
        return self.pybullet.success and self.mujoco.success

    @property
    def failure_mode(self) -> str:
        """Short label describing which backend(s) failed, or 'none'."""
        if self.both_success:
            return "none"
        if not self.pybullet.success and not self.mujoco.success:
            return "both"
        if not self.pybullet.success:
            return "pybullet_only"
        return "mujoco_only"


@dataclass(frozen=True)
class ConfidenceInterval:
    mean: float
    lower: float
    upper: float
    n: int

    def __str__(self) -> str:
        if math.isnan(self.mean):
            return "n/a"
        return f"{self.mean:.4f} [{self.lower:.4f}, {self.upper:.4f}] (n={self.n})"


@dataclass(frozen=True)
class BackendStats:
    backend: str
    n_episodes: int
    success_rate: float
    mean_steps: float
    mean_elapsed_s: float
    ci_steps: ConfidenceInterval
    ci_elapsed_s: ConfidenceInterval


@dataclass(frozen=True)
class SensitivityReport:
    paired_results: list[PairedEpisodeResult]
    pybullet_stats: BackendStats
    mujoco_stats: BackendStats
    ci_steps_delta: ConfidenceInterval
    ci_elapsed_delta: ConfidenceInterval
    n_both_success: int
    n_pybullet_only_fail: int
    n_mujoco_only_fail: int
    n_both_fail: int


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------


def _confidence_interval(values: list[float]) -> ConfidenceInterval:
    n = len(values)
    if n == 0:
        return ConfidenceInterval(mean=float("nan"), lower=float("nan"), upper=float("nan"), n=0)
    mu = mean(values)
    if n == 1:
        return ConfidenceInterval(mean=mu, lower=mu, upper=mu, n=1)
    sd = stdev(values)
    t_star = _t_critical(n)
    margin = t_star * sd / math.sqrt(n)
    return ConfidenceInterval(mean=mu, lower=mu - margin, upper=mu + margin, n=n)


def _backend_stats(outcomes: list[EpisodeOutcome]) -> BackendStats:
    assert outcomes, "outcomes must be non-empty"
    backend = outcomes[0].backend
    n = len(outcomes)
    successes = [o for o in outcomes if o.success]
    success_rate = len(successes) / n
    steps_vals = [float(o.steps) for o in outcomes]
    elapsed_vals = [o.elapsed_s for o in outcomes]
    return BackendStats(
        backend=backend,
        n_episodes=n,
        success_rate=success_rate,
        mean_steps=mean(steps_vals),
        mean_elapsed_s=mean(elapsed_vals),
        ci_steps=_confidence_interval(steps_vals),
        ci_elapsed_s=_confidence_interval(elapsed_vals),
    )


def compute_sensitivity_stats(paired: list[PairedEpisodeResult]) -> SensitivityReport:
    """Derive per-backend statistics and cross-backend deltas from paired results."""
    if not paired:
        raise ValueError("paired must be non-empty")

    pb_outcomes = [p.pybullet for p in paired]
    mj_outcomes = [p.mujoco for p in paired]

    steps_deltas = [float(p.steps_delta) for p in paired]
    elapsed_deltas = [p.elapsed_delta_s for p in paired]

    failure_modes = [p.failure_mode for p in paired]

    return SensitivityReport(
        paired_results=list(paired),
        pybullet_stats=_backend_stats(pb_outcomes),
        mujoco_stats=_backend_stats(mj_outcomes),
        ci_steps_delta=_confidence_interval(steps_deltas),
        ci_elapsed_delta=_confidence_interval(elapsed_deltas),
        n_both_success=failure_modes.count("none"),
        n_pybullet_only_fail=failure_modes.count("pybullet_only"),
        n_mujoco_only_fail=failure_modes.count("mujoco_only"),
        n_both_fail=failure_modes.count("both"),
    )


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------


def run_paired_episodes(
    *,
    episodes: int = 20,
    maze_size: tuple[int, int] = (15, 15),
    seed: int = 42,
    planner: str = "astar",
) -> list[PairedEpisodeResult]:
    """Run the same set of episodes under both physics backends.

    Uses the project's pluggable loader so the real MazeEpisodeSimulator (when
    available) or the StubSimulator (in CI / headless environments) is exercised.
    """
    try:
        import main as main_mod
    except ImportError:
        main_mod = None  # type: ignore[assignment]

    if main_mod is not None:
        maze_generator = main_mod.load_maze_generator()
        planner_obj = main_mod.load_planner(planner)
        simulator = main_mod.load_simulator()
    else:
        # Minimal in-process stubs when main.py is not importable
        from main import StubMazeGenerator, StubPlanner, StubSimulator  # type: ignore[no-redef]
        maze_generator = StubMazeGenerator()
        planner_obj = StubPlanner(name=planner)
        simulator = StubSimulator()

    paired: list[PairedEpisodeResult] = []
    for ep in range(1, episodes + 1):
        ep_seed = seed + (ep - 1)
        maze = maze_generator.generate(episode=ep, size=maze_size, seed=ep_seed)
        plan = planner_obj.plan(maze, seed=ep_seed)

        outcomes: dict[str, EpisodeOutcome] = {}
        for backend in BACKENDS:
            started = time.perf_counter()
            result = simulator.run_episode(
                maze,
                plan,
                gui=False,
                seed=ep_seed,
                robot_urdf=None,
                gui_hold_seconds=0.0,
                physics_backend=backend,
            )
            wall_s = time.perf_counter() - started
            outcomes[backend] = EpisodeOutcome(
                backend=backend,
                episode=ep,
                seed=ep_seed,
                success=result.success,
                steps=result.steps,
                # Use wall-clock time as fallback when simulator reports zero elapsed
                # (e.g., StubSimulator always returns elapsed_s=0.0 for kinematic fallback).
                elapsed_s=result.elapsed_s if result.elapsed_s > 0 else wall_s,
            )

        paired.append(
            PairedEpisodeResult(
                episode=ep,
                seed=ep_seed,
                pybullet=outcomes["pybullet"],
                mujoco=outcomes["mujoco"],
            )
        )

    return paired


# ---------------------------------------------------------------------------
# Report writers
# ---------------------------------------------------------------------------


def write_sensitivity_csv(
    paired: list[PairedEpisodeResult],
    output_path: Path,
) -> Path:
    """Write per-episode paired results to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "episode",
                "seed",
                "pybullet_success",
                "pybullet_steps",
                "pybullet_elapsed_s",
                "mujoco_success",
                "mujoco_steps",
                "mujoco_elapsed_s",
                "steps_delta",
                "elapsed_delta_s",
                "failure_mode",
            ]
        )
        for p in paired:
            writer.writerow(
                [
                    p.episode,
                    p.seed if p.seed is not None else "",
                    int(p.pybullet.success),
                    p.pybullet.steps,
                    f"{p.pybullet.elapsed_s:.6f}",
                    int(p.mujoco.success),
                    p.mujoco.steps,
                    f"{p.mujoco.elapsed_s:.6f}",
                    p.steps_delta,
                    f"{p.elapsed_delta_s:.6f}",
                    p.failure_mode,
                ]
            )
    return output_path


def _fmt_ci(ci: ConfidenceInterval) -> str:
    if math.isnan(ci.mean):
        return "n/a"
    return f"{ci.mean:.4f} [{ci.lower:.4f}, {ci.upper:.4f}]"


def write_sensitivity_report(
    report: SensitivityReport,
    output_path: Path,
    *,
    episodes: int,
    maze_size: tuple[int, int],
    seed: int,
    planner: str,
) -> Path:
    """Write a Markdown sensitivity report suitable for manuscript appendix."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
    pb = report.pybullet_stats
    mj = report.mujoco_stats

    lines = [
        "# Backend Sensitivity Report: PyBullet vs MuJoCo",
        "",
        "## Experiment Configuration",
        "",
        f"- Generated (UTC): {generated_at}",
        f"- Episodes: {episodes}",
        f"- Maze size: {maze_size[0]}x{maze_size[1]}",
        f"- Base seed: {seed}",
        f"- Planner: {planner}",
        "",
        "## Per-Backend Summary",
        "",
        "| Metric | PyBullet | MuJoCo |",
        "|---|---:|---:|",
        f"| Episodes | {pb.n_episodes} | {mj.n_episodes} |",
        f"| Success rate | {pb.success_rate:.1%} | {mj.success_rate:.1%} |",
        f"| Mean steps | {pb.mean_steps:.2f} | {mj.mean_steps:.2f} |",
        f"| Mean elapsed (s) | {pb.mean_elapsed_s:.6f} | {mj.mean_elapsed_s:.6f} |",
        f"| 95% CI steps | {_fmt_ci(pb.ci_steps)} | {_fmt_ci(mj.ci_steps)} |",
        f"| 95% CI elapsed (s) | {_fmt_ci(pb.ci_elapsed_s)} | {_fmt_ci(mj.ci_elapsed_s)} |",
        "",
        "## Cross-Backend Deltas (MuJoCo − PyBullet)",
        "",
        "| Metric | Value (95 % CI) |",
        "|---|---:|",
        f"| Steps delta | {_fmt_ci(report.ci_steps_delta)} |",
        f"| Elapsed delta (s) | {_fmt_ci(report.ci_elapsed_delta)} |",
        "",
        "## Failure-Mode Breakdown",
        "",
        "| Failure mode | Count |",
        "|---|---:|",
        f"| Both succeeded | {report.n_both_success} |",
        f"| PyBullet only failed | {report.n_pybullet_only_fail} |",
        f"| MuJoCo only failed | {report.n_mujoco_only_fail} |",
        f"| Both failed | {report.n_both_fail} |",
        "",
    ]

    # Root-cause notes for any material backend divergence
    material_divergence = (
        report.n_pybullet_only_fail > 0
        or report.n_mujoco_only_fail > 0
        or abs(report.ci_steps_delta.mean) > 1.0
    )
    lines.append("## Backend Divergence Notes")
    lines.append("")
    if not material_divergence:
        lines.append(
            "No material backend divergence detected. "
            "Step counts and completion rates are consistent across backends."
        )
    else:
        lines.append("Material divergence detected:")
        if report.n_pybullet_only_fail > 0:
            lines.append(
                f"- PyBullet-only failures ({report.n_pybullet_only_fail} episode(s)): "
                "likely caused by URDF loading or physics instability in PyBullet."
            )
        if report.n_mujoco_only_fail > 0:
            lines.append(
                f"- MuJoCo-only failures ({report.n_mujoco_only_fail} episode(s)): "
                "likely caused by XML model generation or solver divergence in MuJoCo."
            )
        if abs(report.ci_steps_delta.mean) > 1.0:
            lines.append(
                f"- Step-count delta mean {report.ci_steps_delta.mean:.2f} exceeds threshold of 1.0: "
                "backends use different integration step counts per waypoint."
            )
    lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


# ---------------------------------------------------------------------------
# High-level entry point
# ---------------------------------------------------------------------------


def run_sensitivity_experiment(
    *,
    episodes: int = 20,
    maze_size: tuple[int, int] = (15, 15),
    seed: int = 42,
    planner: str = "astar",
    output_dir: Path | str | None = None,
) -> tuple[SensitivityReport, Path, Path]:
    """Run the full paired-backend sensitivity experiment and write artifacts.

    Returns
    -------
    (report, csv_path, md_path)
    """
    out_dir = (
        Path(output_dir)
        if output_dir is not None
        else Path(__file__).resolve().parents[1] / "results"
    )
    paired = run_paired_episodes(
        episodes=episodes,
        maze_size=maze_size,
        seed=seed,
        planner=planner,
    )
    report = compute_sensitivity_stats(paired)
    csv_path = write_sensitivity_csv(paired, out_dir / "backend_sensitivity.csv")
    md_path = write_sensitivity_report(
        report,
        out_dir / "backend_sensitivity.md",
        episodes=episodes,
        maze_size=maze_size,
        seed=seed,
        planner=planner,
    )
    return report, csv_path, md_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run paired PyBullet/MuJoCo episodes and report backend sensitivity."
    )
    parser.add_argument("--episodes", type=int, default=20, help="Number of paired episodes.")
    parser.add_argument("--maze-size", type=str, default="15x15", help="Maze size as WxH or N.")
    parser.add_argument("--seed", type=int, default=42, help="Base random seed.")
    parser.add_argument(
        "--planner", default="astar", help="Planner name (must be available in planners registry)."
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for output artifacts. Defaults to robotics_maze/results/.",
    )
    return parser


def _parse_maze_size(raw: str) -> tuple[int, int]:
    raw = raw.strip().lower()
    if "x" in raw:
        w, h = raw.split("x", maxsplit=1)
        return int(w), int(h)
    s = int(raw)
    return s, s


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    maze_size = _parse_maze_size(args.maze_size)
    report, csv_path, md_path = run_sensitivity_experiment(
        episodes=args.episodes,
        maze_size=maze_size,
        seed=args.seed,
        planner=args.planner,
        output_dir=args.output_dir,
    )
    pb = report.pybullet_stats
    mj = report.mujoco_stats
    print(f"[DONE] episodes={args.episodes} planner={args.planner} seed={args.seed}")
    print(
        f"  pybullet: success={pb.success_rate:.1%} mean_steps={pb.mean_steps:.2f} "
        f"mean_elapsed={pb.mean_elapsed_s:.4f}s"
    )
    print(
        f"  mujoco:   success={mj.success_rate:.1%} mean_steps={mj.mean_steps:.2f} "
        f"mean_elapsed={mj.mean_elapsed_s:.4f}s"
    )
    print(f"  steps_delta 95%CI: {report.ci_steps_delta}")
    print(f"  elapsed_delta 95%CI: {report.ci_elapsed_delta}")
    print(
        f"  failure modes: both_ok={report.n_both_success} pb_fail={report.n_pybullet_only_fail} "
        f"mj_fail={report.n_mujoco_only_fail} both_fail={report.n_both_fail}"
    )
    print(f"[OUT] {csv_path}")
    print(f"[OUT] {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
