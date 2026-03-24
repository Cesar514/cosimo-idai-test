"""Geometry helpers to convert maze walls into 3D obstacle boxes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

try:
    from .maze import Maze
except ImportError:  # pragma: no cover - supports direct module imports from src/
    from maze import Maze

Vector3 = tuple[float, float, float]


@dataclass(frozen=True)
class ObstacleBox:
    """Axis-aligned 3D obstacle box defined by center position and dimensions."""

    position: Vector3
    dimensions: Vector3

    def as_dict(self) -> dict[str, Vector3]:
        """Serialize the obstacle as a simple mapping."""
        return {"position": self.position, "dimensions": self.dimensions}


def maze_walls_to_obstacle_boxes(
    maze: Maze,
    cell_size: float = 1.0,
    wall_thickness: float = 0.1,
    wall_height: float = 1.0,
    floor_z: float = 0.0,
    merge_collinear: bool = True,
) -> list[ObstacleBox]:
    """Convert maze wall segments into 3D axis-aligned obstacle boxes.

    Args:
        maze: Maze to convert.
        cell_size: Edge length of one maze cell in world units.
        wall_thickness: Wall thickness in world units.
        wall_height: Wall height in world units.
        floor_z: Z value of the floor plane.
        merge_collinear: If True, merge adjacent wall segments into longer boxes.

    Returns:
        List of obstacle boxes represented by center position and dimensions.
    """
    _require_positive(cell_size, name="cell_size")
    _require_positive(wall_thickness, name="wall_thickness")
    _require_positive(wall_height, name="wall_height")

    center_z = floor_z + (wall_height / 2.0)
    boxes: list[ObstacleBox] = []

    for row_index, row in enumerate(maze.horizontal_walls):
        for start, end in _iter_wall_runs(row, merge_collinear):
            length = (end - start) * cell_size
            center_x = (start + end) * 0.5 * cell_size
            center_y = row_index * cell_size
            boxes.append(
                ObstacleBox(
                    position=(center_x, center_y, center_z),
                    dimensions=(length, wall_thickness, wall_height),
                )
            )

    for column_index in range(maze.width + 1):
        column = [maze.vertical_walls[row][column_index] for row in range(maze.height)]
        for start, end in _iter_wall_runs(column, merge_collinear):
            length = (end - start) * cell_size
            center_x = column_index * cell_size
            center_y = (start + end) * 0.5 * cell_size
            boxes.append(
                ObstacleBox(
                    position=(center_x, center_y, center_z),
                    dimensions=(wall_thickness, length, wall_height),
                )
            )

    return boxes


def maze_walls_to_box_dicts(
    maze: Maze,
    cell_size: float = 1.0,
    wall_thickness: float = 0.1,
    wall_height: float = 1.0,
    floor_z: float = 0.0,
    merge_collinear: bool = True,
) -> list[dict[str, Vector3]]:
    """Convert maze walls to dictionaries with `position` and `dimensions`."""
    boxes = maze_walls_to_obstacle_boxes(
        maze=maze,
        cell_size=cell_size,
        wall_thickness=wall_thickness,
        wall_height=wall_height,
        floor_z=floor_z,
        merge_collinear=merge_collinear,
    )
    return obstacle_boxes_as_dicts(boxes)


def obstacle_boxes_as_dicts(boxes: Iterable[ObstacleBox]) -> list[dict[str, Vector3]]:
    """Serialize obstacle boxes into primitive dictionaries."""
    return [box.as_dict() for box in boxes]


def _iter_wall_runs(
    values: Sequence[bool], merge_collinear: bool
) -> list[tuple[int, int]]:
    """Return `[start, end)` index pairs for wall segments marked True."""
    if not merge_collinear:
        return [(index, index + 1) for index, has_wall in enumerate(values) if has_wall]

    runs: list[tuple[int, int]] = []
    run_start: int | None = None
    for index, has_wall in enumerate(values):
        if has_wall and run_start is None:
            run_start = index
        if not has_wall and run_start is not None:
            runs.append((run_start, index))
            run_start = None
    if run_start is not None:
        runs.append((run_start, len(values)))
    return runs


def _require_positive(value: float, name: str) -> None:
    """Raise ValueError when a numeric argument is not strictly positive."""
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0.0, got {value}.")
