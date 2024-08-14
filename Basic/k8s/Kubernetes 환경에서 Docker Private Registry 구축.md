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





## Kubernetes 에서 사용

### secret 생성

```
kubectl create secret docker-registry regcred \
  --docker-server=192.168.0.4:5000 \
  --docker-username=sehooh5 \
  --docker-password=@Dhtpgh1234 \
  --docker-email=sehooh5@gmail.com

```



### yaml 파일에 imagePullSecrets 설정 후 배포

- 예시 파일 : 

  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: monitorings
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: monitorings
    template:
      metadata:
        labels:
          app: monitorings
      spec:
        containers:
          - name: monitorings
            image: 192.168.0.4:5000/monitorings:01
            imagePullPolicy: Always
            ports:
              - containerPort: 6432
        imagePullSecrets: # 이 부분 추가
        - name : regcred
  ```



- 배포했는데 아래 에러 발생

```
Events:                                                                                                                                                        Type     Reason     Age   From               Message                                                                                                         ----     ------     ----  ----               -------                                                                                                         Normal   Scheduled  11s   default-scheduler  Successfully assigned default/monitorings-775cd8fcdb-klxcg to intellivix-worker-02                              Normal   Pulling    11s   kubelet            Pulling image "192.168.0.4:5000/monitorings:01"                                                                 Warning  Failed     11s   kubelet            Failed to pull image "192.168.0.4:5000/monitorings:01": failed to pull and unpack image "192.168.0.4:5000/monitorings:01": failed to resolve reference "192.168.0.4:5000/monitorings:01": failed to do request: Head "https://192.168.0.4:5000/v2/monitorings/manifests/01": http: server gave HTTP response to HTTPS client                                                                                                              Warning  Failed     11s   kubelet            Error: ErrImagePull                                                                                             Normal   BackOff    10s   kubelet            Back-off pulling image "192.168.0.4:5000/monitorings:01"                                                        Warning  Failed     10s   kubelet            Error: ImagePullBackOff    
```

- Kubernetes가 Docker Registry에 접근할 때 HTTPS로 접근하려고 시도
- Docker Registry는 기본적으로 HTTP를 사용하기 때문에 이 문제를 해결하려면 Docker와 Kubernetes가 HTTP로 연결하도록 설정해야 함
- 아래 내용으로 에러 해결



### 모든 Node에서 아래 설정 필요



#### containerd의 config 설정하기위해 위치로 이동

```
cd /etc/containerd/
```



#### config 파일 default 파일 생성

```
# defaul 파일 있으면
mv config.toml config_bkup.toml
 
# "없으면" config 파일 default 내용 포함해서 생성
sudo su
containerd config default > config.toml
exit
```



#### config 파일 설정

```
# config.toml
## 이미 작성된 내용이 있는데 중간에 아래 내용만 추가

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



#### Containerd 재시작

```
# containerd 재시작
sudo systemctl restart containerd

```









---



## ~~아래 내용은 참고만!~~



### ~~5. SSL 인증서 만들기~~

- ~~SSL 인증서는 https 통신을 위한 필수적인 인증 수단~~

- ~~로컬 컴퓨터에 등록하는 방식~~

  ```
  # 원하는 위치에 certs 폴더 만들기
  mkdir certs
  
  # certs 폴더로 이동
  cd certs/
  
  ## registry-service.key | registry-service.csr | registry-service.crt
  # SSL 생성 using OpenSSL
  # openssl genrsa -out server.key 2048
  openssl genrsa -out registry-service.key 2048
  
  # 인증서 서명
  # openssl req -new -key server.key -out server.csr # 각 정보 입력해주면 됨
  openssl req -new -key registry-service.key -out registry-service.csr
  
  # 공개키 생성 ./certs/
  # openssl x509 -req -days 3650 -in ./certs/registry-service.csr -signkey ./certs/registry-service.key -out ./certs/registry-service.crt
  
  
  ## 생성 파일 
  # server.crt  server.csr  server.key
  ```

  

### ~~6. htpasswd 생성~~

- ~~docker registry는 기본적으로 apache htpasswd를 이용한 auth 인증을 제공~~

- ~~htpasswd를 통해 간단히, username, password를 통한 인증정보를 생성~~

- ~~이후 해당 registry을 이용할 때, 해당 인증 정보를 활용~~

  ```
  # htpasswd 설치
  sudo apt install apache2-utils 
  
  # auths 폴더 생성
  mkdir auths
  
  # htpasswd 
  # htpasswd -Bbn <username> <password> > ./auths/htpasswd
  htpasswd -Bbn sehooh5 @Dhtpgh1234 > ./auths/htpasswd
  ```



### ~~Kubernetes secrets에 인증정보 저장~~

- ~~k8s cluster에 credential 정보들을 secret으로 등록~~

  ```
  # SSL 등록
  kubectl create secret generic registry-certs --from-file=registry-service.crt=./certs/registry-service.crt --from-file=registry-service.key=./certs/registry-service.key
  
  # htpasswd 등록
  kubectl create secret generic registry-htpasswd --from-file=htpasswd=./auths/htpasswd
  ```

  

### ~~서버와 클라이언트에 registry-service.crt 등록~~

-  ~~CA 인증을 받지 않았기 때문에, 서버와 클라이언트에 별도로 CA 파일을 등록~~

- ~~이후 container runtime을 재실행~~

  ```
  ## 모든 노드에서 해줘야함!!
  # registry-service.crt 를 서버에 등록하기 
  sudo cp ./certs/registry-service.crt /usr/local/share/ca-certificates/
  
  # 
  update-ca-certificates
  
  # docker 재시작
  sudo systemctl restart docker
  ```