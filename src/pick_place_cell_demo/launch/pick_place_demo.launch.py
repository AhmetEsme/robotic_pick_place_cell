from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pick_place_cell_demo',
            executable='pick_place_demo',
            output='screen',
        )
    ])