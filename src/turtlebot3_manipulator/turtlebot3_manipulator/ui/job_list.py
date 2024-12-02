from PyQt5 import QtCore, QtWidgets


class Ui_Job_List(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(686, 360)

        # 작업 취소 버튼 추가
        self.cancel_job_button = QtWidgets.QPushButton(Dialog)
        self.cancel_job_button.setGeometry(QtCore.QRect(10, 320, 150, 30))  # 위치와 크기 설정
        self.cancel_job_button.setObjectName("cancel_job_button")
        self.cancel_job_button.setText("작업 삭제")

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(330, 320, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.job_list_scrl = QtWidgets.QScrollArea(Dialog)
        self.job_list_scrl.setGeometry(QtCore.QRect(10, 10, 661, 301))
        self.job_list_scrl.setWidgetResizable(True)
        self.job_list_scrl.setObjectName("job_list_scrl")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 659, 299))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # 스크롤 영역의 콘텐츠 위젯 설정
        self.job_list_scrl.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)  # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Job List"))
