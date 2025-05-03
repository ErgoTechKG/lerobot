#!/usr/bin/env python3

import time
import math
import torch
from lerobot.common.robot_devices.robots.manipulator import ManipulatorRobot
from lerobot.common.robot_devices.robots.configs import So101RobotConfig
from lerobot.common.robot_devices.motors.configs import FeetechMotorsBusConfig

# Target angles in degrees
target_deg = [
    {"shoulder_pan": -1.58, "shoulder_lift": 190.37, "elbow_flex": 91.32, "wrist_flex": 77.43, "wrist_roll": -87.54, "gripper": -6.92},
    {"shoulder_pan": 17.14, "shoulder_lift": 190.37, "elbow_flex": 91.32, "wrist_flex": 77.43, "wrist_roll": -87.54, "gripper": -6.92},
    {"shoulder_pan": 36.56, "shoulder_lift": 190.20, "elbow_flex": 92.64, "wrist_flex": 77.43, "wrist_roll": -87.63, "gripper": -6.92},
]

def main():
    # Configure follower arm with explicit port
    follower_config = {
        "main": FeetechMotorsBusConfig(
            port="/dev/tty.usbmodem59700727351",
            motors={
                "shoulder_pan": [1, "sts3215"],
                "shoulder_lift": [2, "sts3215"],
                "elbow_flex": [3, "sts3215"],
                "wrist_flex": [4, "sts3215"],
                "wrist_roll": [5, "sts3215"],
                "gripper": [6, "sts3215"],
            },
        )
    }
    
    # Initialize robot with configuration
    config = So101RobotConfig(follower_arms=follower_config)
    robot = ManipulatorRobot(config)
    
    print("Attempting to connect to the robot...")
    # Connect to the robot
    robot.connect()
    print("Successfully connected to the robot.")
    
    try:
        # Move through each target position
        for i, target in enumerate(target_deg):
            print(f"\nMoving to position {i+1}:")
            print(f"Target angles: {target}")
            
            # Convert degrees to radians and create action tensor
            target_rad = [math.radians(target[joint]) for joint in ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]]
            action = torch.tensor(target_rad, dtype=torch.float32)
            
            # Move to target position
            robot.send_action(action)
            
            # Wait for movement to complete
            time.sleep(2)
            
            # Get current position
            obs = robot.capture_observation()
            current_pos = obs["observation.state"]
            print(f"Current position: {current_pos}")
            
            # Wait before next movement
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nMovement interrupted by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        # Clean up
        print("\nDisconnecting from the robot...")
        robot.disconnect()
        print("Successfully disconnected from the robot.")

if __name__ == "__main__":
    main()
