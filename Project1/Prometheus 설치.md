# Prometheus 설치([참고](https://tommypagy.tistory.com/187))

## 사용 툴 버전

- ubuntu : 18.04
- kubernetes : 1.14
- docker : 최신버전 19.03.12 (현, 2020.08.04)



---

## Helm 설치

- Helm은 k8s 의 package managing tool으로 Prometheus 를 손쉽게 설치 가능



### Prometheus 를 설치하기 전 Helm 설치

- Ubuntu 환경에서는 `snap` 을 활용하여 쉽게 설치 가능하다 ([참고]([https://ssup2.github.io/record/Kubernetes_Helm_%EC%84%A4%EC%B9%98_Ubuntu_18.04/](https://ssup2.github.io/record/Kubernetes_Helm_설치_Ubuntu_18.04/)))

  ```
  - 다운로드
  # snap install helm --classic
  
  - 버전 확인
  $ helm version
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

- 업데이트 : 

  ```
  $ helm repo update
  ```



## Prometheus 설치

### 바로 Prometheus 설치

- 설치 : 

  ```
  - CLI : helm install [release name] [설치할 파일]
  $ helm install monitor stable/prometheus
  ```

- pod 상태 확인 : 

  ```
  $ kubectl get pod
  ```



### *** 여기서 몇가지 에러가 날 수 있다!!

1. Pending 

   - alermanager 와 server 두 개의 pod 에서 Pending 에서 안넘어갈 수 있는데, 그 이유는 k8s 클러스터에 StorageClass가 정의되어있지 않기 때문! (= pvc의 요청을 받아줄 provisioner 가 없기 떄문)

   - **해결 방법** : pv 옵션을 false로 변경 해주어 EmptyDir 을 사용하게 해야한다

     1. 문제가 되는 chart 확인

        ```
        $ helm inspect values stable/prometheus
        ```

     2. 확인하게 되면 엄청 많은 줄의 파일을 확인할 수 있는데, 수정할 부분만 따로 파일로 만들어 `persistentVolume.enabled : true` 를 `false` 로 변경하게 해주면 된다

        ```
        - vim 을 사용하여 대체할 yaml 파일 생성
        $ vim volumeF.yaml
        alertmanager: persistentVolume: enabled: false server: persistentVolume: enabled: false pushgateway: 
        persistentVolume: enabled: false
        
        
        - 대체할 파일내용을 본래 내용과 교체해주어 upgrade
        $ helm upgrade -f volumeF.yaml monitor stable/prometheus
        
        ```

     3. 이렇게 하면 pending 이 풀리게 되는데, 필자는 server 포드의 pending 이 풀리지 않았다. 이유는 ImagePullBackOff

2. ImagePullBackOff

   - 이 문제는 docker 가 Image 를 제대로 끌어오지 못하는데에 있다

     ```
     - 해당 pod의 error message(describe pod으로 확인)
     Normal Scheduled default-scheduler Successfully assigned default/monitor-prometheus-server-7c55cc4c5-kvw28 to keti1-worker1
     Warning Failed 36m kubelet, keti1-worker1 Error: ImagePullBackOff
     Normal Pulling 35m (x3 over 36m) kubelet, keti1-worker1 Pulling image "jimmidyson/configmap-reload:v0.4.0"
     Warning Failed 35m (x3 over 36m) kubelet, keti1-worker1 Failed to pull image "jimmidyson/configmap-reload:v0.4.0": rpc error: code = Unknown desc = Error response from daemon: Get https://registry-1.docker.io/v2/: dial tcp: lookup registry-1.docker.io: no such host
     Warning Failed 35m (x3 over 36m) kubelet, keti1-worker1 Error: ErrImagePull
     Normal Pulling 35m (x3 over 36m) kubelet, keti1-worker1 Pulling image "prom/prometheus:v2.20.1"
     Warning Failed 35m (x3 over 36m) kubelet, keti1-worker1 Failed to pull image "prom/prometheus:v2.20.1": rpc error: code = Unknown desc = Error response from daemon: Get https://registry-1.docker.io/v2/: dial tcp: lookup registry-1.docker.io: no such host
     Warning Failed 35m (x3 over 36m) kubelet, keti1-worker1 Error: ErrImagePull
     Normal BackOff 35m (x2 over 36m) kubelet, keti1-worker1 Back-off pulling image "prom/prometheus:v2.20.1"
     Warning Failed 6m39s (x115 over 36m) kubelet, keti1-worker1 Error: ImagePullBackOff
     Normal BackOff 100s (x136 over 36m) kubelet, keti1-worker1 Back-off pulling image "jimmidyson/configmap-reload:v0.4.0"
     ```

   - 에러 메시지를 확인하면 두 개의 이미지를 제대로 불러오지 못하고 있었다

     1. jimmidyson/configmap-reload:v0.4.0
     2. prom/prometheus:v2.20.1

   - **해결방법** : 따라서 해당 노드에 가서 직접 docker 로 이미지를 pull 해주었다

     ```
     - 해당 worker node 로 가서
     $ docker pull jimmidyson/configmap-reload:v0.4.0
     $ docker pull prom/prometheus:v2.20.1
     ```

   - 이후 pod 모두 Running 상태인 것을 확인 할 수 있었다.



### Port 변경

- svc 확인

```
$ kubectl get svc

-------------------
NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE
kubernetes ClusterIP 10.96.0.1 443/TCP 4h48m
monitor-kube-state-metrics ClusterIP 10.98.119.176 8080/TCP 177m
monitor-prometheus-alertmanager ClusterIP 10.103.42.162 80/TCP 177m
monitor-prometheus-node-exporter ClusterIP None 9100/TCP 177m
monitor-prometheus-pushgateway ClusterIP 10.98.36.22 9091/TCP 177m
monitor-prometheus-server ClusterIP 10.96.133.109 80/TCP 177m
```



- prometheus-server 를 clusterIP에서 NodePort 로 변경해준다 (spec, type 변경)

```
- 반드시 root에서 변경해야 적용됨
# kubectl edit svc monitor-prometheus-server

spec:
	clusterIP: 10.96.133.109
	externalTrafficPolicy: Cluster 	### 추가
	ports:
	- nodePort: 31557		### 변경
		port: 80
		protocol: TCP
		targetPort: 9090
	selector:
		app: prometheus
		component: server
		release: monitor
	sessionAffinity: None
	type: NodePort		### 변경
status:
	loadBalancer: {}
```



- 다시 svc 확인해보면 포트포워딩 된 포트가 보이고, 아래 주소로 접속 가능

```
http://[localhost]:31557
```



---

### **프로메테우스 Uninstall

- 먼저 `helm` 으로 uninstall

```
helm uninstall [인스톨(release) 이름]
```

- docker 부터 k8s 까지 전부 삭제해준다 (방법은 k8s 문서에)



---

### 참고 내용들

- [k8s 참고했던 곳에서 이어서 설명된 prom자료-medium]([https://medium.com/finda-tech/prometheus%EB%9E%80-cf52c9a8785f](https://medium.com/finda-tech/prometheus란-cf52c9a8785f))
- [제일 도움 많이 된 자료 - 호롤리](https://gruuuuu.github.io/cloud/monitoring-02/#)
- [호롤리를 참고해서 좀 더 자세했던 자료](https://tommypagy.tistory.com/187)
- [Helm 사용 설치](https://waspro.tistory.com/588)



