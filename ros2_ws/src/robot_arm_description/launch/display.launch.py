"""Launch the RViz kinematic visualization for the robot arm.

This is a visualization, not a physics simulation. It starts
robot_state_publisher, joint_state_publisher_gui, and RViz. Nothing here computes
mass, contact, or gravity.

Arguments:
  show_collision:=true    show collision primitives with the meshes at 35% alpha
  rviz_config:=<path>     use an explicit RViz config; overrides show_collision
  gui:=false              skip joint_state_publisher_gui (headless joint states)
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

PKG = "robot_arm_description"

# The UTM virtual machine has no hardware OpenGL, so RViz must render in software.
SOFTWARE_RENDERING = {
    "LIBGL_ALWAYS_SOFTWARE": "1",
    "MESA_LOADER_DRIVER_OVERRIDE": "llvmpipe",
    "QT_X11_NO_MITSHM": "1",
}


def _truthy(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes", "on")


def launch_setup(context, *args, **kwargs):
    share = get_package_share_directory(PKG)
    xacro_file = os.path.join(share, "urdf", "robot_arm.urdf.xacro")

    explicit = LaunchConfiguration("rviz_config").perform(context).strip()
    show_collision = _truthy(LaunchConfiguration("show_collision").perform(context))
    use_gui = _truthy(LaunchConfiguration("gui").perform(context))

    if explicit:
        rviz_config = explicit
    else:
        name = "robot_arm_collision.rviz" if show_collision else "robot_arm.rviz"
        rviz_config = os.path.join(share, "rviz", name)

    if not os.path.exists(rviz_config):
        raise RuntimeError(f"RViz config not found: {rviz_config}")

    robot_description = {
        "robot_description": ParameterValue(Command(["xacro ", xacro_file]), value_type=str)
    }

    nodes = [
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[robot_description],
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config],
            additional_env=SOFTWARE_RENDERING,
        ),
    ]

    if use_gui:
        # Only one publisher may drive /joint_states, or the sliders and the model fight.
        nodes.insert(
            1,
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher_gui",
                output="screen",
                parameters=[robot_description],
            ),
        )

    return nodes


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "show_collision",
                default_value="false",
                description="Show collision primitives with the visual meshes at 35% alpha.",
            ),
            DeclareLaunchArgument(
                "rviz_config",
                default_value="",
                description="Absolute path to an RViz config. Overrides show_collision when set.",
            ),
            DeclareLaunchArgument(
                "gui",
                default_value="true",
                description="Start joint_state_publisher_gui. Set false to drive /joint_states elsewhere.",
            ),
            OpaqueFunction(function=launch_setup),
        ]
    )
