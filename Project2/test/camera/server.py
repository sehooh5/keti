import socket
import cv2
import numpy
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
            # queue 는 선입 선출하는, ljust 는 왼쪽 정렬
            stringData = queue.get()
            client_socket.send(str(len(stringData)).ljust(16).encode())
            client_socket.send(stringData)

        except ConnectionResetError as e:

            print('Disconnected by ' + addr[0], ':', addr[1])
            break

    client_socket.close()


# 영상을 출력하는 함수
def webcam(queue):
    # OpenCV 를 사용해 캡쳐
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()

        if ret == False:
            continue
        # 인코딩 설정 : cv2.IMWRITE_JPEG_QUALITY 는 이미지 퀄리티 설정 0-100
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        # cv2.imencode : img encoding 하는 함수
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)

        # numpy.array() 는 행렬로 만들어주는 함수
        data = numpy.array(imgencode)
        stringData = data.tostring()  # 행렬을 string으로 변환

        queue.put(stringData)

        # imshow는 이미지 출력하는 함수
        cv2.imshow('image', frame)

        # key 값을 대기한하는 함수 waitKey(1)
        key = cv2.waitKey(1)
        if key == 27:  # ascii code 27 = ESC
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
