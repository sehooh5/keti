from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
import subprocess
import os
import sys

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'GPS with Gyro'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 450
        self.process = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # GPS 데이터
        # 제목
        title = QLabel('GPS 실시간 데이터', self)
        title.move(95, 10)

        # 실행 버튼
        btn1 = QPushButton('전송', self)
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

        # 영상 데이터
        # 제목
        title = QLabel('영상 데이터 전송', self)
        title.move(95, 190)

        # 입력창 1
        input1 = QLineEdit(self)
        input1.setPlaceholderText('카메라 주소 입력')
        input1.move(50, 220)
        input1.resize(300, 25)

        # 입력창 2
        input2 = QLineEdit(self)
        input2.setPlaceholderText('엣지서버 주소')
        input2.move(50, 260)
        input2.resize(300, 25)

        # 입력창 3
        input3 = QLineEdit(self)
        input3.setPlaceholderText('엣지서버 포트번호')
        input3.move(50, 300)
        input3.resize(300, 25)

        # 실행 버튼
        btn1 = QPushButton('실행', self)
        btn1.setToolTip('VLC 실행')
        btn1.move(50, 340)
        btn1.clicked.connect(lambda: self.start_process2(input1.text(), input2.text(), input3.text()))

        # 멈춤 버튼
        btn2 = QPushButton('멈춤', self)
        btn2.setToolTip('VLC 종료')
        btn2.move(150, 340)
        btn2.clicked.connect(self.stop_process2)
        self.show()

    def start_process(self):
        # 실행 중인 프로세스가 없는 경우에만 실행
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(['python3', 'gps_with_gyro.py'])

    def start_save_process(self):
        # 실행 중인 프로세스가 없는 경우에만 실행
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(['python3', 'gps_with_gyro.py', 'save'])

    def stop_process(self):
        # 실행 중인 프로세스가 있는 경우에만 종료
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

    def start_process2(self, input1, input2, input3):
    # 실행 중인 프로세스가 없는 경우에만 실행
    if self.process is None or self.process.poll() is not None:
        command = ['cvlc', '-vvv', input1, '--sout="#rtp{dst=' + input2 + ',port=' + input3 + ',mux=ts}"', '--no-sout-all', '--sout-keep']
        self.process = subprocess.Popen(command)

    def stop_process2(self):
        # 실행 중인 프로세스가 있는 경우에만 종료
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())