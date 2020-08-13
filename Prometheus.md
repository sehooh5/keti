# Prometheus

- Open Saurce Systems Monitoring

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

- 다이어그램

![image](https://user-images.githubusercontent.com/58541635/89995261-3ccd2700-dcc4-11ea-9975-cf334e39e1b7.png)

1. 단기 작업을 위해 직접 또는 중간 `push gateway` 를 통해 계측된 작업에서 `metric` 을 스크랩
2. 스크랩 된 모든 샘플을 로컬에 저장하고 데이터에 대한 규칙을 실행하여 기존 데이터에서 새 시계열을 집계 및 기록하거나 경고를 생성
3. Granfana 또는 기타 API 소비자를 사용하여 수집 된 데이터를 시각화



## Prometheus 를 이용한 모니터링

- 전체 인프라 환경과 Application 에 대한 모니터링을 하는것이 중요
- 인프라 전체적인 가시성을 확보해야 Application 에 대한 가용성과 안정성 확보
- 고도화된 Cloud Native System 구축 시 사용하는 지표로 활용

![image-20200813111711833](/Users/seho/Library/Application Support/typora-user-images/image-20200813111711833.png)

- Cloud Native 환경에서의 모니터링은 Kubernetes API를 통해 동적으로 확장된 서버 endpoint 를 discovery 하는 방식으로 운영, 이후에 Monitoring backend 에서 discovery 한 endpoint 를 통해 metric 을 수집



## Kubernetes Monitoring Pipeline

- Core Metric Pipeline
- Monitoring



### Core Metric Pipeline

- k8s 관련 구성 요소를 직접 관리하는 파이프 라인