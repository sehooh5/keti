import cv2
import socket
import struct
import pickle
import numpy as np
import utils_PyKinectV2 as utils
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime


ip = '127.0.0.1'  # ip 주소
port = 50001  # port 번호

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓 객체를 생성
server_socket.bind((ip, port))  # 바인드(bind) : 소켓에 주소, 프로토콜, 포트를 할당
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
color_width, color_height = kinect.color_frame_desc.Width, kinect.color_frame_desc.Height
# print(type(kinect.color_frame_desc.Width))


# 인코드 파라미터
# jpg의 경우 cv2.IMWRITE_JPEG_QUALITY를 이용하여 이미지의 품질을 설정
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]

while True:
    if kinect.has_new_color_frame() and \
            kinect.has_new_depth_frame():
        # data
        # streaming data
        color_frame = kinect.get_last_color_frame()
        depth_frame = kinect.get_last_depth_frame()
        # text data
        text = 'TEXT' + '//'
        text_len = str(len(text))
        format = f'>L {text_len}s'

        # data 정제
        color_img = color_frame.reshape(
            ((color_height, color_width, 4))).astype(np.uint8)

        # data Resize (1080, 1920, 4) into half (540, 960, 4)
        color_img_resize = cv2.resize(color_img, (0, 0), fx=0.5, fy=0.5)

        # depth_img = depth_frame.reshape(
        #     ((depth_height, depth_width))).astype(np.uint16)

        result, color_frame = cv2.imencode(
            '.png', color_img_resize, encode_param)
        # print(color_frame)
        data = pickle.dumps(color_frame, 0)
        size = len(data)
        size_str = "//"+str(size) + "//"
        print("Frame Size : ", size)

        # 데이터(프레임) 전송
        # client_conn.sendall(struct.pack(">L", size) + data)
        client_conn.sendall(size_str.encode() + text.encode() + data)
