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

