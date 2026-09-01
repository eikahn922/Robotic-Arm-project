# ROS 2 Progress — 3-DOF Robotic Arm

## Current milestone

- Built a working ROS 2 Jazzy development environment on Ubuntu 24.04 ARM64.
- Created and validated a reusable ROS 2 robot-description package.
- Modeled the arm as an eight-link URDF/Xacro kinematic chain with five commanded joints and one mimic joint.
- Published the robot state and TF tree and rendered the placeholder arm successfully in RViz.
- Integrated the SolidWorks base, waist, upper-arm, forearm, wrist, and complete neutral-pose gripper geometry into the robot model.
- Extracted a 120 mm shoulder-to-elbow spacing from the upper-arm CAD geometry.
- Split the rigid `wrist_gripper_link` into `wrist_link`, `gripper_base_link`, and two moving gripper sides.
- Added `wrist_roll_joint`, `wrist_pitch_joint`, and `gripper_joint`, with three mimic joints driving
  the opposing gripper side and the two-finger parallelogram.
- Added fitted collision geometry and mesh-derived inertial properties for all ten links.
- Added a `ros2_control` configuration with mock hardware, written but not yet run.
- Current phase: run the model in the VM — verify the five joint controls in RViz, then the mock control stack.

> **Terminology.** This is an RViz *kinematic visualization*, not a physics simulation. It runs
> `robot_state_publisher`, `joint_state_publisher_gui`, and RViz. Gazebo Sim and `ros2_control` are
> not implemented yet, so nothing here computes mass, contact, or gravity.

![Placeholder 3-DOF arm rendered in RViz](docs/images/ros/rviz-placeholder-arm.png)

## Step 1 — Set up the ROS 2 environment

**Completed**

- Created an Ubuntu 24.04 ARM64 virtual machine with UTM on an Apple Silicon Mac.
- Installed ROS 2 Jazzy Desktop and the ROS development tools.
- Configured the shell to source ROS automatically.
- Verified node-to-node communication with the ROS talker/listener examples.

**What I learned**

- How ROS 2 packages are installed and sourced in a Linux environment.
- How nodes communicate through topics using a publisher/subscriber model.
- How to diagnose ARM64 package, shell, and software-rendering issues in a virtual machine.

## Step 2 — Create the workspace and package

**Completed**

- Created a colcon workspace at `~/robot_arm_ws`.
- Created the `robot_arm_description` package using `ament_cmake`.
- Added `urdf`, `STL`, `launch`, and `rviz` resource directories.
- Configured CMake to install the robot-description resources with the package.

**What I learned**

- The purpose of the `src`, `build`, `install`, and `log` workspace directories.
- How `colcon`, `ament_cmake`, `package.xml`, and `CMakeLists.txt` work together.
- Why a workspace must be rebuilt and sourced after package changes.

## Step 3 — Build and validate the first URDF/Xacro model

**Completed**

- Defined the initial kinematic chain:
  - `base_link`
  - `waist_link`
  - `upper_arm_link`
  - `forearm_link`
  - `wrist_gripper_link`
- Defined three revolute joints: base yaw, shoulder pitch, and elbow pitch.
- Added provisional joint origins, rotation axes, and motion limits.
- Used Xacro properties for reusable arm dimensions.
- Generated a URDF and verified the XML and link/joint tree with `check_urdf`.

**What I learned**

- How URDF represents a robot as a parent-child tree of links and joints.
- How joint origins, axes, and limits determine the arm's motion.
- How Xacro makes dimensions and repeated model elements easier to maintain.
- How to validate a model before attempting visualization or control.

## Step 4 — Publish and visualize the robot

**Completed**

- Used `robot_state_publisher` to publish the robot's link transforms.
- Used `joint_state_publisher_gui` to generate test joint positions.
- Visualized the robot model and TF axes in RViz.
- Configured software OpenGL rendering for reliable RViz operation in UTM.
- Corrected a launch parameter type issue by passing the generated URDF as an explicit string.

**What I learned**

- The difference between joint states and the TF transform tree.
- How `robot_state_publisher`, `joint_state_publisher_gui`, and RViz work together.
- How to interpret RViz fixed frames, RobotModel status, and TF output while debugging.
- How a ROS 2 launch file starts and configures several nodes as one system.

## Reproduce the current milestone

```bash
cd ~/robot_arm_ws
colcon build --symlink-install --packages-select robot_arm_description
source install/setup.bash
LIBGL_ALWAYS_SOFTWARE=1 ros2 launch robot_arm_description display.launch.py
```

## Next steps

### Step 5 — Export the SolidWorks geometry

**Completed so far**

- Exported the base, waist, and upper arm as meter-scaled binary STL files; the forearm, wrist, and normalized gripper parts remain in SolidWorks millimeters and are scaled by Xacro.
- Validated all nine unique mesh files' dimensions, orientation, binary structure, watertightness, and reference origin before integration.
- Kept the upper-arm origin at the shoulder pivot and measured a 120 mm shoulder-to-elbow distance from the CAD geometry.
- Derived the forearm transform from the STEP assembly and converted its millimeter geometry to ROS meters in Xacro.
- Added all nine unique meshes to `robot_arm_description/STL` with documented ROS frame corrections; the gear, connecting-link, and finger meshes are each instantiated twice from the STEP assembly.

**What I learned**

- How STL export units affect robot scale in RViz.
- Why a joint-centered mesh origin makes URDF placement and motion easier to understand.
- How to correct SolidWorks-to-ROS axis differences using a URDF `origin` rotation instead of modifying the CAD geometry.
- How to validate mesh dimensions and orientation before debugging them in ROS.

**Remaining**

- Verify the complete wrist and gripper geometry in RViz against the STEP assembly.

### Step 6 — Match the ROS model to the CAD assembly

- Replaced the placeholder base, waist, upper arm, and forearm with their corresponding SolidWorks meshes.
- Updated the provisional shoulder-to-elbow distance from 220 mm to the CAD-derived 120 mm value.
- Verify the base, waist, upper-arm, and forearm meshes together in RViz.
- Completed: replaced the gripper placeholder with Link #3 and all seven gripper part instances from the CAD assembly.
- Measure and enter the remaining exact joint origins and rotation axes.
- Replace provisional motion limits with the physical servo/link limits.
- Confirm that each RViz joint moves in the correct direction without separating the assembly.

### Step 6b — Split the wrist and gripper into moving joints

**Completed**

- Replaced the single fixed `wrist_gripper_link` with six links: `wrist_link`, `gripper_base_link`,
  `left_gear_link`, `left_finger_link`, `right_gear_link`, and `right_finger_link`.
- Six commanded joints: base yaw, shoulder, elbow, `wrist_roll_joint`, `wrist_pitch_joint`, and
  `gripper_joint`. Three mimic joints keep the rest passive, so the GUI shows exactly six sliders.
- Every joint's zero position is the STEP neutral pose. A static check confirms the split model
  reproduces the original single-link placement of all twelve visuals to within 1.04 nanometres,
  which is the rounding of the previous file's nine-decimal literals, not a modelling error.

**Wrist: two axes, corrected**

- An earlier revision made the wrist a *pitch* joint. That was wrong. Testing each wrist-frame axis
  against the forearm's long axis gives X 0.011, Y 0.011, **Z 0.9999** — so Z is the roll axis and
  the others only pitch. `wrist_roll_joint` now rolls the gripper about the forearm's own axis.
- The pitch belongs one joint further out, where a fixed mount used to be. `wrist_pitch_joint` uses
  the gripper-base X axis, which is exactly perpendicular to the roll axis (dot product 0.0000) and
  parallel to the jaw-opening direction, so the jaws stay level as the gripper tilts.

**Gripper: parallelogram, not scissors**

- The real mechanism is a geared four-bar closed loop, which URDF cannot express. Each side is now
  split into a gear body and a finger, with the finger counter-rotating against its gear through a
  mimic joint. The finger swings out along the gear's arc while its orientation stays fixed.
- The finger mimic multiplier is **+1**, not −1, because each finger frame's Z axis is anti-parallel
  to its gear frame's Z; a +1 rotation there is a −1 rotation about the gear axis.
- Measured effect: the angle between the two fingers now holds constant at 30.1° across the entire
  range (spread 0.00°). The previous rigid-block model fanned from 30.8° to 80.4° — visibly wrong in
  RViz, and the reason the gripper appeared to grip in the wrong direction.
- Both gear frames share one spin axis: their local Z axes are exactly anti-parallel in the
  gripper-base frame (dot product −1.000000), the meshing-gear signature, so the side mimic
  multiplier is +1 and the two sides counter-rotate in world space.

**Remaining approximation**

- The connecting link is carried rigidly with its gear rather than solved as a true four-bar. It sits
  correctly at zero but does not articulate exactly. Fixing this properly needs a closed-loop solver
  or a fitted mimic ratio measured from the CAD.

**Provisional values, not measurements**

- `wrist_roll_joint` ±3.1416 rad, `wrist_pitch_joint` ±1.5708 rad, `gripper_joint` 0 to 0.75 rad.
  The gripper upper limit is sized so the fingertips reach 51.8 mm, enough for the 2 inch foam ball
  in `analysis/`. All three are conservative choices from geometry, not measured mechanical stops.

### Step 7 — Add engineering properties

**Completed: collision geometry**

- Added one simplified collision primitive per physical link, fitted to the committed meshes rather
  than hand-guessed.
- `base_link` uses a cylinder; the mesh is genuinely round (40.5% of its vertices lie in the outer
  10% of radius) and a cylinder is 21% tighter than the bounding box.
- `waist_link` uses a box. It looks round but is not: only 8% of vertices lie in the outer 10% of
  radius, so a cylinder would be a mere 8% tighter and the box is the simpler primitive.
- The upper arm, forearm, wrist, and gripper base use oriented boxes sized to each mesh's own
  bounding box, so the box inherits the mesh's orientation instead of inflating an axis-aligned one.
- Each gripper side gets collision on the **finger only**. The gears and connecting links are
  internal mechanism that mesh and overlap by design; giving them collision geometry would create
  permanent contact in a physics engine for no benefit.
- A static check samples every visual mesh and confirms 100% of sampled vertices lie inside the
  corresponding collision primitive, and that the internal-mechanism meshes are deliberately
  uncovered.

**Known, expected overlap**

- The left and right finger collision boxes intersect at the neutral pose, because the gripper is
  closed there (2.65 mm between fingertips). Self-collision between `left_finger_link` and
  `right_finger_link` must therefore be disabled downstream — via `self_collide` in Gazebo and the
  SRDF self-collision matrix in MoveIt. This is expected, not a defect.
- `left_gear_link` and `right_gear_link` carry inertia but **no** collision geometry at all. The gears
  and connecting links mesh and overlap by design, so collision there would create permanent contact.

**Fit quality**

- `gripper_base_link` is the loosest primitive at roughly 7.2x the true part volume, because the part
  is an open forked bracket. A convex hull would be tighter if grasp clearance becomes a problem.

**Completed: inertial properties**

- Every link now carries mass, centre of mass, and a full inertia tensor obtained by integrating the
  committed STL meshes (divergence theorem over the closed surface), multiplied by `pla_density`.
- The stored numbers are per-unit-density volume integrals, so changing `pla_density` alone rescales
  every mass *and* every inertia correctly. That matters because workbook validation item 1 requires
  replacing the solid-model density with slicer estimates once infill and walls are chosen.
- Independent cross-check: this method gives the upper arm **79.78 g**. The analysis workbook implies
  **79.71 g** for the same part (297.31 g shoulder-moving minus 217.60 g elbow-moving). Agreement is
  0.1%, which validates both the mesh integration and the 1240 kg/m³ density from two directions.
- Every tensor is positive-definite (Sylvester's criterion) and every set of principal moments
  satisfies the triangle inequality, so all eight are physically realisable rigid bodies.
- Total printed-part mass is 435.8 g.

**Known gap, deliberately not filled**

- These are **printed-part masses only**. The workbook's moving-mass figures exceed the mesh sums by
  a near-constant **82.5 g** at both the shoulder and the elbow — servo, fastener, and hardware mass
  distal to the elbow. It is not distributed across links here, because workbook validation item 3
  ("confirm the servo body mounting side for each joint") is still open. Assigning it without that
  confirmation would be a guess dressed up as a measurement. Add it once mounting sides are known.

**Remaining**

- Compare calculated joint torque requirements against the selected servos once servo masses are
  placed. The workbook already reports the shoulder as the limiting joint at 69.5% design
  utilisation with a 1.44x stall margin, and that figure already includes the hardware mass.

### Step 8 — Add control and simulation

**Completed: `ros2_control` configuration (written, not yet run)**

- Added a `ros2_control` hardware interface, controller YAML, and a separate control launch path.
  `robot_arm.urdf.xacro` stays free of control tags; `robot_arm_control.urdf.xacro` layers the
  interface on top, so a broken controller cannot break the working visualization.
- Mock hardware (`mock_components/GenericSystem`) is the default, so the whole control stack can be
  exercised with no physics engine and no GPU. On an ARM64 VM with software rendering that is far
  cheaper than debugging controllers and Gazebo simultaneously.
- Controllers: `joint_state_broadcaster`, an `arm_controller` over base yaw/shoulder/elbow/wrist, and
  a `gripper_controller` over `gripper_joint`. The arm controller starts only after the broadcaster
  exits successfully, so joint states exist before any trajectory is commanded.
- `right_gripper_joint` is deliberately absent from both the `ros2_control` block and the controller
  YAML, because a mimic joint must not have an independent command interface.

> **Not verified.** No controller has been loaded, no plugin name confirmed, no gain tuned. See
> [docs/SIMULATION.md](docs/SIMULATION.md) for the CLI test commands and the explicit list of
> unverified assumptions — the most fragile being that `ros2_control` propagates URDF `mimic` joints
> automatically.

**Remaining**

- Run the mock-hardware control stack in the VM and confirm the mimic side follows.
- Add Gazebo Sim: world, ground plane, spawn, `gz_ros2_control`, and a pickup target.
- Add MoveIt 2 inverse kinematics, an RGB-D camera, OpenCV ball detection, and autonomous
  pick-and-place.
- Add a microcontroller interface for servo commands and joint feedback.
