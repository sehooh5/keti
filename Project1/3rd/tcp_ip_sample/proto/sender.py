from socket import *
import threading
import time


def send(sock):
    sendData = b'1234$5678$message'
    sock.send(sendData)
    print(type(sock.send(sendData)))


def receive(sock):
    recvData = sock.recv(1024)
    print('상대방 :', recvData.decode('utf-8'))


port = 8080

sendSock = socket(AF_INET, SOCK_STREAM)
sendSock.connect(('127.0.0.1', port))

print('접속 완료')

sender = threading.Thread(target=send, args=(sendSock,))
receiver = threading.Thread(target=receive, args=(sendSock,))

sender.start()
receiver.start()

# while True:
#     time.sleep(1)
#     pass