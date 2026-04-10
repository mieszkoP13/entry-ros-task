## Submission Notes

### 1. Design decisions

- The TF tree was split into static and dynamic parts:
  - Static transforms (`world → base_link`, `link1 → link2`, `link2 → end_effector`) are published using `StaticTransformBroadcaster`.
  - The dynamic joint (`base_link → link1`) is published using `TransformBroadcaster` at 50 Hz.
- The dynamic motion is implemented as a sinusoidal rotation around the Z axis with 0.5 Hz frequency and 45° amplitude.
- The pose publisher uses TF2 lookup via buffer and listener, with proper exception handling to ensure robustness when transforms are temporarily unavailable (no node crashes).

---

### 2. Verification

- Verified using:
```
ros2 topic echo /end_effector_pose
```
- Confirmed that:
  - The end-effector position changes continuously over time.
  - The motion follows a smooth periodic pattern consistent with the rotating joint.
  - Additionally checked TF chain correctness using ROS2 TF tools (tf tree consistency via runtime observation).

---

### 3. Improvements

- Add unit tests validating TF chain structure and expected transform relationships.
- Extend debugging tools (e.g. RViz configuration for easier visualization of motion).
- Improve pose validation by programmatically checking expected sinusoidal behavior.
