# ROS link geometry

This directory stores one consistently named STL mesh for each rigid URDF link.

## Imported meshes

| Mesh | Export format | Dimensions | Coordinate-frame note |
| --- | --- | --- | --- |
| `base_link.stl` | Binary STL, meters | 121.21 × 56.00 × 121.25 mm | Origin is centered on the bottom face; the exported Y axis is up, so the URDF visual will apply a +90° X rotation to align it with ROS Z-up. |
| `waist_link.stl` | Binary STL, meters | 96.86 × 73.80 × 97.00 mm | Origin is centered on the bottom face; the exported Y axis is up, so the URDF visual will apply a +90° X rotation to align it with ROS Z-up. |

Additional meshes will be added and verified individually before they replace the remaining placeholder geometry.
