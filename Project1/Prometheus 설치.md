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



<mark>**위 방법, 즉 helm 을 사용하면, Prometheus 브라우저의 Target 에서  kube-state-metrics 를 확인 할 수 없었다. 그래서 uninstall 후 직접 yaml설정을 해주는 방식으로 변경하였다.**</mark>





## 직접 yaml 파일 작성하여 진행

### 제일 먼저 namespace 를 생성한다

```
$ kubectl create ns monitoring
```



### yaml 파일 작성

- `vim` 명령어를 사용해 작성해 준다

#### Cluster Role 을 작성한다

- 프로메테우스 컨테이너가 k8s API 에 접근할 수 있는 권한을 주기위해 Cluster Role 을 설정해주고 ClusterRoleBinding 해준다
- 생성된 Cluster Role 은 monitoring namespace 의 기본 서비스 어카운트와 연동되어 권한을 부여한다

```
# prometheus-cluster-role.yaml

apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: prometheus
  namespace: monitoring
rules:
- apiGroups: [""]
  resources:
  - nodes
  - nodes/proxy
  - services
  - endpoints
  - pods
  verbs: ["get", "list", "watch"]
- apiGroups:
  - extensions
  resources:
  - ingresses
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: prometheus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: prometheus
subjects:
- kind: ServiceAccount
  name: default
  namespace: monitoring
```



#### Configmap

- 프로메테우스가 기동되려면 환경설정파일이 필요한데 해당 환경 설정 파일을 작성

- data 밑에 `prometheus.rules` 와 `prometheus.yml` 를 각각 정의였음

  (다른예제에선 따로 하는 경우도 있었음)

  - **prometheus.rules** : 수집한 지표에 대한 알람 조건을 지정하여 특정 조건이 되면 AlertManager로 알람을 보낼 수 있음
  - **prometheus.yml** : 수집할 지표(metric)의 종류와 수집 주기등을 기입

```bash
# prometheus-config-map.yaml

apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-server-conf
  labels:
    name: prometheus-server-conf
  namespace: monitoring
data:
# prometheus.rules 정의부분
  prometheus.rules: |-
    groups:
    - name: container memory alert
      rules:
      - alert: container memory usage rate is very high( > 55%)
        expr: sum(container_memory_working_set_bytes{pod!="", name=""})/ sum (kube_node_status_allocatable_memory_bytes) * 100 > 55
        for: 1m
        labels:
          severity: fatal
        annotations:
          summary: High Memory Usage on 
          identifier: ""
          description: " Memory Usage: "
    - name: container CPU alert
      rules:
      - alert: container CPU usage rate is very high( > 10%)
        expr: sum (rate (container_cpu_usage_seconds_total{pod!=""}[1m])) / sum (machine_cpu_cores) * 100 > 10
        for: 1m
        labels:
          severity: fatal
        annotations:
          summary: High Cpu Usage
          
# prometheus.yml 정의부분
  prometheus.yml: |-
    global:
      scrape_interval: 5s
      evaluation_interval: 5s
    rule_files:
      - /etc/prometheus/prometheus.rules
    alerting:
      alertmanagers:
      - scheme: http
        static_configs:
        - targets:
          - "alertmanager.monitoring.svc:9093"

    scrape_configs:
      - job_name: 'kubernetes-apiservers'

        kubernetes_sd_configs:
        - role: endpoints
        scheme: https

        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

        relabel_configs:
        - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
          action: keep
          regex: default;kubernetes;https

      - job_name: 'kubernetes-nodes'

        scheme: https

        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

        kubernetes_sd_configs:
        - role: node

        relabel_configs:
        - action: labelmap
          regex: __meta_kubernetes_node_label_(.+)
        - target_label: __address__
          replacement: kubernetes.default.svc:443
        - source_labels: [__meta_kubernetes_node_name]
          regex: (.+)
          target_label: __metrics_path__
          replacement: /api/v1/nodes/${1}/proxy/metrics


      - job_name: 'kubernetes-pods'

        kubernetes_sd_configs:
        - role: pod

        relabel_configs:
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
          action: keep
          regex: true
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
          action: replace
          target_label: __metrics_path__
          regex: (.+)
        - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
          action: replace
          regex: ([^:]+)(?::\d+)?;(\d+)
          replacement: $1:$2
          target_label: __address__
        - action: labelmap
          regex: __meta_kubernetes_pod_label_(.+)
        - source_labels: [__meta_kubernetes_namespace]
          action: replace
          target_label: kubernetes_namespace
        - source_labels: [__meta_kubernetes_pod_name]
          action: replace
          target_label: kubernetes_pod_name

      - job_name: 'kube-state-metrics'
        static_configs:
          - targets: ['kube-state-metrics.kube-system.svc.cluster.local:8080']

      - job_name: 'kubernetes-cadvisor'

        scheme: https

        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

        kubernetes_sd_configs:
        - role: node

        relabel_configs:
        - action: labelmap
          regex: __meta_kubernetes_node_label_(.+)
        - target_label: __address__
          replacement: kubernetes.default.svc:443
        - source_labels: [__meta_kubernetes_node_name]
          regex: (.+)
          target_label: __metrics_path__
          replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor

      - job_name: 'kubernetes-service-endpoints'

        kubernetes_sd_configs:
        - role: endpoints

        relabel_configs:
        - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
          action: keep
          regex: true
        - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
          action: replace
          target_label: __scheme__
          regex: (https?)
        - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
          action: replace
          target_label: __metrics_path__
          regex: (.+)
        - source_labels: [__address__, __meta_kubernetes_service_annotation_prometheus_io_port]
          action: replace
          target_label: __address__
          regex: ([^:]+)(?::\d+)?;(\d+)
          replacement: $1:$2
        - action: labelmap
          regex: __meta_kubernetes_service_label_(.+)
        - source_labels: [__meta_kubernetes_namespace]
          action: replace
          target_label: kubernetes_namespace
        - source_labels: [__meta_kubernetes_service_name]
          action: replace
          target_label: kubernetes_name
```



#### deployment

- 프로메테우스의 이미지를 담은 pod을 담은 depolyment controller

```
# prometheus-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus-deployment
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus-server
  template:
    metadata:
      labels:
        app: prometheus-server
    spec:
      containers:
        - name: prometheus
          image: prom/prometheus:latest
          args:
            - "--config.file=/etc/prometheus/prometheus.yml"
            - "--storage.tsdb.path=/prometheus/"
          ports:
            - containerPort: 9090
          volumeMounts:
            - name: prometheus-config-volume
              mountPath: /etc/prometheus/
            - name: prometheus-storage-volume
              mountPath: /prometheus/
      volumes:
        - name: prometheus-config-volume
          configMap:
            defaultMode: 420
            name: prometheus-server-conf

        - name: prometheus-storage-volume
          emptyDir: {}
```



#### node exporter

- 프로메테우스가 수집하는 metric 은 쿠버네티스에서 기본적으로 제공하는 system metric 만 수집하는 것이 아니고 그 외의 것들도 수집하기 때문에 수집역할을 하는 에이전트를 따로 두어야 함
- 그 역할을 해주는게 **node-exporter** 이고 각 노드에 하나씩 띄워야 하므로 <mark>**daemonSet**</mark>으로 구성해준다

```
# prometheus-node-exporter.yaml

apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: monitoring
  labels:
    k8s-app: node-exporter
spec:
  selector:
    matchLabels:
      k8s-app: node-exporter
  template:
    metadata:
      labels:
        k8s-app: node-exporter
    spec:
      containers:
      - image: prom/node-exporter
        name: node-exporter
        ports:
        - containerPort: 9100
          protocol: TCP
          name: http
---
apiVersion: v1
kind: Service
metadata:
  labels:
    k8s-app: node-exporter
  name: node-exporter
  namespace: kube-system
spec:
  ports:
  - name: http
    port: 9100
    nodePort: 31672
    protocol: TCP
  type: NodePort
  selector:
    k8s-app: node-exporter
```



#### Service

- 프로메테우스 pod을 외부로 노출시키는 서비스를 구성
- 여기서 port 번호는 8080 (grafana 에서도 사용)
- nodePort  는 30003으로 본인이 임의 지정해준다

```
# prometheus-svc.yaml

apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
  namespace: monitoring
  annotations:
      prometheus.io/scrape: 'true'
      prometheus.io/port:   '9090'
spec:
  selector:
    app: prometheus-server
  type: NodePort
  ports:
    - port: 8080
      targetPort: 9090
      nodePort: 30003
```





### yaml 파일 배포

```
$ kubectl apply -f prometheus-cluster-role.yaml
$ kubectl apply -f prometheus-config-map.yaml
$ kubectl apply -f prometheus-deployment.yaml
$ kubectl apply -f prometheus-node-exporter.yaml
$ kubectl apply -f prometheus-svc.yaml
```



- 배포된 것 확인 : 

```
$ kubectl get pod -n monitoring

NAME                                     READY   STATUS    RESTARTS   AGE
node-exporter-99w2v                      1/1     Running   0          18s
node-exporter-f9q7f                      1/1     Running   0          18s
prometheus-deployment-7bcb5ff899-h4rb7   1/1     Running   0          65s
```





### Browser 에서 Prometheus Web UI로 접근(확인만)

- [localhost]:30003 으로 접근 가능 (30003은 위 service.yaml에서 지정해주었음)
- Target 에서 kube-state-metrics (0/1)으로 아직 올라가지 않은 것을 볼 수 있는데 올려줘야 한다 (kube-state-metrics는 k8s클러스 내 오브젝트(pod..)에 대한 지표를 생성하는 서비스)



### kube-state-metrics 배포

#### ClusterRole, ClusterRoleBinding

```
# kube-state-cluster-role.yaml

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kube-state-metrics
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kube-state-metrics
subjects:
- kind: ServiceAccount
  name: kube-state-metrics
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kube-state-metrics
rules:
- apiGroups:
  - ""
  resources: ["configmaps", "secrets", "nodes", "pods", "services", "resourcequotas", "replicationcontrollers", "limitranges", "persistentvolumeclaims", "persistentvolumes", "namespaces", "endpoints"]
  verbs: ["list","watch"]
- apiGroups:
  - extensions
  resources: ["daemonsets", "deployments", "replicasets", "ingresses"]
  verbs: ["list", "watch"]
- apiGroups:
  - apps
  resources: ["statefulsets", "daemonsets", "deployments", "replicasets"]
  verbs: ["list", "watch"]
- apiGroups:
  - batch
  resources: ["cronjobs", "jobs"]
  verbs: ["list", "watch"]
- apiGroups:
  - autoscaling
  resources: ["horizontalpodautoscalers"]
  verbs: ["list", "watch"]
- apiGroups:
  - authentication.k8s.io
  resources: ["tokenreviews"]
  verbs: ["create"]
- apiGroups:
  - authorization.k8s.io
  resources: ["subjectaccessreviews"]
  verbs: ["create"]
- apiGroups:
  - policy
  resources: ["poddisruptionbudgets"]
  verbs: ["list", "watch"]
- apiGroups:
  - certificates.k8s.io
  resources: ["certificatesigningrequests"]
  verbs: ["list", "watch"]
- apiGroups:
  - storage.k8s.io
  resources: ["storageclasses", "volumeattachments"]
  verbs: ["list", "watch"]
- apiGroups:
  - admissionregistration.k8s.io
  resources: ["mutatingwebhookconfigurations", "validatingwebhookconfigurations"]
  verbs: ["list", "watch"]
- apiGroups:
  - networking.k8s.io
  resources: ["networkpolicies"]
  verbs: ["list", "watch"]
```



#### ServiceAccount 생성

```
# kube-state-svcaccount.yaml

apiVersion: v1
kind: ServiceAccount
metadata:
  name: kube-state-metrics
  namespace: kube-system
```



#### cube-state-metrics의 deployment 구성

```
# kube-state-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: kube-state-metrics
  name: kube-state-metrics
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kube-state-metrics
  template:
    metadata:
      labels:
        app: kube-state-metrics
    spec:
      containers:
      - image: quay.io/coreos/kube-state-metrics:v1.8.0
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          timeoutSeconds: 5
        name: kube-state-metrics
        ports:
        - containerPort: 8080
          name: http-metrics
        - containerPort: 8081
          name: telemetry
        readinessProbe:
          httpGet:
            path: /
            port: 8081
          initialDelaySeconds: 5
          timeoutSeconds: 5
      nodeSelector:
        kubernetes.io/os: linux
      serviceAccountName: kube-state-metrics
```



#### kube-state-metrics의 서비스 생성

```
# kube-state-svc.yaml

apiVersion: v1
kind: Service
metadata:
  labels:
    app: kube-state-metrics
  name: kube-state-metrics
  namespace: kube-system
spec:
  clusterIP: None
  ports:
  - name: http-metrics
    port: 8080
    targetPort: http-metrics
  - name: telemetry
    port: 8081
    targetPort: telemetry
  selector:
    app: kube-state-metrics
```



#### 배포

```
$ kubectl apply -f kube-state-cluster-role.yaml
$ kubectl apply -f kube-state-deployment.yaml
$ kubectl apply -f kube-state-svcaccount.yaml
$ kubectl apply -f kube-state-svc.yaml
```



#### 확인

```
$ kubectl get pod -n kube-system

NAME                                       READY   STATUS    RESTARTS   AGE
...
kube-state-metrics-59bd4d9d-nbfrq          1/1     Running   0          50s
```

- 다시 Browser UI 를 확인하면 정상실행 되는것을 확인할 수 있다.

# 0821 에 그라파나 연동 정리!!!

---

## **프로메테우스 Uninstall

- 먼저 `helm` 으로 uninstall

```
helm uninstall [인스톨(release) 이름]
```

- docker 부터 k8s 까지 전부 삭제해준다 (방법은 k8s 문서에)



---

### 참고 내용들

- [k8s 참고했던 곳에서 이어서 설명된 prom자료-medium](https://medium.com/finda-tech/prometheus란-cf52c9a8785f)
- [제일 도움 많이 된 자료 - 호롤리](https://gruuuuu.github.io/cloud/monitoring-02/#)
- [호롤리를 참고해서 좀 더 자세했던 자료](https://tommypagy.tistory.com/187)
- [Helm 사용 설치](https://waspro.tistory.com/588)



