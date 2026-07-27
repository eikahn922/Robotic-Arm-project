# ROS 2 Workspace

This directory contains the ROS 2 Jazzy packages for the 3-DOF robotic arm. See [ROS_PROGRESS.md](../ROS_PROGRESS.md) for the completed milestones, lessons learned, and next steps.

## Build and launch

Copy or clone this repository into an Ubuntu 24.04 environment with ROS 2 Jazzy installed, then run:

```bash
cd ros2_ws
colcon build --symlink-install --packages-select robot_arm_description
source install/setup.bash
LIBGL_ALWAYS_SOFTWARE=1 ros2 launch robot_arm_description display.launch.py
```

`LIBGL_ALWAYS_SOFTWARE=1` is included for compatibility with the current UTM virtual-machine graphics setup. It may be omitted on a native Linux system with working OpenGL acceleration.
