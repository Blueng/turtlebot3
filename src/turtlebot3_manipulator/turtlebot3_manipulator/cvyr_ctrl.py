import rclpy
from rclpy.node import Node
from manipulator_interface.msg import CvyrMsg
from .modules.functions import *
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy


class CvyrNode(Node):
    def __init__(self):
        super().__init__('CvyrNode')  # 노드 이름 설정
        self.get_logger().info('SimpleNode가 시작되었습니다!')
        self.cvyr_ctrl_sub = self.create_subscription(
            CvyrMsg, 
            'cvyr_ctrl',  
            self.control_conveyer,  
            10  
        )

        log_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
    
        # 로봇의 YoloV8 카메라 스트림을 통해 실시간 객체 감지
        # self.robot_cam_sub = self.create_subscription()

        self.log_pub = self.create_publisher(LogMsg, 'system_logging', qos_profile=log_qos)

    def control_conveyer(self, msg):
        # 컨베이어 벨트 켜짐
        message = mtr_send_clk(int(msg.mv_len) * 10)  # 1mm -> 10clk
        log_msg = LogMsg()
        log_msg.log = str(message)  # str 타입으로 변환
        self.log_pub.publish(log_msg)  # self로 수정


def main(args=None):
    rclpy.init(args=args)  # ROS2 초기화
    node = CvyrNode()  # 노드 인스턴스 생성

    try:
        rclpy.spin(node)  # 노드 실행
    except KeyboardInterrupt:
        node.get_logger().info('종료 신호를 받았습니다.')
    finally:
        node.destroy_node()  # 노드 종료
        rclpy.shutdown()  # ROS
