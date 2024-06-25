# README

- 3차년도 무선 엣지 영상보안시스템 기술 개발
- 무선 엣지 CCTV 개발 및 엣지 AI 보안지능 최적화 및 보안 단말 연계협업
- 엣지간 클러스터링 및 AI 배포, 단말간 협업 기능 개발



### 일정

---

- 6~9월 : KETI 개발부분 진행
- 9월 말:까지 전체 시스템(엣지 CCTV, VMS, AI, 분석서버 등) 가져와서 환경구성
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



### 물리적 구조

---

- #### EDGE-5G, 2.4G 공유기

  - 주소 : 192.168.0.222

- #### AXIS M1135 카메라

  - 주소 : 192.168.0.76

- #### 마스터 서버

  - 이름 : edge-master-01

  - 주소 : 192.168.0.14

  - k8s 명령어 : 

    ```
    kubeadm join 192.168.0.14:6443 --token 3j3fp6.ocl6obtpe1lbju7l \
    	--discovery-token-ca-cert-hash sha256:84fa33eed337bf7ed84a887e7a11014e42f674146b6fe188fb7c75d194b848ff 
    ```

  - JSON 형태 정보 : 

    ```json
    {    
        "name" : “Master01”,
        "ip" : “192.168.0.14”,
        "port" : “5000”,
        "description" : “마스터 서버 1”
    }
    ```

    

- #### 워커 서버

  - 이름 : edge-worker-01
  
  - 주소 : 192.168.0.9
  
  - JSON 형태 정보 : 
  
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
  
- #### 업로드 파일

  - 마스터에 저장되어있는 파일을 사용

  - 위치 : /home/edge-master-01/monitoring.zip

  - API 서버로 cpu, 메모리 사용량 메타데이터(Json) POST 전송

    - API 서버 주소 : http://192.168.0.14:6432/usage

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
- 