# README

- 3차년도 무선 엣지 영상보안시스템 기술 개발
- 무선 엣지 CCTV 개발 및 엣지 AI 보안지능 최적화 및 보안 단말 연계협업
- 엣지간 클러스터링 및 AI 배포, 단말간 협업 기능 개발



### 일정

---

- 6~9월 : KETI 개발부분 진행
- 8월
  - 8/2 : 인텔리빅스 회의, 엣지 모듈 2대 수령 -> 환경구축 시작
- 9월 
  - 중순 : (유선) 엣지 CCTV 5대 완성 후 해당 CCTV로 개발 진행 -> 원주시 설치
  - 9월 말 까지:  전체 시스템(엣지 CCTV, VMS, AI, 분석서버 등) 가져와서 환경구성
- 10월
  - 10월 말 까지 : 최적화 부분 개발 완료, (무선) 엣지 CCTV 완성 후 개발 진행 -> 진현이엔지 설치
- 10~11월 : 전체 시스템 통합



### 개발 목표

---



#### 엣지 AI 보안지능의 지속적 최적화 기술 개발

- 엣지 AI 보안지능의 지속적 최적화 시나리오 연구
  - 서비스 **환경 적응형** 엣지 AI 보안지능 최적화 시나리오 연구
  - 엣지 AI 보안지능의 성능 기반 최적화 시나리오 연구

- 엣지 AI 보안지능 패키지의 등록·관리 기술 개발
  - 엣지 AI 보안지능 패키지 등록·관리 클라이언트 기술 개발
  - 엣지 AI 보안지능 패키지 및 메타데이터 DB 구축 
  - 엣지 AI 보안지능 패키지 및 메타데이터 저장·관리 기술 개발

- 다중 엣지 AI 보안지능 최적화를 위한 엣지 클러스터링 기술 개발
  - 엣지 클러스터 등록·관리 클라이언트 기술 개발
  - 다중 엣지 클러스터링 처리기술 개발
  - 다중 엣지 클러스터링 정보 저장·관리 기술 개발

- 환경 적응형 엣지 AI 패키지 자동 배포·제어기술 개발
  - 서비스 환경정보 모니터링 기술 개발
  - 엣지 AI 보안지능 성능 모니터링 기술 개발
  - 엣지 AI 보안지능의 지속적 최적화 엔진 개발
  - 엣지 AI 패키지 배포 및 제어기술 개발

​    

#### 다중 엣지 보안단말 연계협업 기술 개발

- 다중 엣지 보안단말 연계협업 시나리오 연구
  - 엣지 보안단말 리소스 변화에 따른 연계협업 시나리오 연구
  - 보안 이벤트 발생에 따른 연계협업 시나리오 연구

- 엣지 보안단말 등록·관리 기술 개발
  - 엣지 보안단말 등록·관리 클라이언트 기술 개발
  - 엣지 보안단말 정보 메타데이터 구조 설계 및 메타데이터 처리기술 개발
  - 엣지 보안단말 정보 저장 DB 구조 설계 및 구축
  - 엣지 보안단말 등록·관리 인터페이스 기술 개발 

- 다중 엣지 보안단말 연계협업 알고리즘 개발
  - 다중 엣지 리소스 모니터링 기술 개발
  - 엣지 보안단말 연계협업을 위한 엣지 리소스 예측기술 개발
  - 엣지 보안단말 리소스 및 보안 이벤트 기반 엣지 보안단말 연계협업 결정 알고리즘 개발



## 환경 구성



### [클러스터 구성]

- **Master(New)**

  - Name : edge-m-01(edgem01-NUC11TNKi5)

  - IP : 192.168.0.15

    ```
    # ssh 접속 / keti
    
    ssh edge-m-01@192.168.0.15
    ```

  - 클러스터링 명령

    ```
    # master 실행문
    sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=192.168.0.15
    
    # worker 실행문
    sudo kubeadm join 192.168.0.15:6443 --token qxpxa7.db51bk2m5ge80kpx --discovery-token-ca-cert-hash sha256:fdd4fc4f5a0dc19ce6ffde2cb5410e3c3c8e4df2bb1e0d7dc1c912633eac0b0d 
    ```

  - 초기세팅 다운로드

    ```
    sudo apt install python3-pip
    
    pip3  install flask
    ```

    

    

- ~~**Master(기존)**~~

  - Name : keti-orin-02(keti-jx-02)

  - IP : 192.168.0.4

    ```
    # ssh 접속
    
    ssh keti-jx-02@192.168.0.4
    ```

    

  - JSON 형태 정보 예시 : 

    ```json
    {    
        "name" : “Master01”,
        "ip" : “192.168.0.14”,
        "port" : “5000”,
        "description" : “마스터 서버 1”
    }
    ```

    

- **Worker1**

  - Name : intellivix-worker-01(intellivix)

  - IP : 192.168.0.21

    ```
    # ssh 접속 / admin1234!
    
    ssh intellivix@192.168.0.21
    ```

  - - JSON 형태 정보 예시 : 

      ```json
      {    
          "name" : “EdgeCCTV01”,
          "type" : 1,
          "gps" : 
          {	
            "latitude" : “37.57”,
            "longitude" : “126.98”
          },
          "address" : “서울시 마포구 상암동 1599”,
          "ip" : “192.168.0.9”,
          "isSupportAnnalysis" : “YES”,
          "url" : “rtsp://root:root@192.168.0.12/axis-media/media.amp”,
          "description" : “이 CCTV는 상암동에 설치된 엣지 CCTV 임”
      }
      ```

  

- **Worker2**(내가 사용할것)

  - Name : intellivix-worker-02(intellivix)
  
  - IP : 192.168.0.19
  
    ```
    # ssh 접속 / admin1234!
    
    ssh intellivix@192.168.0.19
    ```
  
    



### [VMS 서버 구성] - [최적화 서버]로 사용중

- Name : edge-master-01

- IP : 192.168.0.14

  ```
  # ssh 접속
  
  ssh edge-master-01@192.168.0.14
  ```

  

- 데이터 확인 서버

  - 기능 : AI에서 전송받는 데이터 출력

  - `vms_edge.py` 

    - 주소 및 포트 : 192.168.0.14:6432

    - API

      - /usage

        - POST

        - Data : 

          - ```json
            # 예시 JSON 데이터
            
            {
                "code": "0000",
                "message": "처리성공",
                "username": username,
                "cpu": cpu_percent,
                "memory": memory_percent,
                "func": "SUNNY"
            }
            ```



### [등록, 설정 서버]

- Name : edge-worker-01

- IP : 192.168.0.9

  ```
  # ssh 접속
  
  ssh edge-worker-01@192.168.0.9
  ```

  

- 등록, 설정 서버
  
  - 기능 : Master 서버에 업로드, 배포, 클러스터링 등 명령,  DB



### [환경 정보 AI]

- KETI_weather_classification
  - 실행방법 : 
    - edgeconfig.xml, CONSTANTS.py 파일 설정 후
    - main.py 실행
  - 동적으로 변경 가능한 파일 : 
    - edgeconfig.xml
    - CONSTANTS.py



### [CCTV 구성]

- #### CCTV 주소

  - rtsp://root:keti@192.168.0.93/onvif-media/media.amp
  - rtsp://root:keti@192.168.0.94/onvif-media/media.amp
  - rtsp://root:keti@192.168.0.96/onvif-media/media.amp
  - rtsp://root:root@192.168.0.12/axis-media/media.amp



## [버전 정보]

### OS

Ubuntu 20.04



### JETPACK

R35 (release), REVISION: 4.1, GCID: 33958178, BOARD: t186ref, EABI: aarch64, DATE: Tue Aug 1 19:57:35 UTC 2023
35.4.1 / 5.1.1

### CUDA

nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Sun_Oct_23_22:16:07_PDT_2022
Cuda compilation tools, release 11.4, V11.4.315
Build cuda_11.4.r11.4/compiler.31964100_0



### Docker

Client: Docker Engine - Community
Version: 27.1.1
API version: 1.46
Go version: go1.21.12
Git commit: 6312585
Built: Tue Jul 23 19:59:27 2024
OS/Arch: linux/arm64
Context: default

Server: Docker Engine - Community
Engine:
Version: 27.1.1
API version: 1.46 (minimum version 1.24)
Go version: go1.21.12
Git commit: cc13f95
Built: Tue Jul 23 19:59:27 2024
OS/Arch: linux/arm64
Experimental: false
containerd:
Version: 1.7.19
GitCommit: 2bf793ef6dc9a18e00cb12efb64355c2c9d5eb41
runc:
Version: 1.7.19
GitCommit: v1.1.13-0-g58aa920
docker-init:
Version: 0.19.0
GitCommit: de40ad0



### Kubernetes

v1.30.3



## SW

- #### 리소스 전송 파일

  - 마스터에 저장되어있는 파일을 사용

  - 위치 : /home/edge-master-01/monitoring.zip

  - VMS 서버로 cpu, 메모리 사용량 메타데이터(Json) POST 전송

    - VMS 서버 주소 및 API : http://192.168.0.14:6432/usage

    - Json 데이터

      ```json
      {
          "code": "0000",
          "message": "처리성공",
          "username": 'edge-master-01-1129',
          "cpu": cpu_percent,
          "memory" : memory_percent
      }
      ```

      

### 데이터 전송방식

---

#### 엣지 CCTV

- 영상
  - **[엣지 CCTV]**에서 RTSP 재전송
  - **[VMS]**에서 끌어감
- 분석결과 및 메타데이터
  - **[VMS]**에서 `Request`
  - **[엣지 CCTV]** 에서 `Response`



### 환경정보 최적화

---

#### Opt.Config

- 최적화를 위한 서버 설정 Config Map

  ```
  # Opt.Config(최적화를 위한 서버 설정 Config Map)
  
  # VMS server
  VMS_URL=192.168.0.14
  VMS_PORT=5350
  ```



#### Json 파일 

```
{
    "nid": "0x01",                  # 노드 ID
    "date": "20240808",			    # 날짜
    "time": "hhmmss",               # 시간
    "result": "4"					# 함수의 결과 값   *해석은 어떻게 하는지 문의필요*
}
```





### Daily report

---

#### 0611

- 7월 16일 5G 종료평가 

  - 서울 IITP 평가장
  - 시연 준비 필요

- 다음주 화요일 4시 회의

  - 작년 2차년도 서버 살리기

  - 연계협업 알고리즘 시나리오 구성 2가지이상 PPT

    - 개발 계획서 마지막 시나리오 보고 새로운 것 구성하기

    - 엣지간, 엣지 - 분석서버간 등등 모두 가능

    - 예시

      \- 엣지 AI 보안단말간 및 엣지 AI 보안단말-VMS 분석서버간 연계협업 시나리오를 4종 이상 정의하고, 시나리오에 따라 정상 동작 여부 평가

        · 예시 1: 특정 엣지 AI 보안단말의 리소스에 과부하가 발생하는 경우, 리소스에 여유가 있는 다른 엣지 AI 보안단말과의 협업형 영상분석 수행 가능

        · 예시 2: 특정 엣지 AI 보안단말의 리소스에 과부하가 발생하고 다른 엣지 AI 보안단말에 여유가 없는 경우, 엣지 AI 보안단말-VMS 분석서버간 협업형 영상분석 수행 가능

        · 예시 3: 특정 엣지 AI 보안단말에서 이벤트 발생시, 엣지 AI 보안단말-VMS 분석서버간 협업을 통해 정밀 분석 수행 가능

        · 예시 4: 특정 엣지 AI 보안단말에서 이벤트 발생시, 엣지 AI 보안단말간 연계협업을 통해 이벤트 발생지에 대한 집중 감시 가능



#### 0612

- 서버 살리고 연동 테스트
  - Master : 
    - IP : 192.168.0.14
    - 이름 : edge-master-01
  - Worker : 
    - IP : 192.168.0.9
    - 이름 : edge-worker-01
  - AI 소프트웨어 : 
    - 이름 : monitoring.zip
- 완료



#### 0613

- 서버 보완점 체크하고 보완하기
  - **보완**
    - 업로드 기능
      - 현재는 VMS = Master 서버로 Linux로 구성되어있는데 파일이 Zip 형태로 서버에 존재
      - Master 서버의 위치가 어떻게 되는지?
        - 다수의 클러스터가 있으려면 Master는 다수 있어야함
    - 내부망(이더넷) 환경에서 클러스터 구성 및 AI 배포가 가능한지?
      - Docker Hub 사용여부를 확실히 해야함
  - **추가**
    - 배포기능 추가
- 연계협업 파트 제안서 만들기



#### 0618

- 연계협업 파트 제안서 만들기

  - 연계협업 알고리즘 시나리오 구성 2가지이상 PPT

    - 개발 계획서 마지막 시나리오 보고 새로운 것 구성하기

    - 엣지간, 엣지 - 분석서버간 등등 모두 가능

    - 예시

      \- 엣지 AI 보안단말간 및 엣지 AI 보안단말-VMS 분석서버간 연계협업 시나리오를 4종 이상 정의하고, 시나리오에 따라 정상 동작 여부 평가

        · 예시 1: 특정 엣지 AI 보안단말의 리소스에 과부하가 발생하는 경우, 리소스에 여유가 있는 다른 엣지 AI 보안단말과의 협업형 영상분석 수행 가능

        · 예시 2: 특정 엣지 AI 보안단말의 리소스에 과부하가 발생하고 다른 엣지 AI 보안단말에 여유가 없는 경우, 엣지 AI 보안단말-VMS 분석서버간 협업형 영상분석 수행 가능

        · 예시 3: 특정 엣지 AI 보안단말에서 이벤트 발생시, 엣지 AI 보안단말-VMS 분석서버간 협업을 통해 정밀 분석 수행 가능

        · 예시 4: 특정 엣지 AI 보안단말에서 이벤트 발생시, 엣지 AI 보안단말간 연계협업을 통해 이벤트 발생지에 대한 집중 감시 가능

- 내부망으로 클러스터 구성 시 자체 Docker Registry 설정

  - 네, 내부 유선망에서 Kubernetes 클러스터를 구성하고 Docker 이미지를 배포할 때 외부 인터넷에 의존하지 않고도 가능합니다. 이를 위해 자체 Docker Registry를 설정할 수 있습니다. 자체 Docker Registry를 설정하면 Docker Hub 대신 내부 네트워크에서 이미지를 저장하고 배포할 수 있습니다.

    다음은 자체 Docker Registry를 설정하고 사용하는 방법입니다.

    ### 1. Docker Registry 설치 및 구성

    #### 1.1 Docker Registry 컨테이너 실행

    먼저, 자체 Docker Registry를 Docker 컨테이너로 실행할 수 있습니다.

    ```
    bash
    코드 복사
    docker run -d -p 5000:5000 --name registry --restart=always registry:2
    ```

    이 명령은 기본 포트 5000에서 Docker Registry를 실행합니다.

    #### 1.2 Docker Registry 보안 설정 (선택 사항)

    보안 설정을 위해 SSL을 사용할 수 있습니다. 먼저, 인증서와 키 파일을 준비합니다.

    ```
    bash코드 복사mkdir -p /certs
    cp your_cert.crt /certs
    cp your_key.key /certs
    ```

    그런 다음, Docker Registry를 다음과 같이 실행합니다.

    ```
    bash코드 복사docker run -d -p 5000:5000 --name registry --restart=always \
      -v /certs:/certs \
      -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/your_cert.crt \
      -e REGISTRY_HTTP_TLS_KEY=/certs/your_key.key \
      registry:2
    ```

    ### 2. Docker Daemon 설정

    내부 Docker Registry를 신뢰할 수 있는 레지스트리로 설정합니다. 각 클러스터 노드에서 `/etc/docker/daemon.json` 파일을 편집합니다.

    ```
    json코드 복사{
      "insecure-registries": ["your_registry_domain_or_ip:5000"]
    }
    ```

    Docker를 재시작합니다.

    ```
    bash
    코드 복사
    sudo systemctl restart docker
    ```

    ### 3. Docker 이미지를 자체 Registry에 푸시

    이미지를 자체 Registry에 푸시합니다.

    ```
    bash코드 복사docker tag your_image:tag your_registry_domain_or_ip:5000/your_image:tag
    docker push your_registry_domain_or_ip:5000/your_image:tag
    ```

    ### 4. Kubernetes에서 이미지 사용

    Kubernetes 배포 파일에서 자체 Registry에서 이미지를 가져오도록 설정합니다.

    ```
    yaml코드 복사apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: myapp
      template:
        metadata:
          labels:
            app: myapp
        spec:
          containers:
          - name: myapp
            image: your_registry_domain_or_ip:5000/your_image:tag
            ports:
            - containerPort: 80
    ```

    ### 5. Registry에 접근하기 위한 Secret 설정 (선택 사항)

    프라이빗 레지스트리의 경우, Kubernetes 클러스터가 이미지를 가져올 수 있도록 secret을 생성해야 합니다.

    ```
    bash
    코드 복사
    kubectl create secret docker-registry regcred --docker-server=your_registry_domain_or_ip:5000 --docker-username=your_username --docker-password=your_password --docker-email=your_email
    ```

    배포 파일에 secret을 참조합니다.

    ```
    yaml코드 복사apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: myapp
      template:
        metadata:
          labels:
            app: myapp
        spec:
          containers:
          - name: myapp
            image: your_registry_domain_or_ip:5000/your_image:tag
            ports:
            - containerPort: 80
          imagePullSecrets:
          - name: regcred
    ```

    이렇게 설정하면 내부 네트워크에서 Docker Hub를 사용하지 않고도 Docker 이미지를 배포할 수 있습니다.



#### 0619

- 도커 내용 정리
- 4시 회의
  - 영상 및 시연 보여드리기
- 연계협업 시나리오
  - 다음주 수요일 2차 회의
  - 추가 시나리오 구상
    - 분석 AI를 나누어서
      - 엣지 : 이미지검출 -> 분석서버 or 엣지2 : 분석 
      - 등등
    - 분석 AI가 작동을 안하면 복구해주는?
    - 다른 엣지의 리소스를 제공하주는?



#### 0620

- 연계협업 시나리오
  - 다음주 수요일 2차 회의
  - 추가 시나리오 구상
    - 분석 AI를 나누어서
      - 엣지 : 이미지검출 -> 분석서버 or 엣지2 : 분석 
      - 등등
    - 분석 AI가 작동을 안하면 복구해주는?
    - 다른 엣지의 리소스를 제공하주는?



- 프로메테우스 수집 메트릭
  - **노드 메트릭**:
    - `node_cpu_seconds_total`: CPU 사용량
    - `node_memory_MemTotal_bytes`: 총 메모리 용량
    - `node_memory_MemAvailable_bytes`: 사용 가능한 메모리
    - `node_disk_io_time_seconds_total`: 디스크 I/O 시간
    - `node_network_receive_bytes_total`: 네트워크 수신 바이트
    - `node_network_transmit_bytes_total`: 네트워크 전송 바이트
  - **파드(Pod) 메트릭**:
    - `container_cpu_usage_seconds_total`: 컨테이너의 CPU 사용량
    - `container_memory_usage_bytes`: 컨테이너의 메모리 사용량
    - `container_fs_usage_bytes`: 컨테이너의 파일 시스템 사용량
  - **클러스터 메트릭**:
    - `kube_node_status_allocatable_cpu_cores`: 노드에서 할당 가능한 CPU 코어
    - `kube_node_status_allocatable_memory_bytes`: 노드에서 할당 가능한 메모리
    - `kube_pod_status_phase`: 파드 상태 (Running, Pending, Failed 등)



#### 0624

- 연계협업 시나리오
  - 다음주 수요일 2차 회의
  - 추가 시나리오 구상
    - 분석 AI를 나누어서
      - 엣지 : 이미지검출 -> 분석서버 or 엣지2 : 분석 
      - 등등
    - 분석 AI가 작동을 안하면 복구해주는?
    - 다른 엣지의 리소스를 제공하주는?



#### 0625

- 연구협약 입력
- 시나리오 조사



#### 0626

- 시나리오 회의
  - 추가 시나리오 2개 더 구성해서 진행
- 일단 세개로 진행
  1. 분석결과 50% -> 분석서버에서 정밀분석
  2. 단말 리소스 과부하 시 (미동작, 오동작) -> 분석서버에서 분석
  3. 설치 오류 등 AI 미동작 -> 연계협업서버에서 복구 = 재배포
- **시나리오 위한 단말, 연계협업서버 등 의 기능 정리하기 -> 화요일까지**





#### 0702(화)

- 3차 시나리오 회의

  - 시나리오 용어정리 및 기능 추가해서 PPT




#### 0717

- 시나리오 내일 회의 준비



#### 0718

- 시나리오 회의
  - 연계협업 시나리오
    1. 분석결과 50% -> 분석서버에서 정밀분석
    2. 단말 리소스 과부하 시 (미동작, 오동작) -> 분석서버에서 분석
    3. 설치 오류 등 AI 미동작 -> 연계협업서버에서 복구 = 재배포
- 밈마켓



#### 0723

- 시나리오 회의 준비 - 틈틈히 진행
  - 연계협업 시나리오
    1. 분석결과 50% -> 분석서버에서 정밀분석
    2. 단말 리소스 과부하 시 (미동작, 오동작) -> 분석서버에서 분석
    3. 설치 오류 등 AI 미동작 -> 연계협업서버에서 복구 = 재배포
  - **시나리오 위한 단말, 연계협업서버 등 의 기능 정리**
    - 서버의 종류
    - 데이터 전송 방식
    - UI 구상
- **무선엣지 3차년도 킥오프**
  - 8/2(금) 인텔리빅스 SW 회의
    - KETI, ETRI, 인텔리빅스
    - SW 파트
      1. 엣지 AI
         - KETI : 환경정보
         - ETRI : 화재
         - 인텔리빅스
      2. 지속적 최적화
      3. 연계협업 
         - 8/1일까지 수석님 시나리오 구성 예정
  - 8월 중순 전체 업체 킥오프 회의
  - **현재 진행해야할 것**
    - 오린 PC 2대 환경 설정
    - 간단한 프로그램 배포, 동작 확인
    - 프로그램 신규 업데이트 가능한지 확인



#### 0724

- 오린 PC 2대 환경 설정
  - keti
    - IP : 192.168.0.32
  - keti-jx-02
    - IP : 192.168.0.13
- 포트포워딩 완료
- docker, k8s 설치
  - k8s 설치가 안됨 - 에러 해석하고 ㄱㄱ

 

#### 0725

- k8s 설치
  - k8s 설치가 안됨 - 에러 해석하고 해결완료
  - k8s 버전 1.29-1.1 로 변경



#### 0801

- monitoring 시스템 배포 완료

- 수정 변경 가능한지 확인

- jetson orin 01 (마스터)가 작동을 안함

  - 기존 서버에서 실행

    - 도커 이미지 빌드

      - ```
        # Sunny
        docker build -f DockerfileS -t sehooh5/monitors:01 .
        
        # Rainy
        docker build -f DockerfileR -t sehooh5/monitorr:01 .
        
        # Docker images 확인
        docker run -it sehooh5/monitorr:02 /bin/bash
        ```

    - K8S 배포 / 삭제

      - ```
        # Sunny
        kubectl apply -f monitoringS/monitors.yaml
        kubectl delete -f monitoringS/monitors.yaml
        
        # Rainy
        kubectl apply -f monitoringR/monitorr.yaml
        kubectl delete -f monitoringR/monitorr.yaml
        ```

    - 업데이트

      - ```
        # Rainy
        
        ## Docker image 삭제
        docker rmi sehooh5/monitorr:01
        
        ## 새로운 Docker image build
        docker build -f DockerfileR02 -t sehooh5/monitorr:02 .
        docker push sehooh5/monitorr:02
        
        ## 새로운 Pod 배포
        kubectl apply -f monitoringR02/monitorr.yaml
        ```

- Sunny / Rainy 배포/삭제 기능 구현 완료



#### 0802

- 인텔리빅스 회의(방배 사옥, 16시)

  - 데이터 전송 방법 
  - 배포형태, 분석결과 등 표준

  

#### 0805

- 클러스터 환경 구성 완료
- 공부해서 적용하기
  - 제로티어
  - Docker private registry
    - https://d0lim.com/blog/2023/05/mac-mini-docker-registry/



#### 0806

- 도커 hub(외부망)을 사용하지 않고 내부망에서 해결하기 위한 방법
  - Docker private registry
    - 참고1 : https://d0lim.com/blog/2023/05/mac-mini-docker-registry/
- VMS 서버용으로 쓸 Mini PC
  - Name : edge-master-01
  - IP 주소 : 192.168.0.14
  - PW : keti



#### 0807

- **서박사님 문의(8일 목요일)**
  - 환경정보 AI GUI 버전에서 메타데이터(아마 JSON) 버전으로 변경이 가능한지?
    1. VMS에서 PULL 하는 방식
    2. VMS로 매 초마다 전송하는 방식
- **진행해야할 것(8/20 화요일까지)**
  - 도커 private registry 설정
    - 제일 먼저 진행하고 배포되는지 확인 필요
  - [모니터링]
    - VMS = edge-master-01 으로 가정하고 데이터 전송받는 서버 실행
    - 데이터 전송받는 서버 `vms_edge.py` 로 재구성하기
    -  SW 배포 및 확인
  - [환경정보 AI]
    - 메타데이터 버전으로 변경
    - 패키징 및 배포



#### 0808

- k8s  구성자체가 망가짐

  - 아래 과정에서 망가진거같은데 확인 후 진행

    ```
    sudo mkdir -p /etc/systemd/system/kubelet.service.d
    sudo vim /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
    ```

  - 해결 완료 : 

    - k8s 재구성

- join 문

  ```
  # master 실행문
  sudo kubeadm init --node-name opt-master --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=192.168.0.15
  
  # 192.168.0.21
  sudo kubeadm join 192.168.0.4:6443 --node-name intellivix-worker-01 --token 4is1yr.jiwj6x16ba0fwwbr --discovery-token-ca-cert-hash sha256:ee35f3a2b1bfcc6d657266488e6b15791e2f0d2ff177fa6ce3627315f15565cb
  
  # 192.168.0.19
  sudo kubeadm join 192.168.0.4:6443 --node-name intellivix-worker-02 --token 4is1yr.jiwj6x16ba0fwwbr --discovery-token-ca-cert-hash sha256:ee35f3a2b1bfcc6d657266488e6b15791e2f0d2ff177fa6ce3627315f15565cb
  
                                                                                    mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
                                                                                    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml 
                                                                                   
  ```

- **서박사님 문의**

  - 환경정보 AI GUI 버전에서 메타데이터(아마 JSON) 버전으로 변경이 가능한지?
    1. VMS에서 PULL 하는 방식
    2. VMS로 매 초마다 전송하는 방식
  - **전송방식 작성 후 공유**
    - 기존
      - config map 작성
        - vms IP, port 등등
      - JSON 파일 예제
      - 데이터 전송방식
    - 작성중
      - Config Map 완료(간단)
      - JSON파일 예제
        - 환경정보 획득 인터페이스.hwp
      - 데이터 전송방식
        - 위 파일에 GET, POST 나누었는데 POST 가 적합해보이긴함

- **진행중(8/20 화요일까지)**

  - 도커 private registry 설정
    - 제일 먼저 진행하고 배포되는지 확인 필요
  - [모니터링]
    - VMS = edge-master-01 으로 가정하고 데이터 전송받는 서버 실행
    - 데이터 전송받는 서버 `vms_edge.py` 로 재구성하기
    -  SW 배포 및 확인
  - [환경정보 AI]
    - 메타데이터 버전으로 변경
    - 패키징 및 배포



#### 0809

- **진행중(8/20 화요일까지)**
  - 도커 private registry 설정
    - 제일 먼저 진행하고 배포되는지 확인 필요
  - [모니터링]
    - VMS = edge-master-01 으로 가정하고 데이터 전송받는 서버 실행
    - 데이터 전송받는 서버 `vms_edge.py` 로 재구성하기
    -  SW 배포 및 확인
  - [환경정보 AI]
    - 메타데이터 버전으로 변경
    - 패키징 및 배포
- 서박사님 의논
  - **JSON파일 예제**
    - **환경정보 획득 인터페이스.hwp**
  - **데이터 전송방식**
    - 위 파일에 GET, POST 나누었는데 **POST 가 적합해보이긴함**



#### 0813

- 서박사님 전달 완료
  - post 방식으로 진행
- private repository 계속 진행



#### 0814

- monitors.yaml 의 containerPort 변경해서 다시해보기
- <mark>**containerd config.toml 파일 생성후 변경해줬더니 해결**</mark>
- imagepullbackoff 오류가 발생하는데 dockerfile, deployment 파일 확인 후 다시 진행해보기
  - post 요청 받는 서버 생성되니 잘 돌아감!! 배포완료!!



#### 0816

- **진행해야할 것(8/20 화요일까지)**
  - [환경정보 AI]
    - 메타데이터 버전으로 변경
      - 서박사님 ai 변경되면 시작
    - 패키징 및 배포
- **진행 완료**
  - [Private registry 설정]
    - 제일 먼저 진행하고 배포되는지 확인 완료
  - [모니터링]
    - VMS = edge-master-01 으로 가정하고 데이터 전송받는 서버 실행
    - 데이터 전송받는 서버 `vms_edge.py` 로 재구성하기
    - SW 배포 및 확인
      - **배포** : sunny배포 
      - **SW 변경** : sunny to rainy
      - **업데이트** : rainy2 업데이트 배포 확인



#### 0819

- **진행해야할 것(8/20 화요일까지)**

  - SW 데이터 전송 시스템

    - `vms_edge.py`

      - ~~/res_edge_data(POST 추가)~~
        - ~~기존 POST 방식에서 변경(요청 후 응답)~~
      - **/save_edgeData**
        - 매초 전달되는 json 데이터를 저장하는 API
        - DB에 저장해서 사용하기위해 DB 종류 선택하고 연결하기

    - ~~`monitoring.py`~~

      - ~~현재 모니터링 데이터 response하는 API 추가~~
      - ~~nodeport 열어줘야함~~

    - `edgeconfig.xml`

      - ```
        <Configuration>
            <vms>
                <IP>192.168.0.14</IP>
                <Port>6432</Port>
                <Path>usage</Path>
            </vms>
        </Configuration>
        ```

  - [환경정보 AI]

    - 메타데이터 버전으로 변경
      - 서박사님 ai 변경되면 시작
    - 패키징 및 배포
      - 

- **진행 완료**

  - [Private registry 설정]
    - 제일 먼저 진행하고 배포되는지 확인 완료
  - [모니터링]
    - VMS = edge-master-01
    - 데이터 전송받는 서버 `vms_edge.py` 로 재구성하기
    - SW 배포 및 확인
      - 배포 : sunny배포 
      - SW 변경 : sunny to rainy
      - 업데이트 : rainy2 업데이트 배포 확인



#### 0820

- 서박사님께 변경사항 말씀드리고 DB 시작하기
- 정기 회의
  - **최적화 시나리오 구성하기**
    - 업체들 AI에는 환경정보를 return  해주는게 없음, 따라서 DB에 저장하는 형태로?
  - **최적화 시나리오에 따른 DB 구축하기**
    - table 작성 등 기초부터 
  - **[클러스터링, 프라이빗 레포지터리 생성] 기능 자동화가 필요한데 생각해보고 구성하기**



#### 0821

- MongoDB 연동 시작
- 서박사님께 변경사항 말씀드리고 
  - 변경사항 한글파일 작석 및 전달 완료
    - 파일명 : (무선엣지)환경정보 저장 인터페이스.hwp
      - 분석결과 전송에 필요한 VMS 정보설정 파일(edgeconfig.xml)에 대한 정보와 VMS에서 실행되는 환경정보 분석결과 저장 API에 대한 인터페이스가 설명되어 있습니다.
    - 파일명 : edgeconfig.xml
      - 분석결과 전송에 필요한 정보설정 파일입니다. 해당 파일은 AI가 배포될 때 함께 배포되며 VMS의 정보가 변경될 때 함께 변경될 수 있습니다. 

- 정기 회의
  - **최적화 시나리오 구성하기**
    - 업체들 AI에는 환경정보를 return  해주는게 없음, 따라서 DB에 저장하는 형태로?
  - **최적화 시나리오에 따른 DB 구축하기**
    - table 작성 등 기초부터 
  - **[클러스터링, 프라이빗 레포지터리 생성] 기능 자동화가 필요한데 생각해보고 구성하기**



#### 0823

- **최적화 시나리오에 따른 DB 구축하기**

  - table 작성 등 기초부터 

  - `sqldbm` 사용

    ```
    -- Warning: You can generate script only for one table/view at a time in your Free plan 
    -- 
    -- **************************** SqlDBM: MySQL ***************************
    -- **** Generated by SqlDBM: Optimize server DB by sehooh5@gmail.com ****
    
    
    
    -- ************************************** `edges`
    
    CREATE TABLE `edges`
    (
     `edge_id`       varchar(45) NOT NULL ,
     `cluster_id`    varchar(45) NOT NULL ,
     `edge_name`     varchar(45) NOT NULL ,
     `edge_ip`       varchar(45) NOT NULL ,
     `edge_cctv_url` varchar(45) NOT NULL ,
     `ai_in_01`      int NOT NULL ,
     `ai_in_02`      int NOT NULL ,
     `ai_in_03`      int NOT NULL ,
     `ai_in_04`      int NOT NULL ,
     `ai_in_05`      int NOT NULL ,
     `ai_in_06`      int NOT NULL ,
     `ai_et_01`      int NOT NULL ,
     `ai_et_02`      int NOT NULL ,
    
    PRIMARY KEY (`edge_id`),
    KEY `FK_1` (`cluster_id`),
    CONSTRAINT `FK_2` FOREIGN KEY `FK_1` (`cluster_id`) REFERENCES `clusters` (`cluster_id`)
    );
    ```

    

- **최적화 시나리오 구성하기**

  - A4에 작성한 내용을 PPT로 자세히 작성

- **[프라이빗 레포지터리 생성] 기능 자동화가 필요한데 생각해보고 구성하기**

  - 각 노드에서 설정해줘야 하는것들

    - sudo vim /etc/docker/daemon.json 변경

      ```
      # 모든 노드에서 Docker 데몬에 특정 레지스트리에 대해 HTTP를 허용하도록 구성
      sudo vim /etc/docker/daemon.json
      
      # 아래내용 추가
      {
        "insecure-registries" : ["192.168.0.4:5000"]
      }
      
      ## 기존
      {                                                                                                                                                                "runtimes": {                                                                                                                                                    "nvidia": {                                                                                                                                                      "path": "nvidia-container-runtime",                                                                                                                          "runtimeArgs": []                                                                                                                                        }                                                                                                                                                        },                                                                                                                                                           "insecure-registries": ["192.168.0.4:5000"]                                                                                                              }     
      
      # 도커 재시작
      sudo systemctl restart docker
      ```

      

    - config 설정

      ```
      # 위치 이동
      cd /etc/containerd/
      
      # defaul 파일 있으면
      mv config.toml config_bkup.toml
       
      # "없으면" config 파일 default 내용 포함해서 생성
      sudo su
      containerd config default > config.toml
      exit
      
      ...
      
      [plugins."io.containerd.grpc.v1.cri".registry.configs] # 아래 내용 추가!
              [plugins."io.containerd.grpc.v1.cri".registry.configs."192.168.0.4:5000".auth]
                username = "sehooh5"
                password = "@Dhtpgh1234"
              [plugins."io.containerd.grpc.v1.cri".registry.configs."192.168.0.4:5000".tls]
                insecure_skip_verify = true
      
      [plugins."io.containerd.grpc.v1.cri".registry.headers] # 추가 X
      
      [plugins."io.containerd.grpc.v1.cri".registry.mirrors] # 아래 내용 추가!
              [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
                endpoint = ["https://registry-1.docker.io"]
              [plugins."io.containerd.grpc.v1.cri".registry.mirrors."192.168.0.4:5000"]
                endpoint = ["http://192.168.0.4:5000"]
          
      ...
      ```

    - 변경 예시 먼저 테스트 해볼 것!

      ```python
      import paramiko
      
      # SSH 연결 정보
      hostname = '192.168.0.1'  # 원격 서버 IP 주소
      port = 22                 # SSH 포트
      username = 'your_username'  # 원격 서버 사용자 이름
      password = 'your_password'  # 사용자 비밀번호
      
      # 추가할 내용
      config_to_add = '''
      [plugins."io.containerd.grpc.v1.cri".registry.configs."192.168.0.4:5000".auth]
        username = "sehooh5"
        password = "@Dhtpgh1234"
      [plugins."io.containerd.grpc.v1.cri".registry.configs."192.168.0.4:5000".tls]
        insecure_skip_verify = true
      '''
      
      try:
          # SSH 클라이언트 초기화 및 서버에 연결
          client = paramiko.SSHClient()
          client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
          client.connect(hostname, port=port, username=username, password=password)
          
          # sftp 클라이언트를 통해 파일 가져오기
          sftp_client = client.open_sftp()
          remote_file_path = '/etc/containerd/config.toml'
          local_file_path = '/tmp/config.toml'
          
          # 원격 파일을 로컬로 다운로드
          sftp_client.get(remote_file_path, local_file_path)
          
          # 로컬 파일 수정
          with open(local_file_path, 'r+') as file:
              content = file.read()
              
              # 특정 위치에 추가할 내용 삽입
              insert_position = content.find('[plugins."io.containerd.grpc.v1.cri".registry]') + len('[plugins."io.containerd.grpc.v1.cri".registry]')
              updated_content = content[:insert_position] + config_to_add + content[insert_position:]
              
              # 파일 덮어쓰기
              file.seek(0)
              file.write(updated_content)
              file.truncate()
          
          # 수정된 파일을 다시 원격 서버에 업로드
          sftp_client.put(local_file_path, remote_file_path)
          
          print("파일이 성공적으로 업데이트되었습니다.")
          
      except Exception as e:
          print(f"오류 발생: {e}")
          
      finally:
          # SFTP 및 SSH 연결 종료
          sftp_client.close()
          client.close()
      ```

      

#### 0828

- 워크샵
- 무선엣지 시나리오 작성 ppt



#### 0830

- 무선엣지 시나리오 작성 ppt 이어서
- 쇼빌리티 
  - 코드리뷰
  - AWS 책 공부시작
    - ~~키페어 전달받기~~ 새로 받아서 하면 됨
- kubeflow
  - 쿠버플로우의 개념 및 장점 (간단히)
    - 쿠버플로우를 이용해서, AI 학습과 AI를 배포하기 위한 제한이나 방법
      
        2. 제한사항은 없고 설정, 관리만 잘해주면 문제 없음
    - KETI에서 해당 기술을 적용할 수 있는지의 가능성..
        3. AI 학습은 KETI에서 진행하는 것이 아니기에 해당사항은 아님
        - 배포는 인텔리빅스와 동일한 조건의 엣지에서 Kubernetes 기반 Kubeflow에서 진행하는 것이므로 가능할 것으로 보임
            3. 다만, kubernetes, kubeflow의 버전, 환경설정 등 인텔리빅스와 환경정보 통합과정 필요



#### 0902

- 무선엣지 시나리오 작성 ppt 이어서



#### 0903

- 시나리오 추가
- 쇼빌리티
  - React-native --- Django 프로젝트간 연동[참고 페이지](https://oliopasta.tistory.com/11)
    - Django 프로젝트 실행중
  - Expo.dev 활용해 백엔드 개발자 서버 구축



#### 0904

- 시나리오 회의
- 쇼빌리티
  - React-native --- Django 프로젝트간 연동[참고 페이지](https://oliopasta.tistory.com/11)
    - Django 프로젝트 실행중
    - 회원가입 전화번호 식별자 확인
  - Expo.dev 연동될 서버구축하면 됨
  - django-flask 연동앱 참고
    - https://django-ninja.dev/



#### 0905

- **최적화 진행**
  - AI
    - 기존 모니터링 SW 
      - 2가지 방법(Sunny, Rainy) 이벤트 발생 필요
        - 발생 방법은 고민해봐야함
    - Edge AI
      - 인텔리빅스 대체제로 사용할 AI 배포 및 실행 필요
      - 환경정보에 의해 2가지로 나눠서 업로드까지 실행
  - 등록,설정 서버
    - Edge AI 등록부터 재작동 시켜야함
    - Edge AI 환경정보 요청/응답 추가
    - 환경정보 비교 결과에 따른 DB 업데이트
    - DB
      - AI 환경정보 저장 필요
  - 최적화 서버
    - 모니터링 SW의 버전 정보와 등록, 설정서버 DB의 AI 환경정보 비교
      - 등록, 설정서버에 환경정보 요청
      - 응답값으로 환경정보 비교
      - DB 업데이트 명령
      - Master 서버에 기종 EdgeAI 삭제 및 맞는 환경정보 EdgeAI 재배포 명령
  - Master 서버
    - 배포 잘 되는지 확인
    - 2종의 Edge AI 업로드
    - 배포, 삭제, 재배포 실행
- 인텔리빅스 전달사항 정리
  - AI 버전
  - 패키징 위한 spec
- **서박사님 오시면 다시 환경정보 `(무선엣지)환경정보 저장 인터페이스`한글파일 전달(nid 추가)**



- **완료 상태**
  - Edge AI(Test)
    - monitoring sunny
      - SUNNY 전송
    - monitoring rainy
      - RAINY전송
  - 최적화서버
    - 엣지CCTV 로부터 데이터 받아 출력
  - Master 서버
    - 현재 테스트에서는 `intellivix-worker-01` 서버에만 배포
    - 배포 AI
      - 환경정보 테스트 AI
      - AI 1
      - AI 2
  - 등록, 설정 서버



- **명령어**

  - 도커

    ```
    # 도커 빌드 with private repository
    docker build -f DockerfileR01 -t 192.168.0.4:5000/monitoringr:01 .
    
    # private repository에 push
    docker push 192.168.0.4:5000/monitoringr:01
    ```

  - k8s

    ```
    # 배포
    kubectl apply -f monitorr.yaml 
    ```





#### 0906

- master_server.py

  - deploy_aiToDevice 중간 주석부터 하면됨

- 배포 파일 필수 조건

  - Dockerfile

    - 

  - YAML 파일

    - ```
      {fname}-{ai_class}.yaml 양식으로 변경 필요
      
      # 내부 docker image 명 또한 변경해줘야함
      {private_repo}/{fname}-{ai_class}:{version}
      ```

- 업로드 기능부터 진행중



#### 0909

- 업로드 : setup-master 서버 연동
  - filename 으로 패키지 폴더가 있어야함
  - 삭제까지 성공!
- 배포 : 완료
  - monitorings로만 완료



#### 0910

- 완료 : 
  - 환경정보 AI 대체할만한 SW 만들고
    - weatherai.py 작성
      - 30초마다 class 01/02를 번갈아가며 실행
  - 배포



#### 0911

- 진행중 : 
  - optimize_server : 배포 후 환경정보 변경에 따른 재배포 실행
    - 기본 api 완료
    - 비교하는 부분 시작해야함
      - aid list를 setup_server로부터 받아오는것까지 완료



#### 0912

- 오산 출장



#### 0913

- 무선엣지
  - 서박사님 요청 기존으로 돌리고 어떤 엣지인지 알수있는 방법 찾아보기
    - ~~배포할때 nid를 사용하는데 그때 Dockerfile을 수정해볼까?~~
    - 배포할때 nid를 사용하는데
  - aid_list 받아온거로 환경정보와 비교해서 재배포 실행하는부분 구현
    - filename 을 통일시켜야할듯
      - 기존 s,r 붙이는데 그냥 monitoring 으로 통일, class로 구분
      - 방법 : uploaded_ai 중 해당 파일명 갖고있는 AI 에서 받은 class와 일치하는 uploaded AI 배포



#### 0920

- 30초마다 최적화(완료)

- optimize_server_bp

  - 완료
  - url_prefix 를 `/user` 등으로 사용하고 bp에서는 `/`만 사용하는 식으로 수정
  
  



#### 0923

- 서박사님 파일 받음
  - 배포 진행해야함
    - 도커 컨테이너부터 생성하고 잘 돌아가는지 확인 필요
- 시나리오 1개 추가
  - **AI 버전정보에 따른 최적화**
    - 새로운 버전의 AI 가 업로드되면 자동으로 인식해서 최적화해주는 시나리오



#### 0924

- Cloud Native Korea community Day 2024 참여
  - kubeflow, MLops 적용



#### 0925

- 회의 자료 만들기
  - 이제까지 완성된 것
- 현재 pod 은 다 삭제
  - weather ai 배포하기



#### 0926

- 클러스터 세팅 다시해야함
  - Master : orint -> MiniPC
  - Edge : 기존 인텔리빅스 사용 1
  - 최적화 : 그대로 사용
  - 셋업서버 : 그대로 사용
- **Flask -> FastAPI 로 변경해보자**
  - 비동기처리, 속도 강점
  - 많은 요청 처리에 좋음
- 시나리오 1개 추가
  - **AI 버전정보에 따른 최적화**
    - 새로운 버전의 AI 가 업로드되면 자동으로 인식해서 최적화해주는 시나리오



#### 0927

- 클러스터 구성하기
  - 마스터 설치가 잘 안됨
  - 마스터 한번밀고 설치완료!
- **Flask -> FastAPI 로 변경해보자**
  - 비동기처리, 속도 강점
  - 많은 요청 처리에 좋음



#### 0930 

- **수요일부터 시작**
- 시나리오 1개 추가
  - **AI 버전정보에 따른 최적화**
    - 새로운 버전의 AI 가 업로드되면 자동으로 인식해서 최적화해주는 시나리오
- 서박사님 AI 컨테이너화
- **Flask -> FastAPI 로 변경해보자(다 되면)**
  - 비동기처리, 속도 강점
  - 많은 요청 처리에 좋음



#### 1002

- 작업 순서
  - AI 버전정보에 따른 최적화
  - 서박사님 AI 컨테이너화
  - Flask -> FastAPI 로 변경



#### 1008

- 작업 순서
  - AI 버전정보에 따른 최적화
    - 코딩 완료
    - 테스트 필요
  - 서박사님 AI 컨테이너화
  - (Flask -> FastAPI 로 변경)



#### 1010

- 작업 순서
  - AI 버전정보에 따른 최적화
    - 테스트 시작
    - 이후로 미루기 다시 스케쥴
  - 서박사님 AI 컨테이너화
  - (Flask -> FastAPI 로 변경)
  
- ```
  sudo kubeadm join 192.168.0.15:6443 --token kwz44s.676qdknwjdguw7hr \
          --discovery-token-ca-cert-hash sha256:2e84c9ba5d580a8baa0d588c2d3e548c4271352e93c4a7e4bc5d3a4d943ff8d1
  ```

  

- 쇼빌 기본틀 버셀에 배포







#### 1011

- 작업순서
  1. 클러스터 환경 설정
     - 일단 클러스터해서 배포하는거 자체가 안됨 왜그러는지....다시 다 뒤엎고 하는게 나을듯
  2. 환경정보 AI 패키징, 배포
  3. AI 모듈 배포
  4. 디스플레이에 환경정보에 따른 최적화 표출













- **API 정보**

  - 마스터 서버

    - /upload_edgeAI 

      - POST

        ```
        <요청>
        filename
        version
        ai_class
        
        <응답>
        기본
        ```

    - /remove_edgeAI 

      - POST

        ```
        <요청>
        id : EdgeAI 의 id값
        
        <응답>
        기본
        ```

    - /deploy_aiToDevice 

      - POST

        ```
        <요청>
        aid - ai ID
        
        (aid 로 등록, 서버에 요청해서 받는 값)
        filename
        version
        ai_class
        
        <응답>
        기본
        ```

    - /undeploy_aiFromDevice

      - POST

        ```
        <요청>
        aid - ai ID
        
        (aid 로 등록, 서버에 요청해서 받는 값)
        filename
        version
        ai_class
        
        
        <응답>
        기본
        ```

      

  - 등록, 설정 서버

    - /request_upload_edgeAi

      ```
      <요청>
      filename
      version
      ai_class
      
      # 환경정보
      {
          "filename": "weatherai",
          "version": "01",
          "ai_class": "00"
      }
      
      # monitorings
      {
          "filename": "monitorings",
          "version": "01",
          "ai_class": "01"
      }
      
      # monitoringr
      {
          "filename": "monitoringr",
          "version": "01",
          "ai_class": "02"
      }
      ```

    - /request_remove_edgeAi

      ```
      <요청>
      aid - ai ID
      
      (aid 로 등록, 서버에 요청해서 받는 값)
      
      filename
      version
      ai_class
      ```

    - /request_deploy_aiToDevice 

      ```
      <요청>
      aid - ai ID
      
      (aid 로 등록, 서버에 요청해서 받는 값)
      filename
      version
      ai_class
      ```

    - /request_undeploy_aiFromDevice

      ```
      <요청>
      aid - ai ID
      
      (aid 로 등록, 서버에 요청해서 받는 값)
      filename
      version
      ai_class
      ```

    - get_uploadedAiInfo

      - GET

        ```
        <요청>
        id : 업로드된 EdgeAI 의 id값
        
        <응답>
        filename
        version
        ```

        

