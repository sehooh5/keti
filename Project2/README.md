# README

- Python-C++ 간 Socket 통신
- Kinect sdk 영상과 string data을 python(server) 에서 C++(client)로 전송
- Start Date : 20/11/02



### Version

---

- Python : 3.6.10
- Cuda : 10.0
- Cudnn : 10.0
- Pytorch : 1.2.0
- Anaconda : 4.9.1 



### 과정

---

- [소켓 가장 기본 자료](https://pymotw.com/2/socket/tcp.html)
- [CppPythonSocket github](https://github.com/OleguerCanal/cpp-python_socket)
- [TCP 소켓을 사용하여 웹캠 이미지 송수신](https://webnautes.tistory.com/1382)
  - [기본 TCP 소켓 통신](https://webnautes.tistory.com/1381) : 전부 실행해봤음
- [OpenCV 를 이용해 Kinect 영상 입력 받기](https://t9t9.com/489)



### Document

---

- Numpy : C로 구현된 Python library 로 고성능 수치계산 위해 제작. array(행렬) 단위로 데이터 관리
- [OpenCV 유용한 함수](https://bskyvision.com/712)



### Daily

---

#### 1102

- 환경 설정
- python 서버에서 C++ 클라이언트 로 데이터 전달하는 자료 서치
  - 우리가 궁극적으로 보내야 할 데이터는 영상, 문자열 데이터



#### 1103

- 먼저 주신 파이썬 및 C++ 파일 해석해보기
  - Visual C++ 다운로드
- python 서버에서 C++ 클라이언트 로 데이터 전달하는 자료 서치
  - 우리가 궁극적으로 보내야 할 데이터는 영상, 문자열 데이터
- 현재까지 한 것
  - TCP 소켓 통신에 대한 기본적인 이해와 실행 (c 에서 s 로 문자열 전송 )
- 앞으로 해야할 것
  - 현재 갖고 있는 소스 해석
    - kinect python 코드는 socket 이 아닌?
    - c++ 소스는 영상 socket 통신? 실제 시연을 봤으면 좋겠
  - **CppPythonSocket 을 사용한 코드 다시 해석하고 실행해보기**
  - **TCP 소켓으로 영상 전달하는 코드 해석/실행 해보기**
  - <mark>위에 두 줄의 두꺼운 글씨 해보고 합치면 되지 않을까 생각됨</mark>



#### 1104

- 현재 갖고 있는 소스 해석
  - kinect python 코드는 socket 이 아닌 kinect 프로그램
  - c++ 소스는 영상 socket 통신 : 동영상 아닌 png를 전달 
- **CppPythonSocket 을 사용한 코드 다시 해석하고 실행해보기**
- **TCP 소켓으로 영상 전달하는 코드 해석/실행 해보기**

