# kubernetes 원격 제어

- k8s에서 Master에서 명령을 내리고 Worker 에서 명령을 받아 실행할 수 있는지 고찰



## Python app을 k8s 통해 배포하는 과정

- [공식문서 참고](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/)
- Docker image를 pull 할 때, 로컬에서 찾는 것이 아닌 Docker hub를 사용하였다.
  - 이유 : 로컬에서 이미지를 찾지 못하였다
  - 사용 아이디 : sehooh5



### App의 컨테이너화

#### App 의 기본 구성을 git 을 사용하여 컴퓨터에 복사

1. 저장소 복사

```bash
git clone https://github.com/JasonHaley/hello-python.git
```

#### 

2. 디렉토리 변경

```bash
cd hello-python/app
```

- 이 디렉토리에는 두개의 파일만 있다. main.py 와 requirements.txt파일

- main.py 는 App 이 "Hello from Python!"이라는 문구를 출력하게 한다. Flask 사용

  ```python
  from flask import Flask
  app = Flask(__name__)
  
  @app.route("/")
  def hello():
      return "Hello from Python!"
  
  if __name__ == "__main__":
      app.run(host='0.0.0.0')
  ```

  

- requirements.txt 에는 main.py 에 필요한 패키지목록이 있고 pip를 사용하여 설치하게 된다

  ```
  Flask
  ```

  



#### 로컬에서 테스트 실행

```bash
pip install -r requirements.txt # Flask install
python main.py # main.py 실행
```





#### Dockerfile 생성

- 컨테이너화의 첫 번째 단계로 Dockerfile 작성
- 해당 경로인 hello-python/app 디렉터리에 다음 내용을 Dockerfile 로 저장
- 이 파일은 Docker 가 이비지를 빌드하는 데 사용하는 일련의 지침으로 다음을 수행

```dockerfile
FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/app/main.py"]
```

> 1. Docker Hub에서 버전 3.7 용 공식 [Python 기본 이미지](https://hub.docker.com/_/python/) 를 가져옵니다.
> 2. 이미지에서 app이라는 디렉토리를 만듭니다.
> 3. 작업 디렉터리를 새 앱 디렉터리로 설정합니다.
> 4. 로컬 디렉토리의 내용을 해당 새 폴더에 이미지로 복사합니다.
> 5. 이전과 마찬가지로 pip 설치 프로그램을 실행하여 요구 사항을 이미지로 가져옵니다.
> 6. 컨테이너가 포트 5000에서 수신 대기하도록 Docker에 알립니다.
> 7. 컨테이너가 시작될 때 사용할 시작 명령을 구성합니다.



#### 이미지 만들기

- 다음 명령을 사용하여 이미지를 빌드

```
docker build -f Dockerfile -t sehooh5/hello-python:latest .
```

- **주의사항**

  - 반드시 마지막 `.`  또한 입력해주어야 한다
  - latest는 최신 버전이란 태그로 주어지지 않아도 default 값이다
  - DockerHub 를 사용하기 위해 Docker 사용자의 이름과 같은 경로를 설정해주어야 한다. 여기서는 `sehooh5`

- 이 명령으로 위 7단계가 실행되고, 이미지 생성 확인은 다음 명령으로 한다

  ```
  docker images
  ```



### 

### Docker 에서 실행

- k8s 에서 실행하기 전 Docker 에서 작동하는지 확인
- Docker 가 컨테이너에서 App을 실행하고 port 5001에 매핑

```
docker run -p 5001:5000 sehooh5/hello-python
```

- `http://localhost:5001` 로 이동하면 "Hello from Python!"이 출력 됨





### k8s 에서 실행

- 버전과 노드 확인 후 deployment.yaml 파일 작성
- deployment.yaml 파일은 일종의 지침서

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-python-service
spec:
  selector:
    app: hello-python
  ports:
  - protocol: "TCP"
    port: 6000
    targetPort: 5000
  type: LoadBalancer

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-python
spec:
  selector:
    matchLabels:
      app: hello-python
  replicas: 4
  template:
    metadata:
      labels:
        app: hello-python
    spec:
      containers:
      - name: hello-python
        image: hello-python:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 5000
```

- `---` 윗 부분은 Service 를 정의한 부분으로 인터넷 연결과 관련된다.
  - port 는 6000으로 노출하고, 대상 port 는 5000 을 지정
  - type 은 LoadBalancer 인 것을 확인할 수 있다
- `---` 아랫 부분은 Deployment 로 pod 에 한꺼번에 배포할 수 있다
  - replicas 는 복제할 개수를 지칭, 4개 만듬
  - 참조할 image 는 sehooh5/hello-python:latest 로 지정해준다
  - imagePullPolicy는 Never 로 해준다(혹은 IfNotPresent)
  - containerPort 는 5000으로 지정



#### deployment 배포

- 아래 명령어로 배포시킨다

```bash
kubectl apply -f deployment.yaml
```



- 다음 명령을 실행하여 포드 실행중인 것을 볼 수 있다

```
kubectl get pods
kubectl get deployment
kubectl get service(=svc)
```



- `http://localhost:6000` 으로 이동하면 "Hello from Python!" 이 실행
  - 나는 실행이 되지 않아 service 를 확인해보니 PORT가 6000:31137 로 포워딩 된 것을 확인 했다. 따라서 `http://localhost:31137` 로 실행 가능했다 (워커노드에서도 동일하게 실행 가능)





## VLC 실행

- terminal 에서 명령어 실행 :  `vlc`
- vlc 켜지면 `미디어 - 네트워크 스트림 열기` 에서 rstp 주소 입력





## 이제 

## 1. 마스터노드에서 실행을 시키면 워커노드에서 작동하게끔 만들어야 한다

## 2. OpenCV 를 활용한 python App이 작동하는지 확인해야 한다



---

## 참고자료



### 외부에서 Pod의 웹 서비스에 접근하는 방법

- https://developer.ibm.com/kr/cloud/container/2019/03/05/kubernetes_practice/
- **영상 띄울수 있는 컨테이너를 만들고 ServiceType을 NodePort 로 하면 되지않을까?**



### Ingress

- 클러스터 내의 서비스에 대한 외부 접근을 관리하는 API 오브젝트
- 일반적으로 HTTP를 관리





### Service







## OpenStack 사용 

- [영어 자료 참고](https://arxiv.org/ftp/arxiv/papers/1901/1901.04946.pdf)

![image](https://user-images.githubusercontent.com/58541635/91115385-13010080-e6c5-11ea-87e0-d1da1e5a118e.png)





---

## [지금 파이썬 배포에 활용하고 있는 사이트](https://lsjsj92.tistory.com/578)

---

### [아래내용](https://blog.naver.com/PostView.nhn?blogId=alice_k106&logNo=221341757624&redirect=Dlog&widgetTypeCall=true&directAccess=false)

**1.1 쿠버네티스 프록시를 localhost로 돌리고 API 서버에 접근하는 방법 (kube proxy)**



쿠버네티스 라이브러리를 사용하는 wrapper 애플리케이션을 Master 노드의 로컬에 둔 뒤, 이 애플리케이션이 localhost로 접근하면 쿠버네티스 클러스터를 제어할 수 있다.

---

### [공식문서 파이썬 배포](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/)

---

## [나중 flask 사용할 시 참고](https://m.blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221585566556&proxyReferer=https:%2F%2Fwww.google.com%2F)

---

