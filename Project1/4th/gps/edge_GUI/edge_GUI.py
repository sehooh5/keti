from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QThread
import subprocess
import os
import sys
import psutil
import signal

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
        self.title = 'RTP converter'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 450
        self.process_thread = None
        self.process2_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # rtp to rtsp
        # 제목
        title = QLabel('RTP to RTSP 재전송', self)
        title.move(95, 10)

        # 입력창 4
        input4 = QLineEdit(self)
        input4.setPlaceholderText('RTP 주소')
        input4.move(50, 50)
        input4.resize(300, 25)

        # 입력창 4
        input5 = QLineEdit(self)
        input5.setPlaceholderText('RTSP 주소')
        input5.move(50, 90)
        input5.resize(300, 25)

        # 재전송 시작 버튼
        btn1 = QPushButton('재전송', self)
        btn1.setToolTip('rtp to rtsp 재전송 시작')
        btn1.move(50, 130)
        btn1.clicked.connect(lambda: self.start_rtsp_process(input4.text(), input5.text()))

        # RTSP 재전송 상태 표시 # 추가
        self.status1 = QLabel('RTSP 재전송 멈춤', self)
        self.status1.move(250, 130)

        # 멈춤 버튼
        btn2 = QPushButton('멈춤', self)
        btn2.setToolTip('rtp to rtsp 재전송 종료')
        btn2.move(150, 130)
        btn2.clicked.connect(self.stop_rtsp_process)

        # rtp 저장 기능
        # 제목
        title = QLabel('RTP 영상 데이터 저장', self)
        title.move(95, 200)

        # 입력창 1
        input1 = QLineEdit(self)
        input1.setPlaceholderText('RTP 입력 주소')
        input1.move(50, 230)
        input1.resize(300, 25)

        # 입력창 2
        input2 = QLineEdit(self)
        input2.setPlaceholderText('파일 저장 경로')
        input2.move(50, 270)
        input2.resize(300, 25)

        # 입력창 3
        input3 = QLineEdit(self)
        input3.setPlaceholderText('파일명')
        input3.move(50, 310)
        input3.resize(300, 25)

        # 실행 버튼
        btn4 = QPushButton('실행', self)
        btn4.setToolTip('저장 실행')
        btn4.move(50, 350)
        btn4.clicked.connect(lambda: self.start_save_rtp_process(input1.text(), input2.text(), input3.text()))

        # RTSP 재전송 상태 표시 # 추가
        self.status2 = QLabel('RTP 영상 저장 멈춤', self)
        self.status2.move(250, 350)

        # 멈춤 버튼
        btn5 = QPushButton('멈춤', self)
        btn5.setToolTip('저장 종료')
        btn5.move(150, 350)
        btn5.clicked.connect(self.stop_save_rtp_process)
        self.show()

    def start_rtsp_process(self, input4, input5):
        # 실행 중인 프로세스가 없는 경우에만 실행
        if self.process_thread is None or not self.process_thread.isRunning():
            command = 'cvlc -vvv rtp://123.214.186.162:5005 --sout="#rtp{sdp=rtsp://:8555/videoMain}" --no-sout-all --sout-keep'
#             command = 'cvlc -vvv {} --sout="#rtp{{sdp={}}}" --no-sout-all --sout-keep'.format(input4, input5)
            self.process_thread = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
            self.status1.setText('RTSP 재전송중')

    def stop_rtsp_process(self):
        # 실행 중인 프로세스가 있는 경우에만 종료
        if self.process_thread is not None:
            os.killpg(os.getpgid(self.process_thread.pid), signal.SIGTERM)
            self.process_thread.wait()
            self.process_thread = None
            self.status1.setText('RTSP 재전송 멈춤')

    def start_save_rtp_process(self, input1, input2, input3):
        # 실행 중인 프로세스가 없는 경우에만 실행
        if self.process2_thread is None or not self.process2_thread.isRunning():
#             command = 'cvlc {}  --sout=file/ps:{}{}'.format(input1, input2, input3)
            command = 'cvlc rtp://123.214.186.162:5005 --sout=file/ps:/home/keti0/비디오/blackbox_test6.mp4'
            self.process2_thread = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
            self.status2.setText('RTP 영상 저장중')

    def stop_save_rtp_process(self):
        # 실행 중인 프로세스가 있는 경우에만 종료
        if self.process2_thread is not None:
            os.killpg(os.getpgid(self.process2_thread.pid), signal.SIGTERM)
            self.process2_thread.wait()
            self.process2_thread = None
            self.status2.setText('RTP 영상 저장 멈춤')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())