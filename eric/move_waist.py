from lerobot.common.robot_devices.robots.configs import So101RobotConfig
from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus
import time

def move_smoothly(motor_bus, motor_name, start_pos, end_pos, steps=50, delay=0.05):
    """Move motor smoothly from start_pos to end_pos in specified number of steps"""
    for i in range(steps + 1):
        # Calculate intermediate position using linear interpolation
        current_pos = start_pos + (end_pos - start_pos) * (i / steps)
        motor_bus.write("Goal_Position", int(current_pos), motor_name)
        time.sleep(delay)

def main():
    # Create robot config
    config = So101RobotConfig()
    
    # Initialize the follower arm motors
    follower_arm = FeetechMotorsBus(config.follower_arms["main"])
    
    # Connect to the motors
    follower_arm.connect()
    
    try:
        # Enable torque on the gripper motor first
        follower_arm.write("Torque_Enable", 1, "gripper")
        print("Gripper torque enabled.")
        
        # Lock the gripper motor to prevent unwanted movement
        follower_arm.write("Lock", 1, "gripper")
        print("Gripper is now locked.")
        
        # Unlock the shoulder_pan motor to allow movement
        follower_arm.write("Lock", 0, "shoulder_pan")
        
        # Get current position of shoulder_pan motor
        current_pos = follower_arm.read("Present_Position", "shoulder_pan")
        print(f"Current shoulder_pan position: {current_pos}")
        
        # Move right 300 units smoothly
        print("Moving right 300 units...")
        move_smoothly(follower_arm, "shoulder_pan", current_pos, current_pos + 300)
        
        # Wait briefly at the right position
        time.sleep(1)
        
        # Move back left 300 units smoothly
        print("Moving back left 300 units...")
        move_smoothly(follower_arm, "shoulder_pan", current_pos + 300, current_pos)
        
        # Get final position
        final_pos = follower_arm.read("Present_Position", "shoulder_pan")
        print(f"Final shoulder_pan position: {final_pos}")
        
        # Lock the motor again
        follower_arm.write("Lock", 1, "shoulder_pan")
        
    finally:
        # Always disconnect when done
        follower_arm.disconnect()

if __name__ == "__main__":
    main() 