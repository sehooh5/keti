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



#### QT-Python TCP/IP 영상통신

- [c++(c) - python(S) 통신](https://hellobird.tistory.com/290)
- [QT TCP Python 예제](https://oceancoding.blogspot.com/2019/05/blog-post_23.html)



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



#### PyQt 자료

- [멀티 스레드 공부자료](https://wikidocs.net/21885)



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

  - UI 코드에서 depth 영상 및 텍스트 데이터 찾아서 하기

  - ```
            # 카메라 키는 작업
            kinect_sources = PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth
            self.kinect = PyKinectRuntime.PyKinectRuntime(kinect_sources)
            depth_width, depth_height = self.kinect.depth_frame_desc.Width, self.kinect.depth_frame_desc.Height
            while True:
                if self.kinect.has_new_depth_frame:
                    depth_frame = self.kinect.get_last_depth_frame()
                    depth_img = np.array(depth_frame, np.uint16,
                                         copy=False).reshape((424, 512))
                    depth_img2 = (depth_img / 256).astype(np.uint8)
                    depth_colormap = make_DEP_colormap(depth_img2).copy()
                    cv2.imshow('test', depth_colormap)
                key = cv2.waitKey(30)
                if key == 27:  # Press esc to break the loop
                    break
            self.kinect.close()
            cv2.destroyAllWindows()
    ```



#### 1119

- 버튼 클릭하면 서버 켜지고, 클라이언트 실행하면 depth 영상 켜지게 구현하기
  - ​	완료 :
    - 소켓 기본 서버 연결 완료
    - 소켓으로 서버 열고 클라이언트로 데이터 보내기 완료
    - 서버 계속 열어두기 완료 // 하지만, client 실행중에는 UI 조작은 불가
    - 영상 vertical flip
  - 할 것 : 
    - text 데이터 바뀌는 거로 받아오기 (기존 데이터 가져오기)
      - 현재는 기본되는 template 만 가져옴
      - template 내부의 3개의 데이터를 바꿔줘야함



#### 1120

- 할 것 : 
  - ~~text 데이터 바뀌는 거로 받아오기 (기존 데이터 가져오기)~~
    - ~~현재는 기본되는 template 만 가져옴~~
    - ~~template 내부의 3개의 데이터를 바꿔줘야함~~
  - 라이브 키면 서버 연동되면서 그 데이터를 사용하기.....
    - 서버가 켜져도 UI 는 사용할 수 잇게
- 완료 : 
  - text 데이터 받아서 전송
  - 영상 구분자로 보내기



#### 1123

- 할 것 : 
  - 라이브 키면 서버 연동되면서 그 데이터를 사용하기.....
    - 서버가 켜져도 UI 는 사용할 수 잇게
  - **test_qt.py  로 멀티 스레드 하는거 연습해보고 적용하기!!**



#### 1124

- 멀티 스레드 구현하기
  - 일단 내 방법으로 실행 후
  - ~~안되면 코드 읽어서 실행해보기(내컴퓨터에서 안돌아갈수도)~~
- 팀뷰어 설치 완료
- 완료:
  - threading 으로 따로 구분해서 실행하기 완료



#### 1125

- 다누시스와 협업
- 서버 안돌아가는 것 확인해서 수정



#### 1126

- 오늘 다시 협업해보고 내일 안되면 방문
- server : server_tag.py
- client : client.py in deepview
- 할 것
  - 소켓 서버 멀티 스레드로 구성하여 안꺼지



#### 1127

- 완료 (deepview : server_jpg.py / client_jpg.py)
  - 소켓 멀티 스레드로 구성
  - jpg 파일 전송하는 서버, 클라이언트 만들어보고 다누시스와 연동
  - Deepview/JPG2 에 컬러 입힌 이미지 잇어서 그거 사용



#### 1130

- deepview 진행상황 정리 및 코드 정리
  - ~~기존 UI 서버 소켓을 멀티 스레드 방식으로 변경~~ 되긴되는데 서버종료가 안됨 나중에 고치기
  - JPG 받는 클라이언트 만들기 
  - JPG 사용하는 버튼 UI 에 추가



#### 1201

- 할것 : 

  - JPG 받는 클라이언트 만들기 
    - 데이터별로 나누어서 데이터는 받아짐
    - 다만 프레임 바이너리 데이터를 어떻게 화면에 표출하지?
    - **완료 : server & client _ test2.py**

  - JPG 사용하는 버튼 UI 에 추가



#### 1202

- 해야할 것
  - ~~JPG 이미지 선명하게 다시 만들기~~ 원래 파일이 화질이 좋지 않음
  - ~~화면에 더 빨리표출?~~ 인코딩해서 보내니까 빨리보내짐
  - ~~JPG 사용하는 버튼 UI 에 추가~~
    - ~~추가 후 text 기존 사용하던 것 처럼 변환되게끔 하고 나머지 내용들도 기존과 같게 진행~~
    - 완료
  - 전체 UI, 서버마다 쓰레드로 구현완료 (port : 8080, 50005)



#### 1203

- 소켓 끄고 닫느거 어떻게하는지 찾아보고 수정해야함
- main_sh.py 884줄 고치는거 하면됨
  - 내용은 바뀌는 텍스트 데이터 보내기



#### 1207

- main_sh.py 고치는거 계속 하면 됩니다



#### 1208

- 책임님 보여드리고 진행
  - 라이브가 켜지고 yolo 등 실행되었을 때, 소켓 서버 키고 전달하면 제대로 전달 가능
  - eventID 는 계속 저장되어있어서 계속 보냄...
    - 이벤트가 바뀔 시에만 보낼 수 있나



#### 1209

- 이벤트 바뀔 시에만 보내도록 수정했음
- 앞으로 계획 : 
  - 5G 과제 내용 백업 + 진행 과정 정리하기
  - 서버에 GPU 장착
  - 5G 내용 서버로 옮기기



#### 1214

- 세미나 및 공부 준비
- 깃 내용 정리





#### 1215

- 클러스터 구성하고 진행한 내용 정리 다시 하기 



#### 1216

- 빅데이터 기초통계 수업 - T academy