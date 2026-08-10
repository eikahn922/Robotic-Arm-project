# Physical Build: Parts List and Purchase Tracker

This page documents the planned hardware for the 3-DOF robotic arm and the engineering reasoning behind each selection. Exact vendors, part numbers, prices, and purchase status should be updated from receipts as parts are ordered and tested.

## 1. Design basis

- Motion: base yaw, shoulder pitch, elbow pitch, and an actuated gripper.
- Target object: a foam ball up to approximately 2 inches in diameter.
- Calculated shoulder requirement: **7.65 kgf-cm**, including a 2x safety factor.
- Calculated elbow requirement: **3.88 kgf-cm**, including a 2x safety factor.
- The shoulder actuator receives the largest margin because it carries the downstream arm, gripper, and payload.

## 2. Actuators

| Joint | Planned actuator | Quantity | Selection basis | Status |
| --- | --- | ---: | --- | --- |
| Base yaw | MG996R metal-gear servo | 1 | Current CAD selection; adequate for low-speed rotation when the base is supported by a bearing | Planned |
| Shoulder pitch | 20–25 kgf-cm, 6 V digital metal-gear servo | 1 | Provides useful margin above the calculated 7.65 kgf-cm requirement | Planned |
| Elbow pitch | MG996R metal-gear servo | 1 | Rated torque is above the calculated 3.88 kgf-cm requirement | Planned |
| Gripper | MG90S preferred; SG90 acceptable for a light foam ball | 1 | Small, lightweight actuator appropriate for the low gripper load | Planned |
| Spare | Match the most failure-prone arm servo | 1 optional | Reduces downtime during testing | Optional |

Servo stall torque is not a continuous operating rating. Final acceptance testing will check current draw, temperature, backlash, joint friction, and the measured mass of the printed assembly.

## 3. Control electronics

| Component | Quantity | Purpose | Status |
| --- | ---: | --- | --- |
| ESP32 development board | 1 | Runs high-level servo commands and communicates with the computer/ROS 2 system | Planned |
| PCA9685 16-channel PWM driver | 1 | Generates stable PWM signals for all servos over I2C | Planned |
| USB data cable for ESP32 | 1 | Programming, debugging, and serial communication | Planned |
| 1,000 µF capacitor rated for at least 10 V | 1 | Reduces voltage dips near the servo power input | Planned |

The ESP32 provides control signals only. The servos use a separate high-current 6 V power rail, with all grounds connected together.

## 4. Bench power and protection

| Component | Recommended specification | Quantity | Status |
| --- | --- | ---: | --- |
| Regulated DC supply | 6 V, 10 A | 1 | Planned |
| Inline fuse and holder | 10 A | 1 | Planned |
| Master power switch | Rated above expected DC current | 1 | Planned |
| Power distribution block or terminal strip | At least 5 servo/electronics branches | 1 | Planned |

Do not power the arm servos through the ESP32, USB port, PCA9685 logic pin, or a solderless breadboard. High-current servo power should use dedicated wiring and distribution hardware.

## 5. Optional mobile power

| Component | Recommended specification | Quantity | Status |
| --- | --- | ---: | --- |
| Battery | 2S, 7.4 V, 2,200–3,000 mAh LiPo | 1 | Optional |
| UBEC | Regulated 6 V, 10 A output | 1 | Optional |
| Balance charger | Compatible with 2S LiPo batteries | 1 | Optional |
| LiPo safety bag | Sized for the selected battery | 1 | Optional |
| Low-voltage alarm | 2S-compatible | 1 | Optional |
| Battery connector | XT60 pair or selected equivalent | 1 pair | Optional |

Never connect a raw 2S LiPo directly to standard MG996R servos. The UBEC must regulate the battery voltage to the servo rail voltage.

## 6. Wiring and connectors

| Item | Recommended size/type | Estimated quantity | Use |
| --- | --- | ---: | --- |
| Main power wire | 18 AWG stranded | 2–3 m | Supply, fuse, switch, and distribution wiring |
| Servo branch wire | 20–22 AWG stranded | 3–5 m | Individual servo power branches |
| Signal wire | 24–26 AWG stranded | 3–5 m | PWM and I2C signals |
| Servo extension leads | 3-pin, suitable lengths | 4–6 | Removable servo connections |
| Connectors | Ferrules, JST-style plugs, or locking equivalents | Assortment | Serviceable electrical connections |
| Heat-shrink tubing | Assorted diameters | 1 kit | Insulation and strain relief |
| Cable ties or braided sleeve | Small assortment | 1 kit | Cable routing and protection |

All servo grounds, the PCA9685 ground, the ESP32 ground, and the power-supply ground must share a common reference.

## 7. Mechanical hardware

| Item | Suggested starting point | Purpose | Status |
| --- | --- | --- | --- |
| M3 screw assortment | M3 x 6, 8, 10, 12, 16, and 20 mm | Printed-part and electronics mounting | Planned |
| M3 washers and nyloc nuts | Matching assortment | Load spreading and vibration resistance | Planned |
| M3 heat-set inserts | Sized for the printed wall thickness | Reusable threads in printed parts | Planned |
| M2 screw assortment | Verify against the selected micro servo | Gripper-servo mounting | Planned |
| M4/M5 shoulder and elbow hardware | Measure CAD holes before ordering | Structural joint pivots | To verify |
| Spacers or standoffs | Assorted M3 sizes | Alignment and electronics mounting | Planned |
| Joint bearings or bushings | Match final shaft diameters | Carry radial joint loads | To verify |
| Base thrust or Lazy Susan bearing | Match the base geometry | Supports the rotating arm above the base servo | To verify |

The servo output shaft should transmit torque, but bearings or bushings should support the arm's structural loads whenever possible.

## 8. Electrical architecture

```text
6 V supply or regulated UBEC
  -> inline fuse
  -> master switch
  -> power distribution
       -> base, shoulder, elbow, and gripper servos
       -> PCA9685 servo-power input

Computer USB -> ESP32 -> I2C -> PCA9685 -> servo signal lines
All grounds connected together
```

## 9. Camera plan

- Initial vision testing will use a phone secured on a fixed tripod or stand and streamed to the computer over Wi-Fi.
- Keeping the phone off the arm avoids adding mass and torque at the shoulder and elbow.
- A dedicated USB camera can be added later if repeatable calibration, lower latency, or fully integrated ROS 2 image topics become necessary.

## 10. Bring-up and verification sequence

- [ ] Set the regulated supply to 6.0 V before connecting servos.
- [ ] Check the power rail for shorts with a multimeter.
- [ ] Confirm the common ground between the controller and servo rail.
- [ ] Install the fuse and verify the master switch.
- [ ] Test one unloaded servo from the PCA9685.
- [ ] Test each joint individually with no payload.
- [ ] Record current draw, servo temperature, range of motion, and mechanical interference.
- [ ] Test the assembled arm with progressively larger loads up to the target foam ball.

## 11. Engineering skills demonstrated

- Converted SolidWorks mass properties and moment arms into torque requirements with a safety factor.
- Selected actuators by joint load instead of using one servo size everywhere.
- Separated logic power from the high-current servo rail and designed a common-ground PWM architecture.
- Added current protection, voltage regulation, strain relief, and staged test procedures.
- Chose a phone-based camera for early experiments to avoid unnecessary mass and cost.

## 12. Purchase record

Update this table from order confirmations and receipts so the repository distinguishes planned components from hardware actually purchased.

| Item | Manufacturer / model | Vendor | Quantity | Unit price | Order date | Status | Test notes |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |

Suggested status values: **Planned**, **Ordered**, **Received**, **Tested**, and **Installed**.
