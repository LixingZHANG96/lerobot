import logging

import zmq

from .so101_follower import SO101Follower
from .config_so101_follower import SO101FollowerConfig, SO101FollowerHostConfig

class SO101FollowerHost:
    def __init__(self, config: SO101FollowerHostConfig):
        self.zmq_context = zmq.Context()
        self.zmq_cmd_socket = self.zmq_context.socket(zmq.PULL)
        self.zmq_cmd_socket.setsockopt(zmq.CONFLATE, 1)
        self.zmq_cmd_socket.bind(f"tcp://*:{config.port_zmq_cmd}")

        self.zmq_observation_socket = self.zmq_context.socket(zmq.PUSH)
        self.zmq_observation_socket.setsockopt(zmq.CONFLATE, 1)
        self.zmq_observation_socket.bind(f"tcp://*:{config.port_zmq_observations}")

        self.connection_time_s = config.connection_time_s
        self.watchdog_timeout_ms = config.watchdog_timeout_ms
        self.max_loop_freq_hz = config.max_loop_freq_hz

    def disconnect(self):
        self.zmq_observation_socket.close()
        self.zmq_cmd_socket.close()
        self.zmq_context.term()

def main():
    logging.info("Configuring SO101 Follower...")
    robot_config = SO101FollowerConfig()
    robot = SO101Follower(robot_config)
    logging.info("SO101 Follower configured successfully.")

if __name__ == "__main__":
    main()