# Prometheus

- Open Saurce Systems Monitoring
- 간단한 텍스트 형식으로 메트릭을 쉽게 노출
- 데이터 모델은 key-value형태로 레이블을 집계한 후, Granfana 같은 대시보드 시스템에서 그래프로 쉽고 간단하게 Dashboard를 만들 수 있다

## 주요 기능

- Metric 이름, key -value 쌍으로 식별되는 시계열 데이터가 있는 다차원 데이터 모델
- 이 차원을 활용하는 유연한 쿼리언어 : PromQL
- 분산 스토리지에 의존하지 않음 : 단일 서버 노드는 자율적
- 시계열 수집은 HTTP를 통한 풀 모델을 통해 발생
- 푸시 시계열은 중간 게이트웨이를 통해 지원
- 서비스 검색 또는 정적 구성을 통해 대상 검색
- 다양한 그래프 및 대시보드 모드 지원



## 구성요소

- Server : 시계열 데이터를 스크레핑하고 저장
- client library : Application Code 를 계측
- push gateway : 단기 작업을 지원
- exporters : HAProxy, StatsD, Graphite 같은 서비스를 위한 툴
- alermanager : 경고 핸들링



## 구조

- Pull 방식을 사용 : 서버에 클라이언트가 떠있으면 서버가 주기적으로 클라이언트에 접속해서 데이터 가져옴
- 다이어그램

![image](https://user-images.githubusercontent.com/58541635/90092279-7143f000-dd63-11ea-8fe7-93398692da6e.png)

1. 단기 작업을 위해 직접 또는 중간 `push gateway` 를 통해 계측된 작업에서 `metric` 을 스크랩
2. 스크랩 된 모든 샘플을 로컬에 저장하고 데이터에 대한 규칙을 실행하여 기존 데이터에서 새 시계열을 집계 및 기록하거나 경고를 생성
3. Granfana 또는 기타 API 소비자를 사용하여 수집 된 데이터를 시각화



### Prometheus Architecture 내용

- **Service discovery** : 
  - Prometheus 는 기본적으로 모니터링 대상 목록을 유지하고 있고, 대상 ip나 기타 접속 정보를 설정 파일에 줘서 모니터링 정보를 가져오는 방식을 사용
  - 오토 스케일링을 하는 환경에서는 ip가 동적으로 변경되는 경우가 많기 때문에, 모니터링 대상이 등록되어있는 저장소에서 목록을 받아 그 대상을 모니터링 하는 형태를 취함 ex) kubelet
- **Push gateway** : 
  - Proxy Forwarding을 해서 접근할 수 없는 곳에 데이터가 존재하는 경우에 사용.
  - 작동 방법 : Application 이 Push gateway 에 metric을 push한 후, Prometheus server가 Push gateway 에 접근해 metric을 pull해서 오는 방식
- **Jobs/Exporters**:
  - 실제로 metric을 수집하는 프로세스
  - Exporter는 Prometheus에게 metric을 가져가도록 특정 Service에 metric을 노출하게 하는 Agent
  - 서버 상태를 나타내는 Node Exporter, SQL Expoter 등 다양함
  - HTTP 통신을 통해 metric data를 가져갈 수 있게 `/metric`이라는 HTTP 엔드포인트를 제공
  - 그러면 Prometheus server가 Exporter의 엔드포인트로 HTTP GET 요청을 날려 pull(수집)한다
- **Data visualization** :
  - Dashboard를 위한 visualization 제공. 
  - 주로 Prometheus가 수집한 데이터에 대한 외부 시각화 툴 및 api를 제공
- **Alert manager** : 
  - metric 에 대한 어떠한 지표를 걸어놓고 그 규칙을 위반하는 사항에 대해 알람 전송



## Prometheus 를 이용한 모니터링

- 전체 인프라 환경과 Application 에 대한 모니터링을 하는것이 중요
- 인프라 전체적인 가시성을 확보해야 Application 에 대한 가용성과 안정성 확보
- 고도화된 Cloud Native System 구축 시 사용하는 지표로 활용

![image](https://user-images.githubusercontent.com/58541635/90090723-bc5c0400-dd5f-11ea-8bec-f6b7f42b0001.png)

- Cloud Native 환경에서의 모니터링은 Kubernetes API를 통해 동적으로 확장된 서버 endpoint 를 discovery 하는 방식으로 운영, 이후에 Monitoring backend 에서 discovery 한 endpoint 를 통해 metric 을 수집



## Kubernetes Monitoring Pipeline

- Core Metric Pipeline
- Monitoring



### Core Metric Pipeline

- k8s 관련 구성 요소를 직접 관리하는 파이프 라인
- kubelet, metrics-server, metric API 구성되어 있으며, 쿠버네티스의 핵심 동작 요소에 대한 모니터링을 담당, 현재 상태가 Desired State 가 되는 것을 모니터링 한다
- kubelet 에 저장된 cadvisor를 통해 Node/Pod/Container의 사용량 정보를 수집하며, 동적으로 확장 된 Node에 관련된 정보도 같이 수집
- kubelet에 저장된 정보는 metric server가 수집하여 메모리에 저장, 단시간의 데이터만 저장한다
- 저장된 정보는 k8s Master Metric API 를 통해 다른 시스템 component가 조회 가능하게 한다

![image](https://user-images.githubusercontent.com/58541635/90089716-098aa680-dd5d-11ea-8959-48eaebdb3512.png)



### Monitoring Pipeline

- MP 는 k8s 에서 제공하는 기본 메트릭 외에 다양한 메트릭을 수집하고 클러스터 사용자들이 필요한 모니터링을 하는데 사용한다
- 시스템 메트릭과 서비스 메트릭을 동시에 수집 가능
- 사용자가 직접 설치하여 MP를 구축해야 한다.
- cAdvisor + Prometheus 조합이 가장 많이 쓰임

![image](https://user-images.githubusercontent.com/58541635/90090162-50c56700-dd5e-11ea-8aa6-d5540e7025d1.png)



