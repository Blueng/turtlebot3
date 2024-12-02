# log_system.py

"""
[Develop]
박현빈: Park Hyunbin 
김기범: Kim Gibeom 
윤찬웅: Yoon Chanwoong 
윤강록: Yoon Kangrok 
"""

import rclpy
from rclpy.node import Node


# interface
from manipulator_interface.msg import LogMsg

class LogSystem(Node):
    def __init__(self):
        super().__init__('log_system')
        self.system_log_subscriber = self.create_subscription(
            LogMsg,
            'system_logging',
            self.system_log_callback,
            10)

    # 시스템 로그 콜백 함수
    def system_log_callback(self, msg):
        # 로그 메시지를 받아서 GUI에 표시
        self.log_window.append_log(msg.log)
        self.get_logger().info(f'Received log: {msg.log}')