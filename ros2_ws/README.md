# ROS 2 Workspace

This directory contains the ROS 2 Jazzy packages for the 3-DOF robotic arm. See [ROS_PROGRESS.md](../ROS_PROGRESS.md) for the completed milestones, lessons learned, and next steps.

## Build and launch

Copy or clone this repository into an Ubuntu 24.04 environment with ROS 2 Jazzy installed, then run:

```bash
cd ros2_ws
colcon build --symlink-install --packages-select robot_arm_description
source install/setup.bash
LIBGL_ALWAYS_SOFTWARE=1 \
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe \
QT_X11_NO_MITSHM=1 \
ros2 launch robot_arm_description display.launch.py
```

The three environment variables force software rendering, which the current UTM virtual machine
requires. They may be omitted on a native Linux system with working OpenGL acceleration.

See [docs/VM_HANDOFF.md](../docs/VM_HANDOFF.md) for the full Ubuntu VM update, build, launch, and
troubleshooting procedure.

## What this package currently is

An RViz **kinematic visualization**: `robot_state_publisher` publishes the TF tree from the URDF,
`joint_state_publisher_gui` provides sliders, and RViz draws the meshes. There is no physics engine.
Gazebo Sim and `ros2_control` are not implemented yet.

## Joint controls

`joint_state_publisher_gui` exposes five sliders:

| Joint | Type | Axis | Limits (rad) | Basis |
| --- | --- | --- | --- | --- |
| `base_yaw_joint` | revolute | `0 0 1` | −3.1416 to 3.1416 | provisional |
| `shoulder_joint` | revolute | `0 1 0` | −1.5708 to 1.5708 | provisional |
| `elbow_joint` | revolute | `0 1 0` | −2.0944 to 2.0944 | provisional |
| `wrist_joint` | revolute | `0 1 0` | −1.5708 to 1.5708 | provisional |
| `gripper_joint` | revolute | `0 0 1` | 0 to 0.30 | provisional; 0 = closed |

`right_gripper_joint` mirrors `gripper_joint` through a URDF `mimic` tag and is deliberately not an
independent control.

## Link tree

```text
base_link
└── base_yaw_joint      (revolute)  → waist_link
    └── shoulder_joint  (revolute)  → upper_arm_link
        └── elbow_joint (revolute)  → forearm_link
            └── wrist_joint (revolute) → wrist_link
                └── gripper_base_joint (fixed) → gripper_base_link
                    ├── gripper_joint       (revolute) → left_gripper_link
                    └── right_gripper_joint (mimic)    → right_gripper_link
```
