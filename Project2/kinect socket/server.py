import cv2
import socket
import struct
import pickle
import numpy as np
import utils_PyKinectV2 as utils
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime

from queue import Queue
from _thread import *


enclosure_queue = Queue()

# 쓰레드 함수


def threaded(client_socket, addr, queue):

    print('Connected by :', addr[0], ':', addr[1])

    while True:

        try:
            data = client_socket.recv(1024)

            if not data:
                print('Disconnected by ' + addr[0], ':', addr[1])
                break

            stringData = queue.get()
            client_socket.send(str(len(stringData)).ljust(16).encode())
            client_socket.send(stringData)

        except ConnectionResetError as e:

            print('Disconnected by ' + addr[0], ':', addr[1])
            break

    client_socket.close()


def webcam(queue):

    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()

        if ret == False:
            continue

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)

        data = numpy.array(imgencode)
        stringData = data.tostring()

        queue.put(stringData)

        cv2.imshow('image', frame)

        key = cv2.waitKey(1)
        if key == 27:
            break


HOST = '127.0.0.1'
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

print('server start')

start_new_thread(webcam, (enclosure_queue,))


while True:

    print('wait')

    client_socket, addr = server_socket.accept()
    start_new_thread(threaded, (client_socket, addr, enclosure_queue,))

server_socket.close()


ip = '192.168.0.71'  # ip 주소
port = 50001  # port 번호
server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)  # 소켓 객체를 생성
server_socket.bind((ip, port))  # 바인드(bind) : 소켓에 주소, 프로토콜, 포트를 할당


def server():
    server_socket.listen(10)  # 연결 수신 대기 상태(리스닝 수(동시 접속) 설정)
    print('클라이언트 연결 대기')

    # 연결 수락(클라이언트 소켓 주소를 반환)
    client_conn, client_addr = server_socket.accept()
    print(client_addr)  # 클라이언트 주소 출력

    # 카메라 선택
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color |
                                             PyKinectV2.FrameSourceTypes_Depth)

    # Default: 512, 424
    depth_width, depth_height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height
    # Default: 1920, 1080
    #color_width, color_height = kinect.color_frame_desc.Width, kinect.color_frame_desc.Height

    # 인코드 파라미터
    # jpg의 경우 cv2.IMWRITE_JPEG_QUALITY를 이용하여 이미지의 품질을 설정
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
    while True:
        if kinect.has_new_color_frame() and \
                kinect.has_new_depth_frame():
            # streaming data
            #color_frame = kinect.get_last_color_frame()
            depth_frame = kinect.get_last_depth_frame()
            # text data
            text = """<text>Cam_Info_List
        -UID: camera0x11
        -Name: camera01
        -Type: 3D Depth Camera
        -Location: Underground Parking(B2)
        -Resolution: 512X424
        -FrameRate: 10fps
    Event_Info_List
        -StartTime: 2020:11:10:13:55:34
        -EndTime: 2020:11:10:13:55:39
        -EventID: 10<text>"""
            text = text.encode()

            # scolor_img = color_frame.reshape(((color_height, depth_width, 4))).astype(np.uint8)
            # data Resize (1080, 1920, 4) into half (540, 960, 4)
            #color_img_resize = cv2.resize(color_img, (0, 0), fx=0.5, fy=0.5)

            # data 정제
            depth_img = depth_frame.reshape(
                ((depth_height, depth_width))).astype(np.uint16)

            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
                depth_img, alpha=255/1500), cv2.COLORMAP_JET)

            # 프레임 데이터 정제
            result, depth_frame = cv2.imencode(
                '.jpg', depth_colormap, encode_param)
            data = "<jpg>".encode()+pickle.dumps(depth_frame, 0)+"<jpg>".encode()
            size = len(data)+len(text)
            print("Frame Size : ", size)

            # 데이터 전송
            client_conn.sendall(struct.pack(
                ">L", size) + text + data)
            msg = client_conn.recv(2).decode()
            print(msg)
            if msg == "1":  # client 만 종료하고 server 재 실행
                server()
            elif msg == "2":  # 모두 종료
                server_socket.shutdown(socket.SHUT_RDWR)
                client_conn.shutdown(socket.SHUT_WR)


server()
