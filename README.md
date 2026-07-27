# Robotic Arm Project

This repository documents the mechanical design, engineering analysis, and ROS 2 development of a 3-DOF robotic arm. It is organized so each stage can be reviewed and reproduced independently.

## Project artifacts

| Area | Artifact | Description |
| --- | --- | --- |
| Active timeline | [3-DOF Robotic Arm Project Timeline](docs/project-workflow/PROJECT_TIMELINE.md) | Daily development plan through August 18, including remote-work constraints and completion criteria. |
| ROS 2 progress | [ROS 2 Progress](ROS_PROGRESS.md) | Recruiter-friendly milestone log covering the completed setup, URDF/Xacro model, RViz result, lessons learned, and next steps. |
| ROS 2 package | [robot_arm_description](ros2_ws/src/robot_arm_description) | Reproducible ROS 2 Jazzy package containing the placeholder 3-DOF URDF/Xacro model and visualization launch file. |
| ROS 2 base mesh | [base_link.stl](ros2_ws/src/robot_arm_description/STL/base_link.stl) | Meter-scaled binary STL exported from SolidWorks for the fixed robot base. |
| ROS 2 waist mesh | [waist_link.stl](ros2_ws/src/robot_arm_description/STL/waist_link.stl) | Meter-scaled binary STL exported from SolidWorks for the rotating waist link. |
| Project workflow | [Robotic Arm Project Workflow](docs/project-workflow/Robotic-Arm-Project-Workflow.pdf) | Detailed engineering and implementation workflow for the project. |
| Engineering analysis | [Torque and Servo Sizing Analysis](analysis/README.md) | Formula-driven shoulder and elbow torque calculations, assumptions, results, and validation plan. |
| Calculation workbook | [3DOF Robotic Arm Torque & Servo Sizing Analysis](analysis/3DOF-Robotic-Arm-Torque-Servo-Sizing-Analysis.xlsx) | Downloadable workbook containing the full servo-sizing calculation model. |
| Final assembly | [Robot Arm Final Assembly](cad/assembly/Robot-Arm-Final-Assembly.SLDASM) | Complete SolidWorks assembly for the robot arm. |
| CAD — base | [Robot Arm Base v1](cad/base/Robot-Arm-Base-v1.SLDPRT) | SolidWorks part model for the robot arm's structural base. |
| CAD — gripper gear | [gearRobotArm.SLDPRT](cad/gripper/gearRobotArm.SLDPRT) | SolidWorks part model for the gripper gear. |
| CAD — gripper connecting link | [Robot Arm Gripper Connecting Link](cad/all-links/Robot-Arm-Gripper-Connecting-Link.SLDPRT) | SolidWorks part model for the gripper connecting link. |
| CAD — gripper first link | [Robot Arm Gripper First Link](cad/gripper/Robot-Arm-Gripper-First-Link.SLDPRT) | SolidWorks part model for the first gripper link. |
| CAD — gripper link | [Robot Arm Gripper Link 1](cad/gripper/Robot-Arm-Gripper-Link-1.SLDPRT) | SolidWorks part model for the gripper connection link. |
| CAD — link 1 | [Robot Arm Link 1](cad/all-links/Robot-Arm-Link-1.SLDPRT) | SolidWorks part model for the first structural arm link. |
| CAD — link 2 | [Robot Arm Link 2](cad/all-links/Robot-Arm-Link-2.SLDPRT) | SolidWorks part model for the second structural arm link. |
| CAD — link 3 | [Robot Arm Link 3](cad/all-links/Robot-Arm-Link-3.SLDPRT) | SolidWorks part model for the third structural arm link. |
| CAD — servo | [MG996R_servo.SLDPRT](cad/servo/MG996R_servo.SLDPRT) | SolidWorks part model for the MG996R servo. |
| CAD — servo | [SG90 - Micro Servo 9g - Tower Pro.1.SLDPRT](cad/servo/SG90%20-%20Micro%20Servo%209g%20-%20Tower%20Pro.1.SLDPRT) | SolidWorks part model for the Tower Pro SG90 micro servo. |
| CAD — waist | [Robot Arm Waist v1](cad/waist/Robot-Arm-Waist-v1.SLDPRT) | SolidWorks part model for the rotating waist component. |

## Repository structure

```text
.
├── cad/
│   ├── README.md
│   ├── assembly/
│   │   ├── README.md
│   │   └── Robot-Arm-Final-Assembly.SLDASM
│   ├── base/
│   │   └── Robot-Arm-Base-v1.SLDPRT
│   ├── gripper/
│   │   ├── Robot-Arm-Gripper-First-Link.SLDPRT
│   │   ├── Robot-Arm-Gripper-Link-1.SLDPRT
│   │   └── gearRobotArm.SLDPRT
│   ├── all-links/
│   │   ├── Robot-Arm-Gripper-Connecting-Link.SLDPRT
│   │   ├── Robot-Arm-Link-1.SLDPRT
│   │   ├── Robot-Arm-Link-2.SLDPRT
│   │   └── Robot-Arm-Link-3.SLDPRT
│   ├── servo/
│   │   ├── MG996R_servo.SLDPRT
│   │   └── SG90 - Micro Servo 9g - Tower Pro.1.SLDPRT
│   └── waist/
│       └── Robot-Arm-Waist-v1.SLDPRT
├── analysis/
│   ├── README.md
│   └── 3DOF-Robotic-Arm-Torque-Servo-Sizing-Analysis.xlsx
├── ros2_ws/
│   ├── README.md
│   └── src/
│       └── robot_arm_description/
│           ├── CMakeLists.txt
│           ├── package.xml
│           ├── STL/
│           │   ├── README.md
│           │   ├── base_link.stl
│           │   └── waist_link.stl
│           ├── launch/
│           ├── rviz/
│           └── urdf/
├── ROS_PROGRESS.md
└── docs/
    ├── images/
    │   └── ros/
    │       └── rviz-placeholder-arm.png
    └── project-workflow/
        ├── PROJECT_TIMELINE.md
        └── Robotic-Arm-Project-Workflow.pdf
```

## File formats

- `.SLDASM` files are native SolidWorks assemblies that reference component documents.
- `.SLDPRT` files are native SolidWorks part models.
- `.md` files contain repository-readable project plans and documentation.
- `.pdf` files contain project documentation suitable for viewing without CAD software.
- `.xlsx` files contain formula-driven engineering calculations and design inputs.
- `.xacro` files define parameterized robot links, joints, origins, axes, and limits for ROS 2.
- `.py` launch files start and configure the ROS 2 visualization nodes.
- `.stl` files contain meter-scaled binary geometry exported from SolidWorks for ROS visualization.
