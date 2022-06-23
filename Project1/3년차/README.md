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



## reference

- [python sqlite3 참고 블로그](https://hleecaster.com/python-sqlite3/)
- [python socket 채팅 프로그램](https://seolin.tistory.com/98?category=762768)



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
  - 서버1(공유기) - 서버2(핸드폰 테더링) 둘 사이간 접속이 안됨.. // 네트워크 문제
  - rtsp 를 받아와서 스트리밍서버로 만드는게 안됨 // ?
- 할 것 : 
  - 서버1 : rtsp -> rtp(?) 로 서버2로 전송
  - 서버2 : 받은 rtp를 rtsp 로 다시 스트리밍