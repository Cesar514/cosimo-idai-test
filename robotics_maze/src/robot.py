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


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _smoothstep01(value: float) -> float:
    clamped = _clamp(value, 0.0, 1.0)
    return clamped * clamped * (3.0 - 2.0 * clamped)


@dataclass
class PathFollowerConfig:
    """Controller gains for simple waypoint tracking."""

    max_linear_speed: float = 4.0
    max_angular_speed: float = 3.5
    heading_gain: float = 3.0
    max_linear_accel: float = 7.0
    max_linear_decel: float = 9.0
    max_angular_accel: float = 12.0
    max_angular_decel: float = 14.0
    heading_drive_blend_start_rad: float = 0.25
    heading_turn_in_place_rad: float = 0.85
    waypoint_tolerance: float = 0.35
    final_waypoint_tolerance: float = 0.50
    wheel_visual_speed_scale: float = 8.0
    wheel_radius_m: float = 0.165
    axle_track_m: float = 0.55
    wheel_max_force: float = 220.0
    base_velocity_assist_gain: float = 0.22
    base_velocity_assist_max_linear: float = 0.45
    base_velocity_assist_max_angular: float = 0.75


class MobileRobotController:
    """Mobile robot controller with wheel-joint dynamics when available."""

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
        self._left_wheel_joint_indices, self._right_wheel_joint_indices = self._split_wheel_sides()
        self._has_differential_drive = bool(
            self._left_wheel_joint_indices and self._right_wheel_joint_indices
        )
        self._effective_wheel_radius_m = max(self.config.wheel_radius_m, 1e-3)
        self._effective_axle_track_m = max(self.config.axle_track_m, 1e-3)
        self._control_dt_s = self._infer_control_dt_s()
        self._smoothed_linear_speed = 0.0
        self._smoothed_angular_speed = 0.0
        if self._has_differential_drive:
            estimated_radius = self._estimate_wheel_radius_m()
            if estimated_radius is not None:
                self._effective_wheel_radius_m = estimated_radius
            estimated_track = self._estimate_axle_track_m()
            if estimated_track is not None:
                self._effective_axle_track_m = estimated_track

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
        self._smoothed_linear_speed = 0.0
        self._smoothed_angular_speed = 0.0
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

        target_linear_speed, target_angular_speed = self._compute_command(
            x, y, yaw, target_x, target_y
        )
        linear_speed, angular_speed = self._apply_command_dynamics(
            target_linear_speed, target_angular_speed
        )
        self._apply_base_velocity(linear_speed, angular_speed, yaw)
        return False

    def stop(self) -> None:
        self._smoothed_linear_speed = 0.0
        self._smoothed_angular_speed = 0.0
        if self._has_differential_drive:
            self._drive_wheels_differential(0.0, 0.0)
            return

        p.resetBaseVelocity(
            self.body_id,
            linearVelocity=(0.0, 0.0, 0.0),
            angularVelocity=(0.0, 0.0, 0.0),
            physicsClientId=self.client_id,
        )
        self._set_wheels_visual(0.0, 0.0)

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
        angular_speed = _clamp(
            self.config.heading_gain * heading_error,
            -self.config.max_angular_speed,
            self.config.max_angular_speed,
        )

        # Reduce speed as we approach the waypoint while respecting a feasible braking profile.
        linear_speed = min(
            self.config.max_linear_speed,
            distance,
            math.sqrt(max(0.0, 2.0 * self.config.max_linear_decel * distance)),
        )

        # Blend from turn-in-place into forward driving to keep heading transitions smooth.
        abs_heading_error = abs(heading_error)
        drive_start = max(self.config.heading_drive_blend_start_rad, 1e-3)
        turn_full = max(self.config.heading_turn_in_place_rad, drive_start + 1e-3)
        if abs_heading_error >= turn_full:
            heading_factor = 0.0
        elif abs_heading_error <= drive_start:
            heading_factor = 1.0
        else:
            blend = (abs_heading_error - drive_start) / (turn_full - drive_start)
            heading_factor = 1.0 - _smoothstep01(blend)
        linear_speed *= heading_factor
        return linear_speed, angular_speed

    def _apply_command_dynamics(
        self,
        target_linear_speed: float,
        target_angular_speed: float,
    ) -> Tuple[float, float]:
        linear_speed = self._slew_rate_limit(
            current=self._smoothed_linear_speed,
            target=target_linear_speed,
            accel_limit=self.config.max_linear_accel,
            decel_limit=self.config.max_linear_decel,
        )
        angular_speed = self._slew_rate_limit(
            current=self._smoothed_angular_speed,
            target=target_angular_speed,
            accel_limit=self.config.max_angular_accel,
            decel_limit=self.config.max_angular_decel,
        )

        max_turn_linear_speed = self._turn_linear_limit(abs(angular_speed))
        linear_speed = _clamp(linear_speed, -max_turn_linear_speed, max_turn_linear_speed)

        if abs(linear_speed) <= 1e-5:
            linear_speed = 0.0
        if abs(angular_speed) <= 1e-5:
            angular_speed = 0.0

        self._smoothed_linear_speed = linear_speed
        self._smoothed_angular_speed = angular_speed
        return linear_speed, angular_speed

    def _slew_rate_limit(
        self,
        *,
        current: float,
        target: float,
        accel_limit: float,
        decel_limit: float,
    ) -> float:
        delta = target - current
        if abs(delta) <= 1e-9:
            return target

        accel_limit = max(accel_limit, 1e-6)
        decel_limit = max(decel_limit, 1e-6)
        same_direction = abs(current) <= 1e-9 or math.copysign(1.0, current) == math.copysign(1.0, target)
        speeding_up = same_direction and abs(target) > abs(current)
        limit = accel_limit if speeding_up else decel_limit
        max_delta = limit * self._control_dt_s
        if delta > max_delta:
            return current + max_delta
        if delta < -max_delta:
            return current - max_delta
        return target

    def _turn_linear_limit(self, angular_speed_abs: float) -> float:
        normalized = _clamp(
            angular_speed_abs / max(self.config.max_angular_speed, 1e-3),
            0.0,
            1.0,
        )
        reduction = 0.68 * _smoothstep01(normalized)
        return self.config.max_linear_speed * max(0.18, 1.0 - reduction)

    def _infer_control_dt_s(self) -> float:
        default_dt = 1.0 / 240.0
        try:
            params = p.getPhysicsEngineParameters(physicsClientId=self.client_id)
        except Exception:
            return default_dt
        raw_dt = params.get("fixedTimeStep", params.get("timeStep", default_dt))
        try:
            dt = float(raw_dt)
        except (TypeError, ValueError):
            return default_dt
        if not math.isfinite(dt) or dt <= 0.0:
            return default_dt
        return dt

    def _apply_base_velocity(self, linear_speed: float, angular_speed: float, yaw: float) -> None:
        if self._has_differential_drive:
            self._drive_wheels_differential(linear_speed, angular_speed)
            self._apply_base_velocity_assist(linear_speed, angular_speed, yaw)
            return

        vx = linear_speed * math.cos(yaw)
        vy = linear_speed * math.sin(yaw)
        p.resetBaseVelocity(
            self.body_id,
            linearVelocity=(vx, vy, 0.0),
            angularVelocity=(0.0, 0.0, angular_speed),
            physicsClientId=self.client_id,
        )
        self._set_wheels_visual(linear_speed, angular_speed)

    def _apply_base_velocity_assist(self, linear_speed: float, angular_speed: float, yaw: float) -> None:
        assist_gain = max(self.config.base_velocity_assist_gain, 0.0)
        if assist_gain <= 0.0:
            return

        max_linear_assist = max(self.config.base_velocity_assist_max_linear, 0.0)
        max_angular_assist = max(self.config.base_velocity_assist_max_angular, 0.0)
        if max_linear_assist <= 0.0 and max_angular_assist <= 0.0:
            return

        base_linear, base_angular = p.getBaseVelocity(self.body_id, physicsClientId=self.client_id)
        current_forward_speed = (
            float(base_linear[0]) * math.cos(yaw) + float(base_linear[1]) * math.sin(yaw)
        )
        linear_error = linear_speed - current_forward_speed
        angular_error = angular_speed - float(base_angular[2])

        linear_assist = _clamp(linear_error * assist_gain, -max_linear_assist, max_linear_assist)
        angular_assist = _clamp(angular_error * assist_gain, -max_angular_assist, max_angular_assist)
        if abs(linear_assist) <= 1e-6 and abs(angular_assist) <= 1e-6:
            return

        p.resetBaseVelocity(
            self.body_id,
            linearVelocity=(
                float(base_linear[0]) + linear_assist * math.cos(yaw),
                float(base_linear[1]) + linear_assist * math.sin(yaw),
                float(base_linear[2]),
            ),
            angularVelocity=(
                float(base_angular[0]),
                float(base_angular[1]),
                float(base_angular[2]) + angular_assist,
            ),
            physicsClientId=self.client_id,
        )

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

    def _split_wheel_sides(self) -> tuple[List[int], List[int]]:
        left: List[int] = []
        right: List[int] = []
        unresolved: List[int] = []
        for joint_idx in self._wheel_joint_indices:
            info = p.getJointInfo(self.body_id, joint_idx, physicsClientId=self.client_id)
            name = info[1].decode("utf-8", errors="ignore").lower()
            if "left" in name:
                left.append(joint_idx)
            elif "right" in name:
                right.append(joint_idx)
            else:
                unresolved.append(joint_idx)

        # Fallback heuristic when wheel naming is incomplete:
        # use the wheel center Y offset in base frame to infer side.
        for joint_idx in unresolved:
            position = self._get_link_position_in_base_frame(joint_idx)
            if position is None:
                continue
            if position[1] > 1e-3:
                left.append(joint_idx)
            elif position[1] < -1e-3:
                right.append(joint_idx)

        if left and right:
            return sorted(left), sorted(right)

        split = len(self._wheel_joint_indices) // 2
        if split == 0:
            return self._wheel_joint_indices[:], []
        return self._wheel_joint_indices[:split], self._wheel_joint_indices[split:]

    def _get_link_position_in_base_frame(self, joint_idx: int) -> Optional[Tuple[float, float, float]]:
        link_state = p.getLinkState(
            self.body_id,
            joint_idx,
            computeForwardKinematics=1,
            physicsClientId=self.client_id,
        )
        if not link_state:
            return None
        base_position, base_orientation = p.getBasePositionAndOrientation(
            self.body_id, physicsClientId=self.client_id
        )
        inverse_position, inverse_orientation = p.invertTransform(base_position, base_orientation)
        local_position, _ = p.multiplyTransforms(
            inverse_position,
            inverse_orientation,
            link_state[0],
            (0.0, 0.0, 0.0, 1.0),
        )
        return float(local_position[0]), float(local_position[1]), float(local_position[2])

    def _estimate_axle_track_m(self) -> Optional[float]:
        left_center = self._mean_wheel_center_xy(self._left_wheel_joint_indices)
        right_center = self._mean_wheel_center_xy(self._right_wheel_joint_indices)
        if left_center is None or right_center is None:
            return None
        track = math.hypot(left_center[0] - right_center[0], left_center[1] - right_center[1])
        if track <= 1e-3:
            return None
        return track

    def _mean_wheel_center_xy(self, wheel_indices: Sequence[int]) -> Optional[Tuple[float, float]]:
        if not wheel_indices:
            return None
        xs: List[float] = []
        ys: List[float] = []
        for joint_idx in wheel_indices:
            position = self._get_link_position_in_base_frame(joint_idx)
            if position is None:
                continue
            xs.append(position[0])
            ys.append(position[1])
        if not xs:
            return None
        return sum(xs) / len(xs), sum(ys) / len(ys)

    def _estimate_wheel_radius_m(self) -> Optional[float]:
        radii: List[float] = []
        for joint_idx in self._wheel_joint_indices:
            wheel_radius = self._estimate_joint_wheel_radius_m(joint_idx)
            if wheel_radius is not None:
                radii.append(wheel_radius)
        if not radii:
            return None
        radii.sort()
        return radii[len(radii) // 2]

    def _estimate_joint_wheel_radius_m(self, joint_idx: int) -> Optional[float]:
        aabb_min, aabb_max = p.getAABB(self.body_id, joint_idx, physicsClientId=self.client_id)
        half_extents = [
            max(0.0, 0.5 * (float(aabb_max[axis]) - float(aabb_min[axis])))
            for axis in range(3)
        ]
        if max(half_extents) <= 1e-6:
            return None

        info = p.getJointInfo(self.body_id, joint_idx, physicsClientId=self.client_id)
        joint_axis = info[13]
        axis_index = max(range(3), key=lambda axis: abs(float(joint_axis[axis])))
        perpendicular_extents = [
            half_extents[axis] for axis in range(3) if axis != axis_index
        ]
        if not perpendicular_extents:
            return None

        radius = max(perpendicular_extents)
        if radius <= 1e-4:
            return None
        return radius

    def _drive_wheels_differential(self, linear_speed: float, angular_speed: float) -> None:
        half_track = self._effective_axle_track_m * 0.5
        left_linear = linear_speed - (angular_speed * half_track)
        right_linear = linear_speed + (angular_speed * half_track)

        radius = self._effective_wheel_radius_m
        left_omega = left_linear / radius
        right_omega = right_linear / radius

        for joint_idx in self._left_wheel_joint_indices:
            p.setJointMotorControl2(
                self.body_id,
                joint_idx,
                p.VELOCITY_CONTROL,
                targetVelocity=left_omega,
                force=self.config.wheel_max_force,
                physicsClientId=self.client_id,
            )
        for joint_idx in self._right_wheel_joint_indices:
            p.setJointMotorControl2(
                self.body_id,
                joint_idx,
                p.VELOCITY_CONTROL,
                targetVelocity=right_omega,
                force=self.config.wheel_max_force,
                physicsClientId=self.client_id,
            )

    def _set_wheels_visual(self, linear_speed: float, angular_speed: float) -> None:
        if not self._wheel_joint_indices:
            return
        base_speed = linear_speed * self.config.wheel_visual_speed_scale
        turn_component = angular_speed * 0.5 * self.config.wheel_visual_speed_scale

        if self._left_wheel_joint_indices and self._right_wheel_joint_indices:
            left = self._left_wheel_joint_indices
            right = self._right_wheel_joint_indices
        else:
            split = len(self._wheel_joint_indices) // 2
            if split == 0:
                left = self._wheel_joint_indices
                right = []
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
