from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder(
            'pick_place_cell_ur5e',
            package_name='pick_place_cell_moveit_config',
        )
        .robot_description(file_path='config/pick_place_cell_ur5e.urdf.xacro')
        .robot_description_semantic(file_path='config/pick_place_cell_ur5e.srdf')
        .trajectory_execution(file_path='config/moveit_controllers.yaml')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )

    move_group = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[moveit_config.to_dict(), {'use_sim_time': True}],
    )

    return LaunchDescription([move_group])
