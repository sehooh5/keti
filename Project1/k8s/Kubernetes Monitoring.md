# K8s Monitoring

**참고 링크들**

1. [아리수/쿠버네티스 모니터링 아키텍처(kubernetes monitoring architecture)](https://arisu1000.tistory.com/27855)
2. [조대협의블로그/쿠버네티스 #13 - 모니터링 (1/2)](https://bcho.tistory.com/1269)
3. [Kubernetes Community/Kubernetes monitoring architecture](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/instrumentation/monitoring_architecture.md#architecture)
4. [alice/167. Kubernetes\] 쿠버네티스 모니터링 : Prometheus Adapter와 Opencensus를 이용한 Custom Metrics 수집 및 HPA 적용](https://blog.naver.com/alice_k106/221521978267)



### Concept

---

![image](https://user-images.githubusercontent.com/58541635/90848485-f5235b00-e3a7-11ea-8b9d-bb29fd3e5c87.png)

- k8s에서 데이터를 수집할 수 있는 오브젝트는 크게 4가지 계층
  1. **Host** : Node 의 CPU, 메모리, 디스크, 네트워크 사용량과 노드os와 커널에 대한 모니터링
  2. **Container** : Node의 기동되는 각각의 컨테이너에 대한 정보. 컨테이너의 CPU, 메모리, 디스크, 네트워크 사용량 모두 모니터링
  3. **Application** : 컨테이너에서 구동되는 개별 어플리케이션에 대한 모니터링
  4. **k8s** : 컨테이너를 컨트롤 하는 쿠버네티스 자체에 대한 모니터링 (POD, 계정정보 등)
- k8s 공식문서에서는 이들을 수집지표, 즉 <mark>**Metric**</mark>이라 부른다



### Metric

---

1. **System metrics**: 노드나 컨테이너의 CPU, 메모리 사용량 같은 일반적인 시스템관련 

   - `core metric` : k8s의 내부 컴포넌트들이 사용하는 메트릭. (kubectl top에서 사용하는 메트릭 값)
   - `non-core metric` : k8s가 직접 사용하지 않는 다른 시스템 메트릭을 의미

2. **Service metrics**: Application 을 모니터링 하는데 필요한 metric

   - k8s 인프라 컨테이너에서 나오는 메트릭은 클러스터를 관리할 때 참고해서 사용

   - 사용자 Application 에서 나오는 metric 은 서비스 관련 정보를 파악할 수 있음 

     (ex. 웹서버의 응답속도, 500 error의 빈도 등)



### Pipeline

---

- 수집 지표들을 수집하는 Pipeline

1. **Resource metric pipeline** : 
   - 핵심 요소들에 대한 모니터링 (kubelet, metrics-server, metricAPI 등)
   - Scheduler나 HPA 등의 기초자료로 활용
   - (*HPA : 시스템의 부하 여부에 따라 pod을 자동으로 scale out 시켜주는 ctrl)
2. **Full metric pipeline** :
   - k8s 가 관리하지 않고 외부 모니터링 시스템을 연계해서 이용하는 것을 권장
   - 시스템, 서비스 metric 둘다 수집 가능