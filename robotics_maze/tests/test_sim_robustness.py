import pytest
import os
import tempfile
from unittest.mock import MagicMock, patch
from robotics_maze.src.sim import (
    MazeEpisodeSimulator, PyBulletMazeSim, URDF_OK, URDF_NOT_FOUND,
    URDF_INVALID_EXTENSION, URDF_LOAD_ERROR, BACKEND_FALLBACK
)

@pytest.fixture
def stub_maze():
    maze = MagicMock()
    maze.width = 5
    maze.height = 5
    maze.start = (0, 0)
    maze.goal = (4, 4)
    maze.has_wall_between.return_value = False
    return maze

@pytest.fixture
def stub_plan():
    return [(0, 0), (1, 1), (4, 4)]

def test_urdf_invalid_extension(stub_maze, stub_plan):
    sim = MazeEpisodeSimulator()
    with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
        result = sim.run_episode(
            stub_maze, stub_plan, gui=False, seed=42,
            robot_urdf=tmp.name, physics_backend="auto"
        )
        # It should fallback to default and record the error
        assert result.diagnostics["urdf_status"] == BACKEND_FALLBACK
        assert "must end with '.urdf'" in result.diagnostics["urdf_fallback_reason"].lower()

def test_urdf_not_found(stub_maze, stub_plan):
    sim = MazeEpisodeSimulator()
    result = sim.run_episode(
        stub_maze, stub_plan, gui=False, seed=42,
        robot_urdf="/tmp/non_existent_robot.urdf", physics_backend="auto"
    )
    assert result.diagnostics["urdf_status"] == BACKEND_FALLBACK
    assert "file not found" in result.diagnostics["urdf_fallback_reason"].lower()

def test_urdf_malformed(stub_maze, stub_plan):
    # This test only makes sense if pybullet is available as it's a runtime load error
    try:
        import pybullet as p
    except ImportError:
        pytest.skip("pybullet not available")

    sim = MazeEpisodeSimulator()
    with tempfile.NamedTemporaryFile(suffix=".urdf", mode='w') as tmp:
        tmp.write("<robot name='broken'>")
        tmp.flush()
        result = sim.run_episode(
            stub_maze, stub_plan, gui=False, seed=42,
            robot_urdf=tmp.name, physics_backend="pybullet"
        )
        assert result.diagnostics["urdf_status"] == BACKEND_FALLBACK
        assert "custom urdf failed" in result.diagnostics["urdf_fallback_reason"].lower()

def test_backend_fallback_pybullet_to_kinematic(stub_maze, stub_plan):
    with patch("robotics_maze.src.sim.p", None), \
         patch("robotics_maze.src.sim.pybullet_data", None), \
         patch("robotics_maze.src.sim.mujoco", None):
        sim = MazeEpisodeSimulator()
        result = sim.run_episode(
            stub_maze, stub_plan, gui=False, seed=42, physics_backend="pybullet"
        )
        assert result.diagnostics["actual_backend"] == "kinematic_fallback"

def test_backend_fallback_order(stub_maze, stub_plan):
    sim = MazeEpisodeSimulator()
    # Mocking availability to test logic
    with patch("robotics_maze.src.sim.p", MagicMock()), \
         patch("robotics_maze.src.sim.pybullet_data", MagicMock()), \
         patch("robotics_maze.src.sim.mujoco", MagicMock()):

        # We need to mock PyBulletMazeSim to fail to trigger next backend
        with patch("robotics_maze.src.sim.PyBulletMazeSim", side_effect=Exception("PB fail")):
            # Also need to mock _run_episode_with_mujoco
            with patch.object(MazeEpisodeSimulator, "_run_episode_with_mujoco") as mock_mujoco:
                mock_mujoco.return_value = MagicMock(success=True, steps=10, elapsed_s=0.1)

                result = sim.run_episode(
                    stub_maze, stub_plan, gui=False, seed=42, physics_backend="auto"
                )
                assert result.diagnostics["actual_backend"] == "mujoco"
                assert "PB fail" in result.diagnostics["pybullet_failure"]
