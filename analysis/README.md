# Torque and Servo Sizing Analysis

This folder documents the preliminary static torque analysis used to evaluate the MG996R servos for the shoulder and elbow joints of the 3-DOF robotic arm.

## Analysis artifacts

- [Calculation workbook](3DOF-Robotic-Arm-Torque-Servo-Sizing-Analysis.xlsx) — formula-driven engineering workbook with inputs, source notes, joint calculations, utilization, safety margins, and a comparison chart.
- [Live Google Sheet](https://docs.google.com/spreadsheets/d/17cgYGMoWEYcnl7br5cGeY7KRNHN3UeBQPRdlAbZkqd0/edit) — browser-accessible version of the same analysis.

## Method

The arm was evaluated in a conservative horizontal pose, where gravity produces the largest moment about the shoulder and elbow axes. For each joint, the static and design torques are calculated as:

```text
arm torque     = moving mass x gravity x center-of-mass radius
payload torque = payload mass x gravity x payload radius
static torque  = arm torque + payload torque
design torque  = static torque x safety factor
```

The model uses a 10 g payload representing a small foam ball, a safety factor of 2.0, and the MG996R advertised stall torque of 11 kgf-cm at 6 V. Masses and centers of mass come from the SolidWorks assembly after assigning PLA to the printed parts.

## Results

| Joint | Moving mass | COM radius | Static torque | Design torque | Servo utilization | Torque margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Elbow | 217.60 g | 76.46 mm | 1.94 kgf-cm | 3.88 kgf-cm | 35.3% | 2.83x |
| Shoulder | 297.31 g | 116.65 mm | 3.82 kgf-cm | 7.65 kgf-cm | 69.5% | 1.44x |

Both joints pass this preliminary static comparison. The shoulder is the limiting joint and therefore receives priority during physical testing.

## Engineering limitations and validation plan

- Advertised stall torque is a short-duration maximum, not a continuous operating rating.
- The current CAD masses treat modeled printed parts as solid PLA. Slicer-estimated printed masses should replace them after infill, wall count, and hardware are finalized.
- Wiring, fasteners, bearings, servo horns, and other unmodeled hardware must be added to the moving mass.
- The completed arm should be bench-tested at reduced command speed while measuring supply voltage, current draw, holding performance, temperature, and joint deflection.
- If the shoulder overheats, stalls, or sags, reduce reach or mass, add a spring/counterbalance, or select a higher-torque actuator.
