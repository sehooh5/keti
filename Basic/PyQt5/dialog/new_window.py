#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(300, 300, 400, 300)  # x, y, w, h
        self.setWindowTitle('Status Window')

        # QButton 위젯 생성
        self.button = QPushButton('Dialog Button', self)
        self.button.clicked.connect(self.dialog_open)
        self.button.setGeometry(10, 10, 200, 50)

        # QDialog 설정
        self.dialog = QDialog()

    # 버튼 이벤트 함수
    def dialog_open(self):
        # 버튼 추가
        btnDialog = QPushButton("OK", self.dialog)
        btnDialog.move(100, 100)
        btnDialog.clicked.connect(self.dialog_close)

        # QDialog 세팅
        self.dialog.setWindowTitle('Dialog')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300, 200)
        self.dialog.show()

    # Dialog 닫기 이벤트
    def dialog_close(self):
        self.dialog.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
