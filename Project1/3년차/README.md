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
- [C++ printf 예시](https://shaeod.tistory.com/283)
- [데이터 형식 범위](https://learn.microsoft.com/ko-kr/cpp/cpp/data-type-ranges?view=msvc-170)
- 



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



#### 0719

- cvlc 명령부분 %s 로 해결
- edge와 tcp 서버간 통신 완료
- 문제점 : 
  - 지금은 같은 공유기 및 wifi 로 실행하는데, 나중에는 edms 서버 및 edge는 다른 주소의 인터넷을 쓸텐데 통신이 가능한지?
- 진행해야 할 것 : (목요일까지 말씀드리기)
  - 5G 모뎀 찾아보기
  - 위치정보 전달, 와이파이로 영상 끌어올수있는 블랙박스



#### 0720

- 5G 모뎀
  - LG CNR-5G100
    - 링크 : http://www.lguplusme.co.kr/page/s2_28
    - 200G/99,000원
    - 2.4GHz/5GHz 두가지 Wifi 제공
  - KT 5G egg
    - 링크 : https://shop.kt.com/unify/mobile.do?prodNo=WL00057791&pplId=0813
- 블랙박스
  - GPS 위치정보 :
    - 블랙박스 구매시 GPS모듈을 구매가능
    - 그에 따른 위치정보 데이터를 활용하는 방법은?
  - wifi 로 영상 데이터 : 
    - wifi 동글 함께 구매 필요
    - 모든 제품들이 해당 회사의 앱, 뷰어 등을 설치 후 다운로드
  - 제품링크 : 
    - 파인뷰 :
      - 링크 : https://brand.naver.com/finevu/products/6022272258
      - 5GHz 속도로 업데이트 및 영상 다운로드
    - 오토비 : 
      - 링크 : http://www.11st.co.kr/products/2707281985/share
    - 드림아이 : 
      - 링크 : https://smartstore.naver.com/gnetsystem/products/6817571059
    - Type S(미국)
      - 링크 : https://typesauto.com/products/type-s-drive-360-dash-cam-live-stream-bt530211
      - 자체 앱 사용으로 유튜브, facebook 에 스트리밍 가능
    - Black vue(미국)
      - 링크 : https://shop.blackvue.com/product/dr750x-2ch-dms-lte-plus/
      - 자체 Cloud 앱에 저장 가능
- 논문
  - 웹서비스 기반 자동차 블랙박스 온라인 사고기록 확인 시스템 개발
    - 링크 : https://koreascience.kr/article/CFKO201423965829244.pdf
  - 모바일 클라우드를 이용한 차량용 블랙박스 영상 통합관리 시스템
    - 링크 : https://koreascience.kr/article/JAKO201333651337175.pdf
  - 차량용 블랙박스를 활용한 교통위반신고 자동화 방법
    - 링크 : https://koreascience.kr/article/JAKO201433552234030.pdf



#### 0721

- 5G 모뎀 및 블랙박스 보고드리기



#### 0725

- 모뎀 블랙박스 더 리서치해보기
- 내일부터 포트폴리오 준비 및 깃허브 좋은 예시 찾아서 차근차근 정리하기



#### 0726

- 블랙박스 리서치
- 모뎀 리서치



#### 0727

- 리서치 계속 진행 후 정리해서 자료로 남기기
- 블랙박스
  - GPI / 차량용 IP 카메라 
    - http://www.gpikorea.com/kr/bbs/board.php?bo_table=pro03_kr&wr_id=2
    - RTSP, OnVIF, POE 지원



#### 0801

- 블랙박스 
  - GPI Korea / 차량용 IP 카메라 
    - http://www.gpikorea.com/kr/bbs/board.php?bo_table=pro03_kr&wr_id=2
    - RTSP, OnVIF, POE 지원
  - 아이디스 / 소형 IP 카메라+모듈
    - http://item.gmarket.co.kr/DetailView/Item.asp?goodscode=2367214347&GoodsSale=Y&jaehuid=200001169&NaPm=ct%3Dl6a6rkog%7Cci%3Dc6282270f259f864f715e5da14a668449750fd95%7Ctr%3Dslsl%7Csn%3D24%7Chk%3Da5e1d6bf3c817f90e17154e21837e75a8bb8eb5e
    - RTSP, OnVIF, POE 지원
- GPS 
  - GPS 수신기 리서치
  - GPS 수신기 활용하여 좌표를 사용할 수 있어야함



#### 0802

- GPS 
  - 아두이노 NEO-6M
- GPS 대체 코드
  - Geoplugin 사용해서 IP 로케이션 찾는 방법 : 
    - 해당 ip 를 가지고 위치를 찾는 방식
    - gps 폴더 내 `geo.py`
    - 집에 가면서 위치 이동될때마다 해보기
  - ~~카카오 API 사용~~ 주소 필요해서 사용 안함
    - 키 : 2e9a9ab884c6c5fbc7d5e13bb9b4818b



#### 0803

- GPS 리서치
  - [라즈베리파이를 이용한 차량 추적 시스템 연구](http://journal.dcs.or.kr/xml/24195/24195.pdf)
    - 라즈베리 파이와 인터넷에 연결되는 스마트폰, 인터넷에 연결된 서버가 필요
    - 라즈베리 파이는 스마트폰의 핫 스폿을 통하여 서버에 접속하여 수 배 차량에 대한 정보를 받고
    - 카메라와 GPS 정보를 핫 스폿을 통하여 서버에게 전송하는 구조



#### 0804

- GPS 및 블랙박스 리서치
  - 블랙박스(소형 RTSP 카메라)
    - 아이디스 NC-V4211XJ
      - 설명 링크 : https://www.idisglobal.com/index/product_view/3058
      - 구매 링크 : http://auction.kr/iCdf_gm
    - GPI Korea / 차량용 IP 카메라 
      - http://www.gpikorea.com/kr/bbs/board.php?bo_table=pro03_kr&wr_id=2
      - 카메라에 무선라우터와 유선연결 필요
      - 구매 시 업체 연락 필요(구매 사이트 없음) : 29만원/50대 미만
  - GPS
    - 라즈베리파이 GPS 모듈 EZ-0048
      - 구매 링크 : https://smartstore.naver.com/mcuboard/products/5665912954
      - 사용법 : https://wiki.52pi.com/index.php?title=EZ-0048
      - GPS와 기존 서버를 바로 연결해서 사용 가능할듯함



#### 0808

- 특허 아이디어
- 차량용 IP 전방 카메라
  - 모델명 : GPCF-673A1GN
  - 업체명 : GPI Korea
  - 설명 링크 : http://www.gpikorea.com/kr/bbs/board.php?bo_table=pro03_kr&wr_id=2
  - 구매 연락처 : sales@gpi360.com
- GPS 모듈
  - 모델명 : NT114990732
  - 업체명 : Seeed
  - 컴퓨존 구매 링크 : http://www.compuzone.co.kr/product/product_detail.htm?ProductNo=462441&banner_check=naver&NaPm=ct%3Dl6kd5vrc%7Cci%3Dfd093879167a6893fee390d5f954430d0b4bf456%7Ctr%3Dsls%7Csn%3D116863%7Chk%3D8239548a655fb62b1811706391ec2596c77cc22a
- 앞으로 일정
  - 카메라, GPS 구매 되는데로 개발 착수
    - ~~GPS 따로 한개 구매 후 책임님께 구매보고~~
  - 기존 했던 CCTV 끊김 현상 step by step 으로 어느 부분에서 끊기는지 확인 및 문제점 찾기
    - 유선으로도 연결해보기



#### 0809

- 기존 했던 CCTV 끊김 현상 step by step 으로 어느 부분에서 끊기는지 확인 및 문제점 찾기
- GPS 도착하면 GPS 데이터 사용법 및 전송하는 테스트
- 인텔리빅스에 CCTV 스트리밍 전달해야하는데 확실하게 되는지 알아보기
  - 포트포워딩?
- POSCAM 카메라 테스트
  - 카메라-PC 무선 연결 :
    1. 그래픽 카드O, 고사양 PC : 끊김 거의 없음
    2. 미니 PC : 끊김현상 심함
  - 카메라-미니PC 유선 연결 : 
    - 스트리밍 주소 자동으로 변경됨 : rtsp://keti:keti1234@192.168.0.73:88/videoMain
    - 미니 PC로만 진행했는데 **끊김현상 없음**
  - 카메라-미니PC 유선연결 후 무선 rtp 재전송 :
    - 미니PC 2에서 rtp 주소 : rtp://192.168.0.60:5004
    - 결과 : **끊김현상 심함**
  - 카메라-미니PC 유선연결 후 미니PC 2로  무선 rtp 재전송 :
    - 미니PC 2에서 rtp 주소 : rtp://192.168.0.75:8080
    - 결과 : **끊김현상 심함**
  - 카메라-미니PC 유선연결 후 미니PC 2로 유선 rtp 재전송 :
    - 미니PC 2에서 rtp 주소 : rtp://192.168.0.75:8080
    - 결과 : **끊김현상 없음**
- AXIS 돔형 카메라 테스트
  - 카메라-PC 유선연결
  - 유선 연결 후 rtp 전송
    - cvlc -vvv rtsp://root:keti@169.254.147.5/onvif-media/media.amp?profile=profile_1_h264&sessiontimeout=60&streamtype=unicast --sout="#rtp{dst=192.168.0.60,port=5004,mux=ts}" --no-sout-all --sout-keep
    - **위 주소로 rtp전송, 미니 pc에서 rtsp 직접 스트리밍 모두 안됨...왜?**
- AXIS 카메라 테스트
  - 카메라-PC 유선연결



#### 0810

- AXIS 돔형 카메라 테스트
  - 카메라-PC 유선연결
    - 윈도우 pc에서는 연결 완료
  - 유선 연결 후 rtp 전송
    - cvlc -vvv rtsp://root:keti@169.254.147.5/onvif-media/media.amp?profile=profile_1_h264&sessiontimeout=60&streamtype=unicast --sout="#rtp{dst=192.168.0.60,port=5004,mux=ts}" --no-sout-all --sout-keep
    - **위 주소로 rtp전송, 미니 pc에서 rtsp 직접 스트리밍 모두 안됨...왜?**
      - 192.168.0.94 주소 사용법 알아보기
- GPS 모듈 변경
  - 변경 할 모듈 찾고
  - 주문 취소 요청 드려야함!
  - **일단 현재 제품으로 우분투 사용가능하다고 하여 진행중인데 데이터 완벽하게 안받아짐**



#### 0811

- GPS 모듈 데이터 받기 (EZ-0048)
  - terminal 에서 안되면 일단 python 코드로 가능한지 해보기!!
    - python 도 gpsd 데이터를 사용하는데 데이터가 온전하지 않음..
  - 참고 사이트
    - 제품 정보(한글) : https://fishpoint.tistory.com/6484
    - wiki 및 튜토리얼 : https://wiki.52pi.com/index.php?title=EZ-0048
    - 기타 튜토리얼 : https://www.dfrobot.com/blog-772.html
- AXIS 돔형 카메라 진행하기
  - (유선) 내 자리에 있는 카메라 주소 : 
    - 
  - (무선) 실험실에 있는 카메라 주소 : 
    - rtsp://192.168.0.93/onvif-media/media.amp?profile=profile_1_h264&sessiontimeout=60&streamtype=unicast



#### 0816

- AXIS 돔형 카메라
  - 유선연결 : 
    - 카메라 주소 :  rtsp://root:keti@192.168.0.94/onvif-media/media.amp?profile=profile_1_h264&sessiontimeout=60&streamtype=unicast
    - 상태 : 
      - 미니PC1 에 연결
      - 3) 느림
  - 무선연결(iptime 사용) : 
    - 카메라 주소 :  rtsp://root:keti@192.168.0.94/onvif-media/media.amp?profile=profile_1_h264&sessiontimeout=60&streamtype=unicast
    - 상태 : 
      - 메인 PC에 연결
      - 1) http 연결 시 제일 딜레이가 적고
      - 2) onvif 시 조금 느림
      - 4) vlc 로 재생하는게 제일 느림
- **AXIS 카메라**
  - 주소 : rtsp://root:ketiabcs@192.168.0.120/axis-media/media.amp
  - 무선 테스트 : 
    - PC1 -> PC2 rtp 전송 : 가까이 사물있으면 끊김, 움직이는 사물이 멀리 있으면 덜 끊김
    - 메인PC -> PC2 rtp 전송 :  끊김 훨씬 덜함
- 진행 상황 : 
  - 무선과 유선으로 연결해서 스트리밍 상태 확인 완료
  - 유선 연결한 PC1 에서 PC2 로 재전송 해보기
  - 보고 완료 후 오후에 양책임님 컴퓨터에 셋업해서 확인 필요
- **GPS 데이터 받아오기**
  - 참고 사이트
    - 제품 정보(한글) : https://fishpoint.tistory.com/6484
    - wiki 및 튜토리얼 : https://wiki.52pi.com/index.php?title=EZ-0048
    - 기타 튜토리얼 : https://www.dfrobot.com/blog-772.html
  - gps 계속 no fix 오류나는데 가져가서 테스트해보기



#### 0817

- GPS 데이터 사용하기

  - 야외(옥상)에서 Mac OS 로 했더니 정보 잘 받아옴

    ```
    $GPRMC,071340.000,A,3734.8516,N,12653.2972,E,0.14,55.26,170822,,,A*54
    $GPVTG,55.26,T,,M,0.14,N,0.26,K,A*08
    $GPGGA,071341.000,3734.8517,N,12653.2973,E,1,8,0.99,79.5,M,19.2,M,,*61
    $GPGLL,3734.8517,N,12653.2973,E,071341.000,A,A*5D
    $GPGSA,A,3,15,24,13,23,30,05,20,18,,,,,1.28,0.99,0.81*0C
    $GPGSV,3,1,10,15,73,312,21,13,57,039,28,05,55,086,42,18,50,300,39*71
    $GPGSV,3,2,10,24,33,188,34,20,22,111,39,23,19,302,37,29,14,232,*71
    $GPGSV,3,3,10,30,12,040,29,193,,,*7C
    $GPRMC,071341.000,A,3734.8517,N,12653.2973,E,0.13,20.24,170822,,,A*52
    $GPVTG,20.24,T,,M,0.13,N,0.24,K,A*0D
    $GPGGA,071342.000,3734.8518,N,12653.2972,E,1,8,0.99,79.5,M,19.2,M,,*6C
    $GPGLL,3734.8518,N,12653.2972,E,071342.000,A,A*50
    $GPGSA,A,3,15,24,13,23,30,05,20,18,,,,,1.28,0.99,0.81*0C
    $GPGSV,3,1,10,15,73,312,20,13,57,039,27,05,55,086,42,18,50,300,39*7F
    $GPGSV,3,2,10,24,34,188,34,20,22,111,39,23,19,302,37,29,14,232,*76
    $GPGSV,3,3,10,30,12,040,29,193,,,*7C
    $GPRMC,071342.000,A,3734.8518,N,12653.2972,E,0.05,9.37,170822,,,A*61
    $GPVTG,9.37,T,,M,0.05,N,0.10,K,A*34
    $GPGGA,071343.000,3734.8518,N,12653.2972,E,1,8,1.00,79.4,M,19.2,M,,*6D
    $GPGLL,3734.8518,N,12653.2972,E,071343.000,A,A*51
    $GPGSA,A,3,15,24,13,23,30,05,20,18,,,,,1.71,1.00,1.38*02
    $GPGSV,3,1,10,15,73,312,20,13,57,039,34,05,55,086,42,18,50,300,39*7D
    $GPGSV,3,2,10,24,34,188,33,20,22,111,39,23,19,302,37,29,14,232,*71
    $GPGSV,3,3,10,30,12,040,29,193,,,*7C
    $GPRMC,071343.000,A,3734.8518,N,12653.2972,E,0.00,46.79,170822,,,A*54
    $GPVTG,46.79,T,,M,0.00,N,0.01,K,A*00
    $GPGGA,071344.000,3734.8519,N,12653.2972,E,1,8,0.99,79.5,M,19.2,M,,*6B
    $GPGLL,3734.8519,N,12653.2972,E,071344.000,A,A*57
    $GPGSA,A,3,15,24,13,23,30,05,20,18,,,,,1.28,0.99,0.81*0C
    $GPGSV,3,1,10,15,73,312,21,13,57,03%
    ```



#### 0818

- 위 GPS 데이터 사용해 python 프로그램 만들기
  - /3년차/gps/gps_data.py 
    - 정확한 전자회관 위치 정보 : 37.580900 N, 126.888402 E
    - GPS가 전달받은 정보 : 37.348517 N, 126.532973 E
    - 방법 : 
      - pyserial, pynmea2 모듈 사용
        - pyserial : serial 데이터를 받아옴
        - pynmea2 : 받아온 gps GPGGA 데이터를 Parsing 해서 사용가능
    - **parseGPS() 에 if 문에 안들어감 문제 해결해야함**
- 프로젝트 총 네트워크 상황
  - 카메라-PC
    - 유선
  - Edge Server
    - 외부망 설정(수동으로 설정 해줘야함) - 엣지 서버
      - IP : 123.214.186.162
      - Sub : 255.255.255.128
      - GW : 123.214.186.129
      - DNS : 128.126.63.1 / 210.220.163.82 / 210.94.0.73 / 210.20.163.82



#### 0819

- CCTV 거치대 찾아보기

- 미니 PC 찾아보기

  - [Minix Technology Limited] NEO N42C-4 Plus N4100([링크](http://www.compuzone.co.kr/product/product_detail.htm?ProductNo=809496&BigDivNo=&MediumDivNo=1005&DivNo=))

    - 사이즈 : 139 * 139 * 35 mm
    - 가격 : 305,000원

  - [GIGABYTE] BRIX GB-BMCE-4500C([링크](http://www.compuzone.co.kr/product/product_detail.htm?ProductNo=856164&BigDivNo=&MediumDivNo=1005&DivNo=))

    - 사이즈 : 116.52 * 103 * 56.22 mm

    - 가격 : 198,000원

  - [ECS] LIVA Q1L N4200([링크](http://www.compuzone.co.kr/product/product_detail.htm?ProductNo=878676&BigDivNo=&MediumDivNo=1005&DivNo=))

    - 사이즈 : 74 * 74 * 34.6 mm
    - 가격 : 279,000원

  - Mele 미니 PC(구매대행)

    - 사이즈 : 131 * 81 * 18.3 mm
    - 가격 : 351,700원
    - 링크 : https://smartstore.naver.com/alishop/products/6286680846



#### 0822

- 도시락
  - https://docs.google.com/forms/d/e/1FAIpQLSfqooy9va0_Iq3CuInAI04sY6Pt__dBqNsUSpaT8sfb5nDc_g/viewform
- oneM2M 교육 참석
  - 일시 : **8월 22일(월) 08시 50분 ~17시 (1일 전일 교육, 중식 제공)**
  - 장소 : **한국과학기술회관 2관 지하1층 중회의실 5**
          (2호선 강남역 12번 출구, 국기원사거리)
  - 주제 : oneM2M 개발, 연동기술 세미나



#### 0823

- 5G 모뎀 사용 가능
  - 설계 : 
    - 미니컴퓨터(뒷자리)를 5G모뎀 유선 연결된 PoE에 연결
    - 카메라(PoE 카메라 아님) 유선연결
    - 엣지서버(실험실)로 rtp 전송
- **구성도**
  - Foscam 카메라
    -  IP : rtsp://root:keti1234@192.168.225.30:88/videoMain 
    - 미니PC와 유선연결
  - 미니PC : 
    - 5G
    - IP : 192.168.225.27
    - 5G라우터를 통해 Edge Server 로 rtp 전송
      - rtp://123.214.186.162:5004
  - Edge Server
    - 유선 외부망
    - IP : 123.214.186.162
    - 유선 외부망을 통해 rtsp 스트리밍
      - rtsp://123.214.186.162:8554/cctv1
- GPS 진행
  - 미니PC(차량용 서버)에서 Edge Server 로 gps 정보 ~~1초마다 전송~~ 생성될 때 마다 전송
  - Edge Server 에서 gps 데이터를 보관해야함
  - GPS 정보 : 
    - 연결된 차량 or cctv ID ---> 서버의 username 으로 대체
    - UTC 시간
    - GPS 정보



#### 0824

- GPS 데이터 client-server (소켓 사용)
  - gps_client.py
    - 현재 데이터는 모두 생성하고 사용가능
    - 데이터 json 형태로 담아서 보냄
  - gps_server.py
    - ~~기본적 서버부터 구성부터 해야함~~  소켓서버로 구성
    - server 에 데이터 json 으로 전달 받으면 저장하는거부터 하면됨



#### 0825

- GPS server 에서 데이터 받기까지는 완료, 저장하는거 하면됨



#### 0826

- 인텔리빅스에서 사용 가능한 rtsp 주소 및 gps rest api

  - 카메라 주소 : rtsp://123.214.186.162:8554/videoMain

  - gps 요청 : http://123.214.186.162:8088/get_gps?did=keti0

    

- GPS

  - 소켓 사용하다가 지금 다시 REST API 형식으로 바꿈(rest 폴더에서 진행)
    - gps_server.py : Edge 에서 동작하는 서버
    - gps_client.py : cctv, 5G 모듈이 연결된 pc 에서 동작하는 client



#### 0830

- 회의 토대로 스트리밍 및 GPS 내용 수정, 보완
  - RTSP
    - 이번주 내로 거치대 오면 실험실에 카메라세팅 with 움직이는 화면
    - 박스형 카메라 제작(9월중순)
      - 5G모듈, 미니 PC 필요
  - GPS
    - 기존 방식대로 REST API 로 전송
    - 해야할 것
      - (수) : 실시간 이동되는 정보를 DB에 저장
      - (목) : 노트북에 리눅스 환경 설치 후 실제로 차량 운행 할 수 있게끔 세팅
  - 다음주 쯤 인텔리빅스 방문 할수도 있음
  - **특허 다음주까지 아이디어 2개 이상 생각해보기**



#### 0831

- GPS 실시간 이동되는 정보 DB에 저장할 수 있게끔
  - Server DB 에 {gps_id}_save 테이블로 GPS 데이터 저장중
  - 노트북 인계받아 우분투 설치 후 환경 설정
    - Ubuntu 20.04 LTS
    - 환경 및 코드 수정 완료



#### 0901

- 데이터 안들어오면 안보내게끔 수정 - 완료
- 데이터 client 터미널에 프린트 되게끔 수정 - 완료
- ttyUSB0에서 숫자가 변경될수 있는데 변경되도 사용가능하게끔 - 완료
- 데이터 오차 수정하는 작업 필요함
  - 전자회관 GPS 데이터 - 오차 내용 : 
    - 안드로이드폰 GPS
      - lat : 37.581156
      - lon : 126.888466
    - GPS 모듈
      - lat : 37.348578
      - lon : 126.532997
    - **오차 : **
      - lat : 0.232578
      - lon : ~~0.355469~~ 0.353769
  - 오차 활용하여 맵에 표시해보기
    - 오차가 있지만 일단 사용하기로함



#### 0902

- 어제 저장된 GPS 정보 1초마다 Edge Server 로 전송하는 코드짜기 - 완료

- CCTV, 5G모듈, PC 를 모두 실험실에 세팅 - rtsp 영상 확인 완료

- **완성 내용**

  - 화요일부터 인텔리빅스에서 사용

    - 영상 전송

      - 주소 : rtsp://123.214.186.162:8554/videoMain
      - 서버 운영 : 
        - 미니pc : 
          - `cvlc -vvv rtsp://root:keti1234@192.168.225.30:88/videoMain --sout="#rtp{dst=123.214.186.162,port=5004,mux=ts}" --no-sout-all --sout-keep  `
        - Edge server :
          - `cvlc -vvv rtp://123.214.186.162:5004 --sout="#rtp{sdp=rtsp://:8554/videoMain}" --no-sout-all --sout-keep`

    - gps 데이터

      - 주소 : http://123.214.186.162:8088/get_gps

      - 데이터 response 예시 : 

        - ```
          {
              "alt": "24.7",
              "alt_units": "M",
              "dt": "09/01/2022, 05:44:04",
              "gps": {
                  "lat": "37.598308",
                  "lat_dir": "N",
                  "lon": "126.841352",
                  "lon_dir": "E"
              },
              "gps_id": "keti0"
          }
          ```

      - 서버 운영 : 

        - 미니pc :
          - `python3 gps_temp_transer.py`
        - Edge server : 
          - `python3 gps_server.py`



#### 0906

- 특허 아이디어
  - 통합 관제형 재난경보 CCTV
    - 아이디어 시작점 : 
      - 올해 초대형 태풍 '힌 남노'에 대한 우려가 높았음
      - 재난 방송국 KBS의 마라도 CCTV가 관심을 받으며 직접 시청자들이 찾아서 보는 등 의 현상 
        - ""마라도 CCTV 볼 수 있다"…힌남노 정보 찾아 '네·카'에 몰린다" https://www.hankyung.com/it/article/202209052376g
      - 
    - 기존 재난 CCTV : 
      - ![image](https://user-images.githubusercontent.com/58541635/188538999-b8693158-859e-45f8-99de-3813b9ea43ef.png)
      - 눈으로 보이는 파도의 세기, 구름 등은 확인 할 수 있지만 자세하고 수치 정보들은 알 수 없음
      - CCTV의 흔들림 정도로 대략적인 바람, 태풍의 세기를 짐작 가능함
    - 발명 CCTV : 
      - 풍량, 풍속, 강우량, 흔들림 등 을 측정할 수 있는 센서를 해당 CCTV와 결합
      - 더 정확하고 다양한 정보를 관제센터에 전달하여 가시적이고 직관적이게 설계 가능
      - 해당 영상데이터 및 센서데이터를 저장, 관리, 표출
      - 추후에 발생하는 태풍과 비교분석 및 예상, 경고 가능



#### 0907

- 특허관련 진행하기
  - 아이디어1. 위험도, 환경 학습 기반 PTZ 카메라 제어 (**좀 더 구체적이게 발전시키기**)
    - 위험도 학습이 가능한 엣지가 장착된 PTZ 카메라
    - 위험도 학습 - 유동인구따라 구역마다 위험도 설정
    - 환경  학습 - 시정, 장애물에 따라
  - 아이디어2. 무인점포 기반한 아이디어 (**아이디어 도출부터 해야함**)+모빌리티 카메라?
  - 아이디어3. 모빌리티, 엣지 기반 아이디어
  - 아이디어4. 센서 사용가능한 cctv
- 차량용 카메라 도착
  - IP 수정
    - 기존 : 192.168.0.100
    - 변경 : 192.168.225.40



#### 0908

- 차량용 카메라 rtp 전송 끊김현상 해결

  - 원래 미니pc -5G 모뎀으로 Edge 서버에 전송시 끊김
  - 다른 컴퓨터에서 다른 네트워크로 rtp 전송해보니 끊김현상 줄어듬
  - 카메라 설정 낮춤
    - bitrate : 7000 to **2000**
    - 화질 : 1920 to **1280**

- GPS 데이터 확인

  - 데이터는 거의 동일, 여전히 서해쪽 표시됨

  ```
  <기존 GPS>
  $GPGGA,034010.000,3734.8743,N,12653.2955,E,1,8,1.16,47.2,M,19.2,M,,6C
  $GPGGA,034024.000,3734.8728,N,12653.2959,E,1,8,1.16,47.1,M,19.2,M,,69
  $GPGGA,034025.000,3734.8727,N,12653.2960,E,1,8,1.16,47.1,M,19.2,M,,6D
  $GPGGA,034026.000,3734.8727,N,12653.2960,E,1,8,1.16,47.1,M,19.2,M,,6E
  $GPGGA,034027.000,3734.8726,N,12653.2961,E,1,8,1.16,47.1,M,19.2,M,,6F
  $GPGGA,034028.000,3734.8725,N,12653.2962,E,1,8,1.16,47.1,M,19.2,M,,60
  $GPGGA,034029.000,3734.8725,N,12653.2963,E,1,8,1.16,47.1,M,19.2,M,,60
  $GPGGA,034030.000,3734.8725,N,12653.2965,E,1,8,1.16,47.1,M,19.2,M,,6E
  
  <GPS 1>
  $GPGGA,030339.000,3734.8657,N,12653.3050,E,1,7,1.17,68.9,M,19.2,M,,*61
  $GPGGA,030341.000,3734.8655,N,12653.3050,E,1,7,1.17,69.0,M,19.2,M,,*64
  $GPGGA,030358.000,3734.8649,N,12653.3048,E,1,7,1.17,69.1,M,19.2,M,,*69
  $GPGGA,030350.000,3734.8651,N,12653.3047,E,1,7,1.17,69.1,M,19.2,M,,*67
  $GPGGA,030357.000,3734.8649,N,12653.3048,E,1,7,1.17,69.1,M,19.2,M,,*66
  $GPGGA,030359.000,3734.8649,N,12653.3048,E,1,7,1.17,69.1,M,19.2,M,,*68
  $GPGGA,030356.000,3734.8649,N,12653.3047,E,1,7,1.17,69.1,M,19.2,M,,*68
  $GPGGA,030339.000,3734.8657,N,12653.3050,E,1,7,1.17,68.9,M,19.2,M,,*61
  $GPGGA,030341.000,3734.8655,N,12653.3050,E,1,7,1.17,69.0,M,19.2,M,,*64
  $GPGGA,030400.000,3734.8649,N,12653.3049,E,1,7,1.17,69.1,M,19.2,M,,*62
  
  <GPS 2>
  $GPGGA,030634.000,3734.8548,N,12653.3005,E,1,6,1.57,70.8,M,19.2,M,,*69
  $GPGGA,030636.000,3734.8544,N,12653.2999,E,1,6,1.47,75.0,M,19.2,M,,*66
  $GPGGA,030639.000,3734.8533,N,12653.2970,E,1,6,1.47,91.4,M,19.2,M,,*60
  $GPGGA,030633.000,3734.8526,N,12653.2987,E,1,6,1.47,72.5,M,19.2,M,,*6A
  $GPGGA,030637.000,3734.8516,N,12653.2978,E,1,6,1.47,78.0,M,19.2,M,,*62
  $GPGGA,030635.000,3734.8554,N,12653.3016,E,1,6,1.47,70.8,M,19.2,M,,*66
  $GPGGA,030641.000,3734.8527,N,12653.2952,E,1,6,1.47,86.3,M,19.2,M,,*6B
  $GPGGA,030632.000,3734.8524,N,12653.2989,E,1,6,1.47,70.9,M,19.2,M,,*69
  $GPGGA,030638.000,3734.8541,N,12653.2981,E,1,6,1.47,82.0,M,19.2,M,,*6C
  $GPGGA,030642.000,3734.8532,N,12653.2955,E,1,6,1.47,84.3,M,19.2,M,,*69
  $GPGGA,030649.000,3734.8503,N,12653.2942,E,1,6,1.47,89.6,M,19.2,M,,*6E
  
  <GPS 3>
  $GPGGA,031051.000,3734.8614,N,12653.3041,E,1,6,1.48,76.8,M,19.2,M,,*6F
  $GPGGA,031053.000,3734.8601,N,12653.3042,E,1,6,1.48,80.3,M,19.2,M,,*68
  $GPGGA,031056.000,3734.8557,N,12653.2989,E,1,7,1.35,93.9,M,19.2,M,,*61
  $GPGGA,031050.000,3734.8607,N,12653.3035,E,1,6,1.52,77.1,M,19.2,M,,*6C
  $GPGGA,031057.000,3734.8558,N,12653.2988,E,1,7,1.35,93.4,M,19.2,M,,*63
  $GPGGA,031036.000,3734.8598,N,12653.3025,E,1,5,1.66,72.9,M,19.2,M,,*61
  $GPGGA,031054.000,3734.8572,N,12653.3029,E,1,6,1.48,83.2,M,19.2,M,,*67
  $GPGGA,031052.000,3734.8597,N,12653.3040,E,1,6,1.48,82.9,M,19.2,M,,*6F
  $GPGGA,031058.000,3734.8560,N,12653.2987,E,1,7,1.35,92.8,M,19.2,M,,*65
  $GPGGA,031049.000,3734.8606,N,12653.3066,E,1,5,1.66,57.6,M,19.2,M,,*62
  $GPGGA,031055.000,3734.8556,N,12653.3025,E,1,6,1.52,85.2,M,19.2,M,,*61
  $GPGGA,031059.000,3734.8562,N,12653.2987,E,1,7,1.35,91.8,M,19.2,M,,*65
  $GPGGA,031051.000,3734.8614,N,12653.3041,E,1,6,1.48,76.8,M,19.2,M,,*6F
  $GPGGA,031106.000,3734.8562,N,12653.2986,E,1,8,1.05,91.8,M,19.2,M,,*63
  
  <GPS 4>
  $GPGGA,031258.000,3734.8583,N,12653.3041,E,1,8,1.04,79.1,M,19.2,M,,*69
  $GPGGA,031311.000,3734.8585,N,12653.3044,E,1,9,1.03,77.8,M,19.2,M,,*67
  $GPGGA,031258.000,3734.8583,N,12653.3041,E,1,8,1.04,79.1,M,19.2,M,,*69
  $GPGGA,031311.000,3734.8585,N,12653.3044,E,1,9,1.03,77.8,M,19.2,M,,*67
  $GPGGA,031312.000,3734.8585,N,12653.3044,E,1,9,1.03,77.8,M,19.2,M,,*64
  $GPGGA,031258.000,3734.8583,N,12653.3041,E,1,8,1.04,79.1,M,19.2,M,,*69
  $GPGGA,031313.000,3734.8585,N,12653.3044,E,1,9,1.03,77.8,M,19.2,M,,*65
  $GPGGA,031311.000,3734.8585,N,12653.3044,E,1,9,1.03,77.8,M,19.2,M,,*67
  $GPGGA,031312.000,3734.8585,N,12653.3044,E,1,9,1.03,77.8,M,19.2,M,,*64
  $GPGGA,031314.000,3734.8585,N,12653.3044,E,1,9,1.03,77.7,M,19.2,M,,*6D
  $GPGGA,031258.000,3734.8583,N,12653.3041,E,1,8,1.04,79.1,M,19.2,M,,*69
  $GPGGA,031313.000,3734.8585,N,12653.3044,E,1,9,1.03,77.8,M,19.2,M,,*65
  $GPGGA,031315.000,3734.8585,N,12653.3044,E,1,9,1.03,77.7,M,19.2,M,,*6C
  $GPGGA,031311.000,3734.8585,N,12653.3044,E,1,9,1.03,77.8,M,19.2,M,,*67
  $GPGGA,031312.000,3734.8585,N,12653.3044,E,1,9,1.03,77.8,M,19.2,M,,*64
  $GPGGA,031316.000,3734.8585,N,12653.3044,E,1,9,1.03,77.7,M,19.2,M,,*6F
  $GPGGA,031314.000,3734.8585,N,12653.3044,E,1,9,1.03,77.7,M,19.2,M,,*6D
  $GPGGA,031317.000,3734.8585,N,12653.3044,E,1,9,1.11,77.7,M,19.2,M,,*6D
  ```

  



#### 0914

- 실험실 컴퓨터 2대 및 카메라, gps 서버 구동하기
- 특허
  - 아이디어1. 위험도, 환경 학습 기반 PTZ 카메라 제어 (**좀 더 구체적이게 발전시키기**)
    - 위험도 학습이 가능한 엣지가 장착된 PTZ 카메라
    - 위험도 학습 - 유동인구따라 구역마다 위험도 설정
    - 환경  학습 - 시정, 장애물에 따라
    - 학습 구성도
      - 장애물 탐지
      - 장애물 학습
      - PTZ 제어 구역 설정
      - 객체 탐지
      - 객체 학습
      - 객체에 따른 집중 PTZ 제어구역 설정
      - 객체 변화 인지
      - 객체 학습
      - 객체 변화에 따른 집중 PTZ 제어구역 설정
  - 아이디어2. 무인점포 기반한 아이디어 (**아이디어 도출부터 해야함**)+모빌리티 카메라?
    - 사각지대를 줄일 수 있는 아이디어?
    - 빠르게 대응할 수 있는 아이디어?
      - 가판 인지, 학습 - 구역설정
      - 도난, 파손에 대한 대응 : 팔을 움직여 가판대 머물렀을때 인지 - 데이터로 저장
    - cctv 소리 사용 가능할 때 이용 가능한 아이디어?
  - 아이디어3. 모빌리티, 엣지 기반 아이디어
    - 사생활 보호 기능 드론cctv
      - 객체 검출 및 분류
        - 사람일 경우 - 얼굴 모자이크
      - 특정 이벤트 발생 인지기능
        - 위험 판단
      - 구성도
        - 특정지역 순찰
        - 객체검출
        - 검출 시 사람 얼굴 사생활 보호처리
        - 특정 이벤트 인지시에만 VMS 에 위험 메시지 전송
        - VMS 에서 확인
  - 아이디어4. 센서 사용가능한 cctv
- 카메라 제어
  - 새 미니 pc 사용하여 차량용 카메라 재전송중 
    - 주소 : rtsp://123.214.186.162:8555/videoMain



#### 0915

- 아이디어 흐름도 짜서 말씀드리기 - 11시까지
- 특허
  - 아이디어1. 위험도, 환경 학습 기반 PTZ 카메라 제어 (**좀 더 구체적이게 발전시키기**)
    - 위험도 학습이 가능한 엣지가 장착된 PTZ 카메라
    - 위험도 학습 - 유동인구따라 구역마다 위험도 설정
    - 환경  학습 - 시정, 장애물에 따라
    - 학습 구성도
      - 장애물 탐지
      - 장애물 학습
      - PTZ 제어 구역 설정
      - 객체 탐지
      - 객체 학습
      - 객체에 따른 집중 PTZ 제어구역 설정
      - 객체 변화 인지
      - 객체 학습
      - 객체 변화에 따른 집중 PTZ 제어구역 설정
  - 아이디어2. 무인점포 기반한 아이디어 (**아이디어 도출부터 해야함**)
    - 무인점포마다 CCTV가 설치돼 있으나 정작 절도 범행을 예방하지는 못한다. CCTV는 범죄 예방보다 사후 검거에 초점을 맞추고 있다. 
    - 보안업체 에스원 범죄예방연구소가 2020년 1월부터 올해 6월까지 2년 6개월간 무인매장 범죄 데이터 분석 결과를 보면 주말 등 휴일에 범죄 43%가 발생했으며, 전체 범죄 가운데 39.1%가 오전 6시~오후 12시 사이에 일어났다.
    - 빠르게 대응할 수 있는 아이디어?
      - 가판 인지, 학습 - 구역설정
      - 도난, 파손에 대한 대응 : 팔을 움직여 가판대 머물렀을때 인지
        - 데이터로 저장?
        - 이벤트 발생시만 녹화?
      - 시간별 녹화?
  - 아이디어3. 모빌리티, 엣지 기반 아이디어
    - 카메라가 움직인다
    - 엣지 서버가 붙어있다
  - 아이디어4. 센서 사용가능한 cctv
    - 사용가능한 센서가 있다
      - 소리



#### 0916

- 특허 구성도 만들기
- gps 및 코드 정리





#### 0919

- 5G 사업계획서 확인 후 3차년도 개발내용에 대해 오후 회의
  - 영상보안 시스템간 연동 검증 소프트웨어



#### 0920

- 5G 모뎀 모델 선정
  - LG u+ 통해서 두개 모델 구매 후 요금제 별도 구매
- 과제 전체 구성회의
  - 진행 순서
    - cvlc rtsp 재전송 명령을 python SW 로 구성하는데 여러대의 device 와 연결을 할 수 있는지 확인
    - 미니PC 4대 - Master, Edge(worker), CCTV, BlackBox
    - CCTV 1대
    - BB 1대
    - IP 는 5G 없이 내부망으로 진행
    - 확보 후 작년 EDMS 서버 살려서 되는지 테스트해보기
  - EDMS 에서 Edge 와 Device 들이 여러대 연결되어있으면 모든 Device 와 연결될 수 있게 구성할 수 있는지 확인



#### 0921

- 진행 순서 : 
  - 미니PC 4대 설치 및 각 카메라 설치 후 
  - 내 원래 PC에서 vlc로 rtsp 재전송되는 주소 틀어놓기
  - PC1,2 에서 Edge PC로 rtp 전송
  - Edge PC에서 [rtsp 재전송 SW] 각각 실행
  - 원래 PC에서 vlc 잘 실행되는지 확인
- 구성 : 
  - 카메라는 실험실에(추후에 5G 모뎀오면 위치 변경)
  - BB - car01(실험실)
    - BB  : rtsp://192.168.0.101:554/h264
  - CCTV - cctv01
    - CCTV  : rtsp://keti:keti1234@192.168.0.73:88/videoMain
  - keti2(M)
  - keti1(W)
- 필요 명령 : 
  - BB : 
    - cvlc -vvv rtsp://admin:admin@192.168.0.101:554/h264 --sout="#rtp{dst=**192.168.0.99**,port=**5001**,mux=ts}" --no-sout-all --sout-keep
  - CCTV : 
    - cvlc -vvv rtsp://keti:keti1234@192.168.0.73:88/videoMain --sout="#rtp{dst=**192.168.0.99**,port=**5002**,mux=ts}" --no-sout-all --sout-keep
  - Edge server :
    - cvlc -vvv rtp://:**5001** --sout="#rtp{sdp=rtsp://:**8551**/videoMain}" --no-sout-all --sout-keep
    - cvlc -vvv rtp://:**5002** --sout="#rtp{sdp=rtsp://:**8552**/videoMain}" --no-sout-all --sout-keep



#### 0922

- SW 배포와 Device 연결 부분 시나리오 구성

  1. SW를 Device 선택 시 만듬 >>> SW 배포

  2. **SW를 배포 >>> Device 선택 시 정보들을 실행중인 Edge 의 Pod으로 전달 >>> Pod 은 해당 정보로 해당 Device 들을 RTSP 재전송 시작 (유력)**

- 의문 : 

  - Pod 은 독립적으로 실행되는데 Device 정보를 보낼수 있고 사용이 가능한지?
    - 외부에서 **nodeport** 로 rest server에 request 요청 가능
  - Pod 의 Port 는 NodePort 인데 각 Device에서 RTP 전송시 보낼 수 있는지? 상관이 있는지?
    - **전년도에는 하지 않앗던 방식이라 해봐야함**

- **2번 내용을 토대로한 SW**

  1. rest server 

  2. 요청 서버에서 Edge-Devices 선택 시 정보들을 json 형식으로 데이터를 받는다

     - 예시 : 

     - ```
       {
       	"d_list" : [
       		{"d_id" : "cctv01", "rtp_port" : "5001"},
       		{"d_id" : "cctv02", "rtp_port" : "5002"},
       		{"d_id" : "car01", "rtp_port" : "5003"},
       		{"d_id" : "car04", "rtp_port" : "5004"},
       	]
       }
       ```

  3. json 데이터를 파싱하여

  4. d_list 내 데이터의 숫자를 파악

  5. d_id 갯수만큼 rtsp 재전송 서버를 구동해준다

- 진행중 : 

  - SW 프로토타입 제작 시작

    - **외부-내부 sw 로 request 요청이 안됨**

    - 포트포워딩 설정

      - ```
        netsh interface portproxy add v4tov4 listenport=6100 listenaddress=123.214.186.244 connectport=5100 connectaddress=192.168.0.20
        
        netsh interface portproxy add v4tov4 listenport=6929 listenaddress=123.214.186.244 connectport=5929 connectaddress=192.168.0.20
        ```

    - 포트포워딩 해제

      - ```
        netsh interface portproxy delete v4tov4 listenport=6100 listenaddress=123.214.186.244
        ```

    - 포트포워딩 확인

      - ```
        netsh interface portproxy show v4tov4
        ```

        

#### 0926

- 계속 해당 sw 서버로 실행이 안된다!!
  - 포트포워딩? 방화벽? 왜 안되나...
  - git 으로 pull 받아서 해당 pc 에서 실행해보자
    - Edge 서버에 python module 설치 : flask, flask_cors
    - 같은 ip 라 어차피 안됨
  - 일단 네트워크 제외하고 진행
- 진행중 : 
  - **디바이스-> 엣지로 rtp 전송하고있는 rtp_port 도 디바이스 DB에 저장해줘야함**
  - 역시 cvlc 실행은 1개밖에 실행이 안됨...여러개 thread(?)로 실행시키는 방법
    - 쓰레드로 만들엇는데 잘 되나 확인해야함(각각 실행시키면 됨) - 실행됨
    - 나중에 네트워크 좋은 상태에서 원활하게 잘 돌아가는지 확인해볼 필요 있음



#### 0927

- 진행 해야할 내용 : 
  - 이제 완성된 소프트웨어 `/edms/edge_rtsp_sw.py` 가 Edge 에서 k8s 에 의해 배포되어 실행되고
    - 마스터 노드에서 실행될 `app.py` 가 필요함
      - 작년꺼와 마찬가지로 sw 업로드(vms -> master)
      - sw 배포(master -> worker)
      - 두 기능이 포함되어야함 
  - 해당 파드(앱)의 노드포트를 vms 에서 알고있고, 노드포트로 앱에 디바이스 정보 전달해 rtsp 재전송 실행
- 진행중 : 
  - 워커노드가 활성화가 안됨..
    - ip가 192.168.0.99 여서 기존 node describe 확인해서 192.168.0.25로 변경함
    - 아직 not ready 상태
  - ~~yang_ex 관리자페이지 들어가야하는데 여쭤봐야함, 안되면 초기화!~~ 초기화해서 진행



#### 0928

- keti1 워커노드의 쿠버네티스 초기화 후 다시 join 해서 해보기! - 완료

- 포트포워딩도 가능!

- 진행 해야할 내용 : 

  - 이제 완성된 소프트웨어 `/edms/edge_rtsp_sw.py` 가 Edge 에서 k8s 에 의해 배포되어 실행되고

    - 마스터 노드에서 실행될 `app.py` 가 필요함
      - 작년꺼와 마찬가지로 sw 업로드(vms -> master)
      - sw 배포(master -> worker)
      - 두 기능이 포함되어야함 

  - 해당 파드(앱)의 노드포트를 vms 에서 알고있고, 노드포트로 앱에 디바이스 정보 전달해 rtsp 재전송 실행

  - 현재 서버 : 

    - **keti2 : master / 192.168.0.28**
    - **keti1 : worker / 192.168.0.25**

  - cors 오류때문에 예지누나 서버에서 master 서버로 api 호출이 안됨, 오류내용 : 완료

    - Access to fetch at 'http://192.168.0.28:5000/add_newEdgeCluster' from origin 'http://123.214.186.244:9998' has been blocked by CORS policy: The request client is not a secure context and the resource is in more-private address space `private`
    - 해결 방법 : 
      - chrome://flags/#block-insecure-private-network-requests 크롬 접속 후 disabled 변경
    - 요청은 위 방법으로 해결했는데 api 요청은 되는데 어떤 동작도 수행하지 않음
      - cors 부분을 손봤는데 다시 원래대로 돌리니까 됨

  - 해결 해야할 것 : (완료)

    - subprocess returned non-zero exit status 1

      - sudo kubeadm reset 으로 master 도 지워가면서 해보기
        - **k8s 초기 설정 시 이미 master 가 설정되어있으면 에러 발생하는현상**

    - paramiko unable to connect to port 22 on 102.168.0.28(마스터, 워커 서버로 명령실행 불가) - 완료

      - 해당 서버에 ssh-server 가 설치되어 있지 않아 발생하는데, openssh-server 를 설치해서 22번 포트를 열어주면 된다

      - ```
        # openssh-server 설치
        sudo apt-get install openssh-server
        
        # 22포트 열렸는지 확인
        netstat -ntl
        ```



#### 0929

- 클러스터링 먼저 잘되게끔 해야함!

  - 클러스터링 - 완료

- 클러스터 삭제가 안됨 - 완료

  - paramiko.ssh_exception.AuthenticationException: Authentication failed. 에러

    - keti2(마스터)에서 paramiko ssh 연결시도시 Auth 에러떠서 if 문으로 분류해서 os.system으로 kubeadm reset 시켜줬음

      ```
              if name == "keti2":
                  os.system("echo 'keti' | echo y | sudo kubeadm reset")
      ```

- Linux 에서 sudo 실행 시 비밀번호 미리 입력하는 방법

  - ```
    echo '비밀번호' | echo y(yes 도 사용가능) | sudo -S 명령어
    ```



#### 0930

- 진행 해야할 내용 : 
  - sw 업로드, 배포 - 작년에 했던 내용 토대로 5G_web 서버에서 어떻게 작동하는지 파악 후 진행
    - 내 pc에 `edge_rtsp_sw.zip` 파일이 5G_web 서버의 /openapi/uploads  폴더에 저장됨
    - **잘 작동하는데 zip 파일에 `_`를 사용하면 안되고 `-`를 사용해야함!!**
    - 문제 발생
      - docker image 이름이 <none>으로 입력됨
        - docker image building 이 제대로 안되서 그럼 수정해서 완료
      - docker push 실행이 되지 않음
      - docker login  기능 실행 - try except 으로 error 캐치해서 처리
  - 이제 완성된 소프트웨어 `/edms/edge_rtsp_sw.py` 가 Edge 에서 k8s 에 의해 배포되어 실행되고
    - 마스터 노드에서 실행될 `app.py` 가 필요함 - 기존 app.py 에서 진행중
      - 작년꺼와 마찬가지로 sw 업로드(vms -> master)
      - sw 배포(master -> worker)
      - 두 기능이 포함되어야함 
  - 해당 파드(앱)의 노드포트를 vms 에서 알고있고, 노드포트로 앱에 디바이스 정보 전달해 rtsp 재전송 실행



#### 1004

- 소프트웨어 `/edms/edge_rtsp_sw.py` 가 Edge 에서 k8s 에 의해 배포되어 실행되고
  - 마스터 노드에서 실행될 `app.py` 가 필요함 - 기존 app.py 에서 진행중
    - 작년꺼와 마찬가지로 sw 업로드(vms -> master)
    - sw 배포(master -> worker)
    - 두 기능이 포함되어야함 
- 해당 파드(앱)의 노드포트를 vms 에서 알고있고, 노드포트로 앱에 디바이스 정보 전달해 rtsp 재전송 실행







#### 1005

- 현재 완료 : 

  - SW 가 upload되어 배포부터 시작하면 됨

  - docker image 는 생성(sw upload)되었으나 run 을 console 에서 실행 시 requests 모듈이 없다고 에러

    - requests 모듈 install 명령을 Dockerfile 에 명시해둘 것 - 완료

  - sw 배포중 오류 :  

    - ```
      Warning  FailedCreatePodSandBox  33s (x4 over 39s)   kubelet  (combined from similar events): Failed to create pod sandbox: rpc error: code = Unknown desc = failed to set up sandbox container "8d4142c7d138aaab04a1e57e35d2c61c1e2352490c9a4da36c68e013f0823342" network for pod "edge-rtsp-sw-keti1-59dd66fd7c-rqj4q": networkPlugin cni failed to set up pod "edge-rtsp-sw-keti1-59dd66fd7c-rqj4q_default" network: failed to delegate add: failed to set bridge addr: "cni0" already has an IP address different from 10.244.1.1/24
      ```

    - 해결 방법 : 

      - 네트워크 (DNS) 문제로 ContainerCreating 에 멈춘 경우.

        - ```
          # kubeadm reset
          #systemctl stop kubelet
          # systemctl stop docker
          # rm -rf /var/lib/cni/
          # rm -rf /var/lib/kubelet/*
          # rm -rf /etc/cni/
          # ifconfig cni0 down
          # ifconfig flannel.1 down
          # ifconfig docker0 down
          # ip link delete cni0
          # ip link delete flannel.1
          ```

        - 위 명령 실행 후 kubeadm 을 통한 init 처음부터 실행

        - 따라해도 잘 안됨 -> master, worker 다 지울것! -완료

        - 출처: https://crystalcube.co.kr/202 

  - Edge에서 실행되고있는 Pod 실행 Index 주소 : 

    - http://192.168.0.28:30453/
      - NodePort : 30453(**포트포워딩으로 외부에서도 접속 가능하게 완료**)
      - TargetPort : 5060(원본 edge-rtsp-sw.py에서 사용하는 Port)



- 진행중 : 

  - edge-rtsp-sw Pod 내부 메시지 : 

    - ```
      10.244.0.0 - - [05/Oct/2022 08:36:02] "POST /act_device HTTP/1.1" 200 -
      sh: 1: cvlc: not found
      sh: 1: cvlc: not found
      ```

    - **아마 sh와 cvlc 명령이 실행되지 않아서 발생하는것 같음,  해결해야함!!**



- <mark>**전체 설계도**</mark>

  - IP : 
    - keti2(Master) : 192.168.0.28
    - keti1(Worker) : 192.168.0.25
    - cctv01 : 192.168.0.60 / rtsp://keti:keti1234@192.168.0.73:88/videoMain
    - car01 : 192.168.0.96 / rtsp://192.168.0.101:554/h264

  

  - 디바이스들에서 SW가 실행되고 있는 keti1(W)로 rtp전송 명령어 : 

    - cctv01 -> keti1(W) : 

      ```
      cvlc -vvv rtsp://keti:keti1234@192.168.0.73:88/videoMain --sout="#rtp{dst=192.168.0.25,port=5002,mux=ts}" --no-sout-all --sout-keep
      ```

    - car01 -> keti1(W) : 

      ```
      cvlc -vvv rtsp://192.168.0.101:554/h264 --sout="#rtp{dst=192.168.0.25,port=5001,m
      ux=ts}" --no-sout-all --sout-keep
      ```

  

  - keti1(W)에 배포된 Pod 에서 rtsp 명령어 : 

    - car01

      ```
      cvlc -vvv rtp://:5001 --sout="#rtp{{sdp=rtsp://:8551/videoMain}}" --no-sout-all --sout-keep
      ```

    - cctv01

      ```
      cvlc -vvv rtp://:5002 --sout="#rtp{{sdp=rtsp://:8552/videoMain}}" --no-sout-all --sout-keep
      ```

    

  - keti1에 배포된 SW의 Pod 으로 request 및 json 데이터 형식 : 

    - request 요청 주소 : http://123.214.186.244:30453/act_device

    - json 데이터 형식

      ```
      {
      	"d_list" : [
      		{"d_id" : "cctv01", "rtp_port" : "5002"},
      		{"d_id" : "car01", "rtp_port" : "5001"}
      	]
      }
      ```

    

  - rtsp 재전송 주소 : 

    - cctv01 : rtsp://123.214.186.244:8552/videoMain
    - car01 : rtsp://123.214.186.244:8551/videoMain



- **의문 :** 
  - 만약 Worker  에서 실행되고있는 edge-rtsp-sw pod이 에러가 뜨면 어떻게?
  - device 를 변경하고 싶을때는 어떻게?



#### 1006

- 진행완료 : 
  - edge-rtsp-sw Pod 내부 메시지 : 

    ```
    10.244.0.0 - - [05/Oct/2022 08:36:02] "POST /act_device HTTP/1.1" 200 -
    sh: 1: cvlc: not found
    sh: 1: cvlc: not found
    ```

    - **아마 sh와 cvlc 명령이 실행되지 않아서 발생하는것 같음,  해결해야함!!** sw 를 변경해야할듯

      - cvlc 인스톨 명령어를 dockerfile 에 명시, opencv 설치는 지웠음 

        - k8s 에서 실행은 됨..하지만, pod이 root에서 실행되는데(?),  vlc 가 root에서 실행되지 않음

          - 아래 명령어를 실행시키고하면, k8s 내부에서 실행하는건 확인 필요한데 일반적으로 console을 사용하면 된다

            ```
            $ sudo sed -i 's/geteuid/getppid/' /usr/bin/vlc
            ```

  - request 주소 변경 : http://123.214.186.244:31924/act_device

  - 일단 안됨...... pod 내부에서 cvlc 명령어 실행중이긴 한듯



#### 1007

- 진행해야할 것 :
  - 일단 A4용지에 정리한데로 기존 방식대로 진행해보기!!!
    - 확인해볼 것 : k8s pod 에서 사용하는 ip 주소?
      - pod 내부 ip : 10.244.1.5
      - pod 외부 ip : 123.214.186.244
      - **외부 ip를 사용해서 --- device -> edge 로 rtp 전송이 가능한지? 그 후에 rtsp 서버도 가능?** 
        - car01 -> keti0(외부망 123.214.186.162) 에서 rtsp 서버는 잘 됨
        - car01 -> keti1(외부망 123.214.186.244) 는 잘 안됨...**왜??**
  - ~~지금 전송이 어떤 서버로 가는지, pod 이 사용하는 ip가 무엇인지 등등 이 필요함....~~
  - 만약 고정ip가 된다면, sw를 변경해서 고정 ip의 카메라 정보를 가져올수 있는지?



#### 1011

- 진행해야할 것 :
  - keti0 클러스터링 해보고 외부 ip 사용하는 방식으로 진행!
  - 일단 A4용지에 정리한데로 기존 방식대로 진행해보기
    - 확인해볼 것 : k8s pod 에서 사용하는 ip 주소?
      - pod 내부 ip : 10.244.1.5
      - pod 외부 ip : 123.214.186.244
      - **외부 ip를 사용해서 --- device -> edge 로 rtp 전송이 가능한지? 그 후에 rtsp 서버도 가능?** 
        - car01 -> keti0(외부망 123.214.186.162) 에서 rtsp 서버는 잘 됨
        - car01 -> keti1(외부망 123.214.186.244) 는 잘 안됨...**왜??**
  - 다른방법 : 
    - 만약 고정ip가 된다면, sw를 변경해서 고정 ip의 카메라 정보를 가져올수 있는지?



#### 1012

- 진행해야할 것 :
  - keti0 클러스터링 해보고 외부 ip 사용하는 방식으로 진행!
    - 클러스터링 안됨..현재 Master에서 192.168.0.5 내부 ip 를 사용하기때문..
  - sw 수정해서 배포해보기
    - cvlc rtp 및 rtsp 주소를 123.214.186.244로 고정한다면?
      - 안됨! dead input..
  - 일단 A4용지에 정리한데로 기존 방식대로 진행해보기
    - 확인해볼 것 : k8s pod 에서 사용하는 ip 주소?
      - pod 내부 ip : 10.244.1.5
      - pod 외부 ip : 123.214.186.244
      - **외부 ip를 사용해서 --- device -> edge 로 rtp 전송이 가능한지? 그 후에 rtsp 서버도 가능?** 
        - car01 -> keti0(외부망 123.214.186.162) 에서 rtsp 서버는 잘 됨
        - car01 -> keti1(외부망 123.214.186.244) 는 잘 안됨...**왜??**
  - 다른방법 : 
    - 만약 고정ip가 된다면, sw를 변경해서 고정 ip의 카메라 정보를 가져올수 있는지?
      - cam-pc(고정ip) rtsp 재전송중 <--- worker 에서 rtsp 재생



- **의문 :** 
  - 쿠버네티스가 외부망끼리 클러스터링이 가능한지?
  - 만약 Worker  에서 실행되고있는 edge-rtsp-sw pod이 에러가 뜨면 어떻게?
  - device 를 변경하고 싶을때는 어떻게?



- **문제점 :** 
  - edge-rtsp-sw 를 배포할때마다 해당 edge의 라우터 설정에서 포트포워딩 필요!



- **일단 위 내용 보류!! SW가 잘 작동하는지만 확인하면 됨!!**



- 카메라 잘 작동하는지 확인하는 SW 만들고 배포하기
  - /3년차/sw_deploy_test 에서 flask-video-streaming 배포해보기 내일!



#### 1013

- 오전에 카메라 잘 작동하는지 확인하는 SW 만들고 배포하기
  - /3년차/sw_deploy_test 에서 flask-video-streaming 배포해보기
  - ~~flask cors 모듈이 없다고 나와서 dockerfile에 명시해줘야함~~ 
  - 잘되는데 cctv 01 화면으로 넘어가면 localhost 오류남
    - js 로 해결
  - video-streaming sw 배포, 작동 완료
- 오후까지 시나리오 잘 생각해보고 회의



#### 1014

- 3차년도 기술개발 실적 평가 방법
  - /배경화면/5G과제/3년차_보고서 에 PPT로 작성완료
- 수정해야될 내용 : 
  - sw 업로드시 port(target port) 입력해주어야함



#### 1017

- 5G 모뎀 오면 실증 시나리오 구성하기
  - Blackbox & GPS - PC - 5G Modem
  - CCTV - PC - 5G Modem
  - 현재 구성은 어떻게 할지 논의 후 진행
- DEMS 변경안
  - sw업로드후 배포할때 5로 시작하는 4개자리 targetport 번호 지정해주면서 배포하게끔..변경..!



#### 1018

- 5G 모뎀 도착, 실증 시나리오 구성하기
  - Blackbox & GPS - PC - 5G Modem
  - CCTV - PC - 5G Modem
  - 현재 5G모뎀 
    - 유동 2기 - 쿠오핀, SK
    - 고정 2기(작동 안됨)
- 서박사님 SW Dockerfile 만들기
  - 모듈, 라이브러리 어떤거 사용해야하는지?
  - 자동으로 추출 가능한지 먼저 알아보고 진행하기
- DEMS 변경안
  - sw업로드후 배포할때 5로 시작하는 4개자리 targetport 번호 지정해주면서 배포하게끔..변경..!



#### 1019

- 서박사님 SW Dockerfile 만들기
  - 모듈, 라이브러리 어떤거 사용해야하는지?
  - 자동으로 추출 가능한지 먼저 알아보고 진행하기

- 5G 모뎀 도착, 실증 시나리오 구성하기
  - 쿠오핀(유동) - skt 모뎀 연결된 디바이스 말고 다른 디바이스에 연결해서 사용하기
    - 현재 yang_ex에 car01 과 cctv01이 연결되어있는데 오늘 캡쳐하는 작업 이후에 5G모뎀과 연결할것!
- 검증 캡쳐 및 사진촬영 - 완료
  - SW 2개화면으로 캡쳐
  - SW 부분 DB 캡쳐
  - SW upload, deploy console 캡쳐
  - Foscam, Carcam 사진찍기 각각
  - GPS+미니PC 사진
  - 5G+미니PC+CCTV 사진



#### 1020

- 무선엣지 진행
  - 자동으로 추출 가능한지 먼저 알아보고 진행하기
    - `pip freeze > requirements.txt` 명령어로 python 모듈 추출 가능
  - 진행 순서 : 
    1. window(master)-linux(worker) 를 클러스터링 할수 있는지 확인
       - 있다 : 예지누나(master)-서박사님(worker) 클러스터링
       - 없다 : 예지누나(web server)-새로운 PC(master)-서박사님(worker) 클러스터링
    2. 기존 keti2(M)-keti1(W)에서 서박사님 SW 가 잘 작동하는지 확인
       - dockerfile 작성 필요!
    3. 1번에서 새롭게 클러스터링 된 시스템에서 기존 rtsp 프로그램이 잘 작동하는지 확인
    4. 무선엣지 시스템에서 서박사님 SW 배포하고 잘 되는지 확인
       - 화면이 자동으로 안뜰 수 있음.. web서버가 아닌 이런 경우에는 어떻게?
- 5G 모뎀 도착, 실증 시나리오 구성하기
  - 쿠오핀(유동) - skt 모뎀 연결된 디바이스 말고 다른 디바이스에 연결해서 사용하기
    - 현재 yang_ex에 car01 과 cctv01이 연결되어있는데 오늘 캡쳐하는 작업 이후에 5G모뎀과 연결할것!



#### 1024

- 무선엣지 진행
  - 자동으로 추출 가능한지 먼저 알아보고 진행하기
    - `pip freeze > requirements.txt` 명령어로 python 모듈 추출 가능
    - 서박사님파이을 python 이 아닌 exe 로 받아서 실행하는거 하는중
  - 서박사님 `main.py` 가 쿠버네티스 pod 으로 실행되었을때 실행이 어떻게 되는지 확인해보기
    - [exe 파일 배포 시 도커에 대한 질의응답](https://www.inflearn.com/questions/27871)
    - docker 에서 exe 게임 실행 시 바로 플레이되는거 보니 잘 실행되는듯? 계속 진행해보기
  - 진행 순서 : 
    1. window(master)-linux(worker) 를 클러스터링 할수 있는지 확인
       - 있다 : 예지누나(master)-서박사님(worker) 클러스터링
         - [리눅스(마스터)-윈도우(워커) 노드 클러스터링 하는 방법](https://people.wikimedia.org/~jayme/k8s-docs/v1.16/ko/docs/setup/production-environment/windows/user-guide-windows-nodes/)
       - **없다 : 예지누나(web server)-새로운 PC(master)-서박사님(worker) 클러스터링**
         - web server를 새로운PC(M)에서 실행하고 worker 와 클러스터링 하는 방향으로 하면 어떨지?
    2. 기존 keti2(M)-keti1(W)에서 서박사님 SW 가 잘 작동하는지 확인
       - dockerfile 작성 필요!
    3. 1번에서 새롭게 클러스터링 된 시스템에서 기존 rtsp 프로그램이 잘 작동하는지 확인
    4. 무선엣지 시스템에서 서박사님 SW 배포하고 잘 되는지 확인
       - 화면이 자동으로 안뜰 수 있음.. web서버가 아닌 이런 경우에는 어떻게? 일단 서박사님 프로그램 완성되면 클러스터링 후 배포해보기
  - 서박사님 `main.py` 돌리기 위해 pip install 리스트
    - PyQt5
    - torch
    - ml-collections
    - torchvision
  - 현재 진행중 : 
    - 1개 미니PC(edge01)에 쿠버네티스까지 **설치 완료**
    - 서박사님 pc - edge01 의 역할 정하기
      - 마스터노드 or 워커노드
    - 1.web server 를 마스터노드에서 실행시킬지? or 2.기존 서버에서 실행시키고 마스터 노드에서 k8s 를 실행시킬 수 있는 API 서버를 실행시킬지? 정해야함
      - 2번이 유력한데 2년차 app.py 의 형태와 비슷하게 진행
      - **시나리오** : 
        - 단말등록 : 기존의 클러스터링으로 worker node 추가하는 기능
        - 엣지 AI 등록 : SW 업로드 기능
        - 엣지 AI 배포 : SW 배포 기능



#### 1110

- 3년차 5G과제 시나리오 구
  - 영상 11/28 부터 제작 시작
  - 영상 내용 : 
    - 협동제어(개별) - 김박사님
    - DEMS(개별)
    - 5G CCTV(개별)
    - 5G Blackbox(개별)
    - 5G CCTV, BB - 인텔리빅스 통합(통합) 
  - DEMS 에서 video-streaming 잘 배포되는지 확인해야함
    - **배포는 잘 되는데 video-streaming app 에서 실제 배포되는 카메라 url 이 변경될 예정**
    - 배포 후에 포트포워딩 해주는 작업이 필요함..
- GPS 모듈 와서 테스트 해봐야함
  - 잘 안되는데....처음부터 다시 잘 해보기



#### 1111

- GPS 진행

  - sample code c 로되어있는거 확인 후 그냥 사용해보기(인텔리빅스도 그거 사용했다고함)

- 현재 데이터 받아와서 binary 파일 읽어보면 이렇게 나옴

  ```
  00000000   55 50 00 00 00 00 05 06 EE 02 A0 55 51 EA FF FE  UP......î. UQê.þ
  00000010   FF 08 0E BC 55 52 00 00 00 00 00 00 0E B9 55 53  ...¼UR.......¹US
  00000020   4F 00 F6 FF E4 EC B8 46 BA 55 54 CD 06 9C E7 AD  O.ö.äì¸FºUTÍ.ç­
  00000030   B4 0E 72 55 56 62 8E 01 00 8F EA FF 00 A0 EA FF  ´.rUVb..ê.. ê.
  00000040   FF 22 55 57 00 00 00 00 00 00 00 00 AC 55 58 00  ."UW........¬UX.
  00000050   00 00 00 00 00 00 00 AD 55 59 86 7C 27 00 AD 00  .......­UY|'.­.
  00000060   69 E2 CF 55 5A 00 00 00 00 00 00 00 00 AF 55 50  iâÏUZ........¯UP
  00000070   00 00 00 00 05 1B 58 02 1F 55 51 E9 FF 00 00 08  ......X..UQé....
  00000080   07 0E C1 55 52 01 00 00 00 00 00 07 0E BD 55 53  ..ÁUR........½US
  00000090   4C 00 F4 FF FD EC B8 46 CE 55 54 6C 07 60 E7 D2  L.ô.ýì¸FÎUTl.`çÒ
  000000A0   B4 07 0E FE 55 56 5F 8E 01 00 A5 EA FF FF 26 55  ´..þUV_..¥ê..&U
  000000B0   57 00 00 00 00 00 00 00 00 AC 55 58 00 00 00 00  W........¬UX....
  000000C0   00 00 00 00 AD 55 59 86 7C 28 00 AD 00 69 E2 D0  ....­UY|(.­.iâÐ
  000000D0   55 5A 00 00 00 00 00 00 00 00 AF 55 50 00 00 00  UZ........¯UP...
  000000E0   00 05 1B EE 02 B5 55 51 E9 FF 00 00 19 08 0E C1  ...î.µUQé......Á
  000000F0   55 52 00 00 00 00 00 00 0E B9 55 53 4C 00 F4 FF  UR.......¹USL.ô.
  00000100   FD EC B8 46 CE 55 54 7C 07 75 E7 A0 B4 08 0E BF  ýì¸FÎUT|.uç ´..¿
  00000110   55 52 FF FF 01 00 00 00 0E B8 55 53 4B 00 F4 FF  UR.......¸USK.ô.
  00000120   FD EC B8 46 CD 55 54 7E 07 AF E7 C1 B4 08 0E BD  ýì¸FÍUT~.¯çÁ´..½
  00000130   55 52 00 00 00 00 00 00 0E B9 55 53 4B 00 F5 FF  UR.......¹USK.õ.
  00000140   FD EC B8 46 CE 55 54 7D 07 19 E7 AD B4 08 0E BC  ýì¸FÎUT}..ç­´..¼
  00000150   55 52 00 00 00 00 00 00 0E B9 55 53 4B 00 F5 FF  UR.......¹USK.õ.
  00000160   FD EC B8 46 CE 55 54 71 07 3F E7 C6 B4 0E D3 55  ýì¸FÎUTq.?çÆ´.ÓU
  00000170   56 5F 8E 01 00 A4 EA FF FF 25 55 57 00 00 00 00  V_..¤ê..%UW....
  00000180   00 00 00 00 AC 55 58 00 00 00 00 00 00 00 00 AD  ....¬UX........­
  00000190   55 59 86 7C 26 00 AF 00 69 E2 D0 55 5A 00 00 00  UY|&.¯.iâÐUZ...
  ```

- 샘플코드로 아래와 같이 데이터 가져올수 있음

  - /gps_cpp/gps_with_gyro.cpp

  ```
  a:-0.003 -0.009  1.010 w:  0.000   0.000   0.000 A: -0.154  -0.505 -52.542 h:28872 28800 -16767 gps:28872.000000 28800.000000 -16767.000000 3692.000000 -22528.000000 3353.000000gps:0.000000 0.000000 0.000000 0.000000 -22528.000000 3353.000000
  T:Fri Nov 11 17:55:49 2022
   a:-0.003 -0.010  1.012 w:  0.000   0.000   0.000 A: -0.154  -0.505 -52.542 h:28872 28908 -16757 gps:28872.000000 28908.000000 -16757.000000 3697.000000 -22528.000000 3353.000000gps:0.000000 0.000000 0.000000 0.000000 -22528.000000 3353.000000
  T:Fri Nov 11 17:55:49 2022
   a:-0.003 -0.011  1.010 w:  0.000   0.000   0.000 A: -0.154  -0.505 -52.542 h:28872 28669 -16767 gps:28872.000000 28669.000000 -16767.000000 3700.000000 -22528.000000 3353.000000gps:0.000000 0.000000 0.000000 0.000000 -22528.000000 3353.000000
  T:Fri Nov 11 17:55:49 2022
   a:-0.002 -0.010  1.012 w:  0.000   0.000   0.000 A: -0.154  -0.505 -52.542 h:28872 28859 -16769 gps:28872.000000 28859.000000 -16769.000000 3695.000000 -22528.000000 3353.000000gps:0.000000 0.000000 0.000000 0.000000 -22528.000000 3353.000000
  T:Fri Nov 11 17:55:49 2022
   a:-0.003 -0.010  1.011 w:  0.000   0.000   0.000 A: -0.154  -0.505 -52.542 h:28872 28689 -16764 gps:28872.000000 28689.000000 -16764.000000 3697.000000 -22528.000000 3353.000000gps:0.000000 0.000000 0.000000 0.000000 -22528.000000 3353.000000
  T:Fri Nov 11 17:55:49 2022
   a:-0.002 -0.010  1.011 w:  0.000   0.000   0.000 A: -0.154  -0.505 -52.542 h:28872 28620 -16749 gps:28872.000000 28620.000000 -16749.000000 3698.000000 -22528.000000 3353.000000gps:0.000000 0.000000 0.000000 0.000000 -22528.000000 3353.000000
  T:Fri Nov 11 17:55:49 2022
   a:-0.003 -0.010  1.011 w:  0.000   0.000   0.000 A: -0.154  -0.505 -52.542 h:28872 28718 -16763 gps:28872.000000 28718.000000 -16763.000000 3695.000000 -22528.000000 3353.000000gps:0.000000 0.000000 0.000000 0.000000 -22528.000000 3353.000000
  T:Fri Nov 11 17:55:49 2022
  ^C
  
  ```

- 이 내용 토대로 해서 코드 수정해서 필요한 데이터 가져오면 될듯!!



#### 1115

- c++ 코드로 모든 정보 뽑아내기

  - 왜 데이터가 정해진 개수가 아니라 계속 들어오는지?

- 왜 gps 데이터는 두번 들어오는지?

  - 추가한 변수들은 한번 이상씩 들어옴..왜?

- 데이터 형태 : 

  ```powershell
  T:Tue Nov 15 12:51:04 2022
   a:-0.007 -0.009  1.009  1.677  7.125  0.349 54.470 254.210
   w:  0.000   0.000   0.000 209.656 890.625  43.640  54.470 254.210
   A: -0.137  -0.198  38.804  99.448  80.156   3.928 5447.000 25421.000
   h:28873 7056 -21009 3435 14592  715 5447 25421
   ph:28873.000000 7056.000000 -21009.000000 3435.000000 14592.000000 715.000000 5447.000000 25421.000000
   gps:28873.000000 7056.000000 -21009.000000 3435.000000 14592.000000 715.000000 5447.000000 25421.000000
   ph:-29995.000000 1.000000 2062.000000 0.000000 14592.000000 715.000000 5447.000000 25421.000000
   gps:-29995.000000 1.000000 2062.000000 0.000000 14592.000000 715.000000 5447.000000 25421.000000
   gps:0.000000 0.000000 0.000000 0.000000 14592.000000 715.000000 5447.000000 25421.000000
   s:0.000000 0.000000 0.000000 0.000000 14592.000000 715.000000 5447.000000 25421.000000
   q:30905.000000 -196.000000 79.000000 10885.000000 14592.000000 715.000000 5447.000000 25421.000000
   sp:0.000000 0.000000 0.000000 0.000000 14592.000000 715.000000 5447.000000 25421.000000
  ```

- 데이터가 제대로 안들어옴...4번째 이후 똑같은 데이터만 들어와서 코드 수정하던지 해서 제대로 받아올 수 있게해야함
- 233번줄에 // for 문의 r_buf[i] 가 늘어나야 될거같은???



#### 1116

- 잘안됨
- vs code 로 되어있는거 실행해보는중
  - 데이터는 받아와지는거같은데 윈도우로 실행해야함..
  - 근본적으로 데이터가 어떻게 들어오는지 모르겠음



#### 1117

- window 에서 gps data setup 부터 시작
  - 1번 고장 / 2번은 gps original도 잘 들어옴
  - 2번 gps 잘 들어와서 location 데이터 확인
- c++ 예제 변경해주신거부터 다시 코드 짜보기
  - /gps/gps_with_gyro2.cpp 에서 진행
    - 코드 0x51번 완료 이것 토대로 진행하기
    - 결과값은 float / 데이터 변환은 signed short



#### 1118

- /gps/gps_with_gyro2.cpp
  - 0x51 수정보고 그것 토대로 모든 데이터 진행
  - gps_with_gyro2_bu.cpp 
    - 0x51
    - 0x52
    - 0x53
    - 0x54
    - 0x56 : 값이 좀 이상한듯? 
      - 32bit 연산할때 변수를 float 으로 하면 안됨(GPS 데이터 및 다른 데이터들도 마찬가지)
    - 0x57 : gps 값 %(나머지) 연산할때 오류를 못고치겠음
    - 0x57 : gps 데이터가 안들어와서 따로 확인해봐야함



#### 1121

- gps 값 들어오게 조정..(운)
- gps 값 들어오면 맞게끔 계산하기
  - 상암 GPS
    - Lat: 37.5808 
    - Lon: 126.8884
  - GPS 모듈 raw 데이터 값
    - lon base : 126.5328980.000000
      - londd : 126.5328980
      - lonmm : 53.28980
      - **lon : 126.126°53.29553'**
      - sw 내 lon 값 : 126.5329553' -> 이값으로 하면 기존 gps 의 서해바다 쪽 위치가 잡힘
    - lat base : 4294965588.000000
      * latdd : 
      * latmm : 
- 모든 값 제대로 들어오면 python 으로 Edge 컴퓨터로 보낼 방법 구상
  - 0x56 : 값이 좀 이상한듯? 
    - 32bit 연산할때 변수를 float 으로 하면 안됨(GPS 데이터 및 다른 데이터들도 마찬가지)
    - float 도 32bit 연산 되는거같은데...일단 고쳐보다 안되서 보류 gps로 넘어가기
  - 0x57 : gps 값 %(나머지) 연산할때 오류를 못고치겠음
    - lon값은 잘 들어오는데 lat 값이 이상함
    - 계산은 내가 다시 고안한 방법으로 진행
  - 0x58 : gps 데이터가 안들어와서 따로 확인해봐야함
    - gps 높이, 속도 관련한건데 얼추 잘 들어옴



#### 1122

- 원격

  - g26112fw
  - 9tf2f7p4

- gps 데이터 값

  ```
  # lon 데이터만 잘 나올때 (tmp변수 unsigned int)
  [0x57] lon : 126.5328980 lat : 42.949664
  [0x58] gpsHeight : 62.9 gpsYaw : 429496736.0 gpsV : 0.000
  
  # 데이터 이상하게 들어올때
  [0x57] lon : 429.496722 lat : 42.949664
  [0x58] gpsHeight : 62.9 gpsYaw : 429496736.0 gpsV : 0.000
  
  # 데이터 이상하게 들어올때 2
  [0x57] lon : 126.532892 lat : 42.949673
  [0x58] gpsHeight : 429496736.0 gpsYaw : 429496736.0 gpsV : 0.000
  
  # 57,58 gps 데이터 tmp변수를 unsigned int 에서 signed int 로 바꿨을때
  [0x57] lon : 126.532901 lat : -0.000004
  [0x58] gpsHeight : -6.2 gpsYaw : -9.9 gpsV : 0.000
  
  # 57 gps 데이터 tmp변수를 unsigned short 로 바꿨을때
  [0x57] lon : 126.536899 lat : 38.587592
  [0x58] gpsHeight : -6.2 gpsYaw : -9.9 gpsV : 0.000
  ```

  - lon 데이터라도 잘 나올 때를 보면 [1]번째 데이터는 잘 들어오고 [2]번째 데이터가 비슷한 형식으로 들어오는 것을 볼 수 있다..왜?
  - 전체 r_burf부터 chrBuf 등등 unsigned char 로 변경해서 되었다
    - unsigned char : ~255
    - signed char : -128~127
    - 여기서는 음수(-)가 나올 수 없는데 마이너스가 나와서 자꾸 데이터가 fffff05 형식으로 넘어와서 에러가 발생하는 것이었음!
  - **이제까지 GPS 값은 정상! 다만 값의 도 를 제외한 분을 60으로 나눠줘야함(중요)**

- 앞으로 할 것 : 

  - 데이터 다 잘 들어오도록 확인!
  - 전체 데이터 잘 들어오면 확인 후 python 으로 이전과 같이 Edge로 전송 할수 있도록!!
  - **GPS 차량 촬영 때 영상데이터 및 GPS 값 Edge에 저장해야함**

- 데이터 값 확인 : 

  - [0x58] Time: O
  - [0x51] Acceleration : X -> (**signed char**)chrBuf[i+2] 로 수정해서 O
  - [0x52] Angular Velocity : △ -> (**signed char**)chrBuf[i+2] 로 수정해서 O
  - [0x53] Angle: △ -> 확인 필요
  - [0x54] Magnetic : X -> (**signed char**)chrBuf[i+2] 로 수정해도 X
  - [0x56] Atmospheric Pressure and Height : O
  - [0x57] Longitude and Latitude : O
  - [0x58] Ground Speed :  △ (변경 X)
  - [0x59] Quaternion : △ (변경 X)
  - [0x5a] Satellite Positioning Accuracy : △ (변경 X)



#### 1123

- 데이터 작업은 여기까지 하고 다음 진행
- 앞으로 할 것 : 
  - 전체 데이터 잘 들어오면 확인 후 python 으로 이전과 같이 Edge로 전송 할수 있도록!!
  - **GPS 차량 촬영 때 영상데이터 및 GPS 값 Edge에 저장해야는 코드 만들어야함**
  - ~~DEMS 영상 캡처 시 항상 사용 가능한 카메라 주소 변경해줘야함~~ 
    - 아마도 video-streaming 파일
- 진행중 : 
  - /gps/cpp_http_test.cpp -> /gps/rest/gps_server.py 로 post 전송 완료
    - 이제 cpp 에서 json으로 데이터 만들어서 보내는 것 진행 후 gps_with_gyro.cpp 에 적용
    - 취소
  - 파일 쓰는거 일단 완료
  - python 으로 파일 읽고 json 으로 parsing 해서 데이터 보내보기



#### 1124

- ~~**gps_server 에서 잘 받아오긴하는데 gps 소수점 데이터가 다 들어오지 않음 어떻게 된건지 확인 필요!~!!**~~
- **<mark>시스템 구조</mark>**
  - 5G CCTV
    - 서버이름 : keti-5g-0
    - 주소 : rtsp://root:keti1234@192.168.225.30:88/videoMain
  - 5G BlackBox
    - <mark>**5G 모뎀 연결 후 주소 업데이트 필요**</mark>
  - GPS server
    - gps_with_gyro3.cpp : gwg 시리얼 데이터 추출 후 txt 파일로 저장
    - gps_with_gyro3.py : txt파일 읽고 Edge server 로 전송 **(저장하려면 py 실행시 arg 줘야함!)**
  - Edge Server
    - gwg_server.py : 
      - 전달받은 gwg 데이터 DB에 저장(현재 DB : gwg_text.db)
      - gwg_temp_transfer 에서 전달받은 데이터 변수 저장 후 get요청시 전달
      - 인텔리빅스에서 요청할때 주소[GET] : http://123.214.186.162:8088/get_gwg
      - 실시간 연동시 요청 주소[GET] : http://123.214.186.162:8088/get_gwgData
    - gwg_temp_transfer.py : gwg_text.db 의 데이터 읽어서 다시 gwg_server로 전송
- 해야할 것 : 
  - 블랙박스 영상데이터 -> Edge 전송 후 저장해야함!!
    - vlc 플레이어로 영상 저장 후 저장된 파일으로 스트리밍 가능
  - 확인 필요 : 
    - 5G CCTV - 5G 모뎀 연결여부



#### 1128

- **<mark>전체 구조</mark>** : 
  - Edge Server
    - 주소 : 123.214.186.162
    - RSTP 재전송 : 
      - 5G CCTV
        - cvlc -vvv rtp://123.214.186.162:5004 --sout="#rtp{sdp=rtsp://123.214.186.162:8554/videoMain}" --no-sout-all --sout-keep
      - 5G Blackbox
        - cvlc -vvv rtp://123.214.186.162:5005 --sout="#rtp{sdp=rtsp://123.214.186.162:8555/videoMain}" --no-sout-all --sout-keep
  - 5G CCTV
    - 모뎀 : SKT
    - rtsp://root:keti1234@192.168.225.30:88/videoMain
    - Edge 로 재전송 :  vlc -vvv rtsp://root:keti1234@192.168.225.30:88/videoMain --sout="#rtp{dst=123.214.186.162,port=5004,mux=ts}" --no-sout-all --sout-keep
  - 5G Blackbox
    - 모뎀 : 큐오핀 
    - rtsp://192.168.0.101:554/h264
    - Edge 로 재전송 : cvlc -vvv rtsp://192.168.1.101:554/h264 --sout="#rtp{dst=123.214.186.162,port=5005,mux=ts}" --no-sout-all --sout-keep
- 해야할 것 : 
  - 블랙박스 영상데이터 -> Edge 전송 후 저장해야함!!
    - vlc 플레이어로 영상 저장 후 저장된 파일으로 스트리밍 가능
  - 확인 필요 : 
    - 5G CCTV - 5G 모뎀 연결여부
- 원격

  - g26112fw
  - 9tf2f7p4

- 휴컵 5G 모뎀
  - key : 20160111
  - 변경 전 : m2m-5G-static.lguplus.co.kr
  - 변경 후 : m2m-5G-router.lguplus.co.kr



#### 1129

- 해야할 것들 : 
  - Blackbox GPS 산책하며 측정
    - 데이터 잘 나옴 - gwg_test_sa_1.db 에 저장 후 송출중
  - Blackbox 내부에서 녹화해보기
  - 녹화본 무한루프로 스트리밍 가능한지
  - C++ - python 컴파일하는 방법 공부
  - DEMS 기능 전부 가능하게끔
- 일정 : 
  - 1월 말까지 모든 것 완성
  - 2월 검증단 회의
- 문제 : 
  - 큐오핀 모뎀이 연결이 끊길때가 있음..



#### 1130

- todo : 

  - Blackbox GPS 산책하며 측정 - **<완료>**
    - 데이터 잘 나옴 - gwg_test_sa_1.db 에 저장 후 송출중
  - Blackbox 내부에서 녹화해보기
  - 녹화본 무한루프로 스트리밍 가능한지
  - C++ - python 컴파일하는 방법 공부
  - DEMS 기능 전부 가능하게끔

- 문제 : 

  - [핑 테스트]

    1. 고정 ip 큐오핀 
       - 412 패킷이 전송되었습니다, 397 수신되었습니다, 3.64078% 패킷 손실, 시간 420847ms
       - 224 패킷이 전송되었습니다, 224 수신되었습니다, 0% 패킷 손실, 시간 228331ms
    2. 큐오핀2(현재 사용중)
       - 955 패킷이 전송되었습니다, 903 수신되었습니다, 5.44503% 패킷 손실, 시간 976865ms		
       - 9205 패킷이 전송되었습니다, 8728 수신되었습니다, 5.18197% 패킷 손실, 시간 9424892ms
       - 1836 패킷이 전송되었습니다, 1621 수신되었습니다, 11.7102% 패킷 손실, 시간 1879031ms
       - 4165 패킷이 전송되었습니다, 3744 수신되었습니다, 10.108% 패킷 손실, 시간 4263937ms

- 원격

  - g26112fw
  - 9tf2f7p4



#### 1201

- todo : 
  - Blackbox GPS 산책하며 측정 - **<완료>**
    - 데이터 잘 나옴 - gwg_test_sa_1.db 에 저장 후 송출중
  - Blackbox 내부에서 녹화해보기
    - 노트북 비디오 폴더에 test2 로 저장함
    - 문제 : 라우터 불안정으로 네트워크 끊김현상이 발생하고 멈춤..
  - MP4 무한루프 스트리밍 - **<완료>**
    - [cvlc document 페이지](https://helpmanual.io/help/cvlc/)
    - `--input-repeat` 옵션으로 반복 가능 **다만 플레이어(클라이언트)에서도 무한반복 해줘야함**
    - mp4 스트리밍 : cvlc /home/keti0/비디오/test2.mp4 --sout=#rtp{sdp=rtsp://:8585/videoMain} --no-sout-all --sout-keep
  - C++ - python 컴파일하는 방법 공부
    - [c/c++ 을 extension 을 통해 python 에서 호출](https://kukuta.tistory.com/374)
  - DEMS 기능 전부 가능하게끔



#### 1205

- todo : 
  - Blackbox GPS 산책하며 측정 - **<완료>**
    - 데이터 잘 나옴 - gwg_test_sa_1.db 에 저장 후 송출중
  - Blackbox 내부에서 녹화해보기
    - 노트북 비디오 폴더에 test2 로 저장함
    - 문제 : 라우터 불안정으로 네트워크 끊김현상이 발생하고 멈춤..
  - MP4 무한루프 스트리밍 - **<완료>**
    - [cvlc document 페이지](https://helpmanual.io/help/cvlc/)
    - `--input-repeat` 옵션으로 반복 가능 **다만 플레이어(클라이언트)에서도 무한반복 해줘야함**
    - mp4 스트리밍 : cvlc /home/keti0/비디오/test2.mp4 --sout=#rtp{sdp=rtsp://:8585/videoMain} --no-sout-all --sout-keep
  - C++ - python 컴파일하는 방법 공부
    - [c/c++ 을 extension 을 통해 python 에서 호출](https://kukuta.tistory.com/374)
    - 이 부분 진행중
  - DEMS 기능 전부 가능하게끔



#### 1207

- C++ - python 컴파일 진행하고 DEMS  기능 살리기
- 무선엣지과제도 확인 후 연동하는거 진행해야함

