# RViz configurations

| File | Purpose |
| --- | --- |
| `robot_arm.rviz` | Normal visual display. Meshes opaque, collision hidden, TF off. |
| `robot_arm_collision.rviz` | Collision verification. Collision primitives drawn with the visual meshes at 35% alpha so the boxes and cylinder show through. |

Both use `base_link` as the fixed frame and read the model from `/robot_description`.

Launch the normal view:

```bash
ros2 launch robot_arm_description display.launch.py
```

Launch the collision view:

```bash
ros2 launch robot_arm_description display.launch.py show_collision:=true
```

Or point RViz at any config explicitly:

```bash
ros2 launch robot_arm_description display.launch.py rviz_config:=/absolute/path/to/config.rviz
```

Previously the launch file borrowed `urdf_launch`'s stock `urdf.rviz`. These configs are committed so
display settings are under version control.
