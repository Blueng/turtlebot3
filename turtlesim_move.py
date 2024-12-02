import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import numpy as np
import sys

class Driver_node(Node):
    def __init__(self):
        super().__init__('turtlesim_driver')
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.pose = None

    def pose_callback(self, data):
        self.pose = data

    def timer_callback(self):
        goal = Pose()
        # W = v / r
        goal.x = float(sys.argv[1])
        goal.y = float(sys.argv[2])
        goal.theta = 1.57

        dist_tol = 0.1
        angular_tol = 0.001
        new_vel = Twist()

        # Ecludian Distance
        distance_to_goal = math.sqrt((goal.x - self.pose.x) ** 2 + (goal.y - self.pose.y) ** 2)
        
        # Angle to Goal
        angle_to_goal = math.atan2(goal.y - self.pose.y, goal.x - self.pose.x)

        
        if abs(angle_to_goal - self.pose.theta) > angular_tol:
            new_vel.angular.z = (angle_to_goal - self.pose.theta)
        else:
            if distance_to_goal >= dist_tol:
                new_vel.linear.x = distance_to_goal
            else:
                new_vel.linear.x = 0.0
                self.get_logger().info('목표 달성')
        self.cmd_vel_publisher.publish(new_vel)


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = Driver_node()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
