#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import subprocess
import threading
import time

JOINTS = [
    'shoulder_pan_joint',
    'shoulder_lift_joint',
    'elbow_joint',
    'wrist_1_joint',
    'wrist_2_joint',
    'wrist_3_joint',
]

# [shoulder_pan, shoulder_lift, elbow, wrist_1, wrist_2, wrist_3]
HOME       = [0.0,   -1.57,  0.0,  -1.57, 0.0,  0.0]
PRE_GRASP  = [0.0,   -1.0,   0.8,  -1.4,  -1.57, 0.0]
GRASP      = [0.0,   -0.75,  1.1,  -1.9,  -1.57, 0.0]
LIFT       = [0.0,   -1.2,   0.7,  -1.1,  -1.57, 0.0]
PRE_PLACE  = [-1.2,  -1.0,   0.5,  -1.1,  -1.57, 0.0]
PLACE      = [-1.05, -0.10,  0.00, -1.45, -1.57, 0.0]
POST_PLACE = [-1.2,  -1.2,   0.7,  -1.1,  -1.57, 0.0]

# Sabit koordinatlar (x, y, z)
BOX_START = (0.5,  0.2,  0.05)
BOX_TABLE = (0.4, -0.5,  0.80)


class PickPlaceDemo(Node):
    def __init__(self):
        super().__init__('pick_place_demo')
        self._action_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/ur_manipulator_controller/follow_joint_trajectory'
        )

    def move_to(self, positions, duration_sec=4.0, label=''):
        self.get_logger().info(f'Moving to: {label}')
        goal = FollowJointTrajectory.Goal()
        traj = JointTrajectory()
        traj.joint_names = JOINTS
        point = JointTrajectoryPoint()
        point.positions = positions
        point.velocities = [0.0] * 6
        point.time_from_start = Duration(sec=int(duration_sec), nanosec=0)
        traj.points = [point]
        goal.trajectory = traj
        self._action_client.wait_for_server()
        future = self._action_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)
        result_future = future.result().get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        self.get_logger().info(f'[OK] {label}')
        time.sleep(0.5)

    def set_box_pose(self, x, y, z):
        cmd = (
            f"gz service -s /world/pick_place_cell_world/set_pose "
            f"--reqtype gz.msgs.Pose "
            f"--reptype gz.msgs.Boolean "
            f"--timeout 300 "
            f"--req 'name: \"package_box\" position: {{x: {x:.3f}, y: {y:.3f}, z: {z:.3f}}}'"
        )
        subprocess.run(cmd, shell=True, capture_output=True)

    def animate_box(self, start, end, steps=36, total_time=0.5):
        for i in range(1, steps + 1):
            t = i / steps
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            z = start[2] + (end[2] - start[2]) * t
            self.set_box_pose(x, y, z)
            time.sleep(total_time / steps)
        self.get_logger().info(
            f'Box carried to ({end[0]:.2f}, {end[1]:.2f}, {end[2]:.2f})'
        )


def main():
    rclpy.init()
    node = PickPlaceDemo()
    time.sleep(2.0)
    print('=== Pick & Place Demo Starting ===', flush=True)

    # Kutuyu zemine sabitle
    node.set_box_pose(*BOX_START)

    node.move_to(HOME,      4.0, 'Home')
    node.move_to(PRE_GRASP, 4.0, 'Pre-grasp')
    node.move_to(GRASP,     4.0, 'Grasp')

    # Tasima: kol Lift -> Pre-place -> Place yaparken kutu es zamanli
    # olarak zeminden masaya kayar (kinematic -> firlatma yok)
    carry = threading.Thread(
        target=node.animate_box,
        args=(BOX_START, BOX_TABLE),
        kwargs={'steps': 36, 'total_time': 0.5},
        daemon=True,
    )
    carry.start()

    node.move_to(LIFT,      4.0, 'Lift')
    node.move_to(PRE_PLACE, 4.0, 'Pre-place')
    node.move_to(PLACE,     4.0, 'Place')

    carry.join()

    node.move_to(POST_PLACE, 3.0, 'Post-place')
    node.move_to(HOME,       4.0, 'Return home')

    print('=== Pick & Place Demo Complete ===', flush=True)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()