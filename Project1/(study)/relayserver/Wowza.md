# Wowza

- wowza 를 활용하여 릴레이서버를 구축
- 릴레이 서버 구축 후 클라이언트에 연결하여 스트리밍(페이스북, 유튜브 등)
- 기본 형태 :`rtsp camera` - `wowza server` - `client`





### Process

---



#### 설치

- wowza 홈페이지에서 해당 OS 에 맞는 Wowza Streaming Engine 설치
- 설치할 때 아이디, 비밀번호 설정



#### 매니저 모드 접속

- `localhost:8088` 로 접속하면 Wowza Streaming Engine 매니저로 접속
- 설치할 때 설정한 아이디, 비밀번호로 접속



#### 주소와 포트번호

- URL : 해당 컴퓨터에 주어지는 주소를 사용하게 됨
- Port : 1935



#### 새로운 어플리케이션 생성

- 맨위 탭에서 `Applications` 탭 사용
- 라이브 혹은 VOD , 두 가지 종류의 앱 생성 가능



#### 서버 설정

- 소스 권한 설정 (Source Authentication)
  - 나중에 어플리케이션을 사용할 때 필요
  - 아이디, 비밀번호 설정



#### 스트리밍 파일 생성

- 스트리밍 할 카메라 등에 대한 정보를 입력하여 사용할 것을 등록

- `Application > (app) > Stream Files` 에서 등록 : `Add Stream File`

- `Add Stream File` 클릭 후 화면

  ![image](https://user-images.githubusercontent.com/58541635/125012926-f041c580-e0a5-11eb-9d29-58184d6007fe.png)

  - 파일 이름을 자유롭게 작성하고 해당 카메라 등의 URI 를 입력해준다
  - 해당 URI : rtsp://keti:keti1234@192.168.100.70:8810/videoMain

- 생성 후 화면

  ![image](https://user-images.githubusercontent.com/58541635/125012773-b2dd3800-e0a5-11eb-8a8e-1d626a4f9e2c.png)



#### 스트리밍 연결 확인

- `Incoming Streams` 에서 연결된 스트리밍을 확인 할 수 있다

- 연결이 잘 되어있으면 Active 상태가 된다. 해당 스트리밍을 사용할 수 있게된 것

  ![image](https://user-images.githubusercontent.com/58541635/125013412-bde49800-e0a6-11eb-8fd5-a30be9f18dbf.png)

- Wowza server에서 재 전송 되는 URI 주소는 위에 `Test Playback` 에서 확인 가능하다

  - 변경된 주소 : rtsp://10.244.0.1:1935/live/test01.stream



#### 스트리밍 전달하기

- `Stream Targets` 을 설정해서 해당 스트리밍을 여러 플랫폼에서 라이브 스트리밍 할 수 있다
- [페이스북에 스트리밍하기](https://www.youtube.com/watch?v=ZRWTnmHof_g)
- [유튜브에 스트리밍하기](https://www.youtube.com/watch?v=9AYCwibnjDE)







### Diagram

---



#### 기본 형태

- `rtsp camera` - `wowza server` - `client`
- rtsp camera : 
  - rtsp://keti:keti1234@192.168.100.70:8810/videoMain
  - rtsp://keti:keti1234@192.168.100.60:8805/videoMain
- wowza server
  - 1 : rtsp://10.244.0.1:1935/live/test01.stream
  - 2 : rtsp://10.244.0.1:1935/live/test02.stream
- client
  - 1 연결 facebook : https://www.facebook.com/100001353957413/videos/295556955588810?comment_id=Y29tbWVudDoyOTU1NTY5NTU1ODg4MTBfMjk1NTY0ODk1NTg4MDE2
  - 2  연결 youtube  :https://www.youtube.com/watch?v=Rq2NUbr92Yk





#### Live Edge

- Live 어플리케이션의 종류

  ![image](https://user-images.githubusercontent.com/58541635/125048904-5ac12880-e0db-11eb-992d-67af68dfb4d6.png)





