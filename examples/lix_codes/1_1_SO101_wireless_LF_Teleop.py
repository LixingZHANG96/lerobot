import time

from lerobot.robots.so101_follower import SO101FollowerClient, SO101FollowerClientConfig
from lerobot.teleoperators.so101_leader import SO101Leader, SO101LeaderConfig
from lerobot.utils.robot_utils import busy_wait
from lerobot.utils.visualization_utils import init_rerun, log_rerun_data

FPS = 30

# Create the robot and teleoperator configurations
remote_ip = "192.168.1.103"
port = "/dev/ttyACM0"  # Adjust this port based on your system
id = "lix_follower_1"
robot_config = SO101FollowerClientConfig(remote_ip=remote_ip)
teleop_arm_config = SO101LeaderConfig(port=port, id=id)

# Initialize the robot and teleoperator
robot = SO101FollowerClient(robot_config)
leader_arm = SO101Leader(teleop_arm_config)

# Connect to the robot and teleoperator
robot.connect()
leader_arm.connect()

# Init rerun viewer
init_rerun(session_name="so101_wireless_LF_control")

if not robot.is_connected or not leader_arm.is_connected:
    raise ValueError("Robot or teleop is not connected!")

print("Starting teleop loop...")
while True:
    t0 = time.perf_counter()

    # Get robot observation
    observation = robot.get_observation()

    # Get teleop action
    arm_action = leader_arm.get_action()
    arm_action = {f"arm_{k}": v for k, v in arm_action.items()}

    # Send action to robot
    _ = robot.send_action(arm_action)

    # Visualize
    log_rerun_data(observation=observation, action=arm_action)

    busy_wait(max(1.0 / FPS - (time.perf_counter() - t0), 0.0))