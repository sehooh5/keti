# Project 6

- **무선 엣지 영상보안 시스템 기술 개발** (2022 신규)

- **과제 목표** : 엣지 AI 보안지능에 대한 지속적 최적화 및 엣지 보안단말의 연계협업을 기반으로, 고립지원격지에 대한 치안 및 생활안전 강화가 가능한 무선 엣지 영상보안시스템 핵심 기술 개발
- **내 수행 과제** : 아래 두개는 비슷
  - 엣지 AI 보안지능 패키지의 등록·관리 기술 개발 (UI 및 클라이언트 포함)
    - 엣지 AI 보안지능 패키지 등록·관리 클라이언트 개발
    - 엣지 AI 보안지능 패키지 및 메타데이터 DB 구조 설계 및 구축
    - 엣지 AI 보안지능 패키지 및 메타데이터 저장·관리 기술 개발
  - 엣지 보안단말 등록·관리 클라이언트 개발 및 등록·관리 기술 설계 (UI 및 클라이언트 포함)
    - 엣지 보안단말 등록·관리 클라이언트 개발
    - 엣지 보안단말 정보 메타데이터 구조 설계
    - 엣지 보안단말 정보 저장 DB 구조 설계
    - 엣지 보안단말 등록·관리 인터페이스 설계
  - 이벤트 발생에 따른 연계협업



### 개발 환경

---

- Server : 
  - Node.js
- DB : 
  - MongoDB
- Container : 
  - Docker
- Deploy : 
  - Kubernetes
- Monitoring : 
  - Prometheus
  - Grafana



### DB 데이터 정보

---

#### AI 패키지 정보 등록/검색 DB 데이터

- AI 패키지 ID
- AI 패키지 명(한글)
- AI 패키지 파일 명
- 저작권자
- 설명
- 등록 날짜



#### 엣지 단말기 정보 등록/검색 DB 데이터

- 엣지 단말기 ID
- 엣지 단말기 명
- 엣지 단말기 IP 주소
- 엣지 단말기 포트번호
- 엣지 단말기 위치정보
  - 한글 주소(도로명 혹은 원하는 형식)
  - 위도
  - 경도
- 설명
- 등록 날짜



### daily

---

#### 0518

- 19일(목) 까지 사업계획서 읽어보고 1년차 시연 어떻게 할지 구성해보기



#### 0525

- 회의 기록
  - Do
    - 엣지 AI패키지 / 단말기 등록 시 필요한 DB 메타데이터 정보 정리해서 보고 (6월 2주까지)
    - 엣지 AI패키지 / 단말기 등록, 검색하는 MongoDB Test code 구성하기
  - Schedule
    - 6월만 3째주에 전체회의 / 매 월 첫째주 전체회의
    - 9월 초 보고서 작성예정이니 그 전까지 어느정도 완성되어야하고 9월 말 중간점검 보고



#### 0526

- 엣지 AI패키지 / 단말기 등록 시 필요한 DB 메타데이터 정보 정리



#### 0527

- 메타데이터 정보 확인 후 MongoDB 로 데이터 로직 구성하기



#### 0531

- 데이터 로직 구성



#### 0602

- 데이터 로직



#### 0603

- nodejs 교과서 로 mongoose 구성중



#### 0607

- p.390 routes/users.js 부터 다시 시작 !!



### 1년차 진행내용

---

- 내 파트에서 DB 사용은 하지 않음
- 쿠버네티스 클러스터링 및 AI SW 배포



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
      - **현재 웹앱 시나리오** : 
        - 단말등록 : 기존의 클러스터링으로 worker node 추가하는 기능
        - 엣지 AI 등록 : SW 업로드 기능
        - 엣지 AI 배포 : SW 배포 기능



#### 1025

- **만들어야 하는 마스터노드에서 실행되는 API 서버 시나리오** : 

  - 단말등록 : 기존의 클러스터링으로 worker node 추가하는 기능
  - 엣지 AI 등록 : SW 업로드 기능
  - 엣지 AI 배포 : SW 배포 기능

- 진행 완료 : 

  - 1개 미니PC(edge01)에 쿠버네티스까지 **설치 완료**

- 진행중 : 

  - 서박사님 pc - edge01 의 역할 정하기

    - 마스터노드 or 워커노드
    - 아직 어떻게 진행할지 모르고, keti2-keti1 으로 잘 돌아가는지만 확인

  - 기존 keti2(M)-keti1(W)에서 서박사님 SW 가 잘 작동하는지 확인

    - Project6/dockerfile/ 에 dockerfile 작성 해서 진행중

    - docker run 실행 시 오류 내용 : 

      ````cmd
      QObject::moveToThread: Current thread (0x55db64d67940) is not the object's thread (0x55db684c3e00).
      Cannot move to target thread (0x55db64d67940)
      
      qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/usr/local/lib/python3.8/site-packages/cv2/qt/plugins" even though it was found.
      This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
      
      Available platform plugins are: xcb, eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl.
      
      Aborted (core dumped)
      
      ````

      - docker 환경에서 display app 이 바로 실행이 되지 않아 생기는 에러인듯
      - 해결 방법 : 
        - xhost +local:docker ? xhost +local:root ? 
        - 해결방법 찾고 내일부터 진행 후 오후에 서박사님과 회의

  - 기존 서버에서 실행시키고 마스터 노드에서 k8s 를 실행시킬 수 있는 API 서버를 만들어야함



#### 1026

- 해결방법 찾기

  - [docker에서 컨테이너 GUI 실행하기](https://conservative-vector.tistory.com/entry/docker%EC%97%90%EC%84%9C-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88-gui-%EC%8B%A4%ED%96%89%ED%95%98%EA%B8%B0)

    - 우분투는 `Xorg`라는 그래픽 프로그램을 이용한다. 즉, 얘가 있어야 그래픽을 띄워줄 수 있다는 얘기.
      그럼 도커에서 그래픽을 띄워주려면? 호스트의 자원을 공유하면 된다. 호스트의 Xorg를 컨테이너가 이용하면 된다는 말. 실행옵션을 추가해주면 컨테이너에서도 그래픽을 볼 수 있다.

    - ![image](https://user-images.githubusercontent.com/58541635/197915019-b27dcd62-5b27-4bf3-9a55-a57a99eb812c.png)

    - **XServer 공유하기**

      - host의 XServer를 볼륨형태로 컨테이너와 공유하자. DISPLAY 환경 변수도 전달해줘야 한다.
        유닉스 도메인 소켓을 이용하여 host의 XServer와 도커 컨테이너를 연결한다.  readonly옵션을 준다. XServer소켓은 `/tmp/.X11-unix`에 존재한다.

        ```
        $ docker run -it \
        --volume /tmp/.X11-unix:/tmp/.X11-unix:ro \
        -e DISPLAY=unix$DISPLAY \
        sehooh5/ai-test
        ```

      - 호스트에서 도커가 xserver와 통신할 수 있도록 설정한다. 다른 터미널을 열고 작업한다.

        ```
        $ xhost +local:docker
        ```

      - 잘 안됨

  - [Running QT GUI apps with Docker](http://tzutalin.blogspot.com/2017/06/running-qt-gui-apps-with-docker.html)

    - 개발자가 사용한 도커파일 - 변경하진 않고 only 비교용

      ```dockerfile
      # Dockerfile to build Ubuntu:14.04 + Python2.7 + Qt4
      FROM ubuntu:14.04
      
      MAINTAINER Python Builds Eng "tzu.ta.lin@gmail.com"
      
      # Sets language to UTF8 : this works in pretty much all cases
      ENV LANG en_US.UTF-8
      RUN locale-gen $LANG
      ENV DOCKER_ANDROID_LANG en_US
      
      # Add some dep
      RUN rm -rf /var/lib/apt/lists/*
      RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y \
        autoconf \
        build-essential \
        bzip2 \
        curl \
        gcc \
        git \
        groff \
        lib32stdc++6 \
        lib32z1 \
        lib32z1-dev \
        lib32ncurses5 \
        lib32bz2-1.0 \
        libc6-dev \
        libgmp-dev \
        libmpc-dev \
        libmpfr-dev \
        libxslt-dev \
        libxml2-dev \
        m4 \
        make \
        ncurses-dev \
        ocaml \
        openssh-client \
        pkg-config \
        python-software-properties \
        rsync \
        software-properties-common \
        unzip \
        wget \
        zip \
        zlib1g-dev \
        cmake \
        python-pip \
        python2.7-dev \
        python-qt4 \
        pyqt4-dev-tools \
        libffi-dev \
        libssl-dev \
        xvfb \
        --no-install-recommends
      
      
      RUN pip install lxml
      # In order to upload to pypi
      RUN pip install pyopenssl ndg-httpsclient pyasn1 twine
      # Install wine
      RUN dpkg --add-architecture i386
      RUN apt-get update -y && apt-get install -y software-properties-common && add-apt-repository -y ppa:ubuntu-wine/ppa &&  apt-get update -y && apt-get install -y wine1.7 winetricks
      ```

    - 개발자의 명령어를 사용하니 켜지자마자 꺼지기까진 했다

      ```cmd
      # docker 에서 QT GUI 실행하는 명령어
      $ docker run -it \
      --device /dev/dri \ 
      --user $(id -u) \
      -e DISPLAY=unix$DISPLAY \
      --workdir=$(pwd) \
      --volume="/home/$USER:/home/$USER" \
      --volume="/etc/group:/etc/group:ro" \
      --volume="/etc/passwd:/etc/passwd:ro" \
      --volume="/etc/shadow:/etc/shadow:ro" \
      --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      acb0aa74e757 # 여기만 변경해줌, 내가 사용한 docker image id
      
      ######## 아래는 에러 메시지 ########
      # 첫줄 QStandardPaths: ~ 에러는 루트로 실행할 경우 발생되는 메시지로 무시 가능
      QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-keti2'
      libGL error: MESA-LOADER: failed to retrieve device information
      libGL error: Version 4 or later of flush extension not found
      libGL error: failed to load driver: i915
      libGL error: failed to open /dev/dri/card0: No such file or directory
      libGL error: failed to load driver: iris
      Traceback (most recent call last):
        File "/app/main.py", line 33, in run
          model.load_state_dict(torch.load(weight_path, map_location=torch.device('cpu')))
        File "/home/keti2/.local/lib/python3.8/site-packages/torch/serialization.py", line 699, in load
          with _open_file_like(f, 'rb') as opened_file:
        File "/home/keti2/.local/lib/python3.8/site-packages/torch/serialization.py", line 230, in _open_file_like
          return _open_file(name_or_buffer, mode)
        File "/home/keti2/.local/lib/python3.8/site-packages/torch/serialization.py", line 211, in __init__
          super(_open_file, self).__init__(open(name, mode))
      FileNotFoundError: [Errno 2] No such file or directory: 'ViT_models/checkpoint/test_checkpoint.bin'
      ```

      - 에러메시지 : 

        - `QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-keti2'` : 루트로 실행할 경우 발생되는 메시지로 무시 가능
        - `libGL error: failed to open /dev/dri/card0: No such file or directory`  : 에서 driver 설정이 안되서 오류가 발생한 듯
          - 해결 방법 :
            1. `$ xhost +local:docker` 를 실행시켜 docker 에서 연결가능하게 해준다
            2. docker 명령어에 `--device /dev/dri`를 추가해준다
        - 위 방법으로 docker를 실행하고 `/bin/bash` 로 컨테이너 내부를 확인해보니 `/app` 디렉토리가 없다...그러니 `FileNotFoundError`가 뜨는 듯 하다
          - 해결 방법 : 
            - docker 실행 명령어에서 `--workdir` 제거해주니 잘 돌아감

      - **최종 docker 명령어 :** 

        - ```cmd
          $ docker run -it --device /dev/dri --user $(id -u) -e DISPLAY=unix$DISPLAY --volume="/home/$USER:/home/$USER" --volume="/etc/group:/etc/group:ro" --volume="/etc/passwd:/etc/passwd:ro" --volume="/etc/shadow:/etc/shadow:ro" --volume="/etc/sudoers.d:/etc/sudoers.d:ro" -v /tmp/.X11-unix:/tmp/.X11-unix acb0aa74e757
          ```

        - AI가 잘 실행된다

        - 이제 문제점은 쿠버네티스 배포과정에서도 어떻게 잘 실행 될 것인가? docker run 할때 추가되는 것들을 어떻게 같이 실행되게 할 것인가?

          - 일단 k8s 배포를 하게되면 워커노드에서 pod 이 생성되고 실행이되면서 docker image 또한 pull 해서 가져오게 된다. 생성된 docker image 를 ssh를 통해 실행하게되면 가능할까?

            - Worker -> Master 로 ssh 접속후 docker run 했을때 에러메시지

              ```
              # 첫번째 에러
              qt.qpa.xcb: could not connect to display unix
              
              # ssh -XY 접속 후 두번째 에러
              qt.qpa.xcb: could not connect to display unixlocalhost:10.0
              ```

          - docker build 시에 run에서 추가되는 옵션들을 추가할 수 있는지?

          - 워커노드에서 docker pull 할 때 run에서 추가된 옵션들을 추가할 수 있는지?



#### 1027

- 진행 완료 : 

  - docker run 으로 실행 시 pyQt5 GUI 실행 가능

  - AI 를 도커 허브에 push 완료

    - 현재 keti1(W) 에 배포완료, docker run 때 발생한 에러와 같은 에러발생

      ```cmd
      QObject::moveToThread: Current thread (0x5592328fcf70) is not the object's thread (0x559235e97540).
      Cannot move to target thread (0x5592328fcf70)
      
      qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/usr/local/lib/python3.8/site-packages/cv2/qt/plugins" even though it was found.
      This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
      
      Available platform plugins are: xcb, eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl.
      
      ```

  - ssh 접속을 통해 docker images 를 실행시켜도 에러 발생

    ```cmd
    qt.qpa.xcb: could not connect to display unixlocalhost:10.0
    qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
    This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
    
    Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.
    ```

    

- 진행중 : 

  - docker run 에서 사용한 **옵션들 배포시 혹은 이미지 빌드 시 사용 가능한지?** (금요일 회의)

    ```cmd
    $ docker run \
    --device /dev/dri \
  --user $(id -u) \
    -e DISPLAY=unix$DISPLAY \
    -v /home/$USER:/home/$USER \
    -v /etc/group:/etc/group:ro \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/shadow:/etc/shadow:ro \
    -v /etc/sudoers.d:/etc/sudoers.d:ro \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    acb0aa74e757
    ```
  
  - 아니면 배포 후에 pod 실행을 하는 방향으로...?!!



#### 1028

- dockerfile entrypoint, cmd 사용방법 확인해보고 해보기 or k8s deployment의 args 추가

  - v1 - deployment.yaml

    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: ai-test-service
    spec:
      selector:
        app: ai-test
      ports:
        - protocol: "TCP"
          port: 6401
          targetPort: 5401
          nodePort: 32401
      type: NodePort
    
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ai-test
    spec:
      selector:
        matchLabels:
          app: ai-test
      replicas: 1
      template:
        metadata:
          labels:
            app: ai-test
        spec:
          nodeName: keti1
          containers:
            - name: ai-test
              image: sehooh5/ai-test:latest
              imagePullPolicy: Always
              ports:
                - containerPort: 5401
              args: ["--device","/dev/dri","--user","$(id -u)","-e","DISPLAY=unix$DISPLAY","-v","/home/$USER:/home/$USER","-v","/etc/group:/etc/group:ro","-v","/etc/passwd:/etc/passwd:ro","-v","/etc/shadow:/etc/shadow:ro","-v","/etc/sudoers.d:/etc/sudoers.d:ro","-v","/tmp/.X11-unix:/tmp/.X11-unix"]
    ```

    - pod 생성중 에러 : 

      ```cmd
      Error: failed to start container "ai-test": 
      Error response from daemon: 
      OCI runtime create failed: 
      container_linux.go:380: 
      starting container process caused: 
      exec: "--device": executable file not found in $PATH: unknown
      ```



- [GUI 를 k8s를 사용해 배포하여 실패한 사례](https://stackoverflow.com/questions/56398680/is-it-possible-to-deploy-a-gui-application-using-kubernetes)
  - Kubernetes is a cluster-management system that's typically used with dozens (or more!) of headless nodes. It doesn't really make sense to try to run a graphical application there: 



- 예상방법 : 

  - deployment 에 xserver를 사용해서 하는방법 

  - dockerfile 에 docker run 의 args 를 명시할 수 있는지

  - deployment 에 docker run 의 args 를 명시할 수 있는지

    - ```
      - /home/$USER:/home/$USER
      - /etc/group:/etc/group:ro
      - /etc/passwd:/etc/passwd:ro
      - /etc/shadow:/etc/shadow:ro
      - /etc/sudoers.d:/etc/sudoers.d:ro
      - /tmp/.X11-unix:/tmp/.X11-unix
      ```



- **docker 실행명령 :** 

  ```cmd
  $ docker run --device /dev/dri --user $(id -u) -e DISPLAY -v /home/$USER:/home/$USER -v /etc/passwd:/etc/passwd:ro -v /tmp/.X11-unix:/tmp/.X11-unix acb0aa74e757
  ```



- 일단 안됨..
  - 이유 : docker-k8s 환경에서 x11? xserver 연결을 해줘야함
  - docker 에서는 option 을 주어서 됐는데
  - k8s 에서 pod을 생성하는 과정에서 docker image 를 pull 하는데 여기서 option 을 줘야 할거 같은데 option 주는 방법을 모르겠음



#### 1031

- k8s 에 대한 세미나 준비
- GUI 앱 도커 및 k8s 환경에서 배포하는 방법
  - 도커 혹은 k8s 의 config 에서 gui 설정(ex. xserver 등)을 통해 하는 방법이 있는지 확인 



#### 1101

- GUI 앱 도커 및 k8s 환경에서 배포하는 방법
  - 도커 혹은 k8s 의 config 에서 gui 설정(ex. xserver 등)을 통해 하는 방법이 있는지 확인 
  - docker-compose 사용...안됨



#### 1102

- 도커환경을 변경할 수 있는 방법?

- 특허 검토

  - PTZ CCTV 카메라 자동제어 방법 및 시스템

    - 객체 자동 추적 장치가 구비된 CCTV 시스템 [출원번호 : 1020140117734]

      ```
      관심영역에 진입한 객체의 이동 반경을 확인할 수 있도록 상기 객체의 영상을 촬영하는 객체 자동 추적기능을 갖는 CCTV 시스템이 개시된다. 이를 위하여 감시영역 내의 관심영역을 설정받는 사용자 인터페이스와, 상기 관심영역의 좌표값에 따라 감시카메라의 회전각도 및 주밍비율이 설정된 클로즈업 정보를 저장하고 상기 관심영역의 좌표값 정보를 저장하며 상기 감시카메라로부터 수신받은 영상을 저장하는 저장모듈과, 상기 감시카메라로부터 수신된 영상 데이터를 분석하여 상기 관심영역에 진입한 객체를 타겟으로 지정하고 상기 객체의 실시간 좌표값을 분석하며 상기 좌표값에 대등된 클로즈업 정보를 추출하는 영상분석모듈, 및 상기 클로즈업 정보를 유무선 네트워크를 통해 상기 감시카메라로 제공하여 감시영역 내부에서 이동하는 객체에 대한 확대영상을 촬영하도록 감시카메라를 제어하는 제어모듈을 포함하는 객체 자동 추적 장치가 구비된 CCTV 시스템을 제공한다. 본 발명에 의하면, 감시영역에 진입한 객체 중 관심영역에 진입한 객체의 확대영상을 획득하여 저장하므로, 관심영역에 대한 감시 정보의 신뢰성을 높일 수 있다.
      ```

      

    - 제어 및 이벤트 분석을 통한 자동PTZ 프리셋 설정 장치 및 방법 [출원번호 : 10-2014-0195463]

      ```
      본 발명은 CCTV장치에서 제어 및 이벤트 분석을 통한 자동PTZ 프리셋 설정 장치에 관한 것으로서, 팬, 틸트, 줌 동작 수행을 할 수 있는 PTZ카메라와, PTZ카메라의 동작을 운영자의 조작정보에 따라 제어하는 운영 단말기와, 운영 단말기에 의해 제어되는 PTZ카메라의 제어데이터를 기록하는 제어기록 데이터베이스와, 제어기록 데이터 베이스에 기록된 PTZ카메라의 제어데이터에 대해 설정된 기간동안에 대한 운영자 조작기록 정보 또는 설정된 시나리오 조건으로부터 PTZ카메라의 운영조건을 생성하는 제어데이터 분석 및 학습모듈과, 제어데이터 분석 및 학습모듈로부터 운영자 부재시 PTZ카메라의 운영조건에 해당하는 프리셋을 생성하고, 운영단말기로부터 부재모드로 설정되면 생성된 프리셋 조건에 따라 PTZ카메라의 구동을 제어하는 자동 프리셋 설정부를 구비한다. 이러한 CCTV장치에서 제어 및 이벤트 분석을 통한 자동PTZ 프리셋 설정 장치에 의하면, 관제사의 지속적인 모니터링이 없는 상태에서도 실제 운영자 조작의 기록과 카메라에서 발생하는 이벤트를 기반으로 과거 데이터를 통해 자동으로 카메라의 일괄제어 프리셋을 생성하여 인간의 조작경험에 유사한 예측 감시 환경을 조성하여 감시활동을 수행할 수 있는 장점을 제공한다.
      ```

      



#### 1103

- 도커 환경파일 수정방법 찾고 수정해보기

  - [도커파일 작성 방법](https://freedeveloper.tistory.com/189)

  - /project6/도커파일에 docker run options 추가(안됨)

    ```dockerfile
    VOLUME ["/home/$USER"]
    VOLUME ["/etc/passwd"]
    VOLUME ["/tmp/.X11-unix"]
    VOLUME ["/dev/dri"]
    ENV DISPLAY=unix$DISPLAY
    USER 1000	
    ```



#### 1104

- config 수정하는방법 계속 찾아보며 진행
  - [docker-compose 사용](https://gursimarsm.medium.com/run-gui-applications-in-a-docker-container-ca625bad4638) - 안됨
- 진행 사항 : 
  1. Docker의 기본 환경 configuration에서 x11을 사용 가능하게 수정하여 사용
     - 어떤 부분에서 config 설정이 가능한지 모름
  2. Docker build 시 Dockerfile에서 옵션을 추가하여 이미지 자체가 x11 을 사용할 수 있도록
     - dockerfile 옵션에 11/3일 처럼 옵션을 줬는데 같은 에러를 발생시키며 안됨
  3. k8s으로 배포시 Docker 이미지를 사용할 때(Pull) 옵션을 주어서 x11 을 사용할 수 있도록
     - 옵션을 줬는데 에러를 발생시키며  안됨
- 대체 방법 : 
  - ai data 를 생성하고 전달하는 부분만 tcp/ip? 통신으로 실행되고 있는 GUI app에 전달할 수 있는지?



#### 1107

- 대체방법 :
  - GUI app은 실행되고 있으나 ai 분석 데이터는 들어오지 않음
  - ai 분석 프로그램을 배포하면 실행되고있는 GUI app에 분석 데이터가 입력되도록

