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

    controllers_file = PathJoinSubstitution([
        FindPackageShare('pick_place_cell_moveit_config'),
        'config',
        'ros2_controllers.yaml',
    ])

    robot_description = {
        'robot_description': Command(['xacro ', xacro_file])
    }

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description],
        output='screen',
    )

    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description, controllers_file],
        output='screen',
    )

    return LaunchDescription([
        robot_state_publisher,
        controller_manager,
    ])
