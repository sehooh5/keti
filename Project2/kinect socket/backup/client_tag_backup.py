import socket
import cv2
import pickle
import struct


ip = '123.214.186.231'  # ip 주소
port = 8080  # port 번호

# 소켓 객체를 생성 및 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
print('연결 성공')

data = b""  # 수신한 데이터를 넣을 변수
payload_size = struct.calcsize(">L 282s")

while True:
    client_socket.send('0'.encode())
    # 프레임 수신
    while len(data) < payload_size:
        data += client_socket.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]

    # size data
    msg_size = struct.unpack(">L 282s", packed_msg_size)[0]
    # text data
    msg_text = struct.unpack(">L 282s", packed_msg_size)[1]
    msg_text = msg_text.split(b'<text>')[1]  # <text> 구분자로 내용만 추출
    msg_text = msg_text.decode()
    print(msg_text)

    while len(data) < msg_size:
        data += client_socket.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    # frame_data = frame_data.split(b'<png>')[1]  # <png> 구분자로 내용만 추출
    print("(CL)Frame Size : {}".format(msg_size))  # 프레임 크기 출력

    # 역직렬화(de-serialization) : 직렬화된 파일이나 바이트를 원래의 객체로 복원하는 것
    # 직렬화되어 있는 binary file로 부터 객체로 역직렬화
    frame = pickle.loads(frame_data.split(b'<png>')[
                         1], fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)  # 프레임 디코딩

    # 영상 출력
    cv2.imshow('TCP_Frame_Socket', frame)

    # 1초 마다 키 입력 상태를 받음
    if cv2.waitKey(1) == ord('q'):  # q를 누르면 client 만 종료
        client_socket.send('1'.encode())
        client_socket.shutdown(socket.SHUT_WR)
    elif cv2.waitKey(1) == ord('x'):  # x를 누르면 둘 다 종료
        client_socket.send('2'.encode())
        client_socket.shutdown(socket.SHUT_WR)
