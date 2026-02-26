"""Mobile robot control helpers for PyBullet maze simulation."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

try:
    import pybullet as p
except ImportError:  # pragma: no cover - dependency availability is environment specific.
    p = None  # type: ignore[assignment]


def _wrap_to_pi(angle: float) -> float:
    """Normalize an angle to [-pi, pi]."""
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


@dataclass
class PathFollowerConfig:
    """Controller gains for simple waypoint tracking."""

    max_linear_speed: float = 1.0
    max_angular_speed: float = 1.8
    heading_gain: float = 2.5
    waypoint_tolerance: float = 0.25
    final_waypoint_tolerance: float = 0.30
    wheel_visual_speed_scale: float = 8.0


class MobileRobotController:
    """Minimal mobile robot controller using base velocity in PyBullet."""

    def __init__(
        self,
        client_id: int,
        body_id: int,
        config: Optional[PathFollowerConfig] = None,
    ) -> None:
        if p is None:
            raise RuntimeError("pybullet is required for MobileRobotController")
        self.client_id = client_id
        self.body_id = body_id
        self.config = config or PathFollowerConfig()
        self._waypoints: List[Tuple[float, float]] = []
        self._current_waypoint_idx = 0
        self._finished = True
        self._wheel_joint_indices = self._discover_wheel_joints()

    @property
    def has_active_path(self) -> bool:
        return not self._finished and bool(self._waypoints)

    @property
    def waypoints(self) -> Tuple[Tuple[float, float], ...]:
        return tuple(self._waypoints)

    def set_waypoints(self, waypoints: Iterable[Sequence[float]]) -> None:
        parsed: List[Tuple[float, float]] = []
        for waypoint in waypoints:
            if len(waypoint) < 2:
                raise ValueError(f"Waypoint requires at least x/y coordinates: {waypoint!r}")
            parsed.append((float(waypoint[0]), float(waypoint[1])))
        self._waypoints = parsed
        self._current_waypoint_idx = 0
        self._finished = len(self._waypoints) == 0
        if self._finished:
            self.stop()

    def get_pose_xy_yaw(self) -> Tuple[float, float, float]:
        position, orientation = p.getBasePositionAndOrientation(
            self.body_id, physicsClientId=self.client_id
        )
        yaw = p.getEulerFromQuaternion(orientation)[2]
        return float(position[0]), float(position[1]), float(yaw)

    def distance_to_goal(self) -> Optional[float]:
        if not self._waypoints or self._finished:
            return None
        x, y, _ = self.get_pose_xy_yaw()
        gx, gy = self._waypoints[-1]
        return math.hypot(gx - x, gy - y)

    def step_path_follow(self) -> bool:
        """Run one controller update. Returns True once final waypoint is reached."""
        if self._finished:
            self.stop()
            return True

        x, y, yaw = self.get_pose_xy_yaw()
        target_x, target_y = self._waypoints[self._current_waypoint_idx]
        distance = math.hypot(target_x - x, target_y - y)

        tolerance = self.config.waypoint_tolerance
        if self._current_waypoint_idx == len(self._waypoints) - 1:
            tolerance = self.config.final_waypoint_tolerance

        if distance <= tolerance:
            self._current_waypoint_idx += 1
            if self._current_waypoint_idx >= len(self._waypoints):
                self._finished = True
                self.stop()
                return True
            target_x, target_y = self._waypoints[self._current_waypoint_idx]

        linear_speed, angular_speed = self._compute_command(x, y, yaw, target_x, target_y)
        self._apply_base_velocity(linear_speed, angular_speed, yaw)
        return False

    def stop(self) -> None:
        p.resetBaseVelocity(
            self.body_id,
            linearVelocity=(0.0, 0.0, 0.0),
            angularVelocity=(0.0, 0.0, 0.0),
            physicsClientId=self.client_id,
        )
        self._set_wheels(0.0, 0.0)

    def _compute_command(
        self,
        x: float,
        y: float,
        yaw: float,
        target_x: float,
        target_y: float,
    ) -> Tuple[float, float]:
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)

        heading = math.atan2(dy, dx)
        heading_error = _wrap_to_pi(heading - yaw)
        angular_speed = max(
            -self.config.max_angular_speed,
            min(self.config.max_angular_speed, self.config.heading_gain * heading_error),
        )

        # Move slower while rotating sharply to avoid overshoot.
        heading_factor = max(0.0, 1.0 - abs(heading_error) / math.pi)
        linear_speed = min(self.config.max_linear_speed, distance) * heading_factor
        return linear_speed, angular_speed

    def _apply_base_velocity(self, linear_speed: float, angular_speed: float, yaw: float) -> None:
        vx = linear_speed * math.cos(yaw)
        vy = linear_speed * math.sin(yaw)
        p.resetBaseVelocity(
            self.body_id,
            linearVelocity=(vx, vy, 0.0),
            angularVelocity=(0.0, 0.0, angular_speed),
            physicsClientId=self.client_id,
        )
        self._set_wheels(linear_speed, angular_speed)

    def _discover_wheel_joints(self) -> List[int]:
        joints: List[int] = []
        num_joints = p.getNumJoints(self.body_id, physicsClientId=self.client_id)
        for joint_idx in range(num_joints):
            info = p.getJointInfo(self.body_id, joint_idx, physicsClientId=self.client_id)
            joint_type = int(info[2])
            name = info[1].decode("utf-8", errors="ignore").lower()
            if joint_type == p.JOINT_REVOLUTE and "wheel" in name:
                joints.append(joint_idx)
        return joints

    def _set_wheels(self, linear_speed: float, angular_speed: float) -> None:
        if not self._wheel_joint_indices:
            return
        base_speed = linear_speed * self.config.wheel_visual_speed_scale
        turn_component = angular_speed * 0.5 * self.config.wheel_visual_speed_scale
        split = len(self._wheel_joint_indices) // 2

        if split == 0:
            left = self._wheel_joint_indices
            right: List[int] = []
        else:
            left = self._wheel_joint_indices[:split]
            right = self._wheel_joint_indices[split:]

        for joint_idx in left:
            p.setJointMotorControl2(
                self.body_id,
                joint_idx,
                p.VELOCITY_CONTROL,
                targetVelocity=base_speed - turn_component,
                force=40.0,
                physicsClientId=self.client_id,
            )
        for joint_idx in right:
            p.setJointMotorControl2(
                self.body_id,
                joint_idx,
                p.VELOCITY_CONTROL,
                targetVelocity=base_speed + turn_component,
                force=40.0,
                physicsClientId=self.client_id,
            )
