#!/usr/bin/env python3

import os
import time

from moveit.core.robot_state import RobotState
from moveit.planning import MoveItPy
import numpy as np


def main():
    moveit = MoveItPy(node_name='moveit_joint_goal_demo')
    arm = moveit.get_planning_component('ur_manipulator')

    robot_state = RobotState(moveit.get_robot_model())
    robot_state.set_to_default_values()
    robot_state.set_joint_group_positions(
        'ur_manipulator',
        np.array([0.0, -1.0, 1.2, -1.4, -1.57, 0.0]),
    )

    arm.set_start_state_to_current_state()
    arm.set_goal_state(robot_state=robot_state)

    plan_result = arm.plan()
    if plan_result:
        time.sleep(2.0)
        moveit.execute(
            plan_result.trajectory,
            controllers=['ur_manipulator_controller'],
        )
        print('MoveIt joint goal executed', flush=True)
        os._exit(0)
    else:
        print('MoveIt planning failed', flush=True)
        os._exit(1)


if __name__ == '__main__':
    main()
