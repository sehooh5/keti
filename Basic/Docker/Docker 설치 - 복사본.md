# Docker Private Registry

- Docker Hub를 사용하지 않고 Private Registry를 사용해 배포 가능하게하는 프로세스





## Process

### 1. Docker Registry 이미지 다운로드 및 실행

```
docker run -d -p 5000:5000 --name registry registry:2
```

- Docker Hub에서 공식 Docker Registry 이미지를 다운로드하고 실행
- Docker Registry를 백그라운드에서 실행하고, 로컬 머신의 포트 5000을 컨테이너의 포트 5000에 매핑



### 2. Docker 이미지 태그 지정

```
docker tag [이미지]:latest localhost:5000/[이미지]:latest
```

- 로컬 Docker 이미지를 Private Registry에 푸시하기 위해 이미지를 태그 지정
  - `[이미지]:latest` 이미지를 `localhost:5000/[이미지]:latest`로 태그 지정
- 혹은, 처음 설정부터  `localhost:5000/[이미지]:latest`로 지정해도 가능?



### 3. Docker 이미지 Push

```
docker push localhost:5000/[이미지]:latest
```

- 태그가 지정된 이미지를 Private Registry에 Push



### 4. Private Registry에서 Docker 이미지 Pull

```
docker pull localhost:5000/[이미지]:latest
```

- Private Registry에서 이미지를 Pull





### 인증 htpasswd 는 아직 진행하지 않음

- htpasswd 인증