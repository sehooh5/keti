# Project 1

- 5G 기반 협력 대응 과제



### 사용 툴 버전

---

- ubuntu : 18.04

- kubernetes : 1.14
- docker : 최신버전 19.03.12 (현, 2020.08.04)



### 참고 자료

---

### 전체적 시나리오 잘 정리된 페이지

- [시나리오](https://medium.com/finda-tech/overview-8d169b2a54ff)
- [기본적인 docker-kubernetes 관계 및 용어들 정리 잘해놓음](https://zzsza.github.io/development/2018/04/17/docker-kubernetes/)



#### Ubuntu

- [Ubuntu 설치방법](https://coding-factory.tistory.com/494)
- [Ubuntu 네트워크 설정 CLI](https://ismydream.tistory.com/99)
- [Ubuntu 네트워크 설정 GUI(이거 사용했음)](https://webdir.tistory.com/188)
- [vi 사용법](https://jhnyang.tistory.com/54)



#### Docker

- [Docker?(subicura)](https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html)
- [설치 및 실행(subicura)](https://subicura.com/2017/01/19/docker-guide-for-beginners-2.html)
- [Ubuntu 18.04 버전 다운로드](http://mirror.kakao.com/ubuntu-releases/bionic/)
- [Ubuntu 에 Docker 최신버전 설치](https://www.dante2k.com/581)
- [Ubuntu에 Docker 설치(HiSEON)](https://hiseon.me/linux/ubuntu/install-docker/)
- [설치-공식문서](https://kubernetes.io/docs/setup/production-environment/container-runtimes/#docker)



#### Kubernetes

- [공식 도큐먼트](https://kubernetes.io/ko/docs/concepts/overview/what-is-kubernetes/)
- [Kubernetes?(subicura)](https://subicura.com/2019/05/19/kubernetes-basic-1.html)
- [Ubuntu에 Kubernetes 설치(HiSEON)](https://hiseon.me/linux/ubuntu/ubuntu-kubernetes-install/)
- [전달받은 설치 문서](https://www.joinc.co.kr/w/man/12/kubernetes/kubecluster)
- [설치 실패시 초기화방법](https://likefree.tistory.com/13)
- [명령어 등 참고하면 좋은자료](https://zzsza.github.io/development/2018/04/17/docker-kubernetes/)



## 진행 단계(daily)

### 2020

---

#### 0804

- 테스트베드 구축에 대한 탐구
  - 사용하는 프로그램, 툴에 대한 언어 공부 및 활용 방법 모색
  - Ubuntu 기반 **Kubernetes**를 사용하여 Master/Worker 서버에 대한 환경 구축(**Docker** 활용)
- 베어본 PC 사용하여 직접 설치해보기
- **설치 순서**: Ubuntu - Docker - Kubernetes
- **Rufus** 로 USB 에 부팅 가능한 ISO 파일 저장후 사용하게끔하기
- 완료 : keti0 컴퓨터에 Ubuntu 설치완료, 네트워크 static IPv4 설정 완료, 3개 컴퓨터 이더넷으로 연결 ( IPv4 : 192.168.100.5, 6, 7)



### 0805

- 완료 : Docker*3 설치 완료



### 0806

- 완료 : kubernetes 용어정리 및 설치 완료

  (쿠버네티스 잘 작동되는지 확인해야함) 



### 0807

- 진행중 :  Kubernetes 설정



### 0810

- 완료 : 3대 설치 완료

- 오류 : 연동 되는데 not ready, unhealthy



### 0811

- 완료 : master 1 / worker 1 설치 완료,  배포완료
- 오류 : unhealthy 여전히 뜨고 한 대는 join 안됨



### 0812

- 오류 : 재부팅하면 `kubectl` 명령어 시 port를 못찾을 때가 있음