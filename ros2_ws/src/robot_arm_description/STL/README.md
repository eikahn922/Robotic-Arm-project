# ROS link geometry

This directory stores one consistently named STL mesh for each rigid URDF link.

## Imported meshes

| Mesh | Export format | Dimensions | Coordinate-frame note |
| --- | --- | --- | --- |
| `base_link.stl` | Binary STL, meters | 121.21 × 56.00 × 121.25 mm | Origin is centered on the bottom face; the exported Y axis is up, so the URDF visual will apply a +90° X rotation to align it with ROS Z-up. |
| `waist_link.stl` | Binary STL, meters | 96.86 × 73.80 × 97.00 mm | Origin is centered on the bottom face; the exported Y axis is up, so the URDF visual will apply a +90° X rotation to align it with ROS Z-up. |
| `upper_arm_link.stl` | Binary STL, meters | 42.00 × 161.97 × 21.00 mm | Origin is the shoulder pivot. The mesh is Z-up and extends along +Y; the URDF applies a −90° Z rotation to align it with link +X. The shoulder-to-elbow spacing is 120 mm. |
| `forearm_link.stl` | Binary STL, millimeters | 125.00 × 38.00 × 27.00 mm | Exported as SolidWorks Link #2 with its mesh origin shifted +63, +19, +8 mm from the STEP component frame. The Xacro converts millimeters to meters and compensates for that export offset before applying the STEP-derived assembly placement. |

The gripper mesh will be added and verified before it replaces the remaining placeholder geometry.
