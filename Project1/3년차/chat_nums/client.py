import socket
import argparse
import threading
#접속하고 싶은 ip와 port를 입력받는 클라이언트 코드를 작성해보자.
# 접속하고 싶은 포트를 입력한다.
port = 4000

def handle_receive(num, lient_socket, user):
    while 1:
        try:
            data = client_socket.recv(1024)
        except:
            print("연결 끊김")
            break
        data = data.decode()
        if not user in data:
            print(data)

def handle_send(num, client_socket):
    while 1:
        data = input()
        # data = 'hi im seho'
        client_socket.sendall(data.encode())
        if data == "/종료":
            break
    client_socket.close()


if __name__ == '__main__':
    #parser와 관련된 메서드 정리된 블로그 : https://docs.python.org/ko/3/library/argparse.html
    #description - 인자 도움말 전에 표시할 텍스트 (기본값: none)
    #help - 인자가 하는 일에 대한 간단한 설명.
    #nargs - 소비되어야 하는 명령행 인자의 수. -> '+'로 설정 시 모든 명령행 인자를 리스트로 모음 + 없으면 경고
    #required - 명령행 옵션을 생략 할 수 있는지 아닌지 (선택적일 때만).
    parser = argparse.ArgumentParser(description="\nJoo's client\n-p port\n-i host\n-s string")
    parser.add_argument('-p', help="port")
    parser.add_argument('-i', help="host", required=True)
    parser.add_argument('-u', help="user", required=True)

    args = parser.parse_args()
    host = args.i
    user = str(args.u)
    try:
        port = int(args.p)
    except:
        pass
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 host와 prot를 통해 서버에 접속합니다.
    client_socket.connect((host, port))


    client_socket.sendall(user.encode())

    receive_thread = threading.Thread(target=handle_receive, args=(1, client_socket, user))
    receive_thread.daemon = True
    receive_thread.start()

    send_thread = threading.Thread(target=handle_send, args=(2, client_socket))
    send_thread.daemon = True
    send_thread.start()

    send_thread.join()
    receive_thread.join()