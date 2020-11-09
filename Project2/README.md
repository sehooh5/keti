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

- [CppPythonSocket github](https://github.com/OleguerCanal/cpp-python_socket)



#### kinect 사용하기

- [Kinect 영상 출력 기초 git**](https://github.com/limgm/PyKinect2)
- [OpenCV 를 이용해 Kinect 영상 입력 받기](https://t9t9.com/489)



#### socket 사용하기 

- [TCP 소켓을 사용하여 웹캠 이미지 송수신](https://webnautes.tistory.com/1382)
  - [기본 TCP 소켓 통신](https://webnautes.tistory.com/1381) : 전부 실행해봤음
- [소켓 가장 기본 자료](https://pymotw.com/2/socket/tcp.html)
- [소켓 기본적인 작동 세부적인 내용 확인 가능](https://itholic.github.io/python-socket/)



#### Socket 사용해 영상 전송

- [python 코드로 된 카메라 영상 전송](https://m.blog.naver.com/PostView.nhn?blogId=dldudcks1779&logNo=222024824853&categoryNo=70&proxyReferer=https:%2F%2Fwww.google.com%2F)



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



#### 1105

- 진행 순서
  - ~~`pykinectv2` 사용하는거 찾아보고 영상 작동되는지 확인하기~~
    - C://Pykinect2 에 kinect.py 로 컬러, depth영상만 출력중
  - ~~영상을 opencv 로 ? 혹은 바이너리 데이터리 변경?~~
  - ~~그 데이터를 소켓통신으로 전송하기(python)~~
    - 1106 내용
  - python - cpp 소켓 통신으로 전환하기



#### 1106

- 방법1 : kinect -> opencv 로 바꾸기

- 방법2 : kinect 를 바로 socket 으로 전송

- socket 전송 완료 되면 python - cpp 로 변환

- 현재 : 

  - ~~kinect_server2.py - kinect_client2.py 로 진행중~~ git에 server - client 로 진행중

  - depth 도 실행 가능하나 지금은 더 명확한 컬러로 진행중

  - server :  카메라에서 영상 데이터 가져오고 변환

    client :  데이터를 가지고 영상 출력



#### 1109

- 사이즈 줄이기
- socket 사용해서 MetaData(일단 string)도 같이보내기
- Clinet 를 C언어로 바꾸기