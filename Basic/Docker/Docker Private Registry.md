# Docker Private Registry

- Docker Hub를 사용하지 않고 Private Registry를 사용해 배포 가능하게하는 프로세스
- Kubernetes 에서 활용할 수 있는 자세한 내용 : [URL](https://medium.com/@craftsangjae/k8s%EC%97%90-docker-private-registry-%EA%B5%AC%EC%B6%95%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95-db705cffe623)



## Process

### 1. Docker Registry 이미지 다운로드 및 실행

```
docker run -d -p 5000:5000 --name registry registry:2
```

- Docker Hub에서 공식 Docker Registry 이미지를 다운로드하고 실행
- Docker Registry를 백그라운드에서 실행하고, 로컬 머신의 포트 5000을 컨테이너의 포트 5000에 매핑



### 2. Docker 이미지 태그 지정

```
# 처음 설정부터 지정
docker build -f DockerfileS -t 192.168.0.4:5000/monitorings:01 .

# 이미지 태그 변경
docker tag [이미지]:latest 192.168.0.4:5000/monitorings:01
```

- 로컬 Docker 이미지를 Private Registry에 푸시하기 위해 이미지를 태그 지정
  - `[이미지]:latest` 이미지를 `192.168.0.4:5000/[이미지]:latest`로 태그 지정
- 혹은, 처음 설정부터  `192.168.0.4:5000/[이미지]:latest`로 지정해도 가능



### 3. Docker 이미지 Push

```
docker push 192.168.0.4:5000/monitorings:01
```

- 태그가 지정된 이미지를 Private Registry에 Push



### 4. Private Registry에서 Docker 이미지 Pull

```
docker pull 192.168.0.4:5000/monitorings:01
```

- Private Registry에서 이미지를 Pull





### 인증 htpasswd 는 아직 진행하지 않음

- htpasswd 인증



### Kubernetes 에서 사용



- namespace 생성

  ```
  # 모든 서비스의 구분을 위한 namespace 생성
  
  kubectl create namespace keti
  ```

  

- secret 생성

  ```
  kubectl create secret docker-registry regcred \
    --namespace=keti \
    --docker-server=192.168.0.4:5000 \
    --docker-username=sehooh5 \
    --docker-password=@Dhtpgh1234 \
    --docker-email=sehooh5@gmail.com
  ```

  



### 에러슈팅

이전 에러

```
Events:                                                                                                                                                        Type     Reason     Age               From               Message                                                                                             ----     ------     ----              ----               -------                                                                                             Normal   Scheduled  12s               default-scheduler  Successfully assigned default/monitorings-6d84b5c5dd-hm5lm to intellivix-worker-02                  Normal   BackOff    12s               kubelet            Back-off pulling image "localhost:5000/monitorings:01"                                              Warning  Failed     12s               kubelet            Error: ImagePullBackOff                                                                             Normal   Pulling    1s (x2 over 12s)  kubelet            Pulling image "localhost:5000/monitorings:01"                                                       Warning  Failed     1s (x2 over 12s)  kubelet            Failed to pull image "localhost:5000/monitorings:01": failed to pull and unpack image "localhost:5000/monitorings:01": failed to resolve reference "localhost:5000/monitorings:01": failed to do request: Head "http://localhost:5000/v2/monitorings/manifests/01": dial tcp 127.0.0.1:5000: connect: connection refused                                                                                                      Warning  Failed     1s (x2 over 12s)  kubelet            Error: ErrImagePull     
```





#### 이후 에러:

```
Events:                                                                                                                                                        Type     Reason     Age   From               Message                                                                                                         ----     ------     ----  ----               -------                                                                                                         Normal   Scheduled  11s   default-scheduler  Successfully assigned default/monitorings-775cd8fcdb-klxcg to intellivix-worker-02                              Normal   Pulling    11s   kubelet            Pulling image "192.168.0.4:5000/monitorings:01"                                                                 Warning  Failed     11s   kubelet            Failed to pull image "192.168.0.4:5000/monitorings:01": failed to pull and unpack image "192.168.0.4:5000/monitorings:01": failed to resolve reference "192.168.0.4:5000/monitorings:01": failed to do request: Head "https://192.168.0.4:5000/v2/monitorings/manifests/01": http: server gave HTTP response to HTTPS client                                                                                                              Warning  Failed     11s   kubelet            Error: ErrImagePull                                                                                             Normal   BackOff    10s   kubelet            Back-off pulling image "192.168.0.4:5000/monitorings:01"                                                        Warning  Failed     10s   kubelet            Error: ImagePullBackOff    
```

- Kubernetes가 Docker Registry에 접근할 때 HTTPS로 접근하려고 시도
- Docker Registry는 기본적으로 HTTP를 사용하기 때문에 이 문제를 해결하려면 Docker와 Kubernetes가 HTTP로 연결하도록 설정해야 함



