import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose, Twist
from cv_bridge import CvBridge
import cv2
import cv2.aruco as aruco
import numpy as np
import math

import time

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Header
import math

from control_msgs.action import GripperCommand
from rclpy.action import ActionClient

# Camera Matrix and Distortion Coefficients
CAMERA_MATRIX = np.array([[445.860105, 0.000000, 304.520700],
                          [0.000000, 443.733547, 236.349816],
                          [0.000000, 0.000000, 1.000000]])

DISTORTION_COEFFICIENTS = np.array([0.010617, -0.000807, -0.000064, -0.001558, 0.000000])


class ArucoPose(Node):
    def __init__(self):
        super().__init__('aruco_pose_node')
        
        self.pose_pub = self.create_publisher(Pose, 'pose', 10)
        self.vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.image_sub = self.create_subscription(Image, '/image_raw', self.image_callback, 10)
        self.joint_pub = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)
        self.gripper_action_client = ActionClient(self, GripperCommand, 'gripper_controller/gripper_cmd')

        self.bridge = CvBridge()
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)
        self.parameters = aruco.DetectorParameters_create()
        
        self.target_distance = 0.13  # 목표 거리 (m)
        self.reached_target = False  # 목표 도달 여부 플래그
        #self.send_gripper_goal(0.025) # open

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)

            if ids is not None:
                self.get_logger().info(f"Markers detected: {ids.flatten()}")

                for i in range(len(ids)):
                    if ids[i][0] == 30:
                        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[i], 0.1, CAMERA_MATRIX, DISTORTION_COEFFICIENTS)
                        aruco.drawDetectedMarkers(frame, corners, ids)
                        aruco.drawAxis(frame, CAMERA_MATRIX, DISTORTION_COEFFICIENTS, rvec, tvec, 0.05)

                        pose = Pose()
                        pose.position.x = tvec[0][0][0]
                        pose.position.y = tvec[0][0][1]
                        pose.position.z = tvec[0][0][2]
                        self.pose_pub.publish(pose)

                        distance = math.sqrt(tvec[0][0][0] ** 2 + tvec[0][0][1] ** 2 + tvec[0][0][2] ** 2)
                        self.get_logger().info(f"Current distance: {distance}")

                        if distance > self.target_distance:
                            self.calculate_and_publish_velocity(tvec)
                        else:
                            self.stop_robot()
                            if not self.reached_target:
                                self.reached_target = True
                                self.send_gripper_goal(0.025)
                                self.activate_robot_arm()

        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

        cv2.imshow("ArUco Detection", frame)
        cv2.waitKey(1)

    def calculate_and_publish_velocity(self, tvec):
        angular = math.atan2(tvec[0][0][0], tvec[0][0][2])
        linear = 0.35 * math.sqrt(tvec[0][0][0] ** 2 + tvec[0][0][2] ** 2)
        linear = max(0.0, min(0.18, linear * 1.5))
        angular *= 1.5
        cmd = Twist()
        cmd.linear.x = -0.04 #-linear
        cmd.angular.z = -angular
        self.vel_pub.publish(cmd)

    def stop_robot(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.vel_pub.publish(cmd)
        self.get_logger().info("Robot stopped.")

    # def activate_robot_arm(self):
    #     self.get_logger().info("Activating robot arm...")
        
    #     joint_positions = [-0.15123541734990567, 0.8446253776408663,  -0.6111530342292582, 0.6175655768671406]
    #     time_sec = 3.0
    #     self.control_arm(joint_positions, time_sec)

    #     time.sleep(5)

    #     self.send_gripper_goal(-0.015) # close

    #     time.sleep(5)

    #     # 초기위치
    #     joint_positions = [0.0, 0.23984096414749578, -0.30315141922511196, 0.9650258157179945]
    #     time_sec = 3.0
    #     self.control_arm(joint_positions, time_sec)

    #     time.sleep(5)

    #     # 컨베이어 벨트 이동
    #     joint_positions = [1.6244856543708943, 0.2696738225102957, -0.0260776733940559, 1.2574270975816038]
    #     time_sec = 3.0
    #     self.control_arm(joint_positions, time_sec)

    #     time.sleep(5)

    #     self.send_gripper_goal(0.025) # open

    #     time.sleep(1)

    #     # 초기위치
    #     joint_positions = [0.0, 0.23984096414749578, -0.30315141922511196, 0.9650258157179945]
    #     time_sec = 3.0
    #     self.control_arm(joint_positions, time_sec)

    def activate_robot_arm(self):
        self.get_logger().info("Activating robot arm...")

        # 순차 작업 리스트
        self.arm_task_queue = [
            {"action": "gripper", "position": 0.025, "time_sec": 1.0},
            {"action": "move_arm", "joint_positions": [0.2638446955163303, 0.3273359443037636, 0.4755340442445488, 0.46633015951723494], "time_sec": 5.0},
            {"action": "gripper", "position": -0.015, "time_sec": 5.0},  # Gripper Close
            {"action": "move_arm", "joint_positions": [0.0, 0.23984096414749578, -0.30315141922511196, 0.9650258157179945], "time_sec": 3.0},  # 초기 위치
            {"action": "move_arm", "joint_positions": [1.6244856543708943, 0.2696738225102957, -0.0260776733940559, 1.2574270975816038], "time_sec": 3.0},  # 컨베이어 벨트 위치
            {"action": "gripper", "position": 0.025, "time_sec": 1.0},  # Gripper Open
            {"action": "move_arm", "joint_positions": [0.0, 0.23984096414749578, -0.30315141922511196, 0.9650258157179945], "time_sec": 3.0},  # 초기 위치
        ]

        # 작업 실행을 위한 타이머 시작
        self.task_index = 0
        self.timer = self.create_timer(0.1, self.execute_next_task)

    def execute_next_task(self):
        if self.task_index >= len(self.arm_task_queue):
            self.get_logger().info("All tasks completed.")
            self.timer.cancel()
            return

        task = self.arm_task_queue[self.task_index]
        if task["action"] == "move_arm":
            self.control_arm(task["joint_positions"], task["time_sec"])
        elif task["action"] == "gripper":
            self.send_gripper_goal(task["position"])

        self.task_index += 1

        # 타이머 간격 조정 (다음 작업까지 대기 시간 설정)
        if self.task_index < len(self.arm_task_queue):
            next_task = self.arm_task_queue[self.task_index]
            self.timer.timer_period_ns = int(next_task["time_sec"] * 1e9)

    def control_arm(self, joint_positions, time_sec):
        trajectory_msg = JointTrajectory()
        current_time = self.get_clock().now()
        trajectory_msg.header = Header()
        trajectory_msg.header.stamp = current_time.to_msg()
        trajectory_msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']
        point = JointTrajectoryPoint()
        point.positions = joint_positions
        point.velocities = [0.0] * len(joint_positions)
        point.time_from_start.sec = int(time_sec)
        point.time_from_start.nanosec = int((time_sec - int(time_sec)) * 1e9)
        trajectory_msg.points = [point]
        self.joint_pub.publish(trajectory_msg)

    def send_gripper_goal(self, position):
        goal = GripperCommand.Goal()
        goal.command.position = position
        goal.command.max_effort = -1.0
        if not self.gripper_action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error("Gripper action server not available!")
            return
        self.gripper_action_client.send_goal_async(goal)


def main(args=None):
    rclpy.init(args=args)

    node = ArucoPose()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down node...")
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()