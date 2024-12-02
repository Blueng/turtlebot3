import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose, Twist
from cv_bridge import CvBridge
import cv2
import cv2.aruco as aruco
import numpy as np
import math

# Camera Matrix and Distortion Coefficients
CAMERA_MATRIX = np.array([[445.860105, 0.000000, 304.520700],
                          [0.000000, 443.733547, 236.349816],
                          [0.000000, 0.000000, 1.000000]])

DISTORTION_COEFFICIENTS = np.array([0.010617, -0.000807, -0.000064, -0.001558, 0.000000])


class ArucoPose(Node):
    def __init__(self):
        super().__init__('aruco_pose_node')
        
        # ROS 2 Publishers and Subscribers
        self.pose_pub = self.create_publisher(Pose, 'pose', 10)
        self.vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.image_sub = self.create_subscription(Image, '/image_raw', self.image_callback, 10)

        # OpenCV Bridge
        self.bridge = CvBridge()

        # ArUco Dictionary and Parameters
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)
        self.parameters = aruco.DetectorParameters_create()

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV Image
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect ArUco Markers
            corners, ids, _ = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)

            if ids is not None:
                self.get_logger().info(f"Markers detected: {ids.flatten()}")

                for i in range(len(ids)):
                    # Estimate Pose of ArUco Marker
                    rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[i], 0.1, CAMERA_MATRIX, DISTORTION_COEFFICIENTS)

                    # Draw Marker and Axis
                    aruco.drawDetectedMarkers(frame, corners, ids)
                    aruco.drawAxis(frame, CAMERA_MATRIX, DISTORTION_COEFFICIENTS, rvec, tvec, 0.05)

                    # Publish Pose
                    pose = Pose()
                    pose.position.x = tvec[0][0][0]
                    pose.position.y = tvec[0][0][1]
                    pose.position.z = tvec[0][0][2]
                    self.pose_pub.publish(pose)

                    # Calculate and Publish Velocity
                    self.calculate_and_publish_velocity(tvec)

        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

        # Display Image
        cv2.imshow("ArUco Detection", frame)
        cv2.waitKey(1)

    def calculate_and_publish_velocity(self, tvec):
        # Calculate angular and linear velocity
        angular = math.atan2(tvec[0][0][0], tvec[0][0][2])
        linear = 0.35 * math.sqrt(tvec[0][0][0] ** 2 + tvec[0][0][2] ** 2)

        # Apply thresholds and scaling
        if linear < 0.1:
            linear = 0.0
        elif linear > 0.18:
            linear *= 1.5

        if angular < -0.0:
            angular *= 1.5
        elif angular > 0.0:
            angular *= 1.5

        # Publish Twist message
        cmd = Twist()
        cmd.linear.x = -linear
        cmd.angular.z = -angular
        self.vel_pub.publish(cmd)


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
