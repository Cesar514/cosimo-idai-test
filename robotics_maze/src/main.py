from __future__ import annotations

import argparse
import importlib
import random
from dataclasses import dataclass
from typing import Any, Protocol, Sequence

MazeSize = tuple[int, int]


@dataclass(frozen=True)
class RunConfig:
    planner: str
    episodes: int
    maze_size: MazeSize
    seed: int | None
    gui: bool


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


class StubSimulator:
    def run_episode(
        self,
        maze: Any,
        plan: Any,
        *,
        gui: bool,
        seed: int | None,
    ) -> EpisodeResult:
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
    return parser


def parse_args(argv: Sequence[str] | None = None) -> RunConfig:
    args = build_parser().parse_args(argv)
    return RunConfig(
        planner=args.planner,
        episodes=args.episodes,
        maze_size=args.maze_size,
        seed=args.seed,
        gui=args.gui,
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

    print(f"[INFO] Planner '{name}' not found; using stub planner.")
    return StubPlanner(name=name)


def run(config: RunConfig) -> int:
    maze_generator = load_maze_generator()
    planner = load_planner(config.planner)
    simulator = load_simulator()

    print(
        "[START] planner={planner} episodes={episodes} maze_size={maze_size} seed={seed} gui={gui}".format(
            planner=getattr(planner, "name", config.planner),
            episodes=config.episodes,
            maze_size=f"{config.maze_size[0]}x{config.maze_size[1]}",
            seed=config.seed,
            gui=config.gui,
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
    config = parse_args(argv)
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
