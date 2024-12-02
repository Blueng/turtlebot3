import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np

class ArucoTracker(Node):
    def __init__(self):
        super().__init__('aruco_tracker')

        # ArUco 마커 설정
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        self.aruco_params = cv2.aruco.DetectorParameters_create()

        # 좌표계 ID
        self.ORIGIN_ID = 32
        self.X_AXIS_ID = 33
        self.Y_AXIS_ID = 35
        self.TARGET_ID = 44 # TurtleBot3를 나타내는 마커 ID

        # 마커 실제 크기 (미터 단위)
        self.MARKER_SIZE = 0.05  # 5cm = 0.05m

        # 카메라 매트릭스와 왜곡 계수
        self.camera_matrix = np.array([[445.860105, 0.000000, 304.520700],
                                       [0.000000, 443.733547, 236.349816],
                                       [0.000000, 0.000000, 1.000000]])
        self.distortion_coefficients = np.array([0.010617, -0.000807, -0.000064, -0.001558, 0.000000])

        # 이미지 구독
        self.image_subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10
        )
        self.bridge = CvBridge()
        self.get_logger().info('Aruco Tracker Node Initialized')

    def image_callback(self, msg):
        try:
            # ROS 이미지를 OpenCV 이미지로 변환
            frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

            # 프레임 처리
            self.process_frame(frame)
        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def process_frame(self, frame):
        # 프레임을 회전 및 크기 조정
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        height, width = frame.shape[:2]
        top_crop, bottom_crop = 0, 0
        frame = frame[top_crop:height - bottom_crop, :]
        scale_factor = 1
        new_width = int(frame.shape[1] * scale_factor)
        new_height = int(frame.shape[0] * scale_factor)
        frame_resized = cv2.resize(frame, (new_width, new_height))

        # 왜곡 보정
        frame_resized = cv2.undistort(frame_resized, self.camera_matrix, self.distortion_coefficients)
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

        # ArUco 마커 탐지
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)

        if ids is not None:
            # 마커 그리기
            cv2.aruco.drawDetectedMarkers(frame_resized, corners, ids)

            # 상대 좌표 계산 및 시각화
            self.calculate_relative_coordinates(corners, ids.flatten(), frame_resized)

        # 결과 출력
        cv2.imshow('Coordinate Tracker', frame_resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()

    def calculate_relative_coordinates(self, corners, ids, frame):
        origin_idx = np.where(ids == self.ORIGIN_ID)[0]
        x_axis_idx = np.where(ids == self.X_AXIS_ID)[0]
        y_axis_idx = np.where(ids == self.Y_AXIS_ID)[0]
        target_idx = np.where(ids == self.TARGET_ID)[0]

        if len(origin_idx) == 0 or len(x_axis_idx) == 0 or len(y_axis_idx) == 0:
            return None

        origin = corners[origin_idx[0]][0].mean(axis=0).astype(int)
        x_axis = corners[x_axis_idx[0]][0].mean(axis=0).astype(int)
        y_axis = corners[y_axis_idx[0]][0].mean(axis=0).astype(int)

        marker_pixel_distance = np.linalg.norm(corners[origin_idx[0]][0][0] - corners[origin_idx[0]][0][1])
        pixel_to_meter = self.MARKER_SIZE / marker_pixel_distance

        x_pixel_distance = np.linalg.norm(x_axis - origin)
        y_pixel_distance = np.linalg.norm(y_axis - origin)

        x_length = x_pixel_distance * pixel_to_meter
        y_length = y_pixel_distance * pixel_to_meter

        x_correction_factor = 1.0 / x_length
        y_correction_factor = 1.2 / y_length

        self.get_logger().info(f"X-axis length (corrected): 1.00 m")
        self.get_logger().info(f"Y-axis length (corrected): 1.20 m")

        if len(target_idx) > 0:
            target = corners[target_idx[0]][0].mean(axis=0).astype(int)
            target_x_pixel = target[0] - origin[0]
            target_y_pixel = target[1] - origin[1]

            corrected_target_x = target_x_pixel * pixel_to_meter * x_correction_factor
            corrected_target_y = -(target_y_pixel * pixel_to_meter * y_correction_factor)

            self.get_logger().info(f"Target ({self.TARGET_ID}) pixel position: ({target_x_pixel:.2f} px, {target_y_pixel:.2f} px)")
            self.get_logger().info(f"Target ({self.TARGET_ID}) corrected position: ({corrected_target_x:.2f} m, {corrected_target_y:.2f} m)")

            cv2.circle(frame, tuple(target), 5, (0, 255, 255), -1)
            cv2.putText(frame, f"Target ({self.TARGET_ID})", (target[0] + 10, target[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)


def main(args=None):
    rclpy.init(args=args)
    node = ArucoTracker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()