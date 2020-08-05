# Docker

- 도커 설치 환경 : Ubuntu 18.04
- 도커 버전은 크게 두가지
  - CE(Community Edition) : 개발자나 작은 팀들에게 이상적. 무료.
  - EE(Enterprise Edition) : 엔터프라이즈 개발이나 실제 확장 가능한 서버. 유료
- [참고 사이트 : HiSEON](https://hiseon.me/linux/ubuntu/install-docker/)



## 준비

- 오래된 버전 도커 삭제

  ```bash
  sudo apt-get remove docker docker0engine docker.io
  ```

- 패키지 설치

```bash
sudo apt-get update && sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```



## 패키지 저장소 추가

- 도커의 공식 gpg 키와 저장소 추가

  ```bash
  # 공식 gpg 키 추가
  $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  # 공식 키 확인
  $ sudo apt-key fingerprint 0EBFCD88
  # 저장소 추가
  $ sudo add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) \
     stable"
  ```

  

