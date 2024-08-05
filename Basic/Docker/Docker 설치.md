# Docker

- Version : 19.03.12
- 도커 설치 환경 : Ubuntu 18.04
- 도커 버전은 크게 두가지
  - CE(Community Edition) : 개발자나 작은 팀들에게 이상적. 무료.
  - EE(Enterprise Edition) : 엔터프라이즈 개발이나 실제 확장 가능한 서버. 유료
- [참고 사이트 : HiSEON](https://hiseon.me/linux/ubuntu/install-docker/)



## 준비

- apt update

  ```bash
  sudo apt-get update
  ```

- 오래된 버전 도커 삭제

  ```bash
  sudo apt-get remove docker docker-engine docker.io
  ```

- 패키지 설치

  ```
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
  # 저장소 추가 ## jetson amd -> arm
  $ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  # docker 패키지 검색되는지 확인
  $ sudo apt-get update 
  $ sudo apt-cache search docker-ce
  ## 출력메시지
  docker-ce - Docker: the open-source application container engine
  ```

  

### 도커 CE설치

```bash
$ sudo apt-get update 
$ sudo apt-get install docker-ce

# 사용자를 docker 그룹에 추가
$ sudo usermod -aG docker $USER
```



### 반드시 스왑 메모리 비활성화

```
sudo swapoff -a
```



### 도커 데몬 드라이버 교체

- from `cgroupfs` to `systemd`

  ```bash
  $ sudo cat > /etc/docker/daemon.json <<EOF
  {
    "exec-opts": ["native.cgroupdriver=systemd"],
    "log-driver": "json-file",
    "log-opts": {
      "max-size": "100m"
    },
    "storage-driver": "overlay2"
  }
  EOF
  $ sudo mkdir -p /etc/systemd/system/docker.service.d
  $ sudo systemctl daemon-reload
  $ sudo systemctl restart docker
  $ newgrp docker # 사용자를 docker 그룹에 추가할 때 안되면 마지막에 실행(sudo 사용 안해도됨)
  ```

- 잘 안되서 슈퍼계정 들어간 상태에서 실행했음 `#`

