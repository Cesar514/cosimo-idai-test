from __future__ import annotations

import argparse
import importlib
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, Sequence

MazeSize = tuple[int, int]
BACKEND_CHOICES = ("auto", "pybullet", "mujoco")

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

DEFAULT_ROBOT_URDF = "husky/husky.urdf"


@dataclass(frozen=True)
class RunConfig:
    planner: str
    episodes: int
    maze_size: MazeSize
    seed: int | None
    gui: bool
    gui_setup: bool = False
    robot_urdf: str | None = None
    gui_hold_seconds: float = 8.0
    physics_backend: str = "auto"


@dataclass(frozen=True)
class EpisodeResult:
    success: bool
    steps: int
    elapsed_s: float


class MazeGenerator(Protocol):
    def generate(self, *, episode: int, size: MazeSize, seed: int | None) -> Any:
        ...


class Planner(Protocol):
    name: str

    def plan(self, maze: Any, *, seed: int | None) -> Any:
        ...


class Simulator(Protocol):
    def run_episode(
        self,
        maze: Any,
        plan: Any,
        *,
        gui: bool,
        seed: int | None,
        robot_urdf: str | None = None,
        gui_hold_seconds: float = 8.0,
        physics_backend: str = "auto",
    ) -> EpisodeResult:
        ...


class StubMazeGenerator:
    def generate(self, *, episode: int, size: MazeSize, seed: int | None) -> dict[str, Any]:
        return {"episode": episode, "size": size, "seed": seed}


class StubPlanner:
    def __init__(self, name: str) -> None:
        self.name = name

    def plan(self, maze: Any, *, seed: int | None) -> dict[str, Any]:
        return {"planner": self.name, "seed": seed, "maze": maze}


class FunctionPlannerAdapter:
    def __init__(self, name: str, planner_fn: Any) -> None:
        self.name = name
        self._planner_fn = planner_fn

    def plan(self, maze: Any, *, seed: int | None) -> dict[str, Any]:
        del seed
        grid, start, goal = _maze_to_grid_triplet(maze)
        if grid is None or start is None or goal is None:
            if hasattr(maze, "shortest_path") and callable(getattr(maze, "shortest_path")):
                try:
                    return {"path": maze.shortest_path()}
                except Exception:
                    return {"path": []}
            return {"path": []}
        return self._planner_fn(grid, start, goal)


class StubSimulator:
    def run_episode(
        self,
        maze: Any,
        plan: Any,
        *,
        gui: bool,
        seed: int | None,
        robot_urdf: str | None = None,
        gui_hold_seconds: float = 8.0,
        physics_backend: str = "auto",
    ) -> EpisodeResult:
        del gui, plan, robot_urdf, gui_hold_seconds, physics_backend
        size = _extract_size(maze)
        rng = random.Random(seed)
        steps = rng.randint(max(size[0], size[1]), max(size[0] * size[1], 1))
        elapsed_s = round(steps / 1000.0, 4)
        return EpisodeResult(success=True, steps=steps, elapsed_s=elapsed_s)


def positive_int(raw_value: str) -> int:
    value = int(raw_value)
    if value <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return value


def parse_maze_size(raw_value: str) -> MazeSize:
    value = raw_value.strip().lower()
    if "x" in value:
        width_raw, height_raw = value.split("x", maxsplit=1)
        width = positive_int(width_raw)
        height = positive_int(height_raw)
        return (width, height)

    side = positive_int(value)
    return (side, side)


def _is_pybullet_data_urdf(candidate: str) -> bool:
    try:
        import pybullet_data
    except Exception:
        return False
    return (Path(pybullet_data.getDataPath()) / candidate).is_file()


def validate_robot_urdf(raw_robot_urdf: str | None) -> str | None:
    if raw_robot_urdf is None:
        return None

    candidate = raw_robot_urdf.strip()
    if not candidate:
        return None
    if not candidate.lower().endswith(".urdf"):
        print(
            f"[WARN] Ignoring robot URDF '{candidate}': expected a .urdf file. "
            f"Falling back to default '{DEFAULT_ROBOT_URDF}'."
        )
        return None

    expanded = Path(candidate).expanduser()
    if expanded.is_file():
        return str(expanded.resolve())
    if _is_pybullet_data_urdf(candidate):
        return candidate

    print(
        f"[WARN] Ignoring robot URDF '{candidate}': file not found. "
        f"Falling back to default '{DEFAULT_ROBOT_URDF}'."
    )
    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the robotics maze planner scaffold.")
    parser.add_argument(
        "--planner",
        default="stub",
        help="Planner name or module path. Supports '<module>:<factory_or_class>'.",
    )
    parser.add_argument(
        "--episodes",
        type=positive_int,
        default=3,
        help="Number of episodes to run.",
    )
    parser.add_argument(
        "--maze-size",
        type=parse_maze_size,
        default=(15, 15),
        metavar="N|WxH",
        help="Maze size. Use N for square or WxH for rectangular mazes.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Base random seed. Episode index is added for deterministic runs.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Enable GUI mode when simulator support is available.",
    )
    parser.add_argument(
        "--physics-backend",
        choices=BACKEND_CHOICES,
        default="auto",
        help="Physics backend preference. GUI mode is best with pybullet.",
    )
    parser.add_argument(
        "--robot-urdf",
        default=None,
        help=(
            "Optional custom robot URDF path for pybullet runs (absolute, relative, or "
            f"pybullet_data path). Defaults to '{DEFAULT_ROBOT_URDF}'. Invalid paths "
            "fall back to the default."
        ),
    )
    parser.add_argument(
        "--gui-hold-seconds",
        type=float,
        default=8.0,
        help="How long to keep GUI open after each episode finishes.",
    )
    gui_setup_group = parser.add_mutually_exclusive_group()
    gui_setup_group.add_argument(
        "--gui-setup",
        dest="gui_setup",
        action="store_true",
        help="Open a Tkinter setup dialog before running the simulation.",
    )
    gui_setup_group.add_argument(
        "--no-gui-setup",
        dest="gui_setup",
        action="store_false",
        help="Skip the setup dialog and run directly with CLI arguments.",
    )
    parser.set_defaults(gui_setup=False)
    return parser


def parse_args(argv: Sequence[str] | None = None) -> RunConfig:
    args = build_parser().parse_args(argv)
    return RunConfig(
        planner=args.planner,
        episodes=args.episodes,
        maze_size=args.maze_size,
        seed=args.seed,
        gui=args.gui,
        gui_setup=args.gui_setup,
        robot_urdf=validate_robot_urdf(args.robot_urdf),
        gui_hold_seconds=max(args.gui_hold_seconds, 0.0),
        physics_backend=args.physics_backend,
    )


def _planner_setup_options(current_planner: str) -> list[str]:
    default_options = [
        "stub",
        "default",
        "astar",
        "bfs",
        "dijkstra",
        "greedy_best_first",
        "weighted_astar",
        "bidirectional_astar",
        "theta_star",
        "idastar",
        "jps",
        "lpa_star",
        "beam_search",
        "fringe_search",
        "bidirectional_bfs",
    ]
    options = [current_planner] if current_planner not in default_options else []
    options.extend(default_options)
    return options


def apply_gui_setup(config: RunConfig) -> tuple[RunConfig, bool]:
    if not config.gui_setup:
        return config, True

    try:
        from gui_setup import GuiSetupConfig, launch_gui_setup
    except Exception as exc:
        print(f"[WARN] GUI setup unavailable ({exc}); continuing with CLI configuration.")
        return config, True

    setup_result = launch_gui_setup(
        GuiSetupConfig(
            planner=config.planner,
            episodes=config.episodes,
            maze_size=config.maze_size,
            seed=config.seed,
            gui=config.gui,
            physics_backend=config.physics_backend,
            robot_urdf=config.robot_urdf,
            gui_hold_seconds=config.gui_hold_seconds,
        ),
        planner_options=_planner_setup_options(config.planner),
    )

    if setup_result.warning is not None:
        print(f"[WARN] GUI setup unavailable ({setup_result.warning}); continuing with CLI configuration.")
        return config, True
    if setup_result.config is None:
        if setup_result.cancelled:
            print("[INFO] GUI setup canceled; exiting without starting a simulation run.")
            return config, False
        print("[INFO] GUI setup closed without selection; continuing with CLI configuration.")
        return config, True

    selected = setup_result.config
    backend = selected.physics_backend.strip().lower()
    if backend not in BACKEND_CHOICES:
        backend = config.physics_backend
    if selected.gui and backend == "auto":
        # GUI runs are intended to stay visual; prefer the GUI-capable backend.
        backend = "pybullet"
    return (
        RunConfig(
            planner=selected.planner,
            episodes=selected.episodes,
            maze_size=selected.maze_size,
            seed=selected.seed,
            gui=selected.gui,
            gui_setup=config.gui_setup,
            robot_urdf=validate_robot_urdf(selected.robot_urdf),
            gui_hold_seconds=max(selected.gui_hold_seconds, 0.0),
            physics_backend=backend,
        ),
        True,
    )


def _extract_size(maze: Any) -> MazeSize:
    if isinstance(maze, dict):
        size = maze.get("size")
        if (
            isinstance(size, tuple)
            and len(size) == 2
            and all(isinstance(v, int) and v > 0 for v in size)
        ):
            return size
    return (10, 10)


def _maze_to_grid_triplet(maze: Any) -> tuple[Any, Any, Any]:
    if isinstance(maze, dict):
        grid = maze.get("grid")
        start = maze.get("start")
        goal = maze.get("goal")
        if grid is not None and start is not None and goal is not None:
            return grid, start, goal

    try:
        import benchmark as bench_mod

        return bench_mod.maze_to_occupancy_grid(maze)
    except Exception:
        return None, None, None


def _load_module_symbol(module_name: str, symbol_name: str) -> Any | None:
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None
    except Exception as exc:
        print(f"[WARN] Failed to import module '{module_name}': {exc}")
        return None
    return getattr(module, symbol_name, None)


def _instantiate(candidate: Any, *args: Any) -> Any | None:
    if candidate is None:
        return None
    if not callable(candidate):
        return candidate
    for call_args in (args, tuple()):
        try:
            return candidate(*call_args)
        except TypeError:
            continue
        except Exception as exc:
            print(f"[WARN] Failed to initialize component '{candidate}': {exc}")
            return None
    return None


def load_maze_generator() -> MazeGenerator:
    candidates = [
        ("maze", "create_maze_generator"),
        ("maze_generator", "create_maze_generator"),
        ("maze_math", "create_maze_generator"),
    ]
    for module_name, symbol_name in candidates:
        loaded = _instantiate(_load_module_symbol(module_name, symbol_name))
        if loaded is not None:
            print(f"[INFO] Maze generator loaded from {module_name}.{symbol_name}")
            return loaded
    print("[INFO] Maze generator not found; using stub implementation.")
    return StubMazeGenerator()


def load_simulator() -> Simulator:
    candidates = [
        ("sim", "create_simulator"),
        ("simulation", "create_simulator"),
        ("simulator", "create_simulator"),
    ]
    for module_name, symbol_name in candidates:
        loaded = _instantiate(_load_module_symbol(module_name, symbol_name))
        if loaded is not None:
            print(f"[INFO] Simulator loaded from {module_name}.{symbol_name}")
            return loaded
    print("[INFO] Simulator not found; using stub implementation.")
    return StubSimulator()


def load_planner(name: str) -> Planner:
    if name in {"stub", "default"}:
        return StubPlanner(name="stub")

    module_candidates: list[tuple[str, str]] = []
    if ":" in name:
        module_name, symbol_name = name.split(":", maxsplit=1)
        module_candidates.append((module_name, symbol_name))
    else:
        module_candidates.extend(
            [
                (f"alt_planners.{name}", "create_planner"),
                (f"alt_planners.{name}", "Planner"),
                (name, "create_planner"),
            ]
        )

    for module_name, symbol_name in module_candidates:
        loaded = _instantiate(_load_module_symbol(module_name, symbol_name), name)
        if loaded is not None:
            planner_name = getattr(loaded, "name", name)
            if not hasattr(loaded, "name"):
                setattr(loaded, "name", planner_name)
            print(f"[INFO] Planner loaded from {module_name}.{symbol_name}")
            return loaded

    # Support baseline planners and registered alternatives from planners.py.
    try:
        import planners as planners_mod

        planner_fn = planners_mod.get_planner(name)
        if callable(planner_fn):
            print(f"[INFO] Planner loaded from planners registry: {name}")
            return FunctionPlannerAdapter(name=name, planner_fn=planner_fn)
    except Exception:
        pass

    alt_map: dict[str, tuple[str, str]] = {
        "weighted_astar": ("alt_planners.r1_weighted_astar", "plan_weighted_astar"),
        "r1_weighted_astar": ("alt_planners.r1_weighted_astar", "plan_weighted_astar"),
        "bidirectional_astar": ("alt_planners.r2_bidirectional_astar", "plan_bidirectional_astar"),
        "r2_bidirectional_astar": ("alt_planners.r2_bidirectional_astar", "plan_bidirectional_astar"),
        "theta_star": ("alt_planners.r3_theta_star", "plan_theta_star"),
        "r3_theta_star": ("alt_planners.r3_theta_star", "plan_theta_star"),
        "idastar": ("alt_planners.r4_idastar", "plan_idastar"),
        "r4_idastar": ("alt_planners.r4_idastar", "plan_idastar"),
        "jps": ("alt_planners.r5_jump_point_search", "plan_jps"),
        "r5_jump_point_search": ("alt_planners.r5_jump_point_search", "plan_jps"),
        "lpa_star": ("alt_planners.r6_lpa_star", "plan_lpa_star"),
        "r6_lpa_star": ("alt_planners.r6_lpa_star", "plan_lpa_star"),
        "beam_search": ("alt_planners.r7_beam_search", "plan_beam_search"),
        "r7_beam_search": ("alt_planners.r7_beam_search", "plan_beam_search"),
        "fringe_search": ("alt_planners.r8_fringe_search", "plan_fringe_search"),
        "r8_fringe_search": ("alt_planners.r8_fringe_search", "plan_fringe_search"),
        "bidirectional_bfs": ("alt_planners.r9_bidirectional_bfs", "plan_bidirectional_bfs"),
        "r9_bidirectional_bfs": ("alt_planners.r9_bidirectional_bfs", "plan_bidirectional_bfs"),
    }
    if name in alt_map:
        module_name, symbol_name = alt_map[name]
        planner_fn = _load_module_symbol(module_name, symbol_name)
        if callable(planner_fn):
            print(f"[INFO] Planner loaded from alt planner module: {module_name}.{symbol_name}")
            return FunctionPlannerAdapter(name=name, planner_fn=planner_fn)

    print(f"[INFO] Planner '{name}' not found; using stub planner.")
    return StubPlanner(name=name)


def run(config: RunConfig) -> int:
    maze_generator = load_maze_generator()
    planner = load_planner(config.planner)
    simulator = load_simulator()

    print(
        (
            "[START] planner={planner} episodes={episodes} maze_size={maze_size} seed={seed} "
            "gui={gui} backend={backend} urdf={urdf} gui_hold_s={gui_hold_s}"
        ).format(
            planner=getattr(planner, "name", config.planner),
            episodes=config.episodes,
            maze_size=f"{config.maze_size[0]}x{config.maze_size[1]}",
            seed=config.seed,
            gui=config.gui,
            backend=config.physics_backend,
            urdf=config.robot_urdf or f"default({DEFAULT_ROBOT_URDF})",
            gui_hold_s=f"{config.gui_hold_seconds:.1f}",
        )
    )

    successes = 0
    total_steps = 0
    total_elapsed_s = 0.0

    for episode in range(1, config.episodes + 1):
        episode_seed = None if config.seed is None else config.seed + (episode - 1)
        maze = maze_generator.generate(
            episode=episode,
            size=config.maze_size,
            seed=episode_seed,
        )
        plan = planner.plan(maze, seed=episode_seed)
        result = simulator.run_episode(
            maze,
            plan,
            gui=config.gui,
            seed=episode_seed,
            robot_urdf=config.robot_urdf,
            gui_hold_seconds=config.gui_hold_seconds,
            physics_backend=config.physics_backend,
        )

        if result.success:
            successes += 1
        total_steps += result.steps
        total_elapsed_s += result.elapsed_s

        print(
            "[EP {ep}/{total}] status={status} steps={steps} elapsed_s={elapsed:.4f}".format(
                ep=episode,
                total=config.episodes,
                status="ok" if result.success else "fail",
                steps=result.steps,
                elapsed=result.elapsed_s,
            )
        )

    average_steps = total_steps / config.episodes
    average_elapsed_s = total_elapsed_s / config.episodes
    print(
        "[DONE] success={successes}/{total} avg_steps={avg_steps:.2f} avg_elapsed_s={avg_elapsed:.4f}".format(
            successes=successes,
            total=config.episodes,
            avg_steps=average_steps,
            avg_elapsed=average_elapsed_s,
        )
    )

    return 0 if successes == config.episodes else 1


def main(argv: Sequence[str] | None = None) -> int:
    config, should_run = apply_gui_setup(parse_args(argv))
    if not should_run:
        return 0
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
