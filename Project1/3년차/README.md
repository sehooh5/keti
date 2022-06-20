# Project 1 3년차

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