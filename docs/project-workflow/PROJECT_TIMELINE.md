# 3-DOF Robotic Arm Project Timeline

Target completion: **August 18, 2026**

Maximum available time: **approximately 87 hours**

This schedule assumes up to three hours of work per day, except July 31 through August 2, which are limited to one hour per day. All work from July 31 through August 8 must be completed remotely, so that period is reserved for ROS, simulation, mathematics, and documentation.

## Phase 1: CAD, ordering, and manufacturing preparation

| Date | Daily goal |
| --- | --- |
| July 19 | Finish CAD revision 1; check joint motion, interference, fastener access, cable paths, and mass properties. |
| July 20 | Complete shoulder and elbow torque calculations; finalize actuators and power requirements. |
| July 21 | Create the bill of materials and order servos, bearings, fasteners, electronics, and power components. |
| July 22 | Produce critical fit-test parts for servo mounts, bearing pockets, and shaft connections. |
| July 23 | Test the fit pieces, correct the CAD, and freeze the final mechanical dimensions. |
| July 24 | Begin manufacturing the base and shoulder components. |
| July 25 | Manufacture the upper-arm and forearm components. |
| July 26 | Manufacture the gripper and remaining brackets. |
| July 27 | Dry-fit the mechanical parts without electronics; check alignment, friction, and fastener access. |
| July 28 | Export simplified CAD meshes and begin the URDF/Xacro robot description. |
| July 29 | Display the arm in RViz and correct mesh scale, coordinate frames, and joint axes. |
| July 30 | Organize physical parts, verify incoming orders, and prepare the ROS workspace for remote work. |

**Milestone:** CAD and manufactured parts are ready, components are ordered, and the robot displays correctly in RViz.

## Phase 2: Remote work with one-hour sessions

| Date | Daily goal |
| --- | --- |
| July 31 | **Remote, 1 hour:** Clean up the ROS workspace, package structure, file names, and launch files. |
| August 1 | **Remote, 1 hour:** Add or correct joint limits, collision geometry, and inertial properties. |
| August 2 | **Remote, 1 hour:** Create the initial `ros2_control` and Joint Trajectory Controller configuration. |

## Phase 3: Remote simulation and coding

| Date | Daily goal |
| --- | --- |
| August 3 | **Remote:** Spawn the arm in Gazebo and stabilize it under gravity. |
| August 4 | **Remote:** Command each simulated joint and fix controller, direction, or joint-limit problems. |
| August 5 | **Remote:** Complete the forward-kinematics math and verify it against ROS TF. |
| August 6 | **Remote:** Complete the inverse-kinematics math for the base, shoulder, and elbow. |
| August 7 | **Remote:** Write the inverse-kinematics Python node with reachability and joint-limit checks. |
| August 8 | **Remote:** Create and test simulated home, approach, pickup, lift, drop, and recovery poses. |

**Milestone:** The simulated arm accepts a target, calculates joint angles, and performs a basic pick-and-place sequence.

## Phase 4: Physical assembly and integration

| Date | Daily goal |
| --- | --- |
| August 9 | Inspect delivered parts and assemble the base and base-rotation joint. |
| August 10 | Assemble the shoulder, elbow, and arm links; check friction manually. |
| August 11 | Assemble the gripper, install the servos, and complete cable routing. |
| August 12 | Wire the power system and test each servo independently at low speed. |
| August 13 | Connect the hardware driver, define zero positions, and calibrate joint directions and offsets. |
| August 14 | Move each physical joint individually and verify that RViz matches the real arm. |
| August 15 | Test slow coordinated movement without a payload; tune speed and safe paths. |

**Milestone:** The physical arm follows ROS commands and matches its state in RViz.

## Phase 5: Pick-and-place, reliability, and final demonstration

| Date | Daily goal |
| --- | --- |
| August 16 | Run the complete pick-and-place sequence without a payload, then test with a lightweight object. |
| August 17 | Run ten repeated trials and fix the most common mechanical or software failure. |
| August 18 | Record the final demonstration and finish the README, CAD screenshots, wiring diagram, and project summary. |

## Completion criteria

- The arm homes consistently.
- The physical joint state is displayed correctly in RViz.
- The arm reaches predefined poses or a validated reachable coordinate.
- The gripper transfers a lightweight object into a predefined bin.
- At least eight of ten repeated pick-and-place attempts succeed.
- The repository contains setup, calibration, launch, and operating instructions.

## Schedule protection

Order components no later than July 21. If time is lost, preserve predefined-pose pick-and-place first and treat arbitrary-coordinate control as the first feature to reduce.
