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

`joint_state_publisher_gui` exposes six sliders:

| Joint | Type | Axis | Limits (rad) | Basis |
| --- | --- | --- | --- | --- |
| `base_yaw_joint` | revolute | `0 0 1` | −3.1416 to 3.1416 | provisional |
| `shoulder_joint` | revolute | `0 1 0` | −1.5708 to 1.5708 | provisional |
| `elbow_joint` | revolute | `0 1 0` | −2.0944 to 2.0944 | provisional |
| `wrist_roll_joint` | revolute | `0 0 1` | −3.1416 to 3.1416 | provisional |
| `wrist_pitch_joint` | revolute | `1 0 0` | −1.5708 to 1.5708 | provisional |
| `gripper_joint` | revolute | `0 0 1` | 0 to 0.75 | provisional; 0 = closed, 0.75 = 51.8 mm |

Three joints follow `gripper_joint` through URDF `mimic` tags and are deliberately not independent
controls: `right_gripper_joint` (opposing side) and `left_finger_joint` / `right_finger_joint`
(the parallelogram counter-rotation that keeps the jaw faces from fanning open).

## Link tree

```text
base_link
└── base_yaw_joint      (revolute)  → waist_link
    └── shoulder_joint  (revolute)  → upper_arm_link
        └── elbow_joint (revolute)  → forearm_link
            └── wrist_roll_joint  (revolute) → wrist_link
                └── wrist_pitch_joint (revolute) → gripper_base_link
                    ├── gripper_joint        (revolute) → left_gear_link
                    │   └── left_finger_joint  (mimic)  → left_finger_link
                    └── right_gripper_joint  (mimic)    → right_gear_link
                        └── right_finger_joint (mimic)  → right_finger_link
```
