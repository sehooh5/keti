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



#### 로컬에서 테스트 실행

```bash
pip install -r requirements.txt # Flask install
python main.py # main.py 실행
```





#### Dockerfile 생성









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

