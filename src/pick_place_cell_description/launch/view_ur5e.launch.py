from launch import LaunchDescription
from launch.substitutions import Command
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    xacro_file = PathJoinSubstitution([
        FindPackageShare('pick_place_cell_description'),
        'urdf',
        'ur5e_cell.urdf.xacro',
    ])

    robot_description = {
        'robot_description': Command(['xacro ', xacro_file])
    }

    rviz_config = PathJoinSubstitution([
        FindPackageShare('pick_place_cell_description'),
        'rviz',
        'ur5e_view.rviz',
    ])

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description],
            output='screen',
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            output='screen',
        ),
    ])
