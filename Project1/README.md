# Project 1

- 5G 기반 협력 대응 과제
- 전체 내용 `5G`  파일에 정리



### 사용 툴 버전

---

- ubuntu : 18.04
- kubernetes : 1.14
- docker : 최신버전 19.03.12 (현, 2020.08.04)
- Prometheus 
- Grafana 
- OpenCV
- VLC
- RTSP
- Flask : 1.0.2



### 참고 자료

---

### 전체적 시나리오 잘 정리된 페이지

- [시나리오](https://medium.com/finda-tech/overview-8d169b2a54ff)
- [기본적인 docker-kubernetes 관계 및 용어들 정리 잘해놓음](https://zzsza.github.io/development/2018/04/17/docker-kubernetes/)



#### Ubuntu

- [Ubuntu 설치방법](https://coding-factory.tistory.com/494)
- [Ubuntu 네트워크 설정 CLI](https://ismydream.tistory.com/99)
- [Ubuntu 네트워크 설정 GUI(이거 사용했음)](https://webdir.tistory.com/188)
- [vi 사용법](https://jhnyang.tistory.com/54)



#### Docker

- [Docker?(subicura)](https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html)
- [설치 및 실행(subicura)](https://subicura.com/2017/01/19/docker-guide-for-beginners-2.html)
- [Ubuntu 18.04 버전 다운로드](http://mirror.kakao.com/ubuntu-releases/bionic/)
- [Ubuntu 에 Docker 최신버전 설치](https://www.dante2k.com/581)
- [Ubuntu에 Docker 설치(HiSEON)](https://hiseon.me/linux/ubuntu/install-docker/)
- [설치-공식문서](https://kubernetes.io/docs/setup/production-environment/container-runtimes/#docker)



#### Kubernetes

- [공식 도큐먼트](https://kubernetes.io/ko/docs/concepts/overview/what-is-kubernetes/)
- [Kubernetes?(subicura)](https://subicura.com/2019/05/19/kubernetes-basic-1.html)
- [Ubuntu에 Kubernetes 설치(HiSEON)](https://hiseon.me/linux/ubuntu/ubuntu-kubernetes-install/)
- [전달받은 설치 문서](https://www.joinc.co.kr/w/man/12/kubernetes/kubecluster)
- [전달받은 설치 문서 2**](https://medium.com/finda-tech/overview-8d169b2a54ff)
- [설치 실패시 초기화방법](https://likefree.tistory.com/13)
- [명령어 등 참고하면 좋은자료](https://zzsza.github.io/development/2018/04/17/docker-kubernetes/)
- [정리 잘해놓은 블로그](https://tommypagy.tistory.com/180)
- [전반적인 쿠버네티스 시작부터 활용까지 잘 정리](https://arisu1000.tistory.com/category/Kubernetes?page=1)



#### Prometheus

- [모니터링 개념 설명]([https://medium.com/@tkdgy0801/prometheus-%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81-part-1-69de3e87d427](https://medium.com/@tkdgy0801/prometheus-를-이용한-모니터링-part-1-69de3e87d427))
- 추가할것



#### Flask video streaming

- [Miguel 자료](https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited/page/4)



#### CSS

- [on / off 똑딱이](https://freshdesignweb.com/css3-buttons/)



## 진행 단계(daily)

### 2020 (1차년도)

---

#### 0804

- 테스트베드 구축에 대한 탐구
  - 사용하는 프로그램, 툴에 대한 언어 공부 및 활용 방법 모색
  - Ubuntu 기반 **Kubernetes**를 사용하여 Master/Worker 서버에 대한 환경 구축(**Docker** 활용)
- 베어본 PC 사용하여 직접 설치해보기
- **설치 순서**: Ubuntu - Docker - Kubernetes
- **Rufus** 로 USB 에 부팅 가능한 ISO 파일 저장후 사용하게끔하기
- 완료 : keti0 컴퓨터에 Ubuntu 설치완료, 네트워크 static IPv4 설정 완료, 3개 컴퓨터 이더넷으로 연결 ( IPv4 : 192.168.100.5, 6, 7)



#### 0805

- 완료 : Docker*3 설치 완료



#### 0806

- 완료 : kubernetes 용어정리 및 설치 완료

  (쿠버네티스 잘 작동되는지 확인해야함) 



#### 0807

- 진행중 :  Kubernetes 설정



#### 0810

- 완료 : 3대 Kubernetes 설치 및 마스터(keti0), 워커 2대(keti1, keti2) 노드설정 완료
- 오류 : keti2 연결 안됨(Status : Not Ready), Scheduler & Kube-Controller-manager : Unhealthy 상태
- 완료 : 3대 설치 완료

- 오류 : 연동 되는데 not ready, unhealthy



#### 0811

- 완료 : master 1 / worker 1 설치 완료,  배포완료
- 오류 : unhealthy 여전히 뜨고 한 대는 join 안됨



#### 0812

- 진행중 : Prometheus 란? , Granfana?, 동적으로 사용가능한 리소스 찾기

- 오류 : 

  - 재부팅하면 `kubectl` 명령어 시 port를 못찾을 때가 있음 - 시간지나면 해결
  - 아직도 `kubectl get cs` : scheduler, c-m - unhealthy 상태

- 완료 : master-worker(2 pc) 연결 완료

- 앞으로 진행할 내용

  

  1. 동적으로 리소스를 확인할 수 잇는지?
  2. 프로메테우스, kubectl 이 찾을 수 있는 리소스 개수들

  

  결론 : 리소스 모니터링에 **프로메테우스 Granfana** 를 사용할 지 **k8s 내부 모듈**을 사용할지




#### 0813-14

- prometheus & grafana 설치 도중 오류 발생시켜 다시 복구중



#### 0818

- master cluster 포맷 후 ubuntu 부터 다시 설치
- master - w1,w2 에 대한 k8s 설치 및 연결 완료
- 진행중 : 프로메테우스 설치 후 image pull 안되는 에러 발생!
- **내일중으로 해결할 것!!**



#### 0819

- server, alertmanager - pending & exporter, pushgateway Imagepullbackoff 고치기!
- **프로메테우스 helm으로 설치완료**



#### 0820

- 그라파나 설치하기
  - 일단 prometheus yaml 파일들 수정 안하고 그라파나 먼저 설치 후 잘 돌아가는지 확인하고 진행
  - **helm 설치 지우고 yaml 파일 직접 작성하여 적용시켰음**



#### 0821

- 프로메테우스, 그라파나 설치 내용 정리하기
- 프로메테우스 및 그라파나 개념 정리
- 프로메테우스 및 그라파나에서 사용할 수 있는 데이터 정리해서 보고



#### 0824

- 내용 정리 : 
  - Grafana, Prometheus 에서 모니터링 가능한 내용 정리하기
- 문제 해결 : 
  - swapoff 모든 컴퓨터에서 다시 해주어야 돌아가는데 고정하는 방법?
  - ~~ImgPullOff 도 수동으로 해주었어야하는데 지금은 작동됨~~
  - 결론 : 껐다 켰을 때 자동으로 셋업되게 하는 방법



#### 0825

- k8s 의 마스터노드를 통해서 워커노드에게 명령 내릴수 잇도록

  (vlc rstp 명령)

- 진행해야할 순서

  1. Container 만드는데 OpenCV로 카메라 URL 열어서 받은 데이터가 있는지 없는지 
  2. Camera 에 대한 CRD 작성하기
  3. FLASK로 MJPEG/HTTP만들어서 전송해주기
  4. 서비스 오픈하게끔
  5. 웹서비스 구현



#### 0826

- python, vs code 설치 완료
- openCV 활용하여 비디오 끌어오기 완료 - python 예제 opencv1.py
- container 만들어보기



#### 0831

- git 연동완료
- Contatiner 만들고 OpenCV 사용하는거 연습



#### 0901

- Container 작성하는거 완성하기



#### 0907

- ~~네트워크 연결~~
  - **앞으로는 이더넷은 연결 끊고 와이파이만 사용하다가 필요시 이더넷 사용**
- ~~네트워크 복구 및 기존 했던것들 진행~~
  - 복구 완료
  - **docker hub** 통해서 image 배포까지 완료
- ~~도커 허브 사용해서 이미지를 워커노드에 배포하고 서비스까지 구성 완료~~
  - **localhost:31137 로 연결 가능**
- 이제 openCV 를 컨테이너에 담아서 배포하기



#### 0908

- openCV 컨테이너에 담아서 배포하기
  - 두개 rtsp 주소 받은거로 진행하면 됨!!



#### 0909 

- rtsp 주소 받은 거로 앞으로 개발 진행하면 됨
  - opencv  는 열리는 것 확인 됨



#### 0911

- opencv 컨테이너화 시키기
- 후 배포
- 오늘 오전은 nvidia 드라이버를 미니컴에 설치하는 바람에 재부팅이 안되서 시간을 다 사용했다. 처음에는 난생 처음 보는 에러에 컴퓨터가 켜지지를 않아서 이제까지 한 모든게 날라가나 싶었는데 세시간정도 붙잡고 서칭하면서 겨우 고쳤다. 오후는 opencv  를 도커라이징하는데 문서는 제대로 없고 잘 만들어놓은 Dockerfile 을 찾아서 이미지로 저장하고 실행시켜봤다. 완벽하게 실행되지는 않지만...잘되길..



#### 0914

- opencv 컨테이너화 시키기



#### 0915

- opencv 컨테이너 환경에서 출력 완료
- 다음 작업 시작



#### 0916

- 컨테이너 환경에서 opencv-python을 다시 다운받아야 실행 가능, 왜?
- Docker Images : 
  - opencv-docker1 : 처음으로 open 적용된
  - opencv-docker2 : 워크스페이스 추가
  - opencv-python3 : kubectl 배포중 CrashLoopBackOff 오류 발생 제거
  - opencv-python4 : 워크스페이스에서 열리지 않은것들 수정, 파일들 복사
  - opencv-python5 : CrashLoopBackOff 다시 발생, deployment 에 천천히 만드는 sleep 명령어 삽입



#### 0917

- 이제까지 과정 정리 후 pdf 변환
- 질문 정리



#### 0918

- docker image : sehooh5/opencv-python7 이 제대로된 이미지 = 작동 가능
  - opencv-python 을 재 컴파일한 것이 아닌 전부 받아서 했더니 됐다



#### 0919

- 외국인 개발자 코드를 가지고 실행시켜보기 - flask 는 설치 되었고 카메라 연동하면 됨



#### 0922

- Flask 를 활용하여 MPEG/HTTP Streaming 하는 파일 만들기
- 현재 미구엘 코드 사용중
  -  app.py, camera_opencv.py 사용
  - rtsp주소를 수동으로 입력하여 웹페이지에 스트리밍되게 완료
    - 사이즈 조절
    - 여러개 동시에 스트리밍? 



#### 0923

- Miguel 코드로 카메라 이미지 가져오기 완료
  -  주소를 Terminal에 직접 입력해줘야한다..
- 앞으로 해야할 것?
  - 사이즈 조절
  - 여러개 동시에 스트리밍
  - 노드포트로 외부 연결하는 것?
- ing
  - ~~버튼 두개(C1, C2) 각 카메라 페이지로 연결시키기 (잘 되면 ajax 까지)~~
    - ~~한개 rtsp는 연결되었는데 두개를 어떻게 나누어서 연결할지 ...?~~
  - ~~Flask 사용법 / 웹 프로젝트 리뷰하면서 연결하는 방법 찾아보기~~
- done
  - 버튼 두개 만들기
  - 버튼으로 카메라 연결 완료
  - 버튼별로 카메라 연결 완료 - 파라미터 no 에따라 환경변수 및 템플릿을 바꿔서 전달



#### 0924

- NodePort 사용법
- curl 사용법 
- ing
  - 해당 앱을 도커라이징 하는중
    - 문제점 : 도커라이징 하면 기존 flask가 d사용하던 포트 5000 을 인식못한다...
  - 일단 배포 완료했으니 확인해보기 6000으로 노드포트(기존 5000 expose)



#### 0925

- NodePort 사용해서 streaming 앱 배포하기\
  - ~~배포해도 도커에서도 안열렸는데 포트를 5000:5000 으로 했더니 열린다!~~
    - 6000:5000 으로 설정했을 때는 localhost:6000으로 해야 열린다... 하지만 카메라 또한 url 을 localhost:6000을 줘야하는데 이 부분은 select.html 에 button 태그에 설정이 0.0.0.0:5000으로 되어있어서 실행되지 않는다...<mark>**어떻게 해야할까?**</mark>
      - 아마도 .. url 입력에 따라 button 설정 값에 들어가는 것도 바뀌어 설정되게끔....?
  - 일단 k8s 배포는 안되서 패쓰
- 그라파나 프로메테우스 잘 돌아가는지 확인(월요일 확인할것)



#### 0928

- 해결하기

  - 6000:5000 으로 설정했을 때는 localhost:6000으로 해야 열린다... 하지만 카메라 또한 url 을 localhost:6000을 줘야하는데 이 부분은 select.html 에 button 태그에 설정이 0.0.0.0:5000으로 되어있어서 실행되지 않는다...

    어떻게 해야할까?

    - 아마도 .. url 입력에 따라 button 설정 값에 들어가는 것도 바뀌어 설정되게끔....?

- 그라파나 30004(import 10000), 프로메테우스 30003  창 켜두기



#### 1005

- 추석 후 이미지 작업 진행
- 위에 내용은 내일부터 다시 해결하기



#### 1006

- 김책임님 출장
  - 07(수), 금책임님께 여쭤볼 것 정리하기
- 내가 한거 다시 정리해서 앞으로 진행 어떻게 할지 찾아보기 



#### 1007

- flask-video-streaming 쿠버네티스에 배포 완료
- 앞으로 방향 회의
  - 1번 REST API 사용 / 2번 CRD 사용
  - 일단 REST API 사용
  - 배포할 때는 ReplicaSet 말고 Demonset 혹은 노드별 Deploy



#### 1008

- ~~Demonset 혹은 노드별 Deploy 배포방법 공부~~
- ~~REST API 공부~~
- ~~공부는 약 1주일~~    
- 현재 새로운 폴더를 만들어서 manager / viewer 나누어서 실행 중
  - 배포 해봤는데 방법을 좀 다르게 해야함
  - ~~지금은 camera_opencv.py 에서 Camera class 를 다르게 지정하는 방법 하는중~~
  - 지금은 manager 에 url 값을 바로 카메라 주소 써서 보내는데 이것도 안될듯



#### 1012

- ~~POST 방법으로 form date 보내고 받는거로 해보기(url 이 변경되지 않음)~~
  - 로컬 환경에서는 제대로 작동하지만, 매니저 화면은 바뀌는 형태로만 됨
  - 우리가 마지막에 구현할 것은 매니저 화면 고정+워커노드의 화면만 바뀌어야함
- SSE 에 관한 내용 더 살펴보고 공부하기



#### 1013

- SSE 에 관한 내용 더 살펴보고 공부하기

- flask-socketio 로 진행했음
  - 지금 예제 구현은 완료 했고 앞으로 어떻게 할지 생각해보기



#### 1014

- ~~Flask-socketio 익숙해지기~~
- 현재는 WebSocket 으로 변경해서 진행하고있음
  - button 형식으로 눌러서, 서버에서  url 값을 os.environ 에 설정하는 방식으로 하는중
  - 현재 생각하는 방식은 client(1개)에서 값을 넘겨주는데, Streaming app 의 서버를 3개 열어주는형식



#### 1015

- Websocket  방법
  - 클라이언트에서 여러 port 로 넘길수 있는지?
- ~~[이 방법으로 구현하기 - flask socketio](https://learn.alwaysai.co/build-your-own-video-streaming-server-with-flask-socketio)~~
- 기존 test  폴더에 flask-socketio 로 다시 진행중 (main.py - session.html + manager.html, viewer.html)



#### 1019

- ~~기존 test  폴더에 flask-socketio 로 다시 진행중 (main.py - session.html + manager.html, viewer.html)~~
- ~~**현재**, LiveStream 폴더로 진행중~~
- 일단 socket 사용 중지!!,,,,,,,,
  1. 기존 방식으로 진행하되 stop 기능이 들어가서 **카메라 전환**이 잘 될 수 있도록!
  2. 카메라 스트리밍 크기 조절할 수 있도록 알아두기
  3. **UI 디자인** 깔끔하게



#### 1020

- 어떻게든 돌아가는 형태 완성 - <u>검사받기</u>
  - /manager - manager.html, app.py
  - /viewer -  cam1.html, cam2.html, cam1-1.py, cam1-2.py (+ camera_opencv.py, base_camera.py * 2개씩)
- 할 것
  1. 카메라 스트리밍 크기 조절할 수 있게
  2. UI 디자인 깔끔하게
- 완료
  - 매니저 UI - 1.1



#### 1021

- ~~마스터 서버 버튼 배열 가로로~~
- ~~워커 서버 버튼별로 테두리~~ **완료**
- ~~상태바, 주소창 가릴수 있는지?~~
  - 주소창 가리기는 아직 못찾음
  - 대신, 듀얼 모니터 가능
- ~~opencv 사이즈 조절하기~~ **완료**
- 우분투 동영상 캡쳐 가능한지 : Ctrl +Alt +Shift + r
- **쿠버네티스에 앱 배포하기!!**
  - 도커환경에서 실행되는 것 확인했음



#### 1022

- ~~k8s 에 배포 실패, 수정하기~~
  - **k8s 에 배포 완료!!** 
    - manager : 30000
    - viewer1 : 30021
    - viewer2 : 30022
- **Grafana - Prometheus** 작동 확인
  - Granfana : 30004
  - Prometheus : 30003



#### 1023

- 김책임님 가이드 주시면 개발 내용 정리하기!

=======
- 개발 내용 정리하기!



#### 1026

- 환경 설정 부분 내부 촬영하기



#### 1027

- 중간 점검까지 내용 정리
- k8s, 프로메테우스, 그라파나 우리 UI 다룰 수 있을 정도로 공부



#### 1028

- 오전만/ 프로메테우스 그라파나 공부



#### 1029

- 프로메테우스





### 2021 (2차년도)

---

#### 0618

- UI 초안 및 추가기능 완료
- 새롭게 시작 :
  - 영상,메타정보를 전달하는 릴레이서버 구성
    - `CCTV(server) - Edge(client+server) - VMS(client)` 형태의 구성



#### 0622

- 전체 회의 내용 토대로 릴레이서버 구성하는 테스트 하기(요번주내)
  - 영상,메타정보를 전달하는 릴레이서버 구성
    - `CCTV(server) - Edge(client+server) - VMS(client)` 형태의 구성



#### 0623

- 릴레이서버 구축 : 
  - Wowza  찾아보는중
    - 와우자는 완성된 프로그램인듯?
  - Gstreamer - python(ubuntu 기반)
    - https://dkant.net/2019/05/17/Gstreamer01/
    - 이 서버내용대로 worker1, 2 딴에서 relay server 가 돌아가면 될듯 
      - 먼저 테스트해서 위 내용대로 잘 작동하는지 master 에서 구현 후
      - relay server 도커로 만든 후 k8s 로 worker1,2 에 배포
  - [관련 논문](http://koreascience.or.kr/article/CFKO200724737420524.pdf)



#### 0624

- 위 내용 중 Gstreamer 개념으로 테스트배드 구축하기
  - [내 작업 내용](https://github.com/sehooh5/keti/blob/master/Project1/relayserver/gstreamer.md)
- 잘 안됨



#### 0625

- 일단 쉘에서는 카메라 켜짐, 파이선파일도 에러는 고친듯
- 그다음 파이썬 예제 찾아보고 이어서해보기
- ~~깃허브에  rtsp-simple-server 보고 하는중~~
  - ~~주소 : https://github.com/aler9/rtsp-simple-server~~ 일단 보류
- version 오류 뜨는거는 무시해도 되는거같은데, 일단 텍스트파일로 저장하면 에러 해결
- 지금은 일단 돌아는 가는거같은데 ..... server 구동되는지 확인 + 클라이언트 연결하는거 하면될듯



#### 0701

- gstreamer 다시 시작
- `relayserver` repository
  - server_test2.py : test video on -> auto off
  - server_test.py : stopped in CLI
- CLI using : OK





#### 0702

- Wowza start
- Using CLI improve



#### 0705

- wowza start with developer license
  - made basic
    - vod sample check
    - live... how to connect my rtsp address to wowza
  - improve about JAVA environ
  - [refo blog](https://m.blog.naver.com/PostView.naver?blogId=woliver&logNo=221833439445&targetKeyword=&targetRecommendationCode=1)



#### 0706

- Wowza keep going
- what shoud i use for relay server?



#### 0707

- meeting for next step
- [와우자 기본적 내용 잘 정리된 블로그](https://help.iwinv.kr/manual/read.html?idx=679)
- wowza ing
  - 다시 rtsp 사용하는 예제 보면서 시작해보기
  - rtsp://192.168.0.29:1935/live/test01.stream 주소로 vlc 플레이어 사용해서 보여지는데 된건가?
    - https://www.wowza.com/docs/how-to-re-stream-video-from-an-ip-camera-rtsp-rtp-re-streaming 이거보고 따라함
    - [해당 내용으로 유튜브 스트리밍 하는 방법](https://www.youtube.com/watch?v=9AYCwibnjDE) : 내일부터 스트리밍 가능
    - [페북 라이브로 스트리밍 성공](https://www.youtube.com/watch?v=ZRWTnmHof_g)
  - **페북 라이브로 스트리밍 넘기는거까지 완성햇음!!**
- git push default setting
- [HLS 멀티뷰 시스템 관련 논문](https://www.koreascience.or.kr/article/JAKO201734963727796.pdf)
- [와우자 리스트리밍 관련 논문](http://koreascience.kr/article/CFKO201130533389393.pdf)



#### 0708

- 페북 라이브 스트리밍 한것 토대로 진



#### 0709

- wowaz improve
- rtsp://keti:keti1234@192.168.100.60:8805/videoMain 새로운 카메라까지 동시 연결하는중
  - 연결 완료 후 두개의 카메라 두개의 클라이언트로 따로 전송 완료



#### 0712

- 완성된것 박사님 보여드리고 연결이 어떻게 구성되어있는지 보고드리기!
- 그 전에 live edge 사용하는거 진행해보고 다음단계로
- **릴레이서버 STOP**
- **2차년도 본격적으로 시작**
  - 클러스터 구성 등에 필요한 Open API 파라미터, 아규먼트 전달드리기



#### 0713

- SW 동작, 중지하는 부분부터 정리하고 책임님께 전달 및 질의
  - 완료 후 컨펌 ok
  - 배포시 설정하는 포트들 어디서 사용하는 포트인지 ? (master or worker)
- OPEN API 종류보고 공부해보기
  - 진행
- 진행 범위는 "DEMS 연동 인터페이스 설계서"의 26쪽 부터



#### 0714

-   에이피아이 구성 시작
- 피피티 및 한글파일 참고
  - 한글파일에는 내꺼 관련한 목록은 없음
  - 일단 작동이 가능하게끔만 프레임 짜두라는 말이신듯



#### 0716

- 기본적으로 내가 생각하는 방향의 API 만들고 있기



#### 0719

- 엣지 클러스터 추가부터 시작..

- DB 만들고 시작해보기 

  - flask-sqlalchemy 로 시작

- 기능 STOP!! 일단 껍데기만 먼저 만들기!!

- 누나 예제

  - get

    ```python
    app.get("/get_edgeInfo", function (req, res) {
        dbclient.connect(url, function (err, db) {
            if (err) throw err;
            db.collection("edgeserver").findOne({
                id: req.query.id
            }, function (err, result) {
                if (result != null) {
                    res.json({
                        code: "0000",
                        message: "처리 성공",
                        id: result.id,
                        name: result.name,
                        type: result.type,
                        ip: result.ip,
                        port: result.port,
                        gps: result.gps
                    })
                } else {
                    res.json(error_code.error9999d);
                }
            })
            db.close()
        })
    });
    ```

  - post

    ```python
    app.post("/add_newEdge", function (req, res) {
        dbclient.connect(url, function (err, db) {
            if (err) throw err;
            let doc = db.collection("edgeserver").update({
                id: req.body.id,
                name: req.body.name,
                type: req.body.type,
                ip: req.body.ip,
                port: req.body.port,
                gps: req.body.gps
            }, req.body, {
                upsert: true
            }, function (err, result) {
                res.json({
                    code: "0000",
                    message: "처리성공",
                    id: req.body.id
                })
            })
            db.close()
        })
    });
    ```



#### 0720

- 껍데기는 다 만들어놨으니 

- flask - **DB 연동**하는 부분부터 다시 공부하면서 시작

  - sqlalchemy (ORM) 방식 사용

    -  특징
       1) 장점

         -  개발자는 DBMS에 대한 큰 고민없이, ORM에 대한 이해만으로 웬만한 CRUD를 다룰 수 있기 때문에,

             비즈로직에 집중할 수 있으므로 개발 생산성을 증가시킬 수 있다.

         - 객체를 통하여 대부분의 데이터를 접근 및 수정을 진행하므로, 코드 가독성이 좋다.

         -  데이터 구조 변경시, 객체에 대한 변경만 이루어지면 되므로, 유지보수성이 좋다.

       

      2) 단점: 

       - 복잡한 쿼리 작성시, ORM 사용에 대한 난이도가 급격히 증가한다.

       - 호출 방식에 따라, 성능이 천차만별이다.

       -  DBMS 고유의 기능을 전부 사용하지는 못한다.

- **postman 사용**하는 방법 진행 - 나중에 

- 질문 : 

  - 2.16~ , 3.4~ 의  사용가능한 포트 조회하는 부분은 같은 내용인데 필요한지?

- 디비 연동부터 시작



#### 0721

- 질문 : 

  - 2.16~ , 3.4~ 의  사용가능한 포트 조회하는 부분은 같은 내용인데 필요한지?

- 외부 api 와 연동해보고 해당 정보가 어떻게 들어오는지(아마도 json) 확인하고 어떻게 사용할 것인지?

  - [urllib.request 사용하여 json 불러오는 예제](https://da-nika.tistory.com/14)
  - [json data 사용하는 예제](https://devpouch.tistory.com/33)
  - [sqlalchemy 사용](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=sys3948&logNo=221624837865)

- 진행 : 

  - SW DB 두개 만들기

    - | 이름        | 타입   | 필수 | 예제값                 | 설명               |
      | ----------- | ------ | ---- | ---------------------- | ------------------ |
      | sid         | String |      | “0xs1”                 | 소프트웨어 고유 ID |
      | name        | String |      | “분석 SW”              | 소프트웨어 명      |
      | fname       | String |      | “content”              | 소프트웨어 파일 명 |
      | copyright   | String |      | “KETI”                 | 저작권자           |
      | type        | String |      | “Container”            | 타입               |
      | description | String |      | “영상 분석 소프트웨어” | 설명               |
      | datetime    | String |      | “2021-07-08”           | 업로드 날자        |

    - | 이름 | 타입   | 필수 | 예제값 | 설명                  |
      | ---- | ------ | ---- | ------ | --------------------- |
      | sid  | String |      | “0xs1” | Master/Worker 서버 ID |
      | wid  | String |      | “0xw1” | 소프트웨어 id         |

  - 포스트맨 사용해보기 - 못함

  - DB에 들어가는거는 확인햇다 DB browser for sqlite 설치함

- 질문 : 

  - api 들이 실행될때 직접적인 기능들이 실행되어야 하는것인지? 기능 실행부분은 다른곳에? (ex 1번기능)



#### 0722

- 2.7 그대로진행하고 sid 만드는 부분했으니 그 다음부터 진행



#### 0726

- [sqlalchemy engine 추가하고 사용하기](https://yujuwon.tistory.com/entry/SQLAlchemy-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0)
- [sqlalchemy 사용](https://edykim.com/ko/post/getting-started-with-sqlalchemy-part-1/)
- [실질적으로 select 찾아서 사용한 부분](https://lowelllll.github.io/til/2019/04/19/TIL-flask-sqlalchemy-orm/)
- API 완성목록
  - 2.1 : 아직 k8s 기능 구현 안됨
  - 2.2 : O, k8s 구현했지만 쿠버네티스에서 사용안해봄
  - 2.3 : ㅁ
  - 2.4 : ㅁ
  - 2.5 : O
  - 2.6 : O
  - 2.7 : O
  - 2.8 : O
  - 2.9 : O
  - 2.10 : O
  - 2.11 : O
  - 2.12 : O
  - 아래부터 포트조회
    - server_sw db에 랜덤한 숫자 부여하는 방식으로
    - 배포될 때 port 3개의 정보를 함께 저장
    - server id 로 POST 전달하면 해당 서버에서 사용 가능한 port 번호 전달
  - 2.13 : O
  - 2.14 : O
  - 2.15 : O



#### 0727

- 2.5부터 시작하면 될듯? 완료
- Datetime 넣기 - 완료



#### 0728

- 포트찾기 완료
  - 수정 : 포트에 대한 DB 를 추가했음(server_sw 3개의 column으로 추가)



#### 0729

- 디바이스 연결 부분 생각하고 API 작성하기 - 내일이후
- 내일까지 쿠버네티스 교육



#### 0802

- 디바이스 연결부분 시작 - 타 API 연동 후 작동하는지 여부 확인하면서 더 진행
- 2.1 클러스터 추가할 때 원격으로 워커노드 cli 명령 보내는 작업 진행중
  - OpenSSH 서버 설치 
    -  [참고1](https://dora-guide.com/ssh-%EC%A0%91%EC%86%8D/)
    - [참고2](https://jootc.com/p/201808031462)
  -  keti0에서 keti1 로 ssh 접속 성공...이내용 대로 명령 할 수 있게 python 코드 구성하면 될듯
  - 코드구성 완료
- 전체적인 틀 및 구현가능하게 완성 app.py 
  - 내일 회의 후에 연동 가능하게 한 후에 작동시켜보면서 작업하기



#### 0803

- 전체 회의
- 엣지 클러스터 추가 시 ssh 연결하는 동작 구현



#### 0804

- 전체 api 검토
- api 연결사례 등 보면서 시뮬레이션



#### 0805

- 06일에는 워크스테이션 글카 채우기
- 에이피아이 진행