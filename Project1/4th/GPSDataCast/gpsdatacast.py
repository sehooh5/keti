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
        self.title = 'Blackbox & GPS with Gyro'
        self.left = 10
        self.top = 10
        self.width = 450
        self.height = 450
        self.process1_thread = None
        self.process2_thread = None
        self.process3_thread = None
        self.process4_thread = None
        self.process5_thread = None
        self.process6_thread = None
        self.process7_thread = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # GPS 데이터
        # 제목
        title = QLabel('영상 및 GPS 데이터 전송', self)
        title.move(95, 10)
        for num in range(1,8):
            print(num)
        # 1번 영상 RTP 전송
        self.status1 = QLabel('blackbox_01 전송 멈춤', self)
        self.status1.move(50, 55)

        # 1번 영상 RTP 전송 버튼
        start1 = QPushButton('전송', self)
        start1.setToolTip('blackbox_01 RTP 전송')
        start1.move(220, 50)
        start1.clicked.connect(lambda: self.start_process(1))

        # 1번 영상 멈춤 버튼
        stop1 = QPushButton('멈춤', self)
        stop1.setToolTip('blackbox_01 RTP 전송 멈춤')
        stop1.move(305, 50)
        stop1.clicked.connect(lambda: self.stop_process(1))


        self.show()


    def start_process(self, num):
        print("rtp 전송 시작")
        process_thread = getattr(self, f"process{num}_thread")
        if process_thread is None or not process_thread.isRunning():
            command = f'cvlc -vvv /media/keti-laptop/T7/blackbox_0{num} --sout "#rtp{{dst=123.214.186.162,port=500{num},mux=ts}}" --loop --no-sout-all'
            process_thread = subprocess.Popen(command, shell=True)
            setattr(self, f"process{num}_thread", process_thread)
            status_label = getattr(self, f"status{num}")
            status_label.setText(f'blackbox_0{num} RTP 전송중')

    def stop_process(self, num):
        # 실행 중인 프로세스가 있는 경우에만 종료
        print("rtp 전송 멈춤")
        process_thread = getattr(self, f"process{num}_thread")
        if process_thread is not None:
            for child in psutil.Process(process_thread.pid).children(recursive=True):
                child.kill()
            process_thread.kill()
            process_thread.wait()
            setattr(self, f"process{num}_thread", None)
            status_label = getattr(self, f"status{num}")
            status_label.setText(f'blackbox_0{num} RTP 전송 멈춤')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())