from lerobot.common.robot_devices.robots.configs import So101RobotConfig
from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus

def main():
    # Create robot config
    config = So101RobotConfig()
    
    # Initialize the follower arm motors
    follower_arm = FeetechMotorsBus(config.follower_arms["main"])
    
    # Connect to the motors
    follower_arm.connect()
    
    try:
        # Unlock the shoulder_pan motor
        follower_arm.write("Lock", 0, "shoulder_pan")
        print("shoulder_pan is now unlocked. You can manually move it.")
        
        # Wait for user input before locking again
        input("Press Enter to lock the motor and exit...")
        
        # Lock the motor again
        follower_arm.write("Lock", 1, "shoulder_pan")
        print("shoulder_pan is now locked.")
        
    finally:
        # Always disconnect when done
        follower_arm.disconnect()

if __name__ == "__main__":
    main() 