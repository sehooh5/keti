# RTSP-OpenCV-Docker 카메라 연동

- RTSP 실시간으로 전달되는 웹캠의 데이터를 OpenCV로 실행되게 하고 Docker 컨테이너에 정보를 담아 사용한다
- 추후에 k8s 를 사용하여 worker 에 배포



## Spec

### rtsp address

- rtsp : // keti : keti1234@192.168.100.60 : 8805 / videoMain -> opencv1.py
- rtsp : // keti : keti1234@192.168.100.70 : 8810 / videoMain -> opencv2.py



### 구조

![image](https://user-images.githubusercontent.com/58541635/93307599-1f97f500-f83c-11ea-8378-c265da8f38f9.png)





### OpenCV-python 파일을 도커라이징

- Dockerfile

  ```
  
  ```

  

















## 참고 자료들

## OpenCV를 Docker  에서 활용

- [잘 다룬 예제 및 참고 페이지](https://curioso365.tistory.com/44) : opencv-python Docker image 참고 문서가 있고, 도커 컨테이너 내에서 cv2 실행시 일어나는 오류에 대한 수정이 있음
- [위 예제 활용한 페이지](https://smprlab.tistory.com/32)
- [Docker hub 에 다른사람들도 참고한 리포](https://hub.docker.com/r/jjanzic/docker-python3-opencv) : 위 예제들에서 사용한 DockerHub image
- [OpenCV 공식문서](https://www.learnopencv.com/install-opencv-docker-image-ubuntu-macos-windows/)

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

## [실제 OpenCV, RSTP, DOCKER 사용된 프로젝트](https://towardsdatascience.com/real-time-and-video-processing-object-detection-using-tensorflow-opencv-and-docker-2be1694726e5)

---

## [웹캠-도커 연결](https://www.mlr2d.org/contents/docker/06_dockercontainersetupexamples_webcam_audio)

---

