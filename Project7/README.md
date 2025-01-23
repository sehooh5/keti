# README

- 신규과제 1차년도
- k8s, Docker, 클러스터링, 배포 시스템
- `NEW` 
  - k8s, docker Python 모듈 사용(예정)
  - private repository 사용(예정)





## 환경구성

- 마스터 1대, 워커 1대 신규 구성



### 마스터

- 운영체제/시스템 : Ubuntu / AMD
- Name : edge-master-01
- IP : 192.168.0.14 
  - ssh 접속 : 10.252.219.225
- Port : 2214
- Server URL : 192.168.0.14:5231
- ID : 6791adaa56342c0a1beb1b09



### 워커

- 운영체제/시스템 : Ubuntu / AMD
- Name : edge-worker-01
- IP : 192.168.0.9 
- Port : 2209
- ID : 6791adcb56342c0a1beb1b27



### Front

- Serve URL : 10.252.219.108:4883





## 진행 상황



### 완료

- 세팅 완료





#### 0124

- 진행완료
  - CLI 로 클러스터 구성 먼저 해보고 
  - 코드 수정
  - 예지누나 오후에 전달
    - 완료
- 진행예정
  - upload 파트 어떻게 파일이 전달되는지? 아니면 master 저장된거에서 진행? 파악후 수정 혹은 진행 필요
    - fileUrl 으로 오는 정보 파싱해서
    - master에 있는 파일로 upload 실행