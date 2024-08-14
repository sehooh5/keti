# Kubernetes 환경에서 Docker Private Registry 구축

- Docker Hub를 사용하지 않고 Private Registry를 사용해 배포 가능하게하는 프로세스
- 작업 위치 : ~/keti/Project6/3rd$
- Kubernetes 사용시 오류해결 참고 : 
  - [Kubernetes 배포시 http 오류 해결](https://jaeyung1001.tistory.com/entry/K8S-containerd-private-registry-%EC%A0%91%EA%B7%BC%ED%95%98%EA%B8%B0)



## Process

### 1. Docker Registry 이미지 다운로드 및 실행

```
docker run -d -p 5000:5000 --restart=always --name registry -v /mnt/registry:/var/lib/registry registry:2
```

- Docker Hub에서 공식 Docker Registry 이미지를 다운로드하고 실행
- Docker Registry를 백그라운드에서 실행하고, 로컬 머신의 포트 5000을 컨테이너의 포트 5000에 매핑



### 2. Docker 이미지 태그 지정

```
# 처음 설정부터 지정 // 127.0.0.1 localhost 사용 가능
docker build -f DockerfileS -t 192.168.0.4:5000/monitorings:01 .
docker build -f DockerfileS -t 127.0.0.1:5000/monitorings:01 .

# 이미지 태그 변경
docker tag [이미지]:latest 192.168.0.4:5000/monitorings:01
```

- 로컬 Docker 이미지를 Private Registry에 푸시하기 위해 이미지를 태그 지정
  - `[이미지]:latest` 이미지를 `192.168.0.4:5000/[이미지]:latest`로 태그 지정
- 혹은, 처음 설정부터  `192.168.0.4:5000/[이미지]:latest`로 지정해도 가능



### 3. Docker 이미지 Push

```
docker push 192.168.0.4:5000/monitorings:01

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

- 태그가 지정된 이미지를 Private Registry에 Push



### 4. Private Registry에서 Docker 이미지 Pull

```
docker pull 192.168.0.4:5000/monitorings:01 # 이게 됨
```

- Private Registry에서 이미지를 Pull




