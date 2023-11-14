from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QThread
import subprocess
import os
import sys
import psutil

# from flask import Flask, render_template, Response, request, g, jsonify
# from flask_cors import CORS, cross_origin
# import json
# import sqlite3
# import datetime
# import res
#
# flask_app = Flask(__name__)
# CORS(flask_app)
# port = 8089

class ProcessThread(QThread):
    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        self.process = None
        self.isRunning = False

    def run(self):
        self.process = subprocess.Popen(self.cmd)
        self.isRunning = True
        self.process.wait()
        self.isRunning = False

    def stop(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            self.isRunning = False

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Blackbox & GPS with Gyro'
        self.left = 10
        self.top = 10
        self.width = 450
        self.height = 480
        self.process1_thread = None
        self.process2_thread = None
        self.process3_thread = None
        self.process4_thread = None
        self.process5_thread = None
        self.process6_thread = None
        self.process7_thread = None
        self.process8_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 제목
        title = QLabel('영상 및 GPS 데이터 재전송', self)
        title.move(95, 10)

        # 1번 영상 전송
        self.status1 = QLabel('blackbox_01 재전송 멈춤', self)
        self.status1.move(50, 50)

        # 1번 영상 RTP 전송 버튼
        start1 = QPushButton('전송', self)
        start1.setToolTip('blackbox_01 RTSP 전송')
        start1.move(220, 50)
        start1.clicked.connect(lambda: self.start_process(1))

        # 1번 영상 멈춤 버튼
        stop1 = QPushButton('멈춤', self)
        stop1.setToolTip('blackbox_01 재전송 멈춤')
        stop1.move(305, 50)
        stop1.clicked.connect(lambda: self.stop_process(1))

        # 2번 영상 전송
        self.status2 = QLabel('blackbox_02 재전송 멈춤', self)
        self.status2.move(50, 100)

        # 2번 영상 RTP 전송 버튼
        start2 = QPushButton('전송', self)
        start2.setToolTip('blackbox_02 RTSP 전송')
        start2.move(220, 100)
        start2.clicked.connect(lambda: self.start_process(2))

        # 2번 영상 멈춤 버튼
        stop2 = QPushButton('멈춤', self)
        stop2.setToolTip('blackbox_02 재전송 멈춤')
        stop2.move(305, 100)
        stop2.clicked.connect(lambda: self.stop_process(2))

        # 3번 영상 전송
        self.status3 = QLabel('blackbox_03 재전송 멈춤', self)
        self.status3.move(50, 150)

        # 3번 영상 RTSP 전송 버튼
        start3 = QPushButton('전송', self)
        start3.setToolTip('blackbox_03 RTSP 전송')
        start3.move(220, 150)
        start3.clicked.connect(lambda: self.start_process(3))

        # 3번 영상 멈춤 버튼
        stop3 = QPushButton('멈춤', self)
        stop3.setToolTip('blackbox_03 재전송 멈춤')
        stop3.move(305, 150)
        stop3.clicked.connect(lambda: self.stop_process(3))

        # 4번 영상 전송
        self.status4 = QLabel('blackbox_04 재전송 멈춤', self)
        self.status4.move(50, 200)

        # 4번 영상 RTSP 전송 버튼
        start4 = QPushButton('전송', self)
        start4.setToolTip('blackbox_04 RTSP 전송')
        start4.move(220, 200)
        start4.clicked.connect(lambda: self.start_process(4))

        # 4번 영상 멈춤 버튼
        stop4 = QPushButton('멈춤', self)
        stop4.setToolTip('blackbox_04 재전송 멈춤')
        stop4.move(305, 200)
        stop4.clicked.connect(lambda: self.stop_process(4))

        # 5번 영상 전송
        self.status5 = QLabel('blackbox_05 재전송 멈춤', self)
        self.status5.move(50, 250)

        # 5번 영상 RTSP 전송 버튼
        start5 = QPushButton('전송', self)
        start5.setToolTip('blackbox_05 RTSP 전송')
        start5.move(220, 250)
        start5.clicked.connect(lambda: self.start_process(5))

        # 5번 영상 멈춤 버튼
        stop5 = QPushButton('멈춤', self)
        stop5.setToolTip('blackbox_05 재전송 멈춤')
        stop5.move(305, 250)
        stop5.clicked.connect(lambda: self.stop_process(5))

        # 6번 영상 전송
        self.status6 = QLabel('blackbox_06 재전송 멈춤', self)
        self.status6.move(50, 300)

        # 6번 영상 RTSP 전송 버튼
        start6 = QPushButton('전송', self)
        start6.setToolTip('blackbox_06 RTSP 전송')
        start6.move(220, 300)
        start6.clicked.connect(lambda: self.start_process(6))

        # 6번 영상 멈춤 버튼
        stop6 = QPushButton('멈춤', self)
        stop6.setToolTip('blackbox_06 재전송 멈춤')
        stop6.move(305, 300)
        stop6.clicked.connect(lambda: self.stop_process(6))

        # 7번 영상 전송
        self.status7 = QLabel('blackbox_07 재전송 멈춤', self)
        self.status7.move(50, 350)

        # 7번 영상 RTSP 전송 버튼
        start7 = QPushButton('전송', self)
        start7.setToolTip('blackbox_07 RTSP 전송')
        start7.move(220, 350)
        start7.clicked.connect(lambda: self.start_process(7))

        # 7번 영상 멈춤 버튼
        stop7 = QPushButton('멈춤', self)
        stop7.setToolTip('blackbox_07 재전송 멈춤')
        stop7.move(305, 350)
        stop7.clicked.connect(lambda: self.stop_process(7))

        # 8번 영상 전송
        self.status8 = QLabel('blackbox_08 재전송 멈춤', self)
        self.status8.move(50, 400)

        # 8번 영상 RTSP 전송 버튼
        start8 = QPushButton('전송', self)
        start8.setToolTip('blackbox_08 RTSP 전송')
        start8.move(220, 400)
        start8.clicked.connect(lambda: self.start_process(8))

        # 8번 영상 멈춤 버튼
        stop8 = QPushButton('멈춤', self)
        stop8.setToolTip('blackbox_08 재전송 멈춤')
        stop8.move(305, 400)
        stop8.clicked.connect(lambda: self.stop_process(8))

        self.show()


    def start_process(self, num):
        print(f"blackbox_0{num} RTSP 전송 시작")
        process_thread = getattr(self, f"process{num}_thread")
        if process_thread is None or not process_thread.isRunning():
#             command = f'cvlc -vvv rtp://123.214.186.162:500{num} --sout="#rtp{{sdp=rtsp://123.214.186.162:800{num}/videoMain}}" --no-sout-all --sout-keep' # 외부망
#             command = f'cvlc -vvv rtp://192.168.0.54:500{num} --sout="#rtp{{sdp=rtsp://192.168.0.54:800{num}/videoMain}}" --no-sout-all --sout-keep' # 내부망
            command = f'cvlc -vvv rtp://192.168.0.54:500{num} --sout="#rtp{{sdp=rtsp://192.168.0.54:800{num}/videoMain}}" --no-sout-all --sout-keep' # 싱크 테스트
            process_thread = subprocess.Popen(command, shell=True)
            setattr(self, f"process{num}_thread", process_thread)
            status_label = getattr(self, f"status{num}")
            status_label.setText(f'blackbox_0{num} 재전송중')

    def stop_process(self, num):
        # 실행 중인 프로세스가 있는 경우에만 종료
        print(f"blackbox_0{num} rtsp 재전송 멈춤")
        process_thread = getattr(self, f"process{num}_thread")
        if process_thread is not None:
            for child in psutil.Process(process_thread.pid).children(recursive=True):
                child.kill()
            process_thread.kill()
            process_thread.wait()
            setattr(self, f"process{num}_thread", None)
            status_label = getattr(self, f"status{num}")
            status_label.setText(f'blackbox_0{num} 재전송 멈춤')
            status_label.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


# @flask_app.route('/gwg_temp', methods=['POST'])
# def gwg_temp():
#     global bb01, bb02, bb03, bb04, bb05, bb06, bb07
#
#     temp_data = json.loads(request.get_json(silent=True))
#
#     bid = temp_data.get('bid')
#
#     if bid == 'bb01':
#         bb01 = temp_data
#     elif bid == 'bb02':
#         bb02 = temp_data
#     elif bid == 'bb03':
#         bb03 = temp_data
#     elif bid == 'bb04':
#         bb04 = temp_data
#     elif bid == 'bb05':
#         bb05 = temp_data
#     elif bid == 'bb06':
#         bb06 = temp_data
#     elif bid == 'bb07':
#         bb07 = temp_data
#
#     return temp_data
#
# @flask_app.route('/get_gps_rdata', methods=['GET'])
# def get_get_gps_rdata():
#     global bb01, bb02, bb03, bb04, bb05, bb06, bb07
#
#     try:
#         bid = request.args['bid']
#         if bid == 'bb01':
#             if 'bb01' in globals() and bb01:
#                 return json.dumps(bb01)
#             else:
#                 return res.msg("0020")
#         elif bid == 'bb02':
#             if 'bb02' in globals() and bb02:
#                 return json.dumps(bb02)
#             else:
#                 return res.msg("0020")
#         elif bid == 'bb03':
#             if 'bb03' in globals() and bb03:
#                 return json.dumps(bb03)
#             else:
#                 return res.msg("0020")
#         elif bid == 'bb04':
#             if 'bb04' in globals() and bb04:
#                 return json.dumps(bb04)
#             else:
#                 return res.msg("0020")
#         elif bid == 'bb05':
#             if 'bb05' in globals() and bb05:
#                 return json.dumps(bb05)
#             else:
#                 return res.msg("0020")
#         elif bid == 'bb06':
#             if 'bb06' in globals() and bb06:
#                 return json.dumps(bb06)
#             else:
#                 return res.msg("0020")
#         elif bid == 'bb07':
#             if 'bb07' in globals() and bb07:
#                 return json.dumps(bb07)
#             else:
#                 return res.msg("0020")
#         else:
#             return res.msg("0020")
#     except KeyError:
#         return res.msg("0015")
#
#     return res.msg("0012")
#
# flask_app.run(host="123.214.186.162",port=port)