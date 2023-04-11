# README

- 5G기반 선제적 위험대응을 위한 예측적 영상보안 핵심기술 개발 (4차년도)
- 오산시와의 실증, 시연 중점의 설계 및 개발
- 인텔리빅스와의 연동



## 일정

- 3월 : 
  - 기존 테스트베드 복구 및 실행
  - 5G 단말기 복구 및 서버 연동



## Repository

#### 폴더

- 내용 적으면됨



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
  - 블랙박스
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

