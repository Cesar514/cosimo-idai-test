"""Deterministic maze generation and validation utilities.

The module provides two mathematical maze generators:
- Recursive backtracker (depth-first carving)
- Randomized Prim variant

Both algorithms build a perfect maze (single connected component, no cycles),
which guarantees solvability between any two cells.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import random

Coordinate = tuple[int, int]
SUPPORTED_MAZE_ALGORITHMS = frozenset({"backtracker", "prim"})


@dataclass
class Maze:
    """Grid maze with explicit horizontal and vertical wall segments.

    Coordinates are `(x, y)` where `x` is the column index and `y` is the row
    index. Walls are represented as booleans where `True` means wall present.

    - `horizontal_walls[y][x]` is the wall segment on row boundary `y`
      between columns `x` and `x + 1`. Shape: `(height + 1, width)`.
    - `vertical_walls[y][x]` is the wall segment on column boundary `x`
      between rows `y` and `y + 1`. Shape: `(height, width + 1)`.
    """

    width: int
    height: int
    horizontal_walls: list[list[bool]]
    vertical_walls: list[list[bool]]
    start: Coordinate
    goal: Coordinate
    algorithm: str
    seed: int | None = None

    def __post_init__(self) -> None:
        """Validate dimensions, wall grid shapes, and endpoint coordinates."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Maze dimensions must be positive integers.")
        if self.algorithm not in SUPPORTED_MAZE_ALGORITHMS:
            raise ValueError(
                f"Unsupported algorithm '{self.algorithm}'. "
                f"Expected one of {sorted(SUPPORTED_MAZE_ALGORITHMS)}."
            )
        if len(self.horizontal_walls) != self.height + 1:
            raise ValueError("horizontal_walls must have height + 1 rows.")
        if any(len(row) != self.width for row in self.horizontal_walls):
            raise ValueError("Each horizontal wall row must have width columns.")
        if len(self.vertical_walls) != self.height:
            raise ValueError("vertical_walls must have height rows.")
        if any(len(row) != self.width + 1 for row in self.vertical_walls):
            raise ValueError("Each vertical wall row must have width + 1 columns.")
        _validate_cell(self.start, self.width, self.height, name="start")
        _validate_cell(self.goal, self.width, self.height, name="goal")

    def neighbors(self, cell: Coordinate) -> list[Coordinate]:
        """Return in-bounds orthogonal neighbors in deterministic order."""
        _validate_cell(cell, self.width, self.height, name="cell")
        return _candidate_neighbors(cell, self.width, self.height)

    def has_wall_between(self, source: Coordinate, target: Coordinate) -> bool:
        """Return whether a wall exists between two adjacent cells."""
        _validate_cell(source, self.width, self.height, name="source")
        _validate_cell(target, self.width, self.height, name="target")
        _validate_adjacent(source, target)
        x1, y1 = source
        x2, y2 = target
        dx = x2 - x1
        dy = y2 - y1
        if dx == 1:
            return self.vertical_walls[y1][x1 + 1]
        if dx == -1:
            return self.vertical_walls[y1][x1]
        if dy == 1:
            return self.horizontal_walls[y1 + 1][x1]
        return self.horizontal_walls[y1][x1]

    def remove_wall_between(self, source: Coordinate, target: Coordinate) -> None:
        """Remove the shared wall between two adjacent cells."""
        _validate_cell(source, self.width, self.height, name="source")
        _validate_cell(target, self.width, self.height, name="target")
        _validate_adjacent(source, target)
        x1, y1 = source
        x2, y2 = target
        dx = x2 - x1
        dy = y2 - y1
        if dx == 1:
            self.vertical_walls[y1][x1 + 1] = False
            return
        if dx == -1:
            self.vertical_walls[y1][x1] = False
            return
        if dy == 1:
            self.horizontal_walls[y1 + 1][x1] = False
            return
        self.horizontal_walls[y1][x1] = False

    def open_neighbors(self, cell: Coordinate) -> list[Coordinate]:
        """Return adjacent cells reachable without crossing walls."""
        return [
            neighbor
            for neighbor in self.neighbors(cell)
            if not self.has_wall_between(cell, neighbor)
        ]

    def shortest_path(
        self, start: Coordinate | None = None, goal: Coordinate | None = None
    ) -> list[Coordinate]:
        """Compute a shortest path with BFS, or return an empty list if none."""
        start_cell = self.start if start is None else start
        goal_cell = self.goal if goal is None else goal
        _validate_cell(start_cell, self.width, self.height, name="start")
        _validate_cell(goal_cell, self.width, self.height, name="goal")
        queue: deque[Coordinate] = deque([start_cell])
        parents: dict[Coordinate, Coordinate | None] = {start_cell: None}

        while queue:
            current = queue.popleft()
            if current == goal_cell:
                break
            for nxt in self.open_neighbors(current):
                if nxt not in parents:
                    parents[nxt] = current
                    queue.append(nxt)

        if goal_cell not in parents:
            return []

        path: list[Coordinate] = []
        cursor: Coordinate | None = goal_cell
        while cursor is not None:
            path.append(cursor)
            cursor = parents[cursor]
        path.reverse()
        return path

    def is_solvable(
        self, start: Coordinate | None = None, goal: Coordinate | None = None
    ) -> bool:
        """Return True when a path exists between start and goal cells."""
        return bool(self.shortest_path(start=start, goal=goal))


@dataclass(frozen=True)
class DeterministicMazeGenerator:
    """Maze generator adapter compatible with the main CLI loader contract."""

    algorithm: str = "backtracker"

    def generate(
        self, *, episode: int, size: tuple[int, int], seed: int | None
    ) -> Maze:
        """Generate one deterministic maze for an episode."""
        width, height = size
        base_seed = 0 if seed is None else seed
        episode_seed = base_seed + int(episode)
        return generate_maze(
            width=width,
            height=height,
            seed=episode_seed,
            algorithm=self.algorithm,
        )


def create_maze_generator(algorithm: str = "backtracker") -> DeterministicMazeGenerator:
    """Create a maze generator instance for CLI/plugin integration."""
    if algorithm not in SUPPORTED_MAZE_ALGORITHMS:
        raise ValueError(
            f"Unsupported algorithm '{algorithm}'. "
            f"Expected one of {sorted(SUPPORTED_MAZE_ALGORITHMS)}."
        )
    return DeterministicMazeGenerator(algorithm=algorithm)


def center_goal(width: int, height: int) -> Coordinate:
    """Return the deterministic center goal coordinate for a maze size."""
    if width <= 0 or height <= 0:
        raise ValueError("Maze dimensions must be positive integers.")
    return (width // 2, height // 2)


def generate_recursive_backtracker_maze(
    width: int,
    height: int,
    seed: int = 0,
    start: Coordinate = (0, 0),
    goal: Coordinate | None = None,
) -> Maze:
    """Generate a deterministic perfect maze using recursive backtracker."""
    return generate_maze(
        width=width,
        height=height,
        seed=seed,
        algorithm="backtracker",
        start=start,
        goal=goal,
    )


def generate_prim_maze(
    width: int,
    height: int,
    seed: int = 0,
    start: Coordinate = (0, 0),
    goal: Coordinate | None = None,
) -> Maze:
    """Generate a deterministic perfect maze using a randomized Prim variant."""
    return generate_maze(
        width=width,
        height=height,
        seed=seed,
        algorithm="prim",
        start=start,
        goal=goal,
    )


def generate_maze(
    width: int,
    height: int,
    seed: int = 0,
    algorithm: str = "backtracker",
    start: Coordinate = (0, 0),
    goal: Coordinate | None = None,
) -> Maze:
    """Generate a deterministic, solvable maze with start and center-goal support."""
    if width <= 0 or height <= 0:
        raise ValueError("Maze dimensions must be positive integers.")
    if algorithm not in SUPPORTED_MAZE_ALGORITHMS:
        raise ValueError(
            f"Unsupported algorithm '{algorithm}'. "
            f"Expected one of {sorted(SUPPORTED_MAZE_ALGORITHMS)}."
        )

    _validate_cell(start, width, height, name="start")
    goal_cell = center_goal(width, height) if goal is None else goal
    _validate_cell(goal_cell, width, height, name="goal")

    maze = Maze(
        width=width,
        height=height,
        horizontal_walls=[[True for _ in range(width)] for _ in range(height + 1)],
        vertical_walls=[[True for _ in range(width + 1)] for _ in range(height)],
        start=start,
        goal=goal_cell,
        algorithm=algorithm,
        seed=seed,
    )
    rng = random.Random(seed)
    if algorithm == "backtracker":
        _carve_backtracker(maze, rng, start_cell=start)
    else:
        _carve_prim(maze, rng, start_cell=start)

    reachable = _reachable_cells(maze, start=start)
    expected_cell_count = width * height
    if len(reachable) != expected_cell_count:
        raise RuntimeError(
            "Maze generation failed to connect all cells. "
            f"reachable={len(reachable)}, expected={expected_cell_count}"
        )
    if not maze.is_solvable():
        raise RuntimeError("Generated maze is not solvable between start and goal.")
    return maze


def _carve_backtracker(
    maze: Maze, rng: random.Random, start_cell: Coordinate
) -> None:
    """Carve passages with iterative depth-first backtracking."""
    visited: set[Coordinate] = {start_cell}
    stack: list[Coordinate] = [start_cell]

    while stack:
        current = stack[-1]
        candidates = [
            candidate
            for candidate in _candidate_neighbors(current, maze.width, maze.height)
            if candidate not in visited
        ]
        if not candidates:
            stack.pop()
            continue

        nxt = candidates[rng.randrange(len(candidates))]
        maze.remove_wall_between(current, nxt)
        visited.add(nxt)
        stack.append(nxt)


def _carve_prim(maze: Maze, rng: random.Random, start_cell: Coordinate) -> None:
    """Carve passages using a deterministic randomized Prim frontier process."""
    visited: set[Coordinate] = {start_cell}
    frontier: list[tuple[Coordinate, Coordinate]] = []

    def push_frontier(cell: Coordinate) -> None:
        for nxt in _candidate_neighbors(cell, maze.width, maze.height):
            if nxt not in visited:
                frontier.append((cell, nxt))

    push_frontier(start_cell)

    while frontier:
        edge_index = rng.randrange(len(frontier))
        source, target = frontier.pop(edge_index)
        if target in visited:
            continue
        maze.remove_wall_between(source, target)
        visited.add(target)
        push_frontier(target)


def _candidate_neighbors(cell: Coordinate, width: int, height: int) -> list[Coordinate]:
    """Return in-bounds neighbors in N/E/S/W order."""
    x, y = cell
    neighbors: list[Coordinate] = []
    if y > 0:
        neighbors.append((x, y - 1))
    if x < width - 1:
        neighbors.append((x + 1, y))
    if y < height - 1:
        neighbors.append((x, y + 1))
    if x > 0:
        neighbors.append((x - 1, y))
    return neighbors


def _reachable_cells(maze: Maze, start: Coordinate) -> set[Coordinate]:
    """Return all cells that can be reached from start."""
    visited: set[Coordinate] = {start}
    queue: deque[Coordinate] = deque([start])
    while queue:
        current = queue.popleft()
        for nxt in maze.open_neighbors(current):
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
    return visited


def _validate_adjacent(source: Coordinate, target: Coordinate) -> None:
    """Raise ValueError unless two coordinates are orthogonally adjacent."""
    if abs(source[0] - target[0]) + abs(source[1] - target[1]) != 1:
        raise ValueError(f"Cells must be orthogonally adjacent: {source} -> {target}.")


def _validate_cell(cell: Coordinate, width: int, height: int, name: str) -> None:
    """Validate cell coordinate bounds for the given maze dimensions."""
    x, y = cell
    if x < 0 or y < 0 or x >= width or y >= height:
        raise ValueError(
            f"{name} cell {cell} out of bounds for maze size ({width}, {height})."
        )
