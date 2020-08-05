# Docker

- 도커 설치 환경 : Ubuntu 18.04
- 도커 버전은 크게 두가지
  - CE(Community Edition) : 개발자나 작은 팀들에게 이상적. 무료.
  - EE(Enterprise Edition) : 엔터프라이즈 개발이나 실제 확장 가능한 서버. 유료



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



