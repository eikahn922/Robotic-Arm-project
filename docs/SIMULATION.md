# Control and Simulation Guide

Status of each layer, and how to test it. Read the status column before assuming something works.

| Layer | State | Verified? |
| --- | --- | --- |
| RViz kinematic visualization | Implemented | Statically validated; **RViz rendering not yet run** |
| Collision geometry | Implemented | Statically validated |
| Inertial properties | Implemented | Statically validated; no physics engine has consumed them |
| `ros2_control` (mock hardware) | Implemented | **Never run** — plugin and parameter names unverified |
| `ros2_control` (Gazebo) | Description only | Not implemented — no world, no spawn, no `gz_ros2_control` launch |
| Gazebo Sim | Not implemented | — |
| MoveIt 2 | Not implemented | — |
| RGB-D camera | Not implemented | — |
| Ball detection | Not implemented | — |
| Autonomous pick-and-place | Not implemented | — |

Everything below the `ros2_control (mock)` row does not exist yet. Do not describe this project as
having a Gazebo simulation.

## Two separate entry points

The visualization path and the control path are deliberately separate, so a broken controller cannot
break the thing that already works.

| File | Purpose | Model |
| --- | --- | --- |
| `launch/display.launch.py` | RViz + slider GUI, no controllers | `urdf/robot_arm.urdf.xacro` |
| `launch/control.launch.py` | `controller_manager` + controllers | `urdf/robot_arm_control.urdf.xacro` |

`robot_arm.urdf.xacro` carries no `ros2_control` tags at all. The control variant includes it and
adds the hardware interface on top.

## Static validation (runs anywhere, no ROS)

```bash
python3 ros2_ws/src/robot_arm_description/test/validate_model.py
```

## Build

```bash
cd ~/robot_arm_ws && colcon build --symlink-install --packages-select robot_arm_description --cmake-clean-cache
```

```bash
source ~/robot_arm_ws/install/setup.bash
```

## 1. Visualization only

```bash
LIBGL_ALWAYS_SOFTWARE=1 MESA_LOADER_DRIVER_OVERRIDE=llvmpipe QT_X11_NO_MITSHM=1 ros2 launch robot_arm_description display.launch.py
```

Show collision primitives instead (meshes drop to 35% alpha so the boxes show through):

```bash
LIBGL_ALWAYS_SOFTWARE=1 MESA_LOADER_DRIVER_OVERRIDE=llvmpipe QT_X11_NO_MITSHM=1 ros2 launch robot_arm_description display.launch.py show_collision:=true
```

## 2. Expand and check the control model

Do this before launching controllers — it catches xacro and URDF errors on their own:

```bash
ros2 run xacro xacro ~/robot_arm_ws/src/robot_arm_description/urdf/robot_arm_control.urdf.xacro hardware:=mock -o /tmp/arm_control.urdf && check_urdf /tmp/arm_control.urdf
```

Confirm the `ros2_control` block survived expansion, and that the mimic joint is *not* in it:

```bash
grep -A3 "<ros2_control" /tmp/arm_control.urdf && grep -c right_gripper_joint /tmp/arm_control.urdf
```

`right_gripper_joint` should appear in the `<joint>`/`<mimic>` model section but **not** inside
`<ros2_control>`.

## 3. Controllers on mock hardware — no simulator needed

This is the cheapest way to find controller problems on an ARM64 VM, because nothing here needs a
physics engine or a GPU.

```bash
LIBGL_ALWAYS_SOFTWARE=1 MESA_LOADER_DRIVER_OVERRIDE=llvmpipe QT_X11_NO_MITSHM=1 ros2 launch robot_arm_description control.launch.py
```

In a second terminal, confirm the controllers loaded and are active:

```bash
ros2 control list_controllers
```

Expect `joint_state_broadcaster`, `arm_controller`, and `gripper_controller`, all `active`.

List the command interfaces — there should be exactly five, and none for `right_gripper_joint`:

```bash
ros2 control list_hardware_interfaces
```

### Command each joint independently

Shoulder to +0.5 rad:

```bash
ros2 topic pub --once /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: [base_yaw_joint, shoulder_joint, elbow_joint, wrist_joint], points: [{positions: [0.0, 0.5, 0.0, 0.0], time_from_start: {sec: 2}}]}"
```

Base yaw to +1.0 rad:

```bash
ros2 topic pub --once /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: [base_yaw_joint, shoulder_joint, elbow_joint, wrist_joint], points: [{positions: [1.0, 0.0, 0.0, 0.0], time_from_start: {sec: 2}}]}"
```

Open the gripper (0 is closed, 0.30 is open):

```bash
ros2 topic pub --once /gripper_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: [gripper_joint], points: [{positions: [0.30], time_from_start: {sec: 1}}]}"
```

Close it again:

```bash
ros2 topic pub --once /gripper_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: [gripper_joint], points: [{positions: [0.0], time_from_start: {sec: 1}}]}"
```

### Confirm the mimic side follows

While the gripper is part-open, both sides should report the same angle:

```bash
ros2 topic echo /joint_states --once
```

`gripper_joint` and `right_gripper_joint` should hold equal positions. If `right_gripper_joint` stays
at zero while `gripper_joint` moves, mimic propagation is not working in the installed
`ros2_control` version and the gripper will need an explicit second command interface instead.

Confirm the transform chain reaches both fingers:

```bash
ros2 run tf2_ros tf2_echo base_link left_gripper_link
```

## Unverified assumptions

These are written from documentation, not from a run. Check them first if something fails:

1. `mock_components/GenericSystem` is the correct mock plugin name for the installed `ros2_control`.
2. `gz_ros2_control/GazeboSimSystem` is the correct Gazebo Sim plugin for ROS 2 Jazzy.
3. `ros2_control` propagates URDF `<mimic>` joints automatically, so `right_gripper_joint` needs no
   command interface. **This is the assumption most likely to be wrong**, and the joint-state check
   above is the test for it.
4. The controller parameter names in `config/controllers.yaml` match the installed
   `joint_trajectory_controller`.
5. Controller gains and tolerances are provisional. They have never been tuned against real dynamics.

## Next steps toward Gazebo

Not started. In order: a world file with ground plane and lighting, a spawn launch file, the
`gz_ros2_control` plugin block, then controller startup against the simulated hardware. Begin
headless (`gz sim -s`) — the VM is ARM64 with LLVMpipe software rendering, and Gazebo physics plus
camera rendering is a substantially harder proposition than RViz. Add the RGB-D camera only after
physics and control are stable.
