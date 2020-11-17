import socket
import cv2
import pickle
import struct
import json
import numpy as np

ip = '127.0.0.1'  # ip 주소 '192.168.0.71'
port = 50001  # port 번호

# 소켓 객체를 생성 및 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
print('연결 성공')

data = b""  # 수신한 데이터를 넣을 변수
payload_size = struct.calcsize(">L 280s")  # = 8


while True:
    client_socket.send('0'.encode())

    data = client_socket.recv(4096)
    json_data = json.loads(data.decode())
    print(data.decode())
    size = json_data["size"]
    text = json_data["text"]
    frame = np.asarray(json_data["data"])

    print(size)
    print(text)
    # print(json_data["data"])
    #frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    # print(frame)
    cv2.imshow('TCP_Frame_Socket', frame)

    # # 프레임 수신
    # while len(data) < payload_size:
    #     data += client_socket.recv(4096)
    # packed_msg_size = data[:payload_size]
    # data = data[payload_size:]

    # # frame size 출력 : print(msg_size)
    # msg_size = struct.unpack(">L 280s", packed_msg_size)[0]
    # # 텍스트 출력 : print(msg_text)
    # msg_text = struct.unpack(">L 280s", packed_msg_size)[1].decode()
    # while len(data) < msg_size:
    #     data += client_socket.recv(4096)
    # frame_data = data[:msg_size]
    # data = data[msg_size:]
    # print("(CL)Frame Size : {}".format(msg_size))  # 프레임 크기 출력

    # 역직렬화(de-serialization) : 직렬화된 파일이나 바이트를 원래의 객체로 복원하는 것
    # 직렬화되어 있는 binary file로 부터 객체로 역직렬화
    # frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    # # print(frame)
    # frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)  # 프레임 디코딩

    # # 영상 출력
    # cv2.imshow('TCP_Frame_Socket', frame)

    # 1초 마다 키 입력 상태를 받음
    if cv2.waitKey(1) == ord('q'):  # q를 누르면 client 만 종료
        client_socket.send('1'.encode())
        client_socket.shutdown(socket.SHUT_WR)
    elif cv2.waitKey(1) == ord('x'):  # x를 누르면 둘 다 종료
        client_socket.send('2'.encode())
        client_socket.shutdown(socket.SHUT_WR)
