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
import threading

from PyQt5.QtCore import QThread, pyqtSignal

import traceback

username = os.getlogin()

# url = "http://123.214.186.162:8089" # 기존 무선 주소
# url = "http://192.168.0.54:8089" # 내부망 주소
url = "http://192.168.0.14:8089" # 싱크 및 영상 추가 주소

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


        # 8번 = 고정형 CCTV
        if self.num == 8:
            while self.running:
                data = {
                            "code": "0000",
                            "message": "처리 성공",
                            "bid": f"bb0{self.num}",
                            "data": {
                                "time": {
                                    "yy": "23", "mm": "11", "dd": "13", "hh": "00", "mi": "00", "ss": "00", "ms": "00"
                                },
                                "acceleration": {
                                    "ax": "0.0", "ay": "0.0", "az": "0.0"
                                },
                                "angular": {
                                    "wx": "0.0", "wy": "0.0", "wz": "0.0"
                                },
                                "angle": {
                                    "roll": "0.0", "pitch": "0.0", "yaw": "0.0"
                                },
                                "magnetic": {
                                    "mx": "0.0", "my": "0.0", "mz": "0.0"
                                },
                                "atmospheric": {
                                     "press": "0.0", "h": "0.0"
                                },
                                "gps": {
                                    "lat": "37.1487", "lon": "127.0773"
                                },
                                "groundspeed": {
                                    "gh": "0.0", "gy": "0.0", "gv": "0.0"
                                },
                                "quaternion": {
                                    "q0": "0.0", "q1": "0.0", "q2": "0.0", "q3": "0.0"
                                },
                                "satellite": {
                                    "snum": "0.0", "pdop": "0.0", "hdop": "0.0", "vdop": "0.0"
                                }
                            }
                        }
                json_data = json.dumps(data)
                response = requests.post(f'{url}/gwg_temp2', json=json_data)
                time.sleep(0.5)
        else:
            print("print num : ", self.num, " 여기로 들어옴")
            gps_num = f'gps_0{self.num}'
            conn = sqlite3.connect(f"gps_parsed.db", isolation_level=None, check_same_thread=False)
            c = conn.cursor()

            c.execute(f"SELECT COUNT(*) FROM {gps_num}")
            for row in c:
                cnt = row[0]

            while self.running:
                for cnt in range(1, cnt + 1):
                    if not self.running:  # 추가: self.running이 False인 경우 루프 종료
                        break

                    if cnt == 1:
                        print("데이터 초기화")
                    c.execute(f"SELECT * FROM {gps_num} WHERE ROWID={cnt}")
                    for row in c:
                        try:
    #                         yy, mm, dd, hh, mi, ss, ms = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
    #                         ax, ay, az, wx, wy, wz = row[7], row[8], row[9], row[10], row[11], row[12]
    #                         roll, pitch, yaw, mx, my, mz = row[13], row[14], row[15], row[16], row[17], row[18]
    #                         press, h, lat, lon, gh, gy, gv = row[19], row[20], row[21], row[22], row[23], row[24], row[25]
    #                         q0, q1, q2, q3, snum, pdop, hdop, vdop = row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33]

                            data = {
                                "code": "0000",
                                "message": "처리 성공",
                                "bid": f"bb0{self.num}",
                                "data": {
                                    "time": {
                                        "yy": row[0], "mm": row[1], "dd": row[2], "hh": row[3], "mi": row[4], "ss": row[5], "ms": row[6]
                                    },
                                    "acceleration": {
                                        "ax": row[7], "ay": row[8], "az": row[9]
                                    },
                                    "angular": {
                                        "wx": row[10], "wy": row[11], "wz": row[12]
                                    },
                                    "angle": {
                                        "roll": row[13], "pitch": row[14], "yaw": row[15]
                                    },
                                    "magnetic": {
                                        "mx": row[16], "my": row[17], "mz": row[18]
                                    },
                                    "atmospheric": {
                                         "press": row[19], "h": row[20]
                                    },
                                    "gps": {
                                        "lat": row[21], "lon": row[22]
                                    },
                                    "groundspeed": {
                                        "gh": row[23], "gy": row[24], "gv": row[25]
                                    },
                                    "quaternion": {
                                        "q0": row[26], "q1": row[27], "q2": row[28], "q3": row[29]
                                    },
                                    "satellite": {
                                        "snum": row[30], "pdop": row[31], "hdop": row[32], "vdop": row[33]
                                    }
                                }
                            }
                            json_data = json.dumps(data)
                            # JSON 데이터를 서버로 전송
                            response = requests.post(f'{url}/gwg_temp2', json=json_data)

                        except Exception as e:
                            print("JSON 데이터 전송 중 오류 발생")
                            traceback.print_exc()

                    time.sleep(0.5)


    def stop(self):
        self.running = False

# 싱크 테스트 추가내용
    def restart(self):
        self.start()


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.running = False
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
        self.gps_thread = None

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

        # 8번 영상 전송
        self.status8 = QLabel('blackbox_08 전송 멈춤', self)
        self.status8.move(50, 400)

        # 8번 영상 RTP 전송 버튼
        start8 = QPushButton('전송', self)
        start8.setToolTip('blackbox_08 RTP 전송')
        start8.move(220, 400)
        start8.clicked.connect(lambda: self.start_process(8))

        # 8번 영상 멈춤 버튼
        stop8 = QPushButton('멈춤', self)
        stop8.setToolTip('blackbox_08 RTP 전송 멈춤')
        stop8.move(305, 400)
        stop8.clicked.connect(lambda: self.stop_process(8))

        self.show()



    def start_process(self, num):
        self.running = True
        # GPS 데이터 전송을 위한 스레드 시작
        self.gps_thread = GPSThread(num)
        self.gps_thread.start()

        # 영상 데이터 전송
        print(f"blackbox_0{num} rtp 전송 시작")
        process_thread = getattr(self, f"process{num}_thread")

        if process_thread is None or not process_thread.isRunning():
            if num == 8:
#                 command = f'cvlc /home/{username}/blackbox_osan/blackbox_0{num}.mp4 --sout "#rtp{{dst=192.168.0.14,port=500{num},mux=ts}}" --loop --no-sout-all' # 싱크 테스트
                command = f'cvlc /home/{username}/blackbox_osan/blackbox_0{num}.mp4 --sout "#rtp{{dst=192.168.0.14,port=500{num},mux=ts}}" --no-sout-all' # 싱크 테스트
            else:
#                 command = f'cvlc /home/{username}/blackbox_osan/blackbox_0{num}.avi --sout "#rtp{{dst=192.168.0.14,port=500{num},mux=ts}}" --loop --no-sout-all' # 싱크 테스트
                command = f'cvlc /home/{username}/blackbox_osan/blackbox_0{num}.avi --sout "#rtp{{dst=192.168.0.14,port=500{num},mux=ts}}" --no-sout-all' # 싱크 테스트
            process_thread = ProcessThread(command)
            process_thread.finished_signal.connect(lambda: self.start_process_monitor(num))  # 연결
            setattr(self, f"process{num}_thread", process_thread)
            status_label = getattr(self, f"status{num}")
            status_label.setText(f'blackbox_0{num} RTP 전송중')
            process_thread.start()  # 스레드 시작


    def start_process_monitor(self, process, num):
        # 프로세스 종료 시 실행되는 코드
        print(f"파일 실행이 종료되었습니다: blackbox_0{num}")


    def stop_process(self, num):
        # 실행 중인 프로세스가 있는 경우에만 종료
        print(f"blackbox_0{num} rtp 전송 멈춤")

        # gps 종료
        if self.gps_thread is not None:
            self.gps_thread.stop()
            self.gps_thread.wait()
            self.gps_thread = None

        # 영상 종료
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

