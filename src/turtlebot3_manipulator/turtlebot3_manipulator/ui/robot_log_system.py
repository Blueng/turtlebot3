# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'robot_log_system.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Robot_log(object):
    def setupUi(self, Robot_log):
        Robot_log.setObjectName("Robot_log")
        Robot_log.resize(400, 600)
        self.Log = QtWidgets.QTextBrowser(Robot_log)
        self.Log.setGeometry(QtCore.QRect(10, 10, 380, 361))
        self.Log.setStyleSheet("QTextBrowser{\n"
                               "    background : black;\n"
                               "    color : white;\n"
                               "}")
        self.Log.setObjectName("Log")
        self.textEdit = QtWidgets.QTextEdit(Robot_log)
        self.textEdit.setGeometry(QtCore.QRect(10, 410, 281, 101))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Robot_log)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 550, 281, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label = QtWidgets.QLabel(Robot_log)
        self.label.setGeometry(QtCore.QRect(20, 380, 91, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Robot_log)
        self.label_2.setGeometry(QtCore.QRect(10, 520, 121, 17))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Robot_log)
        self.pushButton.setGeometry(QtCore.QRect(300, 550, 89, 25))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Robot_log)
        QtCore.QMetaObject.connectSlotsByName(Robot_log)

    def retranslateUi(self, Robot_log):
        _translate = QtCore.QCoreApplication.translate
        Robot_log.setWindowTitle(_translate("Robot_log", "ROBOT LOG SYSTEM"))
        self.label.setText(_translate("Robot_log", "보낼 메세지 "))
        self.label_2.setText(_translate("Robot_log", " 이메일 주소 입력"))
        self.pushButton.setText(_translate("Robot_log", "send"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Robot_log = QtWidgets.QWidget()
#     ui = Ui_Robot_log()
#     ui.setupUi(Robot_log)
#     Robot_log.show()
#     sys.exit(app.exec_())