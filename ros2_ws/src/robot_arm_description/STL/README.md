# ROS link geometry

This directory stores one consistently named STL mesh for each rigid URDF link.

## Imported meshes

| Mesh | Export format | Dimensions | Coordinate-frame note |
| --- | --- | --- | --- |
| `base_link.stl` | Binary STL, meters | 121.21 × 56.00 × 121.25 mm | Origin is centered on the bottom face; the exported Y axis is up, so the URDF visual will apply a +90° X rotation to align it with ROS Z-up. |
| `waist_link.stl` | Binary STL, meters | 96.86 × 73.80 × 97.00 mm | Origin is centered on the bottom face; the exported Y axis is up, so the URDF visual will apply a +90° X rotation to align it with ROS Z-up. |
| `upper_arm_link.stl` | Binary STL, meters | 42.00 × 161.97 × 21.00 mm | Origin is the shoulder pivot. The mesh is Z-up and extends along +Y; the URDF applies a −90° Z rotation to align it with link +X. The shoulder-to-elbow spacing is 120 mm. |
| `forearm_link.stl` | Binary STL, millimeters | 125.00 × 38.00 × 27.00 mm | Exported as SolidWorks Link #2 with its mesh origin shifted +63, +19, +8 mm from the STEP component frame. The Xacro converts millimeters to meters and compensates for that export offset before applying the STEP-derived assembly placement. |
| `wrist_link.stl` | Binary STL, millimeters | 33.00 × 28.00 × 46.00 mm | Extracted as `link#3RoboticArm` directly from `RobotArmAssembly (1).STEP` in its component-local frame. |
| `gripper_base.stl` | Binary STL, millimeters | 53.30 × 28.00 × 77.00 mm | Supplied gripper-first-link export, normalized from assembly coordinates into its STEP component-local frame. |
| `gripper_gear.stl` | Binary STL, millimeters | 26.70 × 10.00 × 49.37 mm | Normalized gear mesh referenced twice at the two STEP gear occurrences. |
| `gripper_connecting_link.stl` | Binary STL, millimeters | 39.00 × 8.00 × 4.00 mm | Normalized connecting-link mesh referenced twice at the two STEP occurrences. |
| `gripper_finger.stl` | Binary STL, millimeters | 65.16 × 17.87 × 4.50 mm | Normalized finger mesh referenced twice at the two STEP occurrences. |

> **Dimension note.** The connecting-link and finger rows list the axis-aligned bounding box of the
> *normalized* mesh as committed here. Earlier revisions of this table listed the bounding box of the
> raw SolidWorks export, before the mesh was rotated into its STEP component-local frame. A rigid
> rotation does not change the part, but it does change its axis-aligned extents, which is why the
> numbers moved.

## Link assignment

Each mesh is now attached to a specific moving URDF link rather than to one combined rigid body:

| Mesh | URDF link | Instances |
| --- | --- | --- |
| `base_link.stl` | `base_link` | 1 |
| `waist_link.stl` | `waist_link` | 1 |
| `upper_arm_link.stl` | `upper_arm_link` | 1 |
| `forearm_link.stl` | `forearm_link` | 1 |
| `wrist_link.stl` | `wrist_link` | 1 |
| `gripper_base.stl` | `gripper_base_link` | 1 |
| `gripper_gear.stl` | `left_gripper_link`, `right_gripper_link` | 2 |
| `gripper_connecting_link.stl` | `left_gripper_link`, `right_gripper_link` | 2 |
| `gripper_finger.stl` | `left_gripper_link`, `right_gripper_link` | 2 |

The gear, connecting link, and finger meshes are each referenced twice on purpose: the two gripper
sides are separate STEP occurrences of the same part.

The full neutral-pose CAD geometry is represented, and the wrist and gripper now articulate. Each
gripper side rotates as one rigid gear/connector/finger group; see the Xacro comments for why the
real geared four-bar cannot be expressed directly in URDF.
