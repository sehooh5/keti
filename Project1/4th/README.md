# README

- 5G기반 선제적 위험대응을 위한 예측적 영상보안 핵심기술 개발 (4차년도)
- 오산시와의 실증, 시연 중점의 설계 및 개발
- 인텔리빅스와의 연동



## 일정

- 3월 : 
  - 기존 테스트베드 복구 및 실행
  - 5G 단말기 복구 및 서버 연동



## Repository

### edms(app)

- edms 어플리케이션





### gps

- gps 데이터 추출 및 저장기능

#### /blackbox_GUI

- **blackbox_save_GUI.py**
  - **GPS 데이터 저장**
    - 로우 데이터 : 앱에 `gps_(루트번호)` 입력 후 `저장` 버튼 누르면 차량용 서버 내 `gps_(루트번호)` db에 저장됨
    - 정제된 데이터 : 앱에 `gps_(루트번호)` 입력 후 `저장` 버튼 누르면 edge서버에 `gwg_server.py` 프로그램과 연동되어 `gps_(루트번호)`  테이블이 생성되면서 저장됨
  - **영상 데이터 저장**
    - `blackbox_(루트번호)` 입력 후 `저장` 버튼 누르면 차량용 서버에 저장됨(avi 형식)
- blackbox_GUI.py
  - 블랙박스 영상과 gps 데이터를 스트리밍하는 앱
- **gps_with_gyro.cpp**
  - gps 데이터를 파싱하는 cpp 파일(파싱이 필요할때만 사용)
- **gps_with_gyro.py**
  - gps 로우데이터를 DB에 저장
  - gps 파싱 데이터를 Edge 서버에 전송
- **res.py**
  - response 응답코드



#### /edge_GUI

- **edge_GUI.py**
  - 블랙박스 영상과 gps 데이터를 스트리밍하는 앱



#### /gwg

- **gps_with_gyro.cpp**
  - gps 데이터를 파싱하는 cpp 파일
- **gps_with_gyro.py**
  - gps 파싱 데이터를 Edge 서버에 전송



#### /test_code

- 테스트 코드 모음



**gwg_server.py**

- gps 데이터 전송받는 서버



**gwg_temper_transfer.py**

- DB에 저장된 gps 데이터 전송해주는 클라이언트





### GPSDataCast

- GPS 데이터 전송



/backup





#### /GPSDataCast

- 저장된 GPS, 영상 데이터를 전송하는 프로그램



## reference

- 레퍼 적으면 됨



## 진행 단계(daily)

#### 0322

- 5G 단말기 복구

  - Quopin(가변) : 잘됨
  - Quopin(고정) : 인터넷 연결 안됨
  - Hucom(고정) : 인터넷 연결 안됨
  - SKT : No signal

  -> 업체에 고정IP 설정, 인터넷 연결 어떻게하는지 문의 필요

- EDMS 서버 실행 방법 숙지해두기

  - 방법 전달받아서 기록해두기

- 기존 시스템 복구 및 시연

  - video-streaming.py 파일 각 카메라 주소 바꿔줘야함**(5G 복구되면)**
    - 현재는 실험실에 사용 가능한 카메라 사용중
      - 1번 카메라 : rtsp://root:keti@192.168.0.94/onvif-media/media.amp
      - 2번 카메라 : rtsp://root:keti@192.168.0.93/onvif-media/media.amp
  - **<mark>전체 구조</mark>** : 
    - Edge Server
      - 주소 : 123.214.186.162
      - RSTP 재전송 : 
        - 5G CCTV
          - cvlc -vvv rtp://123.214.186.162:5004 --sout="#rtp{sdp=rtsp://123.214.186.162:8554/videoMain}" --no-sout-all --sout-keep
        - 5G Blackbox **- <mark>되긴 되는데 패킷손실이 많고 느림</mark>**
          - cvlc -vvv rtp://123.214.186.162:5005 --sout="#rtp{sdp=rtsp://123.214.186.162:8555/videoMain}" --no-sout-all --sout-keep
    - 5G CCTV
      - 모뎀 : SKT
      - rtsp://root:keti1234@192.168.225.30:88/videoMain
      - Edge 로 재전송 :  vlc -vvv rtsp://root:keti1234@192.168.225.30:88/videoMain --sout="#rtp{dst=123.214.186.162,port=5004,mux=ts}" --no-sout-all --sout-keep
    - 5G Blackbox
      - 모뎀 : 큐오핀 (가변)
      - rtsp://192.168.1.101:554/h264
      - Edge 로 재전송 : cvlc -vvv rtsp://192.168.1.101:554/h264 --sout="#rtp{dst=123.214.186.162,port=5005,mux=ts}" --no-sout-all --sout-keep



#### 0323

- video-streaming.py 파일 각 카메라 주소 5G 스트리밍으로 변경해보기
- 핸드폰에 이미지로 EDMS_현황도 그려놓음
  - 지금 이 방법이 맞는지 잘 모르겠으나 잘 됨
- 기존 디바이스 연결하는 구조 확인
  - intro4 파일에 요청이 192.168.0.29:5000 으로 고정되어있는데 지금 사용하는 마스터서버는 192.168.0.28를 사용하므로 바꿔줘야함 
    - 유동적으로 마스터의 주소를 불러와서 요청할 수 있게끔 하면 좋을듯
    - 완료
  - 잘 켜지는데 카메라가 연동이 안됨
    - rtsp://root:keti@192.168.0.93/onvif-media/media.amp 주소를 불러야되는데
    - rtsp://root:keti@192.168.0.93:/onvif-media/media.amp 이렇게 요청하기 때문
      - 포트번호가 왜 안넘어가지?
      - **app.py 에서 /connect_device api 에서 d_url 수정함**, select-cam 파일도 수정하니 됨



#### 0324

- gps 및 영상저장 살리고 어떻게 구성되어잇는지 파악



#### 0329

- 실시간 저장 시스템

  1. GPS 데이터
  2. 블랙박스 카메라 영상 저장

- 5G CCTV 일체형 제작을 위한 필요사항 확인

  - 필요 품목
    1. PoE 스위칭 허브
    2. 서버용 미니 PC
    3. 5G 모뎀
    4. PoE CCTV 카메라

  - 파워 필요 여부
    - 필요 : 1,2,3
    - 불필요 : 4
  - 외부 노출 인터페이스
    - 1,2,3의 파워 및 백패널
    - CCTV 렌즈(?)



#### 0331

- 실시간 저장 시스템 확인

  1. GPS 데이터 실행 방법

     - gps 폴더

       - 엣지서버(현 keti0(W-graphic))에서 실행되는 서버

         - /gwg_server.py : 엣지서버에서 실행되는 앱으로 gps 및 gyro 데이터를 저장 혹은 바로 재전송 가능

       - /gwg 폴더

         - gps 및 gyro 시리얼 통신 데이터 전처리 및 전송 앱

           - /gps_with_gyro.cpp : 단말 서버에서 시리얼 통신으로 gps 및 gyro 데이터를 받아 전처리

             - 실행 방법 : 

               1. 컴파일러 실행

                  `g++ -shared -fPIC -o gwg.so ./gps_with_gyro.cpp`

               2. .so 라이브러리 파일 생성 

                  폴더에 `gwg.so`파일이 생성된 것을 확인 가능

           - /gps_with_gyro.py : 모듈화 된 gps_with_gyro4.cpp의 gps 및 gyro 데이터를 엣지서버에 전달

             - 실행 방법

               - 방법 1. 데이터 실시간 전송

                 `sudo python3 gps_with_gyro.py`

               - 방법 2. 데이터 실시간 전송 후 저장

                 `sudo python3 gps_with_gyro.py (뒤에 입력값 아무거나 입력)`

  2. 블랙박스 카메라 영상 저장



#### 0403

- 논문 양식에 맞게 수정

- gps 데이터 전송중 세그멘테이션 오류

  - chatGPT 참고해서 C++ 메모리 할당 및 해제 함수를 추가해볼 것!!!
  - gps 전송 : 15분

- 블랙박스 카메라 영상 저장 확인 후 GPS 정보 저장과 함께 실행시켜보고 마무리

  - 5G 중계기와 유선연결시 끊김현상 발생
    - **wifi 연결로 200Mbps 사용중**

- **실시간 저장 시스템 확인**

  1. GPS 데이터 실행 방법

     - gps 폴더

       - 엣지서버(현 keti0(W-graphic))에서 실행되는 서버

         - /gwg_server.py : 엣지서버에서 실행되는 앱으로 gps 및 gyro 데이터를 저장 혹은 바로 재전송 가능

       - /gwg 폴더

         - gps 및 gyro 시리얼 통신 데이터 전처리 및 전송 앱

           - /gps_with_gyro.cpp : 단말 서버에서 시리얼 통신으로 gps 및 gyro 데이터를 받아 전처리

             - 실행 방법 : 

               1. 컴파일러 실행

                  `g++ -shared -fPIC -o gwg.so ./gps_with_gyro.cpp`

               2. .so 라이브러리 파일 생성 

                  폴더에 `gwg.so`파일이 생성된 것을 확인 가능

           - /gps_with_gyro.py : 모듈화 된 gps_with_gyro4.cpp의 gps 및 gyro 데이터를 엣지서버에 전달

             - 실행 방법

               - 방법 1. 데이터 실시간 전송

                 `sudo python3 gps_with_gyro.py`

               - 방법 2. 데이터 실시간 전송 후 저장

                 `sudo python3 gps_with_gyro.py (뒤에 입력값 아무거나 입력)`

  2. 블랙박스 카메라 영상 저장

     - 카메라 기본 url : rtsp://192.168.1.101:554/h264

     - Edge 로 영상 rtp 재전송 : 

       ```
       cvlc -vvv rtsp://192.168.1.101:554/h264 --sout="#rtp{dst=123.214.186.162,port=5005,mux=ts}" --no-sout-all --sout-keep
       ```

     - 영상 저장 : 

       ```
       cvlc rtp://123.214.186.162:5005 --sout=file/ps:/home/keti0/비디오/blackbox_test1.mp4
       ```

     - Edge에서 먼저 `저장명령`  실행 후 BlackBox rtp 재전송해도 저장 됨



#### 0404

- 5G 모뎀 연결관련 메일 받았는데 어떻게 진행하는지 양책임님 오시면 진행
- gps 데이터 전송중 세그멘테이션 오류

  - chatGPT 참고해서 C++ 메모리 할당 및 해제 함수를 추가해볼 것!!!
  - gps 전송 : 15분
    - 13:32 ~ 13:47
    - 43 ~ 46
    - 47 ~ 48
    - 49 ~ 00
    - 05 ~ 25
    - 26 ~ 37
    - 37 ~ 43
    - 53 ~ 
    - 01 ~ 03
    - 04 ~ 



#### 0405

- 오전 세그멘테이션 오류 수정 진행
  - 1418 ~ 1428
  - 딜레이 주는 방법으로 했는데 그래도 결국 10여분 후에 오류 발생



#### 0406

- 세그멘테이션 수정 진행 및 전체 확인 후 내일 보고
  - 세그멘테이션 오류 발생 시점
    - fp, 즉 파일을 쓰는 과정이 있었는데 불필요한 과정이기도해서 빼버렸다
    - 이후 too many files open오류가 났는데 이는 `uart_close(fd)` 로 UART 통신을 닫아주며 해결했다.



#### 0407

- 아침에 도착하자마자 gps 테스트 계속 돌리기
  - 완료
- 논문 출처
  1. 정보보호 학회지 :[링크](https://koreascience.kr/journal/JBBHBD/v20n3.page) 
  2.  한국인터넷방송통신학회 : [링크](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002498057)
  3. 한국통신학회 추계종합학술발표회 : [링크](https://www.dbpia.co.kr/pdf/pdfView.do?nodeId=NODE10501346&googleIPSandBox=false&mark=0&ipRange=false&accessgl=Y&language=ko_KR&hasTopBanner=true)
  4. 쿠버네티스 책
  5. 정보기술융합공학논문지 : [링크](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002771821)



#### 0410

- gps 및 영상 저장 확인, 보고
- 논문 제출(퇴근 전까지)
  - 비회원 가능한지 확인 
  - **완료**
- 개인 프로젝트 확인 및 완료 이번주까지



#### 0411

- 개인 프로젝트 기입

- 현재 콘솔에서 사용하는 기능들을 qt 사용해서 실행할 수 있을지?

  - 블랙박스 vjy5pxkx

    - gps 신호 전송
      - 전송
      - 전송 및 저장
      - 멈춤
    - 영상 rtp 전송
      - 전송
      - 멈춤

  - 엣지 서버

    - 영상 rtp 저장
      - 저장
      - 멈춤

  - gpt

    ```
    1. sudo python3 gps_with_gyro.py 실행버튼
    2. sudo python3 gps_with_gyro.py save 실행머튼
    3. 1,2번 기능 멈춤버튼
    4. 글씨 입력창 1
    5. 글씨 입력창 2
    6. 글씨 입력창 3
    7. cvlc -vvv {4번 입력창 내용} --sout="#rtp{dst={5번 입력창 내용},port={6번 입력창 내용},mux=ts}" --no-sout-all --sout-keep 실행버튼
    8. 7번 멈춤 버튼
    
    rtsp://192.168.1.101:554/h264
    123.214.186.162
    5005
    ```



#### 0411

- stop_process2 함수 작동하게끔 만들고

  - ctrl+c 실행?

- 2개 기능 동시에 돌아가는지 확인해주기

  ```
  from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
  import subprocess
  import os
  import sys
  
  class App(QWidget):
  
      def __init__(self):
          super().__init__()
          self.title = 'GPS with Gyro'
          self.left = 10
          self.top = 10
          self.width = 400
          self.height = 450
          self.process = None
          self.process2 = None
          self.initUI()
  
      def initUI(self):
          self.setWindowTitle(self.title)
          self.setGeometry(self.left, self.top, self.width, self.height)
  
          # GPS 데이터
          # 제목
          title = QLabel('GPS 실시간 데이터', self)
          title.move(95, 10)
  
          # 실행 버튼
          btn1 = QPushButton('전송', self)
          btn1.setToolTip('gps_with_gyro.py 실행')
          btn1.move(50, 50)
          btn1.clicked.connect(self.start_process)
  
          # 저장 버튼
          btn2 = QPushButton('저장', self)
          btn2.setToolTip('gps_with_gyro.py save 실행')
          btn2.move(150, 50)
          btn2.clicked.connect(self.start_save_process)
  
          # 멈춤 버튼
          btn3 = QPushButton('멈춤', self)
          btn3.setToolTip('실행 중인 프로세스 중지')
          btn3.move(100, 100)
          btn3.clicked.connect(self.stop_process)
  
  	def start_process(self):
          # 실행 중인 프로세스가 없는 경우에만 실행
          if self.process is None or self.process.poll() is not None:
              self.process = subprocess.Popen(['python3', 'gps_with_gyro.py'])
  
      def start_save_process(self):
          # 실행 중인 프로세스가 없는 경우에만 실행
          if self.process is None or self.process.poll() is not None:
              self.process = subprocess.Popen(['python3', 'gps_with_gyro.py', 'save'])
  
      def stop_process(self):
          # 실행 중인 프로세스가 있는 경우에만 종료
          if self.process is not None and self.process.poll() is None:
              self.process.terminate()
              self.process.wait()
  
  if __name__ == '__main__':
      app = QApplication(sys.argv)
      ex = App()
      sys.exit(app.exec_())
  ```

  

#### 0412

- app_GUI_thread.py  에 GPT 참고해서 수정중

  ```python
  from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
  from PyQt5.QtCore import QThread
  import subprocess
  import os
  import sys
  
  class ProcessThread(QThread):
      def __init__(self, cmd):
          super().__init__()
          self.cmd = cmd
          self.process = None
  
      def run(self):
          self.process = subprocess.Popen(self.cmd)
          self.process.wait()
  
      def stop(self):
          if self.process is not None and self.process.poll() is None:
              self.process.terminate()
              self.process.wait()
  
  class App(QWidget):
  
      def __init__(self):
          super().__init__()
          self.title = 'GPS with Gyro'
          self.left = 10
          self.top = 10
          self.width = 400
          self.height = 450
  #         self.process = None
  #         self.process2 = None
          self.process_thread = None
          self.process_save_thread = None
          self.process2_thread = None
          self.initUI()
  
      def initUI(self):
          self.setWindowTitle(self.title)
          self.setGeometry(self.left, self.top, self.width, self.height)
  
          # GPS 데이터
          # 제목
          title = QLabel('GPS 실시간 데이터', self)
          title.move(95, 10)
  
          # 실행 버튼
          btn1 = QPushButton('전송', self)
          btn1.setToolTip('gps_with_gyro.py 실행')
          btn1.move(50, 50)
          btn1.clicked.connect(self.start_process)
  
          # 저장 버튼
          btn2 = QPushButton('저장', self)
          btn2.setToolTip('gps_with_gyro.py save 실행')
          btn2.move(150, 50)
          btn2.clicked.connect(self.start_save_process)
  
          # 멈춤 버튼
          btn3 = QPushButton('멈춤', self)
          btn3.setToolTip('실행 중인 프로세스 중지')
          btn3.move(100, 100)
          btn3.clicked.connect(self.stop_process)
  
          # 영상 데이터
          # 제목
          title = QLabel('영상 데이터 전송', self)
          title.move(95, 190)
  
          # 입력창 1
          input1 = QLineEdit(self)
          input1.setPlaceholderText('카메라 주소 입력')
          input1.move(50, 220)
          input1.resize(300, 25)
  
          # 입력창 2
          input2 = QLineEdit(self)
          input2.setPlaceholderText('엣지서버 주소')
          input2.move(50, 260)
          input2.resize(300, 25)
  
          # 입력창 3
          input3 = QLineEdit(self)
          input3.setPlaceholderText('엣지서버 포트번호')
          input3.move(50, 300)
          input3.resize(300, 25)
  
          # 실행 버튼
          btn4 = QPushButton('실행', self)
          btn4.setToolTip('VLC 실행')
          btn4.move(50, 340)
          btn4.clicked.connect(lambda: self.start_process2(input1.text(), input2.text(), input3.text()))
  
          # 멈춤 버튼
          btn5 = QPushButton('멈춤', self)
          btn5.setToolTip('VLC 종료')
          btn5.move(150, 340)
          btn5.clicked.connect(self.stop_process2)
          self.show()
  
      def start_process(self):
          # 실행 중인 프로세스가 없는 경우에만 실행
          if self.process is None or self.process.poll() is not None:
              self.process = subprocess.Popen(['python3', 'gps_with_gyro.py'])
  
      def start_save_process(self):
          # 실행 중인 프로세스가 없는 경우에만 실행
          if self.process is None or self.process.poll() is not None:
              self.process = subprocess.Popen(['python3', 'gps_with_gyro.py', 'save'])
  
      def stop_process(self):
          # 실행 중인 프로세스가 있는 경우에만 종료
          if self.process is not None and self.process.poll() is None:
              self.process.terminate()
              self.process.wait()
  
      def start_process2(self, input1, input2, input3):
          # 실행 중인 프로세스가 없는 경우에만 실행
          if self.process2 is None or self.process2.poll() is not None:
              command = 'cvlc -vvv {} --sout="#rtp{{dst={},port={},mux=ts}}" --no-sout-all --sout-keep'.format(input1, input2, input3)
              self.process2 = subprocess.Popen(command, shell=True)
  
      def stop_process2(self):
          # 실행 중인 프로세스가 있는 경우에만 종료
          if self.process2 is not None and self.process2.poll() is None:
              self.process2.terminate()
  
              # 5초간 기다렸다가 아직 실행중이면 강제종료
              try:
                  self.process2.communicate(timeout=5)
              except subprocess.TimeoutExpired:
                  self.process2.kill()
  
              self.process2.wait()
  
  if __name__ == '__main__':
      app = QApplication(sys.argv)
      ex = App()
      sys.exit(app.exec_())
  ```



#### 0414

- vlc 오류 해결 및 쓰레드 사용

  - rtsp://192.168.1.101:554/h264

  - 123.214.186.162

  - 5005

    ```
    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
    from PyQt5.QtCore import QThread
    import subprocess
    import os
    import sys
    
    class ProcessThread(QThread):
        def __init__(self, cmd):
            super().__init__()
            self.cmd = cmd
            self.process = None
    
        def run(self):
            self.process = subprocess.Popen(self.cmd)
            self.process.wait()
    
        def stop(self):
            if self.process is not None and self.process.poll() is None:
                self.process.terminate()
                self.process.wait()
    
    class App(QWidget):
    
        def __init__(self):
            super().__init__()
            self.title = 'GPS with Gyro'
            self.left = 10
            self.top = 10
            self.width = 400
            self.height = 450
    #         self.process = None
    #         self.process2 = None
            self.process_thread = None
            self.process_save_thread = None
            self.process2_thread = None
            self.initUI()
    
        def initUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)
    
            # 영상 데이터
            # 제목
            title = QLabel('영상 데이터 전송', self)
            title.move(95, 190)
    
            # 입력창 1
            input1 = QLineEdit(self)
            input1.setPlaceholderText('카메라 주소 입력')
            input1.move(50, 220)
            input1.resize(300, 25)
    
            # 입력창 2
            input2 = QLineEdit(self)
            input2.setPlaceholderText('엣지서버 주소')
            input2.move(50, 260)
            input2.resize(300, 25)
    
            # 입력창 3
            input3 = QLineEdit(self)
            input3.setPlaceholderText('엣지서버 포트번호')
            input3.move(50, 300)
            input3.resize(300, 25)
    
            # 실행 버튼
            btn4 = QPushButton('실행', self)
            btn4.setToolTip('VLC 실행')
            btn4.move(50, 340)
            btn4.clicked.connect(lambda: self.start_process2(input1.text(), input2.text(), input3.text()))
    
            # 멈춤 버튼
            btn5 = QPushButton('멈춤', self)
            btn5.setToolTip('VLC 종료')
            btn5.move(150, 340)
            btn5.clicked.connect(self.stop_process2)
            self.show()
    
        def start_process2(self, input1, input2, input3):
            # 실행 중인 프로세스가 없는 경우에만 실행
            if self.process2_thread is None or not self.process2_thread.isRunning():
                command = 'cvlc -vvv {} --sout="#rtp{{dst={},port={},mux=ts}}" --no-sout-all --sout-keep'.format(input1, input2, input3)
                self.process2_thread = subprocess.Popen(command, shell=True)
    
        def stop_process2(self):
            # 실행 중인 프로세스가 있는 경우에만 종료
            if self.process2_thread is not None:
                self.process2_thread.stop()
                
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = App()
        sys.exit(app.exec_())            
    ```

    

#### 0417

- vlc 수정
  - 블랙박스 console 3개의 창
    - /바탕화면/keti/Project1/3rd/gps/blackbox_GUI : `python3 app_GUI_thread.py`
    - ~ : `cvlc -vvv rtsp://192.168.1.101:554/h264 --sout="#rtp{dst=123.214.186.162,port=5005,mux=ts}" --no-sout-all --sout-keep`
    - /바탕화면/keti : git 및 기본
  - ctrl+c 하면 종료되긴 함
- gps uart serial port 변경되는데로 적용 되도록 코드 변경
  - 변경 완료



#### 0418

- vlc 종료 안되는것 수정하기

  - psutil 모듈 사용해 해결 완료!

    ```
    rtsp://192.168.1.101:554/h264
    123.214.186.162
    5005
    ```

    

#### 0419

- edge 서버에서도 pyqt로 rtp 영상 저장, rtsp 재전송 기능 만들기

  - rtsp 재전송 기능 

    - cvlc -vvv rtp://123.214.186.162:5005 --sout="#rtp{sdp=rtsp://:8555/videoMain}" --no-sout-all --sout-keep
    - rtp 주소 : rtp://123.214.186.162:5005
    - rtsp 주소 : rtsp://:8555/videoMain

  - rtp 영상 저장

    - rtp 주소 : rtp://123.214.186.162:5005 
    - 파일경로 : /home/keti0/비디오/
    - 파일명 : blackbox_test6.mp4

- process 함수 부분 진행중!!!!



#### 0420

- edge GUI Process수정



#### 0421

- bbGUI - edgeGUI 간 연동

  - 확인완료

  - 현재는 임의의 주소를 집력 중이나 추후에는 실제 기능하도록 다시 변경해줘야함

    ```
    [blackbox_GUI.py]
    1. rtp 전송 기능
    - 카메라 주소 : rtsp://192.168.1.101:554/h264
    - rtp 전송받을 서버 주소 : 123.214.186.162
    - 서버 포트 번호 : 5005
    
    [edge_GUI.py]
    1. rtsp 재전송 기능
    - rtp 주소 : rtp://123.214.186.162:5005
    - rtsp 주소 : rtsp://:8555/videoMain
    
    2. rtp 영상 저장 기능
    - rtp 주소 : rtp://123.214.186.162:5005 
    - 파일경로 : /home/keti0/비디오/
    - 파일명 : blackbox_test6.mp4
    ```



#### 0428

- 다음주 화요일까지 확인해야할 내용
  - 저장된 영상 RTP 전송 무한루프 되는지 확인
    - 명령어 : `cvlc -vvv /home/keti-laptop/비디오/blackbox_test4.mp4 --sout "#rtp{dst=123.214.186.162,port=5005,mux=ts}" --loop --no-sout-all`
  - GPS 로우데이터로 저장할 수 있게 변경
    - /4th/gps/test_code/raw_data_save.py 에서 진행중ㄴ
  - 차량 서버에 바로 영상, GPS 데이터 저장할 수 있게 만들어 놓기
  - GPS 데이터 싱크 어떻게 맞출수 있을까? 



#### <mark>0502</mark>

- 확인 
  - 저장된 영상 RTP 전송 무한루프 되는지 확인
  - - 명령어 : `cvlc -vvv /home/keti-laptop/비디오/blackbox_test4.mp4 --sout "#rtp{dst=123.214.186.162,port=5005,mux=ts}" --loop --no-sout-all`
  - GPS 로우데이터로 저장할 수 있게 변경
    - /4th/gps/test_code/raw_data_save.py 에서 진행중
  - 차량 서버에 바로 영상, GPS 데이터 저장할 수 있게 만들어 놓기(blackbox_save_GUI.py)
    - 영상 저장 : `cvlc rtsp://192.168.1.101:554/h264 --sout=file/mp4:/home/keti-laptop/비디오/blackbox_test4.mp4`
  - GPS 데이터 싱크 어떻게 맞출수 있을까? 
    - 일단 타임스탬프로 데이터 저장중
- `blackbox_save_GUI.py`로 GPS 데이터, 영상 데이터 저장중
  - **GPS 데이터 저장**
    - 로우 데이터 : 앱에 `gps_(루트번호)` 입력 후 `저장` 버튼 누르면 차량용 서버 내 `gps_(루트번호)` db에 저장됨
    - 정제된 데이터 : 앱에 `gps_(루트번호)` 입력 후 `저장` 버튼 누르면 edge서버에 `gwg_server.py` 프로그램과 연동되어 `gps_(루트번호)`  테이블이 생성되면서 저장됨
  - **영상 데이터 저장**
    - `blackbox_(루트번호)` 입력 후 `저장` 버튼 누르면 차량용 서버에 저장됨(avi 형식)



#### 0503

- 오산 출장
- 준비
  - 멀티탭, 모든 장치 챙겨서 차량설치(오전)
  - 이동 후 촬영 및 데이터 저장(오후)
  - QT, DS 할수 잇으면 하기
- 영상데이터 저장 확인
- GPS 데이터는 sqlite 테이블에서 BLOB형태로 저장중인데 readline()으로 한줄 씩 저장중 이게 나중에 어떻게 사용할지는 모르겠지만 일단 이렇게 저장하는중, edge에도 원래 방식대로 저장중



#### 0509

- 내일 제주도 출장 준비
- 제주도 다녀와서 데이터 확인 후 어떻게 진행할지 회의



#### 0515

- 개인 일정 정리
  - ~~도서평쓰기~~ - 완료
  - ~~출장~~ - 내일 진행
    - 복명?
    - 실비처리 어떻게?



#### 0516

- 출장 데이터 정리

  - 영상

    - 채널 개수 : 7

    - **서버1 : 채널 개수 만큼 RTP 전송(무한루프)**

      - blackbox_01 : 

        ```
        cvlc -vvv /media/keti-laptop/T7/blackbox_01.avi --sout "#rtp{dst=123.214.186.162,port=5001,mux=ts}" --loop --no-sout-all
        ```

        

    - **서버2(Edge) : 채널 개수 만큼 RTP 받은 것 RTSP 전송**

      - blackbox_01 : 

        ```
        cvlc -vvv rtp://123.214.186.162:5001 --sout="#rtp{sdp=rtsp://123.214.186.162:8001/videoMain}" --no-sout-all --sout-keep
        ```

    - 확인 완료, python 으로 7개 실행할 수 있는지 확인

      - 기존 blackbox_GUI.py 를 gpsdatacast.py 에 복사해놨음..
      - 쓰레드 사용해서 rtp 전송 여러개를 사용하고 종료 할 수 있게 변경해보기

  - gps

    - ~~로우 데이터로 gps 데이터 추출 가능한지 확인~~ 일단 로우데이터를 전송하는거로
    - 채널 7개 GPS 데이터를 
    - 서버1 : post 요청/전송
    - 서버2 : 업데이트 된 gps 데이터 대기

- 영상 데이터랑 gps 데이터 어떻게 싱크를 맞출지?

- 영상 스트리밍 상태 확인

  - Test1 : 3개 영상 rtp -> rtsp 스트리밍중
    - 패킷손실 발생
    - 연속 재생 확인되면 1개만 틀어서 패킷 손실 줄어드는지 확인 - 비슷함

- 영상 종료 확인하는 코드

  ```python
  import subprocess
  import time
  
  def monitor_vlc_process():
      command = [
          'cvlc',
          '-vvv',
          '/media/keti-laptop/T7/blackbox_01.avi',
          '--sout',
          '#rtp{dst=123.214.186.162,port=5001,mux=ts}',
          '--loop',
          '--no-sout-all'
      ]
  
      process = subprocess.Popen(command)
  
      while True:
          process.poll()  # 프로세스의 상태를 확인
  
          if process.returncode is not None:
              print("동영상 재생이 종료되었습니다.")
              break
  
          # 추가적인 작업을 수행하거나 종료 조건을 설정할 수 있습니다.
          # 예를 들어, 특정 시간이 지나면 종료하도록 설정할 수 있습니다.
          # if time.time() > end_time:
          #     process.terminate()
          #     break
  
          time.sleep(1)  # 프로세스 상태를 확인하는 간격 설정
  
  if __name__ == '__main__':
      monitor_vlc_process()
  ```

  



- 출장 관련 서류
  - 복명
    - 파일 만들기
    - 파일추가 - 증빙저장 - 결재요청
  - 프린트
    - 발표논문 편집본
    - 복명
    - 항공결제카드영수증
  - 서박사님 전달
    - 발표논문 편집본

  

#### 0517

- 총 애플리케이션 2개

  1. 서버1에서 실행되는 영상, GPS 전송
  2. 서버2에서 실행되는 영상, GPS 재전송

- 출장 데이터 전송

  - 영상

    - 채널 개수 : 7

    - **서버1 : 채널 개수 만큼 RTP 전송(무한루프)**

      - blackbox_01 : 

        ```
        cvlc -vvv /media/keti-laptop/T7/blackbox_01.avi --sout "#rtp{dst=123.214.186.162,port=5001,mux=ts}" --loop --no-sout-all
        ```

        

    - **서버2(Edge) : 채널 개수 만큼 RTP 받은 것 RTSP 전송**

      - blackbox_01 : 

        ```
        cvlc -vvv rtp://123.214.186.162:5001 --sout="#rtp{sdp=rtsp://123.214.186.162:8001/videoMain}" --no-sout-all --sout-keep
        ```

    - 확인 완료, python 으로 7개 실행할 수 있는지 확인

      - 기존 blackbox_GUI.py 를 gpsdatacast.py 에 복사해놨음..
      - 쓰레드 사용해서 rtp 전송 여러개를 사용하고 종료 할 수 있게 변경해보기

  - gps

    - ~~로우 데이터로 gps 데이터 추출 가능한지 확인~~ 일단 로우데이터를 전송하는거로
    - 채널 7개 GPS 데이터를 
    - 서버1 : post 요청/전송
    - 서버2 : 업데이트 된 gps 데이터 대기



- GPS 데이터
  - 서버1 에서 로우데이터



- 영상 데이터랑 gps 데이터 어떻게 싱크를 맞출지?



- 영상 스트리밍 상태 확인
  - Test1 : 3개 영상 rtp -> rtsp 스트리밍중
    - 패킷손실 발생
    - 연속 재생 확인되면 1개만 틀어서 패킷 손실 줄어드는지 확인 - 비슷함



- 영상 종료 확인하는 코드

  ```python
  import subprocess
  import time
  
  def monitor_vlc_process():
      command = [
          'cvlc',
          '-vvv',
          '/media/keti-laptop/T7/blackbox_01.avi',
          '--sout',
          '#rtp{dst=123.214.186.162,port=5001,mux=ts}',
          '--loop',
          '--no-sout-all'
      ]
  
      process = subprocess.Popen(command)
  
      while True:
          process.poll()  # 프로세스의 상태를 확인
  
          if process.returncode is not None:
              print("동영상 재생이 종료되었습니다.")
              break
  
          # 추가적인 작업을 수행하거나 종료 조건을 설정할 수 있습니다.
          # 예를 들어, 특정 시간이 지나면 종료하도록 설정할 수 있습니다.
          # if time.time() > end_time:
          #     process.terminate()
          #     break
  
          time.sleep(1)  # 프로세스 상태를 확인하는 간격 설정
  
  if __name__ == '__main__':
      monitor_vlc_process()
  ```



- 현재 완료단계
  - 7개 영상 rtp 전송
  - 엣지에서 7개 영상 rtsp 재전송
- 진행해야할 것
  - 각 애플리케이션에 GPS 전송기능 탑재
    - 일단은 로우데이터 전송으로 고고
  - GPS 데이터 전송에 대한 API 문서 작업
  - 영상2, gps2 총 4개 애플리케이션으로 나눌까?
- 문제점
  - 현재 저장된 GPS 로우 데이터를 0.5초마다 서버1에서 서버2로 전송
  - 서버2에서는 전송받은 데이터를 계속 갱신해주는데
  - 만약 인텔리빅스에서 0.5초 마다 데이터를 restAPI로 응답받는다 해도
  - 때로는 똑같은 로우데이터가 전송되거나 누락되는 데이터가 있을 수 있음



#### 0518

- 현재 완료단계
  - 7개 영상 rtp 전송
  - 엣지에서 7개 영상 rtsp 재전송
- 진행중
  - gpsdatacast2.py 파일에서 진행중
    - 맨밑 주석처리하면 영상, gps 가 병렬 처리되어 **1번은 전송이되는데 나머지가 안됨**
    - gps 1번은 잘넘어가는데 2번부터는 인코딩에러
      - hex() 로 해결
      - 근데 첫번째 실행되는 gps 전송이 stop 명령어를 해도 멈추지 않음
- 진행해야할 것
  - 각 애플리케이션에 GPS 전송기능 탑재
    - 일단은 로우데이터 전송으로 고고
    - GPS 기능은 따로 만들고, 7개를 실행할수 있는 앱이 가능한지 해보고 안되면 7개 터미널에서 실행
  - GPS 데이터 전송에 대한 API 문서 작업
  - 영상2, gps2 총 4개 애플리케이션으로 나눌까?
    - 나누면 싱크 맞추는 문제가 있음
- 문제점
  - 현재 저장된 GPS 로우 데이터를 0.5초마다 서버1에서 서버2로 전송
  - 서버2에서는 전송받은 데이터를 계속 갱신해주는데
  - 만약 인텔리빅스에서 0.5초 마다 데이터를 restAPI로 응답받는다 해도
  - 때로는 똑같은 로우데이터가 전송되거나 누락되는 데이터가 있을 수 있음
  - gps : 
    - 데이터 7개 동시에 실행하면 멈추기가 안될 수 있음 -> 원래는 7개의 서버에서 따로 실행되야함



#### 0519

- 현재 완료단계
  - **서버1 : gpsdatacast2.py 에서 영상+GPS 모두 처리중**	
    - 7개 영상 rtp 전송
    - gps 데이터 0.5초마다 로우데이터 전송
  - **서버2 : **
    - **영상 RTSP 재전송(gpsdatacast_Edge.py)**
      - 엣지에서 7개 영상 rtsp 재전송
    -  **GPS 처리(gps_test_edge.py)**
      - flask 서버로 전달받은 gps 데이터 갱신하고 받아갈 수 있음
  - GPS 데이터 전송에 대한 API 문서 작업
- 문제점
  - 현재 저장된 GPS 로우 데이터를 0.5초마다 서버1에서 서버2로 전송
  - 서버2에서는 전송받은 데이터를 계속 갱신해주는데
  - 만약 인텔리빅스에서 0.5초 마다 데이터를 restAPI로 응답받는다 해도
  - 때로는 똑같은 로우데이터가 전송되거나 누락되는 데이터가 있을 수 있음
  - gps : 
    - 데이터 7개 동시에 실행하면 멈추기가 안될 수 있음 -> 원래는 7개의 서버에서 따로 실행되야함
  - 5G모뎀 속도제한 걸린듯
- 진행중
  - gpsdatacast2.py 파일에서 진행중
    - 맨밑 주석처리하면 영상, gps 가 병렬 처리되어 **1번은 전송이되는데 나머지가 안됨**
    - gps 1번은 잘넘어가는데 2번부터는 인코딩에러
      - hex() 로 해결
        - **데이터베이스에서 가져온 값이 바이너리 형식이라면, 이를 텍스트 형식으로 변환해함.  `hex()` 함수는 이러한 바이너리 데이터를 16진수 문자열로 변환하는 데 사용.  이렇게 변환한 16진수 데이터는 JSON 객체에 포함되어 서버로 전송함**
      - 근데 첫번째 실행되는 gps 전송이 stop 명령어를 해도 멈추지 않음



#### 0523

- 주말동안 잘 실행됨
- 견적 전달드리기
- **데이터 전송**
  - **서버1 : gpsdatacast2.py 에서 영상+GPS 모두 처리중**	
    - 7개 영상 rtp 전송
    - gps 데이터 0.5초마다 로우데이터 전송
  - **서버2 : **
    - **영상 RTSP 재전송(gpsdatacast_Edge.py)**
      - 엣지에서 7개 영상 rtsp 재전송
    -  **GPS 처리(gps_saved_edge.py)**
      - flask 서버로 전달받은 gps 데이터 갱신하고 받아갈 수 있음



#### 0524

- ~~체크카드 앞뒷면 재은씨 드리기~~ 내일
- 25일 목요일 인텔리빅스 출장 준비
  - 데이터 저장된거 변환 가능한지 확인해보기 - **GPSDataCast/gps_test.py**
    - 데이터 한 개씩 빼서 파싱하기 - 한개씩 사용하는건 완료
      - 이미 55로 시작되는게 binary 형태인듯?
    - 파싱하는 코드는 더 고민해봐야할 듯



#### 0525

- 데이터 저장된거 파싱 가능한지 확인해보기 - **GPSDataCast/gps_test.py**
  - 데이터 한 개씩 빼서 파싱하기 - 한개씩 사용하는건 완료
    - 이미 55로 시작되는게 binary 형태인듯?



#### 0530

- 데이터 저장된거 파싱 가능한지 확인해보기 - **GPSDataCast/gps_parsing_test.py**
  - 데이터 한 개씩 빼서 파싱하기 - 한개씩 사용하는건 완료
    - 이미 55로 시작되는게 binary 형태인듯?
  - 원본 데이터 cpp 찾아서 파싱하는거 연구해야함



#### 0531

- 원본데이터에서 cpp 파싱하는거 python 으로 변경 조금 해보기



#### 0601

- 파싱 금요일까지
- ctype 



#### 0602

- 토요일 숙소
- 가방 구매?
- ~~리니아 숙제~~ 완



#### 0607

- gps_parsing_test2.py 에서 진행중
  - 로우데이터 읽을 때 11바이트씩 끊는데 이 처리 어떻게든 해줘야함
- cpp 코드 변경해서 되는지 확인
- 출장 가져가서 회의할 내용 확인하기



#### 0608

- gps_parsing_test2.py 에서 파싱 준비하고 CPP코드에서도 해보기
  - 로우데이터 읽을 때 11바이트씩 끊는데 이 처리 어떻게든 해줘야함
- ~~아침에 컴퓨터 견적 보내드리기~~



#### 0609

- gps_parsing_test2.py 에서 파싱 준비하고 CPP코드에서도 해보기
- 포폴 재시작



#### 0612

- 포폴 및 파싱 준비

  - c 파일 찾는중 
    - /test_code/gps_with_gyro(basic).cpp 가 기본파일
    - **/GPSDataCast/gps_with_gyro(basic).cpp 에서 진행중!**

  

#### 0613

- gpt 변경된거 토대로 변경해가면서 파싱해보기(/GPSDataCast/gps_with_gyro(basic).cpp)
- gps_parsing_test3.py 로 파이썬 코드 구성해보기..
  - unpacked_data 만들기 시작하면됨



#### 0614

- gps_parsing_test3.py 로 파이썬 코드에서 파싱
  - unpacked_data 로 파싱중
- 도커 리소스 확인해서 python 으로 printout 할수 있는지 확인하기(서박사님)



#### 0619

- gps_parsing_test3.py 로 파이썬 코드에서 파싱

  - unpacked_data 로 파싱중

- 도커 리소스 확인해서 python 으로 printout 할수 있는지 확인하기(서박사님)

  - 도커 리소스 확인

    - `docker stats`

      - 컨테이너 name으로 확인 가능

      - CPU, 메모리 사용량, 사용률

      - 응답 메시지

        ```
        # docker container
        b'CONTAINER ID   NAME  CPU %     MEM USAGE / LIMIT     MEM %     NET I/O   BLOCK I/O         PIDS\n
        7f4e45cc7993   k8s_coredns_coredns-78fcd69978-8gt2g_kube-system_5380fe1d-dc62-41a7-b806-b2c65ff395ce_15   0.30%     22.34MiB / 170MiB     13.14%    0B / 0B   21MB / 0B         10\n3
        ```

        

  - 쿠버네티스 리소스 확인 [(참고)](https://ihp001.tistory.com/249?category=869545)

    - **k8s의 metrics-server 사용**

      - 명령어 : `kubectl top pod (or node)`

      - 리소스 : CPU, 메모리 사용량, 사용률

      - 응답 메시지

        ```
        # pod
        b'NAME                                CPU(cores)   MEMORY(bytes)  \n
        select-cam-keti1-5dc4bcd4b4-cvd8n   1m           41Mi            \n'
        
        # node
        b'NAME    CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   \n
        keti1   626m         15%    3065Mi          39%       \n
        keti2   583m         14%    4356Mi          56%       \n'
        
        ```

  - 해당 코드

    ```python
    import sys
    import subprocess
    
    if sys.argv[1] == 'd':
        print("docker resources check")
        output = subprocess.check_output("docker stats --no-stream",shell=True)
        print(output)
    elif sys.argv[1] == 'kp':
        print("k8s pod resources check")
        output = subprocess.check_output("kubectl top po",shell=True)
        print(output)
    elif sys.argv[1] == 'kn':
        print("k8s node resources check")
        output = subprocess.check_output("kubectl top no",shell=True)
        print(output)
    else:
        print("argument not available")
    ```



#### 0620

- 위 코드와 응답 값 정리하는 문서 만들기
  - 한글파일 완료



#### 0621

- 개인 프로젝트 및 파싱..



#### 0623

- 파싱 잘 안되는데 파이썬으로 연구
- 서버 2대 설치 완료



#### 062425

- 주말 개인프로젝트 포트폴리오!!!



#### 0626

- 개인 프로젝트 다시 시작
- **서버 2대로 데이터 보내기 시작하기**
  - **keti1 : bb01~bb04**
  - **keti2 : bb05~bb07**
  - **keti0 : gpsdatacast_edge.py, gps_saved_edge.py 실행중**



#### 0627

- 파이썬 파싱
  - gps_parsing_test3.py
- 개인 프로젝트
- 영상 편집



#### 0628

- 영상편집
  - 오전 : DEMS 편집 -<mark>**완**</mark> 
  - 오후 : 
    - 모빌리티 설치, 실행장면 촬영 - **편집할껀지 어떻게 보여질껀지, 시간 책임님과 회의**
      - **현재는 GPS 데이터 내가 따로 저장한 DB 에서 사용 - 나중에 어떻게 할건지?**
        - lat, lon데이터 0.5초 간격으로 출력하는 영상 캡쳐 필요
      - OBS 로 6개 vlc 영상 실행중
    - 고정형 - 아래 주소로 실행장면 촬영 - **어떤 화면 보여줄껀지, 시간 책임님과 회의**
      - cvlc rtsp://root:keti1234@192.168.225.30:88/videoMain
      - 우분투 화변 영상 캡쳐방법 : `ctrl+alt+shift+r `



#### 0629

- 오전 : 
  - 파워뱅크 테스트해보기
  - GPS 캡쳐 하기
  - 책임님 오시면 테스트
- 오후 : 
  - 모빌리티 
    - GPS 캡쳐
    - OBS 영상에 캡쳐본 입히기
  - 고정형 실행장면 촬영 캡쳐하기
- 완료!
- 파싱 진행



#### 0630

- 주말동안 파싱, 개인프로젝트 진행



#### 0704

- 파싱 : gps_parsing_test3.py



#### 0705

- 파싱 : gps_parsing_test4.py
  - 파싱하는 계산법 사용



#### 0706

- 파싱 : gps_parsing_test3.py
  - split 사용



#### 0707

- 파싱 : gps_parsing_test3.py
  - split 사용
  - 현재 데이터 정보 : 
    - 데이터당 11 byte(각 8bit)
    - Header : 
      - 0x55 로 시작
      - 0x50~0x59, 0x5a
    - Data : 
      - 8 byte
    - Check sum : 
      - 1byte



#### 0711

- 파싱 : gps_parsing_test3.py
  - split 사용
  - 현재 데이터 정보 : 
    - 데이터당 11 byte(각 8bit)
    - Header : 
      - 0x55 로 시작
      - 0x50~0x59, 0x5a
    - Data : 
      - 8 byte
    - Check sum : 
      - 1byte



#### 0711

- 파싱 :  gps_parsing_test3.py
  - 현재 데이터에서 데이터 길이(data_len)가 짧으면 짤리는 데이터들이 있음..
  - 온전한 데이터 507개/ 총데이터 3200여개
  - 진행 방향 : 
    - 110~140여개를 갖고있는 데이터 2개를 대상으로 파싱 테스트 진행할 것임
    - data_hex 의 string 형태에서 5551, 5552, 5553 등의 데이터로 구분되는데 이것을 다시 byte 로 변환하여 파싱 진행해야할듯



#### 0712

- db1은 hex 데이터가 55로 시작되서 잘 파싱됨
- 현재까지는 time 50 부분만 했고
- 데이터 시작이 55가 아니면 에러가 떠서 안되는것 **해결!**
- 아마 데이터의 길이 다르면 해석 안될듯 정크데이터 지워주기



#### 0713

- 정크데이터 필터링 데이터길이 맞춰주는거 진행하기
  - 40번째 줄 : chunk_size가 22개로 맞춰져잇는데 이거로 나누어서 떨어지는 것들만 남기면 될듯
  - 44번째줄
  - 둘중에 하나로 진행하기!



#### 0714

- 파싱 :  gps_parsing_test3.py
  - 정크데이터 필터링 데이터길이 맞춰주는거 진행하기
    - 40번째 줄 : chunk_size가 22개로 맞춰져잇는데 이거로 나누어서 떨어지는 것들만 남기면 될듯
  - 4,7 번 DB 같은 에러남
    - 정크 데이터 필터링함
- **가장 큰 문제점은 데이터가 온전하지 않다는 것.....**
  - 다시 데이터를 찍거나 기존에 파싱해놓은 데이터를 쓸 것..!!



#### 0717

- 파싱 :  /GPSParsing/gps_parsing_test.py
  - gps 부분 파싱중인데 계산이 틀린듯
- GPS 데이터
  - 구해야하는 값 : 37.12935283    /    127.0712005
  - 구해지는 값 : 3.70776117 7.76117   /   12.70427203 4.27203



#### 0717

- 파싱 :  /GPSParsing/gps_parsing_test.py
  - GPS 데이터
    - 구해야하는 값 : 37.12935283    /    127.0712005
    - 구해지는 값 : 37.12935283333333   /   127.0712005



#### 0721

- 데이터 정확도
  - 50 : O
  - 51 : X
  - 52 : X
  - 53 : O
  - 54 : X
  - 56 : X
  - 57 : O
  - 58 : O
  - 59 : O
  - 5a : 안나옴



#### 0724

- 데이터 수정중
- 데이터 정확도
  - 50 : O
  - 51 : X
  - 52 : X
  - 53 : O
  - 54 : X
  - 56 : X
  - 57 : O
  - 58 : O
  - 59 : O
  - 5a : 안나옴



#### 0725

- 내일부터 광운대 세팅
- 데이터 수정 잘 안됨



#### 0726

- 2시부터 세팅



#### 0727

- 광운대 협업 및 설치
- 5G 데이터 오류
  - **일단 파싱되서 저장된 자료들 보내는 API 만들기**



#### 0731

- 데이터 전송 API 문서 및 코드 작성
  - gpsdatacast_parsed.py
    - json_data 만들어서 전송하는거는 거의 완료
    - 받는대서 잘 받아지는지 확인 후 api 작성
- 광운대
  - 실험실 정리
  - 실행 되는지 확인



#### 0801

- 광운대
  - 실행 가능한지 확인
    - pw : coco2006
- 데이터 전송 API 문서 및 코드 작성
  - gpsdatacast_parsed.py
    - json_data 만들어서 전송하는거는 거의 완료
    - 받는대서 잘 받아지는지 확인 후 api 작성



#### 0804

- 레포지터리 정리 및 파싱 코드 정리



#### 0807

- 전체 코드 정리 및 일정 정리 



#### 0808

- 파싱 코드 수정 및 전체코드 정리



#### 0809

- gps 및 영상 데이터 전송 방법 연구 및 개선



#### 0821

- 코드 정리 및 개인일정 시작



#### 0822

- ci cd 데브옵스 공부 및 준비



#### 0823

- 젠킨스

  - 젠킨스는 소프트웨어 개발 시 지속적으로 통합 서비스를 제공하는 툴이다. CI(Continuous Integration) 툴 이라고 표현한다.

    다수의 개발자들이 하나의 프로그램을 개발할 때 버전 충돌을 방지하기 위해 각자 작업한 내용을 공유영역에 있는 저장소에 빈번히 업로드함으로써 지속적 통합이 가능하도록 해준다.



#### 0829

- 젠킨스 공부
- ci cd 사례 확인



#### 0830

- 사례 따라하기
- 재료비 구매
  - [MachLink] HDMI 2.1 케이블, 울트라 블루메탈, ML-H8K030 [3m] - 3개
  - [로지텍] 무선 미니키보드, K400 Plus 터치패드 [로지텍코리아 정품] [블랙] - 2개
  - [벡셀] 152000mAh, 550W 파워뱅크 캠핑용 보조배터리 [BPB-550W] - 2개
  - [INTEL] NUC11TNKi5 (기존에 구매했던 미니 PC)



#### 0901

- 근무기록표 발송 하기
- 데브옵스 공부



#### 0904

- CI//CD 공부
- 무선엣지 회의



#### 0905

- 작년 무선엣지 파악 및 올해 내용 구상



#### 1006

- 공인인증 시험 관련 회의
  - **M1- E1 리소스 정보(1)** 
    - **json 형식으로 반환**
    - 어떤 리소스 사용 가능한지 확인
      - 기존 클러스터링 되고 monitoring(프메, 그라파나) 되어있는 환경에서 확인 가능하면 확인하고 진행
  - **Jetson AGXOrin 서버 2대 설치(2)**
    - **기존 CCTV 3대 + 1개의 새로운 장치 추가 및 RTSP 주소(3)** 
    - 환경
      - Ubuntu 20.04 LTS
    - 질문 : 
      - ~~원래 밑에 오픈?~~
      - ~~파워 어댑터 필요~~



#### 1023

- **Jetson AGXOrin 서버 1대 설치중**
- 성과보고 문서작업완료



#### 1024

- Jetson AGXOrin 서버 2대 설치 완료하기
  - CUDA, pytorch 잘 설치 되었는지 확인 필요
- CCTV 는 일단 무선엣지 과제 API 연동 후 진행
  - 이미 신규 2대는 연결 되어있음
    - rtsp://root:root@192.168.0.12/axis-media/media.amp
    - rtsp://root:root@192.168.0.76/axis-media/media.amp?videocodec=h264&resolution=640x480



#### 1030

- 5G CCTV 오후에 업체가 실험실에 세팅 후 테스트
  - 필요 항목 : 
    - 외부망 인터넷(인텔리빅스 사용중인거 테스트때만 잠시 사용)
    - 파워선



#### 1102

- 5GCCTV 테스트 배드 실행
  - 중계 서버 양책임님 자리 외부 IP 사용 : 123.214.186.214
  - **카메라 URL : rtsp://ADMIN:1234@123.214.186.214:10101/live/main**
- 1108(수) 인텔리빅스 가져가서 설치 후 함께 연동 실행
- 모든 것 완료되면 오산가서 설치



#### 1103

- 카메라 연결 해제됨
  - 시간이 지나면? 
    - 15:29 분 시작
  - 이더넷 연결을 해제하면?
- 다음주 수요일 인텔리빅스 출장
  - GPS 및 영상 서버 2대, 영상 재전송 서버 1대
  - 5G CCTV 1대, 중계서버 1대



#### 1106

- 수요일 인텔리빅스 출장
  - GPS 및 영상 서버 2대, 영상 재전송 서버 1대
    - 파워 3 / 랜선 3 
  - 5G CCTV 1대, 중계서버 1대, 노트북
    - 파워 1 / 외부망 1(인텔리빅스)
  - 블루투스 키보드(마우스)
  - 모니터 1대
    -  파워 1 / HDMI 2개 정도

- 영상, GPS 전송 : 

  - 서버 주소 : 

    ```
    	# 재전송 서버
    192.168.0.54
    
    # 서버 1
    192.168.0.123
    
    # 서버 2 
    192.168.0.124
    
    # OBS 서버주소
    192.168.0.97
    ```

- 실행 순서 : 

  - 재전송 서버 프로그램 2개 실행
    - `/바탕화면/git/keti/Project1/4th/GPSDataCast/` 에서 `python3 gps_saved_edge.py` 실행
    - `/바탕화면/git/keti/Project1/4th/GPSDataCast/` 에서 `python3 gpsdatacast_Edge.py` 실행
  - 각 영상 서버에서 프로그램 1개씩 실행
    - `/keti/Project1/4th/GPSDataCast/`에서 `python3 gpsdatacast_parsed.py` 실행
    - 실행 후 3개, 4개 씩 전송
  - 재전송 서버 프로그램에서 모두 재전송 시작
  - 재전송 영상 주소 : 
    - rtsp://192.168.0.54:800**1(-7)**/videoMain



#### 1107

- 출장 준비 (아침)
  - 서버 3대 해체 및 선 정리해서 모아두기
    - 서버당 선 2개(파워, 랜선)
- 실증 하드웨어 스펙
  - 테이블
    - X : 1400
    - Y : 900
    - Z :450
  - 렉
    - X : 600
    - Y : 700
    - Z : 1000
  - 재전송 서버
    - X : 210
    - Y : 465
    - Z : 470
  - 서버 1,2
    - X : 235
    - Y : 490
    - Z : 450



#### 1110

- 출장 
  - 월요일 출장 신청 올리기 - 완료
  - 서버 재시작 관련 문서 작성해서 프린트해서 월요일에 전달 드리기 - 완료
- 영상-지피에스 싱크 맞추기!! 
  - edge-worker-01 -> edge-master-01 로 rtp 보내는거로 싱크 맞추기 진행
  - /data_sync_test
    - worker : gpsdatacast_parsed.py 실행
    - master : gps_saved_edge.py, gpsdatacast_Edge.py 실행



#### 1113

- 진행중
  - 영상-지피에스 싱크 맞추기!! 
    - edge-worker-01 -> edge-master-01 로 rtp 보내는거로 싱크 맞추기 진행
    - /data_sync_test
      - worker : gpsdatacast_parsed.py 실행
      - master : gps_saved_edge.py, gpsdatacast_Edge.py 실행
- 완료 : 
  - 영상 1개 추가, 고정 GPS 주소 갖게하는 1개 채널 늘리기
    - 오산시청 GPS 주소
      - Lat: 37.1500 Lon: 127.0775
    - 일단 07번 영상으로 진행하는데 나중에 사용하는 5G CCTV 영상 파일명을 지정해줘야함 : 
      - blackbox_08.avi
  - 기존 영상 8개 동시에 스트리밍되는 영상 편집 프로그램 사용예정
    - 서버 1대 필요 - NUC
    - 윈도우에서만 되는지 확인 필요
    - IP : 192.168.0.97
  - 공유기 1대 설정 
    - 포트포워딩 : 192.168.0.54:8089 열어둠



#### 1114

- 진행중

  - 영상-지피에스 싱크 맞추기!! 

    - edge-worker-01 -> edge-master-01 로 rtp 보내는거로 싱크 맞추기 진행
    - /data_sync_test
      - worker : gpsdatacast_parsed.py 실행
      - master : gps_saved_edge.py, gpsdatacast_Edge.py 실행
    - 방법 : 
      1. 영상이 마치면 어떤 이벤트가 발생해서 GPS 를 처음으로 돌리기
         - 영상이 끝나면 신호 발생시킬 수 있는지 먼저 확인
         - 해당 신호가 오면 GPS 쓰레드 재시작 하도록 진행
      2. ~~GPS 데이터가 끝나면 영상을 다시 실행해주기~~

  - GPS 오산시 고정 영상 찍기

    - GPS  값은 의미없는 값으로 진행 

      - **지금 프린트 영상 떠야함 !!! 정지영상이라도** - 완료

      - ```
        print("\n\n\n\n\n         lat: 37.1487  lon: 127.0773 \n\n\n\n\n")
        ```

    - Lat: 37.1487 Lon: 127.0773

  - ~~고정 영상 MP4 -> avi 로 변환하기**~~**

- **지금 사용중인 파일**

  - **gpsdatacast_parsed.py, gps_saved_edge.py, gpsdatacast_Edge.py**

- 이전 파일

  - gpsdatacast_parsed_v01.py, gps_saved_edge_v01.py, gpsdatacast_Edge_v01.py

**짧은 영상 구해서 08 번 파일로 저장 후 신호 발생 하는지 확인하기!!**



#### 1115

- 출장 준비
  - 빠진 준비물 없나 확인
  - 아침에 wifi 어댑터 챙겨야함!
- 가서 설치 내용
  - 무선 인터넷 사용 하여 서버 1,2,3에 모두 git update 해줘야함
    - /GPSDataCast 폴더에 **gpsdatacast_parsed.py, gps_saved_edge.py, gpsdatacast_Edge.py** 사용
  - 전송서버 1,2에 blackbox_08.mp4 파일 추가해줘야함(ssd에 있음)
  - 각 서버 재구동 후 잘 되는지 확인 필요 with 인텔리빅스
  - 8개 영상 스트리밍 서버 실행 후 영상들 각 주소로 변경하여 실행
    - 영상 사이즈 480 x 390



#### 1116

- 설치 완료 후 피드백
  - 추가 모든영상 재생 멈추는건 rtsp 반복재생떄문 -> 녹화 영상으로 대체
  - 서버 멈추면? -> 다시 가서 재생해줘야함..
  - **싱크 테스트 추후에 추가해주면 좋을듯(중요!)**



#### 1130

- 싱크테스트 재시작
- 진행중
  - 영상-지피에스 싱크 맞추기!! 

    - edge-worker-01 -> edge-master-01 로 rtp 보내는거로 싱크 맞추기 진행
    - /data_sync_test
      - worker : gpsdatacast_parsed.py 실행
      - master : gps_saved_edge.py, gpsdatacast_Edge.py 실행
    - 방법 : 
      1. 영상이 마치면 어떤 이벤트가 발생해서 GPS 를 처음으로 돌리기
         - 영상이 끝나면 신호 발생시킬 수 있는지 먼저 확인
         - 해당 신호가 오면 GPS 쓰레드 재시작 하도록 진행
      2. ~~GPS 데이터가 끝나면 영상을 다시 실행해주기~~

- **지금 사용중인 파일 /data_sync_test**
  - **gpsdatacast_parsed.py, gps_saved_edge.py, gpsdatacast_Edge.py**
- 이전 파일

  - gpsdatacast_parsed_v01.py, gps_saved_edge_v01.py, gpsdatacast_Edge_v01.py

**짧은 영상 구해서 08 번 파일로 저장 후 신호 발생 하는지 확인하기!!**



#### 1201

- 지금 사용중인 파일 /data_sync_test
  - gpsdatacast_parsed.py, gps_saved_edge.py, gpsdatacast_Edge.py
- ~~짧은 영상 구해서 08 번 파일로 저장 후 신호 발생 하는지 확인하기!!~~
  - ~~사용중~~
- 일단 영상, GPS 중에 어떤게 더 긴지 확인하고 진행
- vlc EOF 위주로 검색해서 진행하기!
  - **VLC documents : https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc-module.html**



#### 1204

- 리서치 : 
  - how to stream mp4 to rtp on python-vlc
  - how to loop mp4 file streaming to rtp on python-vlc
- 아니면 그냥 loop 돌리지말고 영상 끝나면 재시작 하도록 코드 변경하기



#### 1205

- 영상 끝나는 지점을 못찾고있음..
  - 찾음
  - 현재 while if문에서 찾았는데 여기서 쓰레드 모두 죽이고 다시 실행하면됨
    - 근데 쓰레드 멈춤 해도 다 잘 안죽음 왜?
    - while 문 때문에 app 작동을 안함
- **gps_parsed.db 오산에서 복사해야함!!**



#### 1206

- 완료 : 
  - 일단 gps, 영상 시작하고 종료하고 그 지점 찾는것 까지 완료
- 진행중 : 
  - 멈춤 버튼이 작동을 안함 이거 먼저 실행 시키고 진행해야할듯 
  - on_process 함수에서 그다음 재실행할것 해주면 될듯



#### 1207

- on process 함수 재실행 시작
- 금요일까지 해보고 월요일 출장 



#### 1211

- 내일 출장 준비, 프로젝트 재기동 필요하면 어떻게 하는지 다시 파악 ㄱㄱ



#### 1212

- 우분투 화면 녹화
  -  Ctrl+Alt+Shift+R   녹화 종료할때 도 동일하게 Ctrl+Alt+Shift+R
  - simple screan recorder 설치
    - sudo apt install simplescreenrecorder



#### 1213

- 싱크 맞추기 계속 진행해보고
- 오산 촬영 영상 편집 



#### 1214

- 영상편집 완료
- 싱크 맞추기



#### 1219

- 싱크테스트 진행 계속 이어서 하기



#### 1220

- 싱크 어디서 동작하는지 확인 완료
- 그 이후 어떻게 진행할지 리서치



#### 1222

- 싱크 테스트
  - gpsdatacaast_parsed.py 
    - run 파트에서 영상재생 종료되면 발생하는 시그널 확인
- 2,291,453 / 143,215/  *8,916,749*
- *11,017,475*



#### 1226

- 오산 출장 준비
- 목요일 오산 준비
- 싱크...



#### 1227

- 오산 출장 준비
  - 5G CCTV 설치하고 실행해보기
    - CCTV RTP로 바로 노트북(외부망)에 전송해보기
    - 되면 CCTV RTP -> 노트북(테더링)에 전송해보기
  - 블랙박스 고정 어떻게할지 고민하고 설치 고민해보기 실행까지
    - 5G 모뎀 사용 가능하지 확인하고 그거로 진행
      - No SIM 상태(=심 확인 필요)

