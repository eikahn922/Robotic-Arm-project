# Model validation

`validate_model.py` statically validates the committed URDF/Xacro model and meshes. It uses only the
Python standard library — no ROS, no numpy — so it runs on the development Mac and inside the Ubuntu
VM alike.

```bash
python3 ros2_ws/src/robot_arm_description/test/validate_model.py
```

Exit code is 0 when every check passes and 1 otherwise, so it can be wired into CI or a pre-commit
hook.

## What it checks

Every assertion is recomputed from the real project files. The script deliberately avoids
re-stating constants that the Xacro already contains.

| Group | Checks |
| --- | --- |
| Xacro / XML | Every `${property}` expands; the expanded document parses |
| Tree | One root link, root is `base_link`, no cycles, no orphans, no link with two parent joints, no dangling parent/child references |
| Joints | All seven required joints exist with the expected type; exactly five non-mimic controls, in order |
| Mimic | Exactly one mimic joint; its target exists, is a real control, has a finite non-zero multiplier, and its own limits cover the mimicked range |
| Limits | Every non-fixed joint declares finite, correctly ordered limits that contain zero, and a non-degenerate axis |
| Meshes | Every `package://` reference resolves on disk and is a structurally valid binary STL (header triangle count matches file length); the gear, connector, and finger are each referenced exactly twice |
| Gripper kinematics | Reads `gripper_finger.stl`, finds the fingertip, and recomputes jaw separation through the actual joint transforms: closed at zero, opening with positive rotation, monotonic across the commanded range |
| Hygiene | No `build/`, `install/`, `log/`, `__pycache__`, `.pyc`, or `.DS_Store` files tracked by git |

## Runtime validation in the Ubuntu VM

The script cannot test ROS behaviour. Run these in the VM — see
[`docs/VM_HANDOFF.md`](../../../../docs/VM_HANDOFF.md) for the full procedure.

Expand the Xacro and validate the URDF tree:

```bash
ros2 run xacro xacro ~/robot_arm_ws/src/robot_arm_description/urdf/robot_arm.urdf.xacro -o /tmp/robot_arm.urdf && check_urdf /tmp/robot_arm.urdf
```

`check_urdf` should report `base_link` as the root and list the eight links.

Build the package:

```bash
cd ~/robot_arm_ws && colcon build --symlink-install --packages-select robot_arm_description --cmake-clean-cache
```

Launch the visualization:

```bash
LIBGL_ALWAYS_SOFTWARE=1 MESA_LOADER_DRIVER_OVERRIDE=llvmpipe QT_X11_NO_MITSHM=1 ros2 launch robot_arm_description display.launch.py
```

Confirm the transform chain reaches the moving gripper side:

```bash
ros2 run tf2_ros tf2_echo base_link left_gripper_link
```

Confirm the joint states, and that `right_gripper_joint` tracks `gripper_joint`:

```bash
ros2 topic echo /joint_states
```

Confirm exactly one publisher is driving the sliders:

```bash
ros2 topic info /joint_states --verbose
```
