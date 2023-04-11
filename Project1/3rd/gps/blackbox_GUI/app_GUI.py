from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import subprocess
import os
import sys

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'GPS with Gyro'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.process = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 실행 버튼
        btn1 = QPushButton('실행', self)
        btn1.setToolTip('gps_with_gyro.py 실행')
        btn1.move(50, 50)
        btn1.clicked.connect(self.start_process)

        # 저장 버튼
        btn2 = QPushButton('저장', self)
        btn2.setToolTip('gps_with_gyro.py save 실행')
        btn2.move(150, 50)
        btn2.clicked.connect(self.start_save_process)

        # 멈춤 버튼
        btn3 = QPushButton('멈춤', self)
        btn3.setToolTip('실행 중인 프로세스 중지')
        btn3.move(100, 100)
        btn3.clicked.connect(self.stop_process)

        self.show()

    def start_process(self):
        # 실행 중인 프로세스가 없는 경우에만 실행
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(['sudo', 'python3', 'gps_with_gyro.py'])

    def start_save_process(self):
        # 실행 중인 프로세스가 없는 경우에만 실행
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(['sudo', 'python3', 'gps_with_gyro.py', 'save'])

    def stop_process(self):
    # 실행 중인 프로세스가 있는 경우에만 종료
        if self.process is not None and self.process.poll() is None:
            os.system('sudo kill -9 {}'.format(self.process.pid))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())