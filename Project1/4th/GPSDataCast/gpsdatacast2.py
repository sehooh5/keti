from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QThread
import subprocess
import os
import sys
import psutil

from flask import Flask, render_template, Response, request, g, jsonify
from flask_cors import CORS, cross_origin
import json
import sqlite3
import time
import requests
from threading import Thread

from PyQt5.QtCore import QThread, pyqtSignal

url = "http://123.214.186.162:8089"

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

class GPSThread(QThread):
    data_ready = pyqtSignal(dict)

    def __init__(self, num):
        super().__init__()
        self.num = num
        self.running = False

    def run(self):
        self.running = True

        conn = sqlite3.connect(f"gps_0{self.num}.db", isolation_level=None, check_same_thread=False)
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM gps_raw_data")
        for row in c:
            cnt = row[0]

        while self.running:
            for cnt in range(1, cnt + 1):
                if cnt == 1:
                    print("데이터 초기화")
                c.execute(f"SELECT * FROM gps_raw_data WHERE ROWID={cnt}")
                for row in c:
                    data = {
                        "code": "0000",
                        "message": "처리 성공",
                        "bid": row[0],
                        "time": row[1],
                        "gps_raw_data": row[2]
                    }
                    self.data_ready.emit(data)

                time.sleep(0.5)

    def stop(self):
        self.running = False


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.running = False
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
        self.gps_thread = None

        # 제목
        title = QLabel('영상 및 GPS 데이터 전송', self)
        title.move(95, 10)

        # 1번 영상 전송
        self.status1 = QLabel('blackbox_01 전송 멈춤', self)
        self.status1.move(50, 50)

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

        # 2번 영상 전송
        self.status2 = QLabel('blackbox_02 전송 멈춤', self)
        self.status2.move(50, 100)

        # 2번 영상 RTP 전송 버튼
        start2 = QPushButton('전송', self)
        start2.setToolTip('blackbox_02 RTP 전송')
        start2.move(220, 100)
        start2.clicked.connect(lambda: self.start_process(2))

        # 2번 영상 멈춤 버튼
        stop2 = QPushButton('멈춤', self)
        stop2.setToolTip('blackbox_02 RTP 전송 멈춤')
        stop2.move(305, 100)
        stop2.clicked.connect(lambda: self.stop_process(2))

        # 3번 영상 전송
        self.status3 = QLabel('blackbox_03 전송 멈춤', self)
        self.status3.move(50, 150)

        # 3번 영상 RTP 전송 버튼
        start3 = QPushButton('전송', self)
        start3.setToolTip('blackbox_03 RTP 전송')
        start3.move(220, 150)
        start3.clicked.connect(lambda: self.start_process(3))

        # 3번 영상 멈춤 버튼
        stop3 = QPushButton('멈춤', self)
        stop3.setToolTip('blackbox_03 RTP 전송 멈춤')
        stop3.move(305, 150)
        stop3.clicked.connect(lambda: self.stop_process(3))

        # 4번 영상 전송
        self.status4 = QLabel('blackbox_04 전송 멈춤', self)
        self.status4.move(50, 200)

        # 4번 영상 RTP 전송 버튼
        start4 = QPushButton('전송', self)
        start4.setToolTip('blackbox_04 RTP 전송')
        start4.move(220, 200)
        start4.clicked.connect(lambda: self.start_process(4))

        # 4번 영상 멈춤 버튼
        stop4 = QPushButton('멈춤', self)
        stop4.setToolTip('blackbox_04 RTP 전송 멈춤')
        stop4.move(305, 200)
        stop4.clicked.connect(lambda: self.stop_process(4))

        # 5번 영상 전송
        self.status5 = QLabel('blackbox_05 전송 멈춤', self)
        self.status5.move(50, 250)

        # 5번 영상 RTP 전송 버튼
        start5 = QPushButton('전송', self)
        start5.setToolTip('blackbox_05 RTP 전송')
        start5.move(220, 250)
        start5.clicked.connect(lambda: self.start_process(5))

        # 5번 영상 멈춤 버튼
        stop5 = QPushButton('멈춤', self)
        stop5.setToolTip('blackbox_05 RTP 전송 멈춤')
        stop5.move(305, 250)
        stop5.clicked.connect(lambda: self.stop_process(5))

        # 6번 영상 전송
        self.status6 = QLabel('blackbox_06 전송 멈춤', self)
        self.status6.move(50, 300)

        # 6번 영상 RTP 전송 버튼
        start6 = QPushButton('전송', self)
        start6.setToolTip('blackbox_06 RTP 전송')
        start6.move(220, 300)
        start6.clicked.connect(lambda: self.start_process(6))

        # 6번 영상 멈춤 버튼
        stop6 = QPushButton('멈춤', self)
        stop6.setToolTip('blackbox_06 RTP 전송 멈춤')
        stop6.move(305, 300)
        stop6.clicked.connect(lambda: self.stop_process(6))

        # 7번 영상 전송
        self.status7 = QLabel('blackbox_07 전송 멈춤', self)
        self.status7.move(50, 350)

        # 7번 영상 RTP 전송 버튼
        start7 = QPushButton('전송', self)
        start7.setToolTip('blackbox_07 RTP 전송')
        start7.move(220, 350)
        start7.clicked.connect(lambda: self.start_process(7))

        # 7번 영상 멈춤 버튼
        stop7 = QPushButton('멈춤', self)
        stop7.setToolTip('blackbox_07 RTP 전송 멈춤')
        stop7.move(305, 350)
        stop7.clicked.connect(lambda: self.stop_process(7))

        self.show()



    def start_process(self, num):
        self.running = True

        # GPS 데이터 전송을 위한 스레드 시작
        self.gps_thread = GPSThread(num)
        self.gps_thread.data_ready.connect(self.send_gps_data)
        self.gps_thread.start()

        # 영상 데이터 전송
        print(f"blackbox_0{num} rtp 전송 시작")
        process_thread = getattr(self, f"process{num}_thread")
        if process_thread is None or not process_thread.isRunning():
            command = f'cvlc -vvv /media/keti-laptop/T7/blackbox_0{num}.avi --sout "#rtp{{dst=123.214.186.162,port=500{num},mux=ts}}" --loop --no-sout-all'
            process_thread = subprocess.Popen(command, shell=True)
            setattr(self, f"process{num}_thread", process_thread)
            status_label = getattr(self, f"status{num}")
            status_label.setText(f'blackbox_0{num} RTP 전송중')

    def stop_process(self, num):
        # 실행 중인 프로세스가 있는 경우에만 종료
        print(f"blackbox_0{num} rtp 전송 멈춤")
        self.running = False
        process_thread = getattr(self, f"process{num}_thread")
        if process_thread is not None:
            for child in psutil.Process(process_thread.pid).children(recursive=True):
                child.kill()
            process_thread.kill()
            process_thread.wait()
            setattr(self, f"process{num}_thread", None)
            status_label = getattr(self, f"status{num}")
            status_label.setText(f'blackbox_0{num} RTP 전송 멈춤')
            status_label.repaint()

        if self.gps_thread is not None:
        self.gps_thread.stop()
        self.gps_thread.wait()

    def send_gps_data(self, data):
        requests.post(f'{url}/gwg_temp', json=data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())





#     def start_process(self, num):
#         self.running = True
#
#         # gps 데이터 전송
#         gps_thread = Thread(target=self.send_gps_data, args=(num,))
#         gps_thread.start()
#
#         # 영상 데이터 전송
#         video_thread = Thread(target=self.send_video_data, args=(num,))
#         video_thread.start()
#
#     def send_gps_data(self, num):
#         self.process_thread = ProcessThread(cmd="")
#         self.process_thread.isRunning = True  # isRunning 값을 True로 설정
#
#         conn = sqlite3.connect(f"gps_0{num}.db", isolation_level=None, check_same_thread=False)
#         c = conn.cursor()
#
#         c.execute("SELECT COUNT(*) FROM gps_raw_data")
#         for row in c:
#             cnt = row[0]
#         print(num)
#
#         while True:
#             if not self.running:
#                 break
#
#             for cnt in range(1, cnt+1):
#                 if cnt == 1:
#                     print("데이터 초기화")
#                 c.execute(f"SELECT * FROM gps_raw_data WHERE ROWID={cnt}")
#                 for row in c:
#                     print(f'{row[0]}, {row[1]}, {row[2]}')
#                     data = {
#                         "code": "0000",
#                         "message": "처리 성공",
#                         "bid": row[0],
#                         "time": row[1],
#                         "gps_raw_data": row[2]
#                     }
#                     requests.post(f'{url}/gwg_temp', json=data)
#
#                 time.sleep(0.5)
#
#     def send_video_data(self, num):
#         print(f"blackbox_0{num} rtp 전송 시작")
#         process_thread = getattr(self, f"process{num}_thread")
#         if process_thread is None or not process_thread.isRunning:
#             command = f'cvlc -vvv /media/keti-laptop/T7/blackbox_0{num}.avi --sout "#rtp{{dst=123.214.186.162,port=500{num},mux=ts}}" --loop --no-sout-all'
#             process_thread = subprocess.Popen(command, shell=True)
#             setattr(self, f"process{num}_thread", process_thread)
#             status_label = getattr(self, f"status{num}")
#             status_label.setText(f'blackbox_0{num} RTP 전송중')