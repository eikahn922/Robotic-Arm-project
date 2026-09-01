"""Launch the arm with ros2_control, without any simulator.

This starts a controller_manager backed by mock hardware, so the whole control
stack - broadcaster, arm controller, gripper controller - can be exercised
before Gazebo is involved. On an ARM64 VM with software rendering that is the
cheapest way to find controller problems, because nothing here needs a physics
engine or a GPU.

  hardware:=mock    (default) mock_components/GenericSystem
  hardware:=gazebo  expand for Gazebo Sim instead; note this launch file does
                    NOT start Gazebo, it only builds the description
  rviz:=false       skip RViz

Commands are position-based. See docs/SIMULATION.md for CLI test commands.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

PKG = "robot_arm_description"

SOFTWARE_RENDERING = {
    "LIBGL_ALWAYS_SOFTWARE": "1",
    "MESA_LOADER_DRIVER_OVERRIDE": "llvmpipe",
    "QT_X11_NO_MITSHM": "1",
}


def _truthy(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes", "on")


def launch_setup(context, *args, **kwargs):
    share = get_package_share_directory(PKG)
    hardware = LaunchConfiguration("hardware").perform(context).strip()
    use_rviz = _truthy(LaunchConfiguration("rviz").perform(context))

    if hardware not in ("mock", "gazebo"):
        raise RuntimeError(f"hardware must be 'mock' or 'gazebo', got {hardware!r}")

    xacro_file = os.path.join(share, "urdf", "robot_arm_control.urdf.xacro")
    controllers = os.path.join(share, "config", "controllers.yaml")
    rviz_config = os.path.join(share, "rviz", "robot_arm.rviz")

    for path in (xacro_file, controllers):
        if not os.path.exists(path):
            raise RuntimeError(f"missing required file: {path}")

    robot_description = {
        "robot_description": ParameterValue(
            Command(["xacro ", xacro_file, " hardware:=", hardware]), value_type=str
        )
    }

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        output="screen",
        parameters=[robot_description, controllers],
    )
    state_pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    def spawner(name, *extra):
        return Node(package="controller_manager", executable="spawner",
                    arguments=[name, "--controller-manager", "/controller_manager", *extra],
                    output="screen")

    broadcaster = spawner("joint_state_broadcaster")
    arm = spawner("arm_controller")
    gripper = spawner("gripper_controller")

    nodes = [
        control_node,
        state_pub,
        broadcaster,
        # Start the controllers only once the broadcaster is up, so joint states
        # exist before anything tries to command a trajectory.
        RegisterEventHandler(OnProcessExit(target_action=broadcaster, on_exit=[arm, gripper])),
    ]

    if use_rviz:
        nodes.append(Node(package="rviz2", executable="rviz2", name="rviz2", output="screen",
                          arguments=["-d", rviz_config], additional_env=SOFTWARE_RENDERING))
    return nodes


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("hardware", default_value="mock",
                              description="mock | gazebo"),
        DeclareLaunchArgument("rviz", default_value="true",
                              description="Start RViz alongside the controllers."),
        OpaqueFunction(function=launch_setup),
    ])
