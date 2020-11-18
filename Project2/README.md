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



#### ~~python embeding to cpp~~사용안함

- [Embeding 필요한 종속성 설정](https://kjk92.tistory.com/28)
- [한줄한줄 파이썬 명령어로 가능하게끔 한 자료](https://m.blog.naver.com/PostView.nhn?blogId=wwwkasa&logNo=220527874475&proxyReferer=https:%2F%2Fwww.google.com%2F)



#### C++ 사용

- [C++ socket 통신](https://nowonbun.tistory.com/736)
- [C++ opencv](https://nowonbun.tistory.com/745)
- [단계별로 설명 잘해놓음](https://kevinthegrey.tistory.com/26)
- [struct 해결방법 1](https://www.codeproject.com/Questions/455507/confused-to-use-struct-unpack-from-function-in-c-o)
- [struct 해결방법 2 - git](https://github.com/mpapierski/struct)



#### TCP protocol 및 Wireshark 등

- [TCP Python Document](https://realpython.com/python-sockets/)



### C++ Project 디렉터리 및 링커 추가

---

- 프로젝트 속성 > vc++ 디렉토리 > python include 폴더와 libs 폴더 추가
  - C/C++ : C:\Python27\include;
  - 라이브러리 디렉토리 : $(LibraryPath);C:\Python39\libs;C:\Python39\Lib;
- OpenCV 설치 및 Path 추가 (v 4.4.0)
  - 

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

- ~~사이즈 줄이기~~ 완

- socket 사용해서 MetaData(일단 string)도 같이보내기

  - Text는 struct.packt()으로 보내는게 되는데, Text 사이즈에 대한 정보를 전달하기 어렵다

    미리 Text의 사이즈를 알면 보낼 수 있고, 받을 때도 사이즈를 알고 있어야 한다

- Clinet 를 C언어로 바꾸기



#### 1110

- ~~server, client 3으로 text 전달하는거 (사이즈 알때) 구현하기~~
  - back up 에 다른 파일들 백업 완료
  - 사이즈 고정! 전제 하에 전송 가능하게 완료
- python -> cpp 변환하기
  - include <Python.h> 로 자바에서 한줄한줄 쓰듯이 하면 된다...?
  - [ C 로 파이썬 모듈 끌어오기](http://blog.tcltk.co.kr/?p=2851)



#### 1111

- 일단 cpp 에 대한...공부먼저........
- cpp 는 VS 로 실행을 하고 Python 을 실행 가능할 수 있게 Embeding 해줌
- python 3.9 설치하고 opencv4.4.0 설치해서, 그 lib, include 사용해서 진행중
  - 하지만, cv2랑 numpy import error 가 c에서 실행될때 나는듯



#### 1112

- C++에서 코드 다시짜기
  - 일단 byte 객체를 전송 받기 [이거 참고](http://blog.naver.com/PostView.nhn?blogId=war2i7i7&logNo=220791180984&parentCategoryNo=&categoryNo=6&viewDate=&isShowPopularPosts=false&from=postView)
- 아래 프로젝트를 연결해야한다
  - cppClient : 기본 토대가 될 socket client
  - Project2 :  opencv 기본



#### 1113

- 이전에 데이터 읽어오는 자료 잘 활용해서 데이터 받아오기 
  - 지금은 서버쪽으로 구현되어있는데 이걸 클라이언트로 하면 될듯?
    - cline.cpp 랑 server2data.cpp 합치면 될꺼같은데..
- ~~c로 변환 일단 보류, 데이터 어떻게 넘어가는지만 정리해서 드리기~~**완료**
- ~~일단 클라이언트 연결이 끊겨도 서버가 계속 열려있게끔 코드 짜기~~ **완료**

- video stop btn 으로 서버 돌아가게끔 만들어놨음



#### 1118

- 계속해서 서버는 켜두는 기능 완료
- 데이터끼리 구분하려다가 일단 보류
- 와이어 샤크 설치해서 데이터 어떻게 넘어가는지 확인해서 전달
- 할 것 : 
  - UI 에 서버 추가하는 방식 고고