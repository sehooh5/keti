# Prometheus



## Prometheus?

- Time-series DB(시계열 DB) 인 CNCF 프로젝트 중 하나
- 주로 CPU, 메모리 사용량 과 같은 Metrics 데이터에 대한  APM 구축을 목적
- MSA 형태의 컨테이너 서비스, 대규모 서버 클러스터 모니터링 등에서 사용
- 예 : HTTP 응답 데이터 Metrics(Appication), Container 서비스 단위의 리소스 사용량(Container & Service Layer), 서버 클러스터 전체의 가용률:Utilization (Cluster & Node Layer) 모니터링



### 장점

- **다차원 데이터 모델** 가능 (Metric 이름과 key-value 활용)
- 다차원 데이터 모델을 활용할 수 있는 유연한 쿼리 언어 (**PromQL**)
- 분산 스토리지에 대해서 어떠한 의존성도 없음
- 모든 데이터는 HTTP(REST) **Pull** 기반으로 가져온다, Push 도 가능하긴 함
- 모니터링 타켓은 YAML 설정값으로 Discovery
- Vertical - Horizontal Federation 가능 (상위-하위 구조를 통한 Aggregation 가능)



---

## 주석

- CNCF : Cloud Native Computing Foundation
- APM : Application Performance Management, 응용 소프트웨어의 성능과 서비스 이용성을 감시, 관리
- MSA : MicroService Architecture, 작고 독립적으로 배포가능 각각의 기능을 수행하는 서비스로 구성된 프레임 워크. 다른 기술 스택, 언어, DB 등이 사용 가능한 단일 사업 영역에 초점을 둔다

