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

`blackbox_save_GUI.py`로 GPS 데이터, 영상 데이터 저장중

- **GPS 데이터 저장**
  - 로우 데이터 : 앱에 `gps_(루트번호)` 입력 후 `저장` 버튼 누르면 차량용 서버 내 `gps_(루트번호)` db에 저장됨
  - 정제된 데이터 : 앱에 `gps_(루트번호)` 입력 후 `저장` 버튼 누르면 edge서버에 `gwg_server.py` 프로그램과 연동되어 `gps_(루트번호)`  테이블이 생성되면서 저장됨
- **영상 데이터 저장**
  - `blackbox_(루트번호)` 입력 후 `저장` 버튼 누르면 차량용 서버에 저장됨(avi 형식)



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