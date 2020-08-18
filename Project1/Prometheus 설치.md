# Prometheus 설치

## 사용 툴 버전

- ubuntu : 18.04
- kubernetes : 1.14
- docker : 최신버전 19.03.12 (현, 2020.08.04)



---

### Prometheus 를 설치하기 전 Helm 설치

- Ubuntu 환경에서는 `snap` 을 활용하여 쉽게 설치 가능하다 ([참고]([https://ssup2.github.io/record/Kubernetes_Helm_%EC%84%A4%EC%B9%98_Ubuntu_18.04/](https://ssup2.github.io/record/Kubernetes_Helm_설치_Ubuntu_18.04/)))

  ```
  # snap install helm --classic
  ```



### Helm 레포지토리를 로컬에 stable 이름으로 추가

```
$ helm repo add stable https://kubernetes-charts.storage.googleapis.com/
```

- Helm Chart list : 

  ```
  $ helm search repo stable (prometheus 검색 가능)
  ```



### *Helm Chart 설치

- [HELM_CHAR]를 [RELEASE_NAME]으로 쿠버네티스 클러스터안에 배포

  ```bash
  ## $ helm install [RELEASE_NAME] [HELM_CHART]
  
  $ helm install prometheus stable/prometheus
  ```

- 배포된 릴리즈 목록 조회 : 

  ```
  $ helm ls
  ```

- 



- [참고]([https://medium.com/finda-tech/prometheus%EB%9E%80-cf52c9a8785f](https://medium.com/finda-tech/prometheus란-cf52c9a8785f))
- [설치1](https://gruuuuu.github.io/cloud/monitoring-02/#)
- [Helm 사용 설치](https://waspro.tistory.com/588)

