# main_system.py

"""
[Develop]
박현빈: Park Hyunbin 
김기범: Kim Gibeom 
윤찬웅: Yoon Chanwoong 
윤강록: Yoon Kangrok 
"""
from PyQt5.QtCore import pyqtSignal
import sys
import rclpy
from rclpy.node import Node

import smtplib
from email.mime.text import MIMEText

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QGraphicsScene, QGraphicsPixmapItem

import datetime
# interface
from manipulator_interface.msg import LogMsg

from manipulator_interface.msg import CvyrMsg

# UI modules
from .ui.main_window import Ui_MainWindow
from .ui.log_in import Ui_Log_In
from .ui.robot_log_system import Ui_Robot_log
from .ui.mtr_ctrl import Ui_Mtr_Ctrl
from .ui.job_list import Ui_Job_List
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy

import cv2 
import rclpy
from sensor_msgs.msg import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from rclpy.node import Node

import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem


class ROS2Thread(QThread):
    def __init__(self, node):
        super().__init__()
        self.node = node

    def run(self):
        rclpy.spin(self.node)
    
    def stop(self):
        if self.node:
            self.node.destroy_node()
        rclpy.shutdown()
        self.quit()
        self.wait()

class MainSystem(Node, QObject):
    # UI 업데이트를 위해 시그널 정의
    image_signal = pyqtSignal(QtGui.QImage)

    def __init__(self, main_window):
        # QObject와 Node 초기화
        QObject.__init__(self)
        Node.__init__(self, 'main_system')
        
        self.main_window = main_window  # MainWindow 객체 참조

        # 시그널 슬롯 연결
        self.image_signal.connect(self.main_window.update_image_wildview)
        log_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )

        # usb_cam(wild view)
        #self.create_subscription(Image, '/image_raw', self.image_callback, 10)
        self.log_pub = self.create_publisher(LogMsg, 'system_logging', qos_profile=log_qos)
        self.cvyr_ctrl_pub = self.create_publisher(CvyrMsg, 'cvyr_ctrl', 10)

    def image_callback(self, msg, crop_size=(461, 331)):
        # 메시지에서 데이터를 받아옴
        data = msg.data

        # 이미지의 크기와 채널 수를 확인하여 예상 크기와 비교
        height = msg.height
        width = msg.width

        if msg.encoding in ["yuyv", "yuv422_yuy2"]:  # YUYV 또는 YUV422일 경우
            expected_size = height * width * 2  # 두 픽셀당 4바이트 사용
            channels = 2
        elif msg.encoding == "mono8":  # 흑백일 경우
            expected_size = height * width
            channels = 1
        else:
            self.get_logger().error(f"Unsupported encoding: {msg.encoding}")
            return

        actual_size = len(data)

        if actual_size != expected_size:
            self.get_logger().error(f"Data size mismatch: expected {expected_size}, got {actual_size}")
            return

        try:
            # 원본 이미지 데이터를 numpy 배열로 변환
            img_data = np.frombuffer(data, dtype=np.uint8).reshape((height, width, channels) if channels > 1 else (height, width))
        except ValueError as e:
            self.get_logger().error(f"Error reshaping data: {e}")
            return

        # QImage 포맷 지정 및 데이터 변환
        if msg.encoding in ["yuyv", "yuv422_yuy2"]:
            # YUV 데이터를 RGB로 변환
            img_data = cv2.cvtColor(img_data, cv2.COLOR_YUV2RGB_YUYV)
            img_format = QtGui.QImage.Format_RGB888
        elif channels == 1:
            img_format = QtGui.QImage.Format_Grayscale8

        # QImage로 변환 후 시그널을 통해 메인 스레드에서 업데이트 수행
        q_image = QtGui.QImage(img_data.data, img_data.shape[1], img_data.shape[0], img_data.shape[1] * 3, img_format)
        self.image_signal.emit(q_image)

# 로그인 시스템
class LogInWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(LogInWindow, self).__init__()
        self.ui = Ui_Log_In()
        self.ui.setupUi(self)
        self.app = app

        # 로그인 버튼에 이벤트 연결
        self.ui.log_in.clicked.connect(self.handle_login)
    
    def handle_login(self):
        user_id = self.ui.input_id.toPlainText()
        password = self.ui.input_pwd.toPlainText()

        if user_id == "rokey" and password == "1234":
            QtWidgets.QMessageBox.information(self, "로그인 성공", "로그인에 성공했습니다.")
            self.open_main_window()
        else:
            QtWidgets.QMessageBox.warning(self, "로그인 실패", "ID 또는 비밀번호가 올바르지 않습니다.")

    def open_main_window(self):
        self.close()
        self.main_window = MainWindow(self.app)
        self.main_window.show()

# 로그 부분
class RobotLogWindow(QtWidgets.QMainWindow):
    log_signal = QtCore.pyqtSignal(str)

    def __init__(self, node):
        super().__init__()
        self.ui = Ui_Robot_log()
        self.ui.setupUi(self)
        self.node = node

        # QoS 설정
        log_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )

        # Log 메시지 구독
        self.system_log_subscriber = self.node.create_subscription(
            LogMsg,
            'system_logging',
            self.system_log_callback,
            qos_profile=log_qos
        )

        # Signal 연결
        self.log_signal.connect(self.update_log)

        # 버튼 이벤트 연결
        self.ui.pushButton.clicked.connect(self.handle_send)

    def handle_send(self):
        """사용자 입력을 이메일로 전송하는 버튼 이벤트 핸들러"""
        user_message = self.ui.textEdit.toPlainText().strip()  # 사용자가 입력한 메시지
        recipient_email = self.ui.textEdit_2.toPlainText().strip()  # 수신자 이메일 주소

        # 기본 이메일 주소 설정
        if not recipient_email:
            recipient_email = "example@naver.com"

        # 이메일 본문 생성
        email_body = (
            f"사용자 메시지:\n"
            f"{user_message}\n\n"
            f"-- 시스템 로그 추가 --\n"
            f"{self.ui.Log.toPlainText()}"  # UI에 표시된 모든 로그를 추가
        )

        # 이메일 전송 시도
        try:
            self.send_email(recipient_email, email_body)
            QtWidgets.QMessageBox.information(self, "전송 완료", f"메시지가 {recipient_email}로 전송되었습니다.")
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "전송 실패", f"이메일 전송 중 오류가 발생했습니다.\n{str(e)}")

    def system_log_callback(self, msg):
        """ROS Log 메시지를 처리하는 콜백 함수"""
        log_message = msg.log
        self.log_signal.emit(log_message)

        # 특정 조건 만족 시 이메일로 로그 전송
        if "ERROR" in log_message or "CRITICAL" in log_message:
            try:
                email_body = (
                    f"자동 생성된 시스템 로그 알림:\n"
                    f"Log Message: {log_message}\n"
                    f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"-- 사용자 추가 메시지 --\n"
                    f"{self.ui.textEdit.toPlainText()}"  # 사용자가 입력한 메시지를 포함
                )
                self.send_email("ycy1407@naver.com", email_body)
            except Exception as e:
                self.ui.Log.append(f"이메일 전송 실패: {str(e)}")

    def update_log(self, log_message):
        """UI의 로그 표시 영역에 메시지 추가"""
        self.ui.Log.append(log_message)

    def send_email(self, recipient, message):
        """이메일 전송 기능"""
        sender_email = "a01046997267@gmail.com"  # 발신자 이메일
        sender_password = "leth fwdf bgeo erce"  # 발신자 앱 비밀번호

        # 이메일 구성
        msg = MIMEText(message)
        msg['Subject'] = "로봇 시스템 에러 보고"
        msg['From'] = sender_email
        msg['To'] = recipient

        # SMTP 서버를 통해 이메일 전송
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient, msg.as_string())
        except smtplib.SMTPException as e:
            raise RuntimeError(f"SMTP 오류 발생: {e}")

# 메인 윈도우
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        # ROS2 초기화 및 스레드 시작
        rclpy.init()
        self.node = MainSystem(self)
        self.ros_thread = ROS2Thread(self.node)
        self.ros_thread.start()
        #다른창에 노드 전달
        self.job_list_window = JobList(self.node)
        self.mtr_ctrl_window = MtrCtrl(self.node)
        
        self.cvyr_class = MtrCtrl(self.node)


        
        # usb_cam(wild view)
        self.ui.top_view  # QGraphicsView 객체입니다.
        self.top_view_scene = QGraphicsScene()  # QGraphicsScene 생성
        self.ui.top_view.setScene(self.top_view_scene)  # QGraphicsView에 Scene 설정

        # rbt_cam (별도로 처리할 필요가 있을 경우 동일한 방식으로 처리 가능)
        self.ui.rbt_view
        self.rbt_view_scene = QGraphicsScene()  # QGraphicsScene 생성
        self.ui.rbt_view.setScene(self.rbt_view_scene)  # QGraphicsView에 Scene 설정

        # 버튼 이벤트 연결
        self.ui.play_btn.clicked.connect(self.handle_play)
        self.ui.pause_btn.clicked.connect(self.handle_pause)
        self.ui.reset_btn.clicked.connect(self.handle_reset)
        self.ui.log_out_btn.clicked.connect(self.handle_logout)
        self.ui.send_err_msg_btn.clicked.connect(self.handle_log_system)

        # add button connect start -----------------------------------------------------------------S
        self.ui.add_job.clicked.connect(lambda: self.add_job_to_window())
        self.ui.job_list.clicked.connect(self.open_job_list_window)
        self.ui.cnvyr_btn.clicked.connect(self.open_mtr_ctrl_window)
        self.ui.resume_btn.clicked.connect(self.handle_reset)

        # add button connect end -----------------------------------------------------------------E

        # select job start -------------------------------------------------------------------------S
        self.job_to_add = {'red' : 0, 'blue' : 0, 'goal' : 1}
        self.ui.chk_blue.stateChanged.connect(self.color_chk_box_changed)
        self.ui.chk_red.stateChanged.connect(self.color_chk_box_changed)
        self.ui.goal_cnt.valueChanged.connect(self.goal_change)
        self.ui.red_cnt.valueChanged.connect(self.red_num_change)
        self.ui.blue_cnt.valueChanged.connect(self.blue_num_change)


        # select job end   ------------------------------------------

        # 앱 종료 시 동작 정의
        self.app = app
        self.app.aboutToQuit.connect(self.cleanup)

    # usb_cam(wild view)
    def update_image_wildview(self, q_image):
        # QImage로부터 QPixmap 생성
        pixmap = QtGui.QPixmap.fromImage(q_image)

        # QGraphicsPixmapItem을 생성하여 Scene에 추가
        self.top_view_scene.clear()  # 이전의 Scene 아이템을 모두 제거
        pixmap_item = QGraphicsPixmapItem(pixmap)
        self.top_view_scene.addItem(pixmap_item)

    def cleanup(self):
        self.ros_thread.stop()

    # rbt_cam
    # def update_image_rbtview(self, q_image):
    #     # PyQt UI에서 top_view 위젯에 이미지를 업데이트
    #     pixmap = QtGui.QPixmap.fromImage(q_image)
    #     self.ui.rbt_view.setPixmap(pixmap)


    def handle_play(self):
        try:
            msg = "[INFO] Play 버튼 클릭 처리"
            log_msg = LogMsg()
            log_msg.log = msg
            self.node.log_pub.publish(log_msg)
        except Exception as e:
            # 예외 발생 시 로그 출력
            msg = f"[ERROR] Play 버튼 클릭 에러 : {str(e)}"
            log_msg = LogMsg()
            log_msg.log = msg
            self.node.log_pub.publish(log_msg)

    def handle_pause(self):
        self.node.get_logger().info("Pause 버튼 클릭 처리")
        self.cvyr_class.send_pause_msg()

    def handle_reset(self):
        self.node.get_logger().info("Reset 버튼 클릭 처리")

    def handle_logout(self):
        self.node.get_logger().info("로그아웃 버튼 클릭 처리")
        self.cleanup()
        self.close()
        self.login_window = LogInWindow(self.app)
        self.login_window.show()

    def handle_log_system(self):
        if not hasattr(self, 'log_system_window'):
            self.log_system_window = RobotLogWindow(self.node)
        self.log_system_window.show()


    def cleanup(self):
        self.ros_thread.stop()
    

    def color_chk_box_changed(self):
        # 체크박스 상태 확인
        if self.ui.chk_blue.isChecked():
            self.job_to_add['blue'] = self.ui.blue_cnt.value()
            self.ui.blue_cnt.setEnabled(True)
        else:
            self.job_to_add['blue'] = 0
            self.ui.blue_cnt.setEnabled(False)
        if self.ui.chk_red.isChecked():
            self.job_to_add['red'] = self.ui.red_cnt.value()
            self.ui.red_cnt.setEnabled(True)
        else:
            self.job_to_add['red'] = 0
            self.ui.red_cnt.setEnabled(False)

    def goal_change(self):
        self.job_to_add['goal'] = self.ui.goal_cnt.value()
    def red_num_change(self):
        self.job_to_add['red'] = self.ui.red_cnt.value()
    def blue_num_change(self):
        self.job_to_add['blue'] = self.ui.blue_cnt.value()

    def add_job_to_window(self):
        # 딕셔너리 내용을 문자열로 변환
        checkbox_text = self.job_to_add
        self.job_list_window.add_checkbox_and_button(checkbox_text)


    def open_job_list_window(self):
        self.job_list_window.show()  # 창 표시

    def open_mtr_ctrl_window(self):
        self.mtr_ctrl_window.show()  # 창 표시

    # select job function start --------------------------------------------------------------------S
    def handle_resume(self):
        self.cvyr_class.send_resume_msg()

    def color_chk_box_changed(self):
        # 체크박스 상태 확인
        if self.ui.chk_blue.isChecked():
            self.job_to_add['blue'] = self.ui.blue_cnt.value()
            self.ui.blue_cnt.setEnabled(True)
        else:
            self.job_to_add['blue'] = 0
            self.ui.blue_cnt.setEnabled(False)
        if self.ui.chk_red.isChecked():
            self.job_to_add['red'] = self.ui.red_cnt.value()
            self.ui.red_cnt.setEnabled(True)
        else:
            self.job_to_add['red'] = 0
            self.ui.red_cnt.setEnabled(False)

    def goal_change(self):
        self.job_to_add['goal'] = self.ui.goal_cnt.value()
    def red_num_change(self):
        self.job_to_add['red'] = self.ui.red_cnt.value()
    def blue_num_change(self):
        self.job_to_add['blue'] = self.ui.blue_cnt.value()

    def add_job_to_window(self):
        # 딕셔너리 내용을 문자열로 변환
        checkbox_text = self.job_to_add
        self.job_list_window.add_checkbox_and_button(checkbox_text)


    def open_job_list_window(self):
        self.job_list_window.show()  # 창 표시


    # select job function end   --------------------------------------------------------------------E

    def cleanup(self):
        self.ros_thread.stop()

# job list gui start -------------------------------------------------------------------------------S
class JobList(QDialog):
    def __init__(self, node):
        super(JobList, self).__init__()
        self.ui = Ui_Job_List()
        self.ui.setupUi(self)
        self.job_id = 0
        self.node = node

        # QScrollArea의 콘텐츠 위젯에 레이아웃 설정
        self.scroll_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.scroll_layout.setAlignment(Qt.AlignTop)  # 상단 정렬

        # 작업 항목 추적을 위한 리스트
        self.job_widgets = []

        # 작업 취소 버튼 이벤트 연결
        self.ui.cancel_job_button.clicked.connect(self.remove_checked_jobs)

    def add_checkbox_and_button(self, checkbox_text):
        # 수평 레이아웃 생성
        hbox_layout = QHBoxLayout()

        # 체크박스 추가
        checkbox = QCheckBox(f"{self.job_id} : {checkbox_text}", self.ui.scrollAreaWidgetContents)
        hbox_layout.addWidget(checkbox)

        # 버튼 추가
        button = QPushButton("작업 개시", self.ui.scrollAreaWidgetContents)
        button.clicked.connect(lambda: self.start_job(self.job_id))
        hbox_layout.addWidget(button)

        # 수평 레이아웃을 수직 레이아웃에 추가
        self.scroll_layout.addLayout(hbox_layout)

        # 작업 항목 추가 (ID 포함)
        self.job_widgets.append({
            "id": self.job_id,
            "layout": hbox_layout,
            "checkbox": checkbox,
            "button": button,
            "text": f"{self.job_id} : Red: {checkbox_text['red']}, Blue: {checkbox_text['blue']}, Goal: {checkbox_text['goal']}"
        })

        print(f"Added job with ID {self.job_id}: {checkbox_text}")
        self.job_id += 1


    def remove_checked_jobs(self):
        # 체크된 항목 삭제
        for job in self.job_widgets[:]:  
            if job["checkbox"].isChecked():
                # 레이아웃에서 삭제
                for i in reversed(range(job["layout"].count())):
                    widget = job["layout"].itemAt(i).widget()
                    if widget:
                        widget.setParent(None)  # 위젯 삭제
                self.scroll_layout.removeItem(job["layout"])

    def start_job(self, checkbox_text):
        print(f"작업 '{checkbox_text}' 시작")

# job list gui end   -------------------------------------------------------------------------------E

# Moter control gui start --------------------------------------------------------------------------S
class MtrCtrl(QDialog):
    def __init__(self, node):
        super(MtrCtrl, self).__init__()
        self.ui = Ui_Mtr_Ctrl()
        self.ui.setupUi(self)        
        self.node = node

        self.cvyr_len = 0
        self.cvyr_len2 = 0
        self.state = 0
        self.ui.len_show.setText(f'mv len : {self.cvyr_len}')

        # len_set_bar 초기화
        self.ui.len_set_bar.setMinimum(0)  # 최소값
        self.ui.len_set_bar.setMaximum(1090)  # 최대값
        self.ui.len_set_bar.setValue(0)  # 초기값
        self.ui.len_set_bar.valueChanged.connect(self.update_cvyr_mv)

        # 버튼 연결
        self.ui.mtr_on_btn.clicked.connect(self.send_on_msg)
        self.ui.mtr_off_btn.clicked.connect(self.send_off_msg)
        self.ui.chk_inf.stateChanged.connect(self.send_inf_msg)

    def update_cvyr_mv(self, len):
        self.ui.len_show.setText(f"mv len : {len}")
        self.cvyr_len2 = len
        self.cvyr_len = len

    def send_on_msg(self):
        print("pubbb")
        try:
            # CvyrMsg의 인스턴스 생성
            msg = CvyrMsg()
            msg.mv_len = self.cvyr_len

            # 메시지 퍼블리시
            self.node.cvyr_ctrl_pub.publish(msg)

            # 성공 로그 출력
            self.node.get_logger().info('Message sent successfully: '
                                        f'mv_len={msg.mv_len}')
        except Exception as e:
            # 실패 로그 출력
            self.node.get_logger().error(f'Failed to send message: {e}')

    def send_state_msg(self, state):
        try:
            # CvyrMsg의 인스턴스 생성
            msg = CvyrMsg()
            msg.mv_len = self.state

            # 메시지 퍼블리시
            self.node.cvyr_ctrl_pub.publish(msg)

            # 성공 로그 출력
            self.node.get_logger().info(f'send {state} message')
        except Exception as e:
            # 실패 로그 출력
            self.node.get_logger().error(f'Failed to send message: {e}')

    def send_off_msg(self):
        self.state = -1
        self.send_state_msg('off')


    def send_pause_msg(self):
        self.state = -2
        self.send_state_msg('pause')


    def send_resume_msg(self):
        self.state = -3
        self.send_state_msg('resume')

    def send_inf_msg(self, state):
        if state == 2:
            self.cvyr_len = 2000
            self.ui.len_set_bar.setEnabled(False)

        elif state == 0:
            self.cvyr_len = self.cvyr_len2
            self.ui.len_set_bar.setEnabled(True)



def main():
    app = QtWidgets.QApplication(sys.argv)

    # 로그인 창 실행
    login_window = LogInWindow(app)
    login_window.show()

    try:
        sys.exit(app.exec_())  # PyQt5 이벤트 루프 실행
    finally:
        rclpy.shutdown()  # ROS 2 종료

if __name__ == "__main__":
    main()
