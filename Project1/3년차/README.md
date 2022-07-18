# Project 1 / 3년차

- 5G 기반 협력 대응 과제
- KETI + Intelivix 개발내용 통합에 중점



## 일정

- 6월 : 
  - TCP/IP 서버 샘플 만들기(8일까지)
  - 보고 후 과제에 필요한 Message Broker 제작
  - 6월 내 CCTV+5G+PC -----> Edge Server 형태로 RTSP 영상 전송
- 7월 : 
  - GPS 및 블랙박스관련 개발



## Repository

#### tcp_ip_sample

- server - client 간 채팅 수준의 socket 통신



#### proto

- tcp/ip 서버를 중심으로 sender에서 client 로 message를 전송
- 문제발생 : 
  - tcp/ip 서버가 계속 열려있게 하기



#### multiple_client

- 다수의 클라이언트에서 1개의 서버로 메시지 전송
  - server : socket 서버
  - sender : edge server 로 메시지를 전달
  - device1,2,3 : msg 를 최종적으로 전달받을 device



#### EMDS 구성

- DB
  - Device
    - id
    - type
  - Edge
    - id
    - type
    - ip
- Device-Edge 연결제어



## reference

- [python sqlite3 참고 블로그](https://hleecaster.com/python-sqlite3/)
- [python socket 채팅 프로그램](https://seolin.tistory.com/98?category=762768)
- [VLC CLI 사용 예제](http://akshayc.com/blog/Stream-Audio-via-VLC/)



## 진행 단계(daily)

#### 0607

- 전체회의
  - 6월 : 
    - **TCP/IP 서버 샘플 만들기(8일까지)** - 기존에 했던 소켓통신
    - 보고 후 과제에 필요한 Message Broker 제작
    - 6월 내 CCTV+5G+PC -----> Edge Server 형태로 RTSP 영상 전송
  - 7월 : 
    - GPS 및 블랙박스관련 RTSP  영상 전송 개발



#### 0608

- TCP/IP 서버 샘플 완성 후 보고
  - 기본 샘플은 완성
  - ~~채팅 샘플 만들어보고 완성하면 보고하기~~ 완성



#### 0609

- 어제 회의 토대로 socket 통신 구성해보기 1단계
  - server 한개 - 클라이언트는 2종류 여러개가 메시지를 주고받게된다
  - multiple_client 폴더에서 진행중
    - json 으로 데이터를 주고받음
    - type 으로 device와 server 를 구분
    - 현재 server 와 device 로 구분되서 보내지고 있는거까지 확인
  - 앞으로 해야할 것 : 
    - device에 전달할 데이터 저장햇다가.. <mark>선입선출 가능해야함</mark>
      - DB사용?
      - 아니면 다른방법..? 
    - device 에서 요청이오면 데이터 전달하기



#### 0614

- 앞으로 해야할 것 : 
  - device에 전달할 데이터 저장햇다가.. <mark>선입선출 가능해야함</mark>
    - DB사용?
    - 아니면 다른방법..? 
  - device 에서 요청이오면 데이터 전달하기



#### 0615

- 선입선출 가능하게 DB연동 - SQLite3 사용중
- 아래 내용대로 일단 완성 후 차일 보고
  - ![image](https://user-images.githubusercontent.com/58541635/173778018-02f932f9-27df-44dd-ae73-e22dbc48085c.png)



#### 0616

- 오전, 논문 피드백
- ~~오후에 보고 드린 후 진행~~ 내일 오후 보고



#### 0620

- Message Broker 보고 완료
- 6월 내 CCTV+5G+PC -----> Edge Server 형태로 RTSP 영상 전송 기능 개발 시작
  - 일단 카메라와 PC 연동 진행중
  - 현재 사용중인 카메라 주소
    - **rtsp://keti:keti1234@192.168.0.46:88/videoMain**
  - 한 것
    - yang_ex 를 AP 에 연결해서 AP를 통해서 사용 가능하게끔 하기([무선 브릿지 - 무선 wifi 이용해서 공유기에 무선 wifi 가능하게 하기](https://favoritepps.tistory.com/49))
      - iptime 주소 : 192.168.0.78
      - 현재 iptime(2.4G) 에 카메라와 컴퓨터 연결 완료!



#### 0621

- 해야할 것
  - 서버1 : rtsp -> rtp(?) 로 서버2로 전송
  - 서버2 : 받은 rtp를 rtsp 로 다시 스트리밍
  - 두개가 완성되면 서버2에서 돌아가고있는 스트리밍 서버가 잘 돌아가고 스트리밍 할 수 있는지 확인



#### 0623

- 할 것
  - ~~카메라 작동 확인~~ 확인
  - 서버1 : rtsp -> rtp(?) 로 서버2로 전송
  - 서버2 : 받은 rtp를 rtsp 로 다시 스트리밍
- 완료 : 
  - 서버1 에서 동영상파일을 스트리밍 후 서버2 에서 재생 완료(같은 네트워크일때만 됨)
    - 주소 : rtp://239.0.0.1:5004 
    - 문제 : 
      - 스트리밍 끊김
      - 다른 네트워크일때 하는 방법 찾아야함!
- 문제점 : 
  - 서버1(공유기) - 서버2(핸드폰 테더링) 둘 사이간 접속이 안됨..
  - rtsp 를 받아와서 스트리밍서버로 만드는게 안됨



#### 0624

- 문제점 : 
  - ~~서버1(공유기) - 서버2(핸드폰 테더링) 둘 사이간 접속이 안됨.. // 네트워크 문제~~같은 공유기 내 ip 사용
  - ~~rtsp 를 받아와서 스트리밍서버로 만드는게 안됨 // ?~~ **트랜스코딩 활성화 안하고 하니까 됨**
- 완료 : 
  - 서버1 : rtsp -> rtp 로 서버2로 전송/스트림
    - 서버2의 url 로 unicast 전송
    - 주소 : rtp://192.168.0.50:5004 
  - 서버2 : 받은 rtp를 rtsp 로 다시 스트리밍
    - 서버1과 같이 rtsp 스트림서버로 
    - 주소 : rtsp://192.168.0.50:8554/videoMain



#### 0627

- 위 완료된 내용으로 Linux 환경에서 실행
  - 미니컴 2대, 카메라 1대 사용
  - ip는192.168.0.XX 사용할 것
  - 터미널 명령어로 vlc 실행해서 서버 구성



#### 0629

- 리눅스 환경에서 서버 구성
  - 미니컴 2대, 카메라 1대 사용
    - keti0 : 192.168.0.59 - rtsp 받아서 rtp 로 keti1에 전송
    - keti1 : 192.168.0.60 - rtp 받아서 rtsp 스트리밍하는 서버
    - 카메라 : rtsp://keti:keti1234@192.168.0.46:88/videoMain
  - ip는yang_ex, 192.168.0.XX 사용할 것
  - 터미널 명령어로 vlc 실행해서 서버 구성



#### 0630

- 위 서버구성과 vlc 설치 완료 후 카메라 작동 확인 완료
- 기존 윈도우 서버대로 커맨드 명령 환경에서 진행
  - 카메라 연결 완료
- 완료 :
  - keti0 : 192.168.0.59 - rtsp 받아서 keti1에 전송 - rtp://192.168.0.60:5004
  - keti1 : 192.168.0.60 - rtp 받아서 rtsp 스트리밍하는 서버 - **rtsp://192.168.0.60:8554/videoMain(최종 주소)**
  - 카메라 : rtsp://keti:keti1234@192.168.0.46:88/videoMain
- 문제 : 
  - 스트리밍 지속이 안됨..연결은 되어있는 상태



#### 0701

- vlc 앱으로는 구동 완료

- 커맨드라인에서 하는 방법 서칭하고 실행

- 커맨드 라인으로 실행

  - keti0 : 

    - 주소 : 192.168.0.59
    - 역할 : 카메라에서 rtsp 받아서 keti1에 rtp 전송하는 서버
    - 명령어 : `cvlc -vvv rtsp://keti:keti1234@192.168.0.46:88/videoMain --sout="#rtp{dst=192.168.0.60,port=5004,mux=ts}" --no-sout-all --sout-keep  `

  - keti1 : 

    - 주소 : 192.168.0.60
    - 역할 : rtp 받아서 rtsp 스트리밍하는 서버

    - `cvlc -vvv rtp://192.168.0.60:5004 --sout="#rtp{sdp=rtsp://:8554/videoMain}" --no-sout-all --sout-keep`



#### 0704

- 재전송 서버 지속이 얼마나 되는지 확인
- 카메라 세팅



#### 0705

- 카메라 오디오 제거하기
  - 제거 안됨
- 프레임 레이트 확인하기
  - 30으로 수정완료
- 초소형 PC 성능 좋은거 찾아보기
  - 천차만별...기본 100이상 [예시](https://www.usashop.co.kr/goods/goods_view.php?goodsNo=1000035135&inflow=naver&NaPm=ct%3Dl57mtiwg%7Cci%3D760498f05ee6e5f686bb3ab4b4313631dfbad647%7Ctr%3Dslsl%7Csn%3D1212958%7Chk%3De89be7be25eeaa0dcea6c83032891ec9722ab70e)
- 블랙박스 wifi  가능한것 찾아보기
  - 기본적으로 앱을 통해 영상 스트리밍 및 저장
  - [파인뷰](https://brand.naver.com/finevu/products/6022272258?NaPm=ct%3Dl57slkvc%7Cci%3Dc0b6646e785120697e5128b27f95aa0c93364f5a%7Ctr%3Dplac%7Csn%3D156008%7Chk%3Decd30e120cb48e84e4cf00bbb3ce59be06cf6e86)
  - [한라홀딩스 오토비](https://www.11st.co.kr/products/2707281985?NaPm=ct=l57srgag|ci=7af5b8d9ba760da645730cd287effca710adc51b|tr=slsbrc|sn=17703|hk=a5e86f68de63cb7011c5c230b32ab591a959ab0d&utm_term=&utm_campaign=%B3%D7%C0%CC%B9%F6pc_%B0%A1%B0%DD%BA%F1%B1%B3%B1%E2%BA%BB&utm_source=%B3%D7%C0%CC%B9%F6_PC_PCS&utm_medium=%B0%A1%B0%DD%BA%F1%B1%B3)



#### 0707

- 회의 내용
  - 앞으로 진행할 내용 : 
    - 완성한 Device(CCTV-Server) --- TCP/IP Server --- Edge Server --- EDMS 통합하기
    - EDMS 부분 구성하기
      - DB 추가
      - Device 등록
      - Edge 등록
      - Device-Edge 간 연결제어
    - 결과물 : EDMS에서 명령을통해 Edge에서 RTSP Server 가 구성되고 재생되어야함
- 확인한 내용 : 
  - Edge 에서 rtsp 서버가 구성되기 전 실행시키고 무한 루프를 돌려놓는건 불가능



#### 0708

- 진행중 :
  - 하드웨어 설정 : 
    - 메인 pc : EDMS (TCP/IP 서버 보유)
    - keti0 : CCTV와 연결되어있는 서버
    - keti1 : Edge 서버 역할로 최종 RTSP 서버
  - EDMS 부분 구성하기
    - **DB 추가** (완료)
    - **Device 등록** 
    - **Edge 등록** 
    - Device-Edge 간 연결제어
- 진행해야할 것 : 
  - Device 및 Edge 등록 간단하게 구현되어있는거 추후 수정해야함
  - ~~socket 통신이 다른 ip로 전달이 안되는데 해결해야함~~ 해결은됨



#### 0714

- socket 통신 되니까 이제 연결제어부분 시작
- 진행중 : 
  - `tcp_server.py` : edms / socket 통신으로 메시지(ip 등)을 전달하고 DB와 연동
  - `msg_send.py` : edms / edms에서 msg를 보내는 역할
  - `device1.py` : cctv-device / cctv와 연결되어있는 server로 d_id 를 갖고있고 해당 정보로 cctv의 rtsp주소와 edge server의 ip 를 응답받는다
- 문제 : 
  - 내부망으로 바껴서 IP, 네트워크 변화 있음
    - 동시에 외부망(wifi) 사용해서 해결
  - ~~`tcp_server.py` 에서 mid 변수가 int 가 아닌 str 로 인식이됨..(기존서버에서는 잘됨)~~



#### 0715

- ~~14일 문제에서 mid 변수 해결 후 진행~~ ip 보낼때 send.py 에서 fetchone()[0] 해줘서 해결
- device.py에 rtp 전송 명령어 잘 실행되는지 확인해야함
- 문제 : 
  - keti1 (rtp 받아서 rtsp로 재전송하는 서버)에서 rtp -> rtsp 재전송하려면 이벤트발생 트리거가 필요함..



#### 0718

- 문제 : 
  - keti1 (rtp 받아서 rtsp로 재전송하는 서버)에서 rtp -> rtsp 재전송하려면 이벤트발생 트리거가 필요함..
    - /tcp_ip/edge.py 만들어서 해볼까하는데 더 생각해야됨
      - device.py 에서 cvlc 명령이 실행된 뒤에 edge.py 에서 실행되어야함!!
    - 어떻게 해결할지 고민해보기 + 보고드리기
- 진행중 : 
  - edge 와 tcp server 간 통신
  - device.py 에 cvlc 명령 부분에서 rtsp주소와 edge server주소를 변수로 입력하게끔 변경해야함

