from lerobot.common.robot_devices.robots.configs import So101RobotConfig
from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus
import time

def main():
    # Create robot config
    config = So101RobotConfig()
    
    # Initialize the follower arm motors
    follower_arm = FeetechMotorsBus(config.follower_arms["main"])
    
    # Connect to the motors
    follower_arm.connect()
    
    try:
        # Unlock the motor to allow movement
        follower_arm.write("Lock", 0, "shoulder_pan")
        
        # Get current position of shoulder_pan motor
        current_pos = follower_arm.read("Present_Position", "shoulder_pan")
        print(f"Current shoulder_pan position: {current_pos}")
        
        # Calculate new position (100 units left)
        new_pos = current_pos + 50
        
        # Move to new position
        print(f"Moving shoulder_pan to position: {new_pos}")
        follower_arm.write("Goal_Position", new_pos, "shoulder_pan")
        
        # Wait for movement to complete
        time.sleep(2)
        
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