# Robotic Arm Project

This repository documents the mechanical design and development of a robotic arm. It is organized so project planning and CAD work can be reviewed independently.

## Project artifacts

| Area | Artifact | Description |
| --- | --- | --- |
| Project workflow | [Robotic Arm Project Workflow](docs/project-workflow/Robotic-Arm-Project-Workflow.pdf) | Planning and workflow documentation for the project. |
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
└── docs/
    └── project-workflow/
        └── Robotic-Arm-Project-Workflow.pdf
```

## File formats

- `.SLDPRT` files are native SolidWorks part models.
- `.pdf` files contain project documentation suitable for viewing without CAD software.
