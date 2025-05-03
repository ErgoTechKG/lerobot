import time
import numpy as np
from lerobot.common.robot_devices.motors.configs import FeetechMotorsBusConfig
from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus
import json

# 1. 配置 main_follower
config = FeetechMotorsBusConfig(
    port="/dev/tty.usbmodem59700727351",  # TODO: 替换为你的端口
    motors={
        "shoulder_pan": [1, "sts3215"],
        "shoulder_lift": [2, "sts3215"],
        "elbow_flex": [3, "sts3215"],
        "wrist_flex": [4, "sts3215"],
        "wrist_roll": [5, "sts3215"],
        "gripper": [6, "sts3215"],
    }
)

# 2. 连接
bus = FeetechMotorsBus(config)
bus.connect()

# 3. 加载校准数据
with open(".cache/calibration/so101/main_follower.json", "r") as f:
    calibration_data = json.load(f)
bus.calibration = calibration_data

# 4. 获取当前关节位置
current_pos = bus.read("Present_Position")  # numpy array, shape (6,)

# 4.5. 打印当前关节位置
print("Current joint positions (raw motor values):")
for i, (name, pos) in enumerate(zip(calibration_data["motor_names"], current_pos)):
    print(f"  {name}: {pos}")

# # 4.6. 将电机步进值转换为角度并打印
# current_deg = bus.apply_calibration(current_pos, None)
# print("\nCurrent joint positions (calibrated degrees):")
# for i, (name, pos) in enumerate(zip(calibration_data["motor_names"], current_deg)):
#     print(f"  {name}: {pos:.2f}°")

# # 4.7. 打印校准数据
# print("\nCalibration data:")
# print(f"  Homing offset: {calibration_data['homing_offset']}")
# print(f"  Drive mode: {calibration_data['drive_mode']}")
# print(f"  Start positions: {calibration_data['start_pos']}")
# print(f"  End positions: {calibration_data['end_pos']}")
# print(f"  Calibration mode: {calibration_data['calib_mode']}")


# # 5. 目标zero position（所有关节0度，需用revert_calibration转为电机步进值）
# zero_deg = np.zeros(6)
# zero_motor = bus.revert_calibration(zero_deg, None)  # shape (6,)

# # 6. 分200步慢慢插值
# steps = 200
# for i in range(1, steps + 1):
#     intermediate = current_pos + (zero_motor - current_pos) * i / steps
#     bus.write("Goal_Position", intermediate)
#     time.sleep(0.05)  # 每步50ms，总共约10秒

# 7. 断开
bus.disconnect()