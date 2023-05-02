from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QThread
import subprocess
import os
import sys
import psutil

class ProcessThread(QThread):
    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        self.process = None
        self.isRunning = False # 추가

    def run(self):
        self.process = subprocess.Popen(self.cmd)
        self.isRunning = True # 추가
        self.process.wait()
        self.isRunning = False # 추가

    def stop(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            self.isRunning = False # 추가

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'GPS with Gyro'
        self.left = 10
        self.top = 10
        self.width = 450
        self.height = 450
        self.process_thread = None
        self.process_save_thread = None
        self.process2_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # GPS 데이터
        # 제목
        title = QLabel('GPS 실시간 데이터', self)
        title.move(95, 10)

        # 입력창 1
        input2 = QLineEdit(self)
        input2.setText('gps_')
        input2.move(50, 50)
        input2.resize(300, 25)

        # 실행 버튼
        btn1 = QPushButton('전송', self)
        btn1.setToolTip('gps_with_gyro.py 실행')
        btn1.move(50, 100)
        btn1.clicked.connect(self.start_process)

        # 실행 상태 표시 # 추가
        self.status1 = QLabel('GPS 데이터 전송 멈춤', self)
        self.status1.move(250, 105)

        # 저장 버튼
        btn2 = QPushButton('저장', self)
        btn2.setToolTip('gps_with_gyro.py save 실행')
        btn2.move(150, 100)
        btn2.clicked.connect(lambda: self.start_save_process(input2.text()))

        # 저장 실행 상태 표시 # 추가
        self.status2 = QLabel('GPS 데이터 저장 멈춤', self)
        self.status2.move(250, 155)

        # 멈춤 버튼
        btn3 = QPushButton('멈춤', self)
        btn3.setToolTip('실행 중인 프로세스 중지')
        btn3.move(100, 150)
        btn3.clicked.connect(self.stop_process)


        # 영상 데이터
        # 제목
        title = QLabel('영상 데이터 저장', self)
        title.move(95, 190)

        # 입력창 1
        input1 = QLineEdit(self)
        input1.setText('blackbox_')
        input1.move(50, 220)
        input1.resize(300, 25)

        # 실행 버튼
        btn4 = QPushButton('저장', self)
        btn4.setToolTip('영상 저장')
        btn4.move(50, 260)
        btn4.clicked.connect(lambda: self.start_process2(input1.text()))

        # 멈춤 버튼
        btn5 = QPushButton('멈춤', self)
        btn5.setToolTip('저장 종료')
        btn5.move(150, 260)
        btn5.clicked.connect(self.stop_process2)

        # rtp 전송 상태 표시 # 추가
        self.status3 = QLabel('영상 저장 멈춤', self)
        self.status3.move(250, 260)

        self.show()



    def start_process(self):
        # 실행 중인 프로세스가 없는 경우에만 실행
        if self.process_thread is None or not self.process_thread.isRunning():
            self.process_thread = ProcessThread(['python3', 'gps_with_gyro.py'])
            self.process_thread.start()
            self.status1.setText('GPS 데이터 전송중')

    def start_save_process(self, input2):
        # 실행 중인 프로세스가 없는 경우에만 실행
        if self.process_save_thread is None or not self.process_save_thread.isRunning():
            self.process_save_thread = ProcessThread(['python3', 'gps_with_gyro.py', input2])
            self.process_save_thread.start()
            self.status2.setText('GPS 데이터 저장중')

    def stop_process(self):
        # 실행 중인 프로세스가 있는 경우에만 종료
        if self.process_thread is not None:
            self.process_thread.stop()
            self.process_thread.wait()
            self.process_thread = None
            self.status1.setText('GPS 데이터 전송 멈춤')
        if self.process_save_thread is not None:
            self.process_save_thread.stop()
            self.process_save_thread.wait()
            self.process_save_thread = None
            self.status2.setText('GPS 데이터 저장 멈춤')

    def start_process2(self, input1):
        # 실행 중인 프로세스가 없는 경우에만 실행
        if self.process2_thread is None or not self.process2_thread.isRunning():
#             command = 'cvlc rtsp://192.168.1.101:554/h264 --sout=file/mp4:/home/keti-laptop/비디오/{}'.format(input1)
            command = 'cvlc rtsp://192.168.1.101:554/h264 --sout=file/avi:/home/keti-laptop/비디오/{}.avi'.format(input1)
            self.process2_thread = subprocess.Popen(command, shell=True)
            self.status3.setText('영상 저장중')

    def stop_process2(self):
        # 실행 중인 프로세스가 있는 경우에만 종료
        print("rtp 전송 멈춤")
        if self.process2_thread is not None:
            for child in psutil.Process(self.process2_thread.pid).children(recursive=True):
                    child.kill()
            self.process2_thread.kill()
            self.process2_thread.wait()
            self.process2_thread = None
            self.status3.setText('영상 저장 멈춤')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())