# Ubuntu VM Handoff — Build, Launch, and Troubleshoot

Keep this file current whenever package paths, link names, launch files, or simulation commands
change.

## Development environment

| Item | Value |
| --- | --- |
| Host | Apple Silicon Mac |
| Virtualization | UTM / QEMU |
| Guest OS | Ubuntu 24.04 ARM64 |
| ROS distribution | ROS 2 Jazzy |
| Linux username | `ezra` |
| VM hostname | `ezra-QEMU-Virtual-Machine` |
| ROS workspace | `/home/ezra/robot_arm_ws` |
| GitHub clone | `/home/ezra/Robotic-Arm-project-main` |
| ROS package | `robot_arm_description` |
| Package source | `/home/ezra/robot_arm_ws/src/robot_arm_description` |
| Installed package | `/home/ezra/robot_arm_ws/install/robot_arm_description` |

## Terminology

The current program is an RViz **kinematic visualization**, not a physics simulation. It runs
`robot_state_publisher`, `joint_state_publisher_gui`, and RViz. Gazebo Sim and `ros2_control` have
not been implemented. Do not call this a Gazebo simulation.

## Update the VM from GitHub

Stop any running ROS launch with Ctrl+C, then:

```bash
git -C ~/Robotic-Arm-project-main pull --ff-only origin main
```

Check the retrieved version:

```bash
git -C ~/Robotic-Arm-project-main log --oneline -1
```

Copy the package from the clone into the ROS workspace:

```bash
cp -a ~/Robotic-Arm-project-main/ros2_ws/src/robot_arm_description/. ~/robot_arm_ws/src/robot_arm_description/
```

Load ROS:

```bash
source /opt/ros/jazzy/setup.bash
```

Build:

```bash
cd ~/robot_arm_ws && colcon build --symlink-install --packages-select robot_arm_description --cmake-clean-cache
```

Load the built workspace:

```bash
source ~/robot_arm_ws/install/setup.bash
```

Confirm which package ROS will load:

```bash
ros2 pkg prefix robot_arm_description
```

Expected output: `/home/ezra/robot_arm_ws/install/robot_arm_description`

## Launch RViz and the joint controls

The VM requires software rendering:

```bash
LIBGL_ALWAYS_SOFTWARE=1 MESA_LOADER_DRIVER_OVERRIDE=llvmpipe QT_X11_NO_MITSHM=1 ros2 launch robot_arm_description display.launch.py
```

Keep this terminal open. Ctrl+C stops RViz, `robot_state_publisher`, and Joint State Publisher.

The launch file starts `robot_state_publisher`, `joint_state_publisher_gui`, and `rviz2`. Do not
start a second `joint_state_publisher_gui` while the launch file's instance is running — two
publishers on `/joint_states` make the sliders and model fight each other.

## Finding the slider window

Joint State Publisher opens as a separate Ubuntu window. If RViz covers it:

- Minimize RViz with the minus button, not the close button.
- Click the running gray gear icons in the Ubuntu dock.
- On a Mac keyboard, Option acts as Ubuntu Alt, so Option+Tab may switch windows after clicking
  inside the VM.
- Startup succeeded when the terminal logs contain `Got description, configuring robot` and
  `Centering`.

The "Zero" button in RViz resets the camera. It is not the Joint State Publisher Center button.

## RViz viewing

- Set Fixed Frame to `base_link`.
- Ensure RobotModel is enabled.
- Disable TF to hide the red/green/blue axis markers.
- Use the mouse wheel to zoom.
- Press Center in Joint State Publisher to return all movable joints to zero.

## Joint controls

Six sliders are exposed:

| Slider | Type | Notes |
| --- | --- | --- |
| `base_yaw_joint` | revolute | base rotation |
| `shoulder_joint` | revolute | pitch |
| `elbow_joint` | revolute | pitch |
| `wrist_roll_joint` | revolute | rolls the gripper about the forearm's long axis |
| `wrist_pitch_joint` | revolute | tilts the gripper up and down |
| `gripper_joint` | revolute | 0 = closed (STEP neutral), 0.75 = open (51.8 mm) |

Three joints are `mimic` joints and must **not** appear as sliders: `right_gripper_joint`,
`left_finger_joint`, and `right_finger_joint`. If any of them shows up, the mimic tags were lost —
rebuild with `--cmake-clean-cache`.

## Diagnostics

Confirm the transform tree reaches the end of the arm. The old `wrist_gripper_link` no longer
exists; use the new link names:

```bash
ros2 run tf2_ros tf2_echo base_link left_finger_link
```

Other useful frames: `wrist_link`, `gripper_base_link`, `left_gear_link`, `right_finger_link`.

Confirm joint states are publishing:

```bash
ros2 topic echo /joint_states
```

Check publisher count — there should be exactly one during RViz testing:

```bash
ros2 topic info /joint_states --verbose
```

Confirm the robot description exists:

```bash
ros2 topic echo /robot_description --once
```

Verify installed meshes:

```bash
ls -lh ~/robot_arm_ws/install/robot_arm_description/share/robot_arm_description/STL/
```

The mesh list should contain nine files: `base_link.stl`, `waist_link.stl`, `upper_arm_link.stl`,
`forearm_link.stl`, `wrist_link.stl`, `gripper_base.stl`, `gripper_gear.stl`,
`gripper_connecting_link.stl`, `gripper_finger.stl`.

Validate the model without launching RViz:

```bash
ros2 run xacro xacro ~/robot_arm_ws/src/robot_arm_description/urdf/robot_arm.urdf.xacro -o /tmp/robot_arm.urdf && check_urdf /tmp/robot_arm.urdf
```

## Common problems

**RViz opens but the arm is missing.** Expand RobotModel and inspect Status. Confirm Fixed Frame is
`base_link`, the installed STL files exist, and `ros2 pkg prefix` points at the workspace install.
Rebuild with `--cmake-clean-cache`.

**The model is tiny.** Usually camera distance. Open Panels → Views, set Distance to about 0.5–1.0
and Focal Point near `0, 0, 0.1`.

**Joint State Publisher says it is waiting for robot_description.** It was started separately
without `robot_state_publisher`. Stop it and use the full `display.launch.py`.

**Sliders change but the model does not move.** Check for competing `/joint_states` publishers, stop
any manually launched Joint State Publisher, and relaunch once via `display.launch.py`.

**Graphics errors mention ZINK, EGL, or Mesa.** Use all three environment settings shown above.

**Newly added meshes do not appear.** Confirm the VM pulled the expected commit, copy the package
into `~/robot_arm_ws/src` again, rebuild with `--cmake-clean-cache`, re-source
`install/setup.bash`, and confirm the files exist under the installed package.

## Future Gazebo warning

Gazebo Sim has not been installed or configured for this repository. The VM is ARM64 and renders
RViz through LLVMpipe software rendering, so Gazebo physics plus camera rendering may be slow. When
Gazebo is added: begin with a headless server if rendering is unstable, test joint control without
the camera first, and add the RGB-D camera only after physics and `ros2_control` work.
