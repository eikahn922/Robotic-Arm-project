# Robotic Arm Project

This repository documents the mechanical design and development of a robotic arm. It is organized so project planning and CAD work can be reviewed independently.

## Project artifacts

| Area | Artifact | Description |
| --- | --- | --- |
| Project workflow | [Robotic Arm Project Workflow](docs/project-workflow/Robotic-Arm-Project-Workflow.pdf) | Planning and workflow documentation for the project. |
| CAD — base | [Robot Arm Base v1](cad/base/Robot-Arm-Base-v1.SLDPRT) | SolidWorks part model for the robot arm's structural base. |
| CAD — link | [Robot Arm Link v1](cad/link/Robot-Arm-Link-v1.SLDPRT) | SolidWorks part model for a structural arm linkage. |
| CAD — waist | [Robot Arm Waist v1](cad/waist/Robot-Arm-Waist-v1.SLDPRT) | SolidWorks part model for the rotating waist component. |

## Repository structure

```text
.
├── cad/
│   ├── README.md
│   ├── base/
│   │   └── Robot-Arm-Base-v1.SLDPRT
│   ├── link/
│   │   └── Robot-Arm-Link-v1.SLDPRT
│   └── waist/
│       └── Robot-Arm-Waist-v1.SLDPRT
└── docs/
    └── project-workflow/
        └── Robotic-Arm-Project-Workflow.pdf
```

## File formats

- `.SLDPRT` files are native SolidWorks part models.
- `.pdf` files contain project documentation suitable for viewing without CAD software.
