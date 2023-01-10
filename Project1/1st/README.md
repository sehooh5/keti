# README

- 5G기반 선제적 위험대응을 위한 예측적 영상보안 핵심기술 개발 (1차년도)
- Kubernetes로 클러스터 관리, IP CCTV 스트리밍 제어앱 개발



## 사용 툴 버전

- ubuntu : 18.04
- python 3.7.6
- kubernetes : 1.14
- docker : 19.03.12 
- Prometheus  : 최신버전
- Grafana : 최신버전
- OpenCV : 
- VLC
- RTSP 카메라 사용
- Flask : 1.0.2



## Repository

#### manager

- 카메라 선택 제어하는 프로그램



#### viewer

- 카메라 실시간 스트리밍 앱



####  test

- 테스트 코드



## 프로그램 설치 프로세스

### 1. Docker

#### 준비

- 업데이트 apt update

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

  

#### 패키지 저장소 추가

- 도커의 공식 gpg 키와 저장소 추가

  ```bash
  # 공식 gpg 키 추가
  $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  # 공식 키 확인
  $ sudo apt-key fingerprint 0EBFCD88
  # 저장소 추가
  $ sudo add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
     bionic \
     stable"
  # docker 패키지 검색되는지 확인
  $ sudo apt-get update 
  $ sudo apt-cache search docker-ce
  ## 출력메시지
  docker-ce - Docker: the open-source application container engine
  ```

  

#### 도커 CE설치

```bash
$ sudo apt-get update 
$ sudo apt-get install docker-ce

# 사용자를 docker 그룹에 추가
$ sudo usermod -aG docker $USER
```



#### 반드시 스왑 메모리 비활성화

```
sudo swapoff -a
```



#### 도커 데몬 드라이버 교체

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
  ```

- 잘 안되서 슈퍼계정 들어간 상태에서 실행했음 `#`





---





### 2. Kubernetes

#### Kubernetes 설치

- Version : 1.14



#### 신뢰할 수 있는 APT 키 추가

```bash
$ sudo apt install apt-transport-https
$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```



#### Repository 추가 및 Kubernetes 설치

```bash
# Repository 추가
$ cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
$ sudo apt-get update
$ sudo apt-get install -y kubelet kubeadm kubectl
# 패키지가 자동으로 설치, 업그레이드, 제거되지 않도록 hold함.
$ sudo apt-mark hold kubelet kubeadm kubectl
# 설치 완료 확인
$ kubeadm version
$ kubelet --version
$ kubectl version
```



#### kube-router 설치를 위해

```
# sysctl net.bridge.bridge-nf-call-iptables=1
```





#### Master 노드 초기화

- root 계정 접속 :

  ```bash
  sudo passwd root 입력 후 패스워드 설정
  su 명령어로 root 계정 연결
  # 현 keti
  ```

- 초기화 시 사용할 Pod Network 에 따라 코드가 달라질 수 있다

- [Pod Network 사용 방법 및 초기화 코드 확인 페이지](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#pod-network)

- 해당 명령어를 실행하고 제대로 마스터노드가 셋업되면 아래와 같은 메시지를 출력한다

- **설치 시 사용한 애드온은 Flannel으로 "10.244.0.0/16" 네트워크 대역을 사용한다**

```bash
# Master 노드 생성 명령어
$ sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=192.168.100.5

# 셋업 성공 메시지
[init] Using Kubernetes version: v1.16.3
[preflight] Running pre-flight checks
	[WARNING IsDockerSystemdCheck]: detected "cgroupfs" as the Docker cgroup driver. The recommended driver is "systemd". Please follow the guide at <https://kubernetes.io/docs/setup/cri/>
	[WARNING SystemVerification]: this Docker version is not on the list of validated versions: 19.03.4. Latest validated version: 18.09
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
...
...
[bootstrap-token] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy
Your Kubernetes control-plane has initialized successfully!
To start using your cluster, you need to run the following as a regular user:
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  <https://kubernetes.io/docs/concepts/cluster-administration/addons/>
Then you can join any number of worker nodes by running the following on each as root:
kubeadm join 192.168.99.102:6443 --token fnbiji.5wob1hu12wdtnmyr \
    --discovery-token-ca-cert-hash sha256:701d4da5cbf67347595e0653b31a7f6625a130de72ad8881a108093afd06188b
```



#### **여기서 자꾸 에러가 떠서 진행이 안되엇다

- 도커와 kubernetes간 cgroup 이 일치하지 않아서 그럼, `systemd`로 변경했는데도 안되서 아래 내용을 추가해봤다
- 아래 명령어 실행하여 해당 내용 추가

```
- 10-kobeadm.conf 내용 변경
# vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf 

- 아래 내용 추가
Environment=”KUBELET_CGROUP_ARGS=–cgroup-driver=systemd”

```





#### kubectl 권한설정(*꼭 root 에서 나와서 설정해준다!)

- 다음 명령어 실행로 `kubectl`권한 설정

  ```bash
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
  ```

- `admin.conf` 파일은 `kubeadm init` 명령어 수행했을 때 생성

- 즉, Master 노드에서만 `kubectl` 명령어를 사용가능하며, 다른 노드에서 사용하고 싶을때는 admin.conf 파일을 복사해서 사용한다

- 

#### Pod 네트워크 구성 - Flannel

- Pod 이 서로 통신할 수 있도록 Network Add-on(여기선 Flannel)을 설치한다

```bash
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```



#### **설치 확인

- 아래 명령어로 잘 구성되었는지 확인한다

```bash
# 확인 명령어
kubectl get nodes
## 응답
NAME         STATUS     ROLES     AGE       VERSION
kubemaster   NotReady   master    4m        v1.18.6
```

- 아직 NotReady 상태이다
- 만약 이 때, <mark>에러메시지</mark>가 뜨면 아래처럼 해결해준다

```bash
## Error message. 1
Unable to connect to the server: x509: certificate signed by unkown authority~~

# 해결 방법
export KUBECONFIG=/etc/kubernetes/admin.conf


## Error message. 2 (자주 뜨는 에러!) 
<localhost:6443> was refuesed~~~~~~~~

# 해결 방법 : 그냥 기다리면 되거나 아래
sudo -i
swappoff -a
sudo vi /etc/fstab # 여기서 swapfile  관련된거 주석처리해주기!!(꼭)
strace -eopenat kubectl version
```

##### **Master Node 세팅 완료**



---



#### Worker Nodes 세팅

- Docker 설치 후 Master 와 동일한 방법으로 Kubernetes 설치 후 **Join**
- Worker Node 에서 아래 명령어 실행

```bash
# 이 명령어는 Master 세팅 시 맨 아래 출력됨
kubeadm join 192.168.100.5:6443 --token 813ucf.89bo9j9mfk6pm4vx \
    --discovery-token-ca-cert-hash sha256:7f1758ca4cfd117cda27099644cbe4ef672559a47ab33dce8dd87ddf2e8bea1c
```



#### **설치 실패 시 초기화 방법

```
- docker 초기화

$ docker rm -f `docker ps -aq`

$ docker volume rm `docker volume ls -q`
$ umount /var/lib/docker/volumes
# rm -rf /var/lib/docker/

# systemctl restart docker 


- k8s 초기화

# sudo kubeadm reset

$ systemctl restart kubelet



# iptables에 있는 데이터를 청소하기 위해

$ reboot 
```



---

#### Kubernetes 명령어 [(공식문서)](https://kubernetes.io/ko/docs/reference/kubectl/cheatsheet/)

- [참고](https://judo0179.tistory.com/66)

#### kuberctl 명령어

- 쿠버네티스는 `kubectl` 이라는 CLI 명령어를 통해서 쿠버네티스 및 클러스터 관리, 디버그 및 트러블 슈팅을 할 수 있다
- 기본적 명령어는 기본적으로 아래와 같다

```bash
$ kubectl [command] [type] [name] [flag]
```

- `command` : 자원에서 실행하려는 동작
  - `create` : 생성
  - `get` : 정보 가져오기
  - `describe` : 자세한 상태 정보
  - `delete` : 삭제
- `type` : 자원 타입
  - `pod` : Pod
  - `service` : 서비스(네트워크)
- `name` : 자원 이름
- `flag` : 옵션



#### kubectl 기본 사용법

- `run` : 특정 이미지를 가지고 pod을 생성

  ```bash
  $ kubectl run [Pod Name] --generator=[Repolication Controller 지정] --image=[사용할 이미지] --port=[포트 정보]
  ```

- pod의 서비스 생성

  ```bash
  $ kubectl expose pod echoserver --type=NodePort
  ```

- kubeconfig 환경 변수 확인

  ```bash
  $ kubectl config view
  ```

- 서비스 확인

  ```bash
  $ kubectl get svc
  ```

- deployment 확인

  ```bash
  $ kubect get deployment
  ```

- Nodes 확인 : `kubectl get nodes`

- pods 확인 : `kubectl get pods --all-namespaces`

- 구성요소 확인 : `kubectl get componentstatuses`

- Node 삭제 : 마스터에서 `kubectl delete node $NODENAME`

- config 확인(scheduler, c-manager 확인) : `kubeadm config print init-defaults`

- Node 세부사항 확인 : `kubectl --kubeconfig=$KUBE_CONFIG describe node $NODENAME (이것도 똑같은데..? kubectl describe node $NODENAME)`

- 토큰 리스트 보기 : `kubeadm token list`

- 토큰 생성하기 : `kubeadm token create`

- deployment(배포) 명령어로 배포 : `kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1`

- deployment 확인 : `kubectl get deployments`

- pod 확인 : `kubectl get pods -o wide`

- 워커노드에서 컨테이너 통신 시도 : `curl http://10.244.x.x:8080`





---





### 3. Prometheus 



#### yaml 파일 작성하여 설치

##### 제일 먼저 namespace 를 생성한다

```
$ kubectl create ns monitoring
```



#### yaml 파일 작성

- `vim` 명령어를 사용해 작성해 준다

#### Cluster Role 을 작성한다

- 프로메테우스 컨테이너가 k8s API 에 접근할 수 있는 권한을 주기위해 Cluster Role 을 설정해주고 ClusterRoleBinding 해준다
- 생성된 Cluster Role 은 monitoring namespace 의 기본 서비스 어카운트와 연동되어 권한을 부여한다

```yaml
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

```yaml
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

```yaml
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

```yaml
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

```yaml
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





#### yaml 파일 배포

```
kubectl apply -f prometheus-cluster-role.yaml
kubectl apply -f prometheus-config-map.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f prometheus-node-exporter.yaml
kubectl apply -f prometheus-svc.yaml

kubectl delete -f prometheus-cluster-role.yaml
kubectl delete -f prometheus-config-map.yaml
kubectl delete -f prometheus-deployment.yaml
kubectl delete -f prometheus-node-exporter.yaml
kubectl delete -f prometheus-svc.yaml
```



- 배포된 것 확인 : 

```
$ kubectl get pod -n monitoring

NAME                                     READY   STATUS    RESTARTS   AGE
node-exporter-99w2v                      1/1     Running   0          18s
node-exporter-f9q7f                      1/1     Running   0          18s
prometheus-deployment-7bcb5ff899-h4rb7   1/1     Running   0          65s
```





#### Browser 에서 Prometheus Web UI로 접근(확인만)

- [localhost]:30003 으로 접근 가능 (30003은 위 service.yaml에서 지정해주었음)
- Target 에서 kube-state-metrics (0/1)으로 아직 올라가지 않은 것을 볼 수 있는데 올려줘야 한다 (kube-state-metrics는 k8s클러스 내 오브젝트(pod..)에 대한 지표를 생성하는 서비스)



#### kube-state-metrics 배포 위한 yaml 작성

#### ClusterRole, ClusterRoleBinding

```yaml
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

```yaml
# kube-state-svcaccount.yaml

apiVersion: v1
kind: ServiceAccount
metadata:
  name: kube-state-metrics
  namespace: kube-system
```



#### cube-state-metrics의 deployment 구성

```yaml
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

```yaml
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
kubectl apply -f kube-state-cluster-role.yaml
kubectl apply -f kube-state-deployment.yaml
kubectl apply -f kube-state-svcaccount.yaml
kubectl apply -f kube-state-svc.yaml

kubectl delete -f kube-state-cluster-role.yaml
kubectl delete -f kube-state-deployment.yaml
kubectl delete -f kube-state-svcaccount.yaml
kubectl delete -f kube-state-svc.yaml

```



#### 확인

```
$ kubectl get pod -n kube-system

NAME                                       READY   STATUS    RESTARTS   AGE
...
kube-state-metrics-59bd4d9d-nbfrq          1/1     Running   0          50s
```

- 다시 Browser UI 를 확인하면 정상실행 되는것을 확인할 수 있다.





---





### 4. Grafana



#### yaml 파일 작성/배포하여 pod과 svc 생성

- 여기서 nodePort : 30004 중요!!

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      name: grafana
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - name: grafana
          containerPort: 3000
        env:
        - name: GF_SERVER_HTTP_PORT
          value: "3000"
        - name: GF_AUTH_BASIC_ENABLED
          value: "false"
        - name: GF_AUTH_ANONYMOUS_ENABLED
          value: "true"
        - name: GF_AUTH_ANONYMOUS_ORG_ROLE
          value: Admin
        - name: GF_SERVER_ROOT_URL
          value: /
---
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: monitoring
  annotations:
      prometheus.io/scrape: 'true'
      prometheus.io/port:   '3000'
spec:
  selector:
    app: grafana
  type: NodePort
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30004
```



- 작성 후 배포 및 pod 확인

```bash
$ kubectl apply -f grafana.yaml

$ kubectl get pod -n monitoring
NAME                                     READY   STATUS    RESTARTS   AGE
grafana-799c99855d-kxhkm                 1/1     Running   0          16s
node-exporter-99w2v                      1/1     Running   0          66m
node-exporter-f9q7f                      1/1     Running   0          66m
prometheus-deployment-7bcb5ff899-h4rb7   1/1     Running   0          67m
```



- `localhost:30004` 로 Grafana 접속 가능!



#### Grafana 작동

1. datasource 추가

   - Add data source 로 이동 
   - Prometheus 선택
   - 연동할 프로메테우스 정보 기입, url 은 서비스의 CLUSTER-IP + PORT 참고하여 적어주면 된다

   ```bash
   $ kubectl get svc -n monitoring
   
   NAME                 TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   grafana              NodePort   10.101.152.163   <none>        3000:30004/TCP   6m43s
   prometheus-service   NodePort   10.101.196.111   <none>        8080:30003/TCP   73m
   ```

   - 여기서는 10.101.196.111:8080
   - 여기서 `Save & Test` 버튼 눌렀을 때 "Data source is working" 메시지가 뜨면 됨

2. Dashboard 추가

   - Grafana Homepage -> Dashboard -> "kubernetes" 검색 후, 마음에드는 Dashboard 선택 하고  copy id 룰 눌러 대시보드의 id 복사
   - Garafana UI 로 돌아와서 `Import` 
   - 입력된 datasource 인 prometheus (이름은 본인이 저장한 것으로 나온다)를 넣어주면 완료





---







## App 및 배포과정

- manager 폴더는 viewer 앱을 제어하는 앱이 포함된 폴더이다
- viewer 폴더는 카메라를 사용하여 보여주는 앱이 포함된 폴더이다



### 순서

1. manager, viewer 폴더 다운로드 
2. 각 폴더의 도커이미지를 빌드 해준다(Dockerfile 로 배포)
3. manager 폴더에서 manager app 배포
4. viewer 폴더에서 cam1-1, cam1-2 배포







## 진행 단계(daily)

#### 0804

- 테스트베드 구축에 대한 탐구
  - 사용하는 프로그램, 툴에 대한 언어 공부 및 활용 방법 모색
  - Ubuntu 기반 **Kubernetes**를 사용하여 Master/Worker 서버에 대한 환경 구축(**Docker** 활용)
- 베어본 PC 사용하여 직접 설치해보기
- **설치 순서**: Ubuntu - Docker - Kubernetes
- **Rufus** 로 USB 에 부팅 가능한 ISO 파일 저장후 사용하게끔하기
- 완료 : keti0 컴퓨터에 Ubuntu 설치완료, 네트워크 static IPv4 설정 완료, 3개 컴퓨터 이더넷으로 연결 ( IPv4 : 192.168.100.5, 6, 7)



#### 0805

- 완료 : Docker*3 설치 완료



#### 0806

- 완료 : kubernetes 용어정리 및 설치 완료

  (쿠버네티스 잘 작동되는지 확인해야함) 



#### 0807

- 진행중 :  Kubernetes 설정



#### 0810

- 완료 : 3대 Kubernetes 설치 및 마스터(keti0), 워커 2대(keti1, keti2) 노드설정 완료
- 오류 : keti2 연결 안됨(Status : Not Ready), Scheduler & Kube-Controller-manager : Unhealthy 상태
- 완료 : 3대 설치 완료

- 오류 : 연동 되는데 not ready, unhealthy



#### 0811

- 완료 : master 1 / worker 1 설치 완료,  배포완료
- 오류 : unhealthy 여전히 뜨고 한 대는 join 안됨



#### 0812

- 진행중 : Prometheus 란? , Granfana?, 동적으로 사용가능한 리소스 찾기

- 오류 : 

  - 재부팅하면 `kubectl` 명령어 시 port를 못찾을 때가 있음 - 시간지나면 해결
  - 아직도 `kubectl get cs` : scheduler, c-m - unhealthy 상태

- 완료 : master-worker(2 pc) 연결 완료

- 앞으로 진행할 내용

  

  1. 동적으로 리소스를 확인할 수 잇는지?
  2. 프로메테우스, kubectl 이 찾을 수 있는 리소스 개수들

  

  결론 : 리소스 모니터링에 **프로메테우스 Granfana** 를 사용할 지 **k8s 내부 모듈**을 사용할지




#### 0813-14

- prometheus & grafana 설치 도중 오류 발생시켜 다시 복구중



#### 0818

- master cluster 포맷 후 ubuntu 부터 다시 설치
- master - w1,w2 에 대한 k8s 설치 및 연결 완료
- 진행중 : 프로메테우스 설치 후 image pull 안되는 에러 발생!
- **내일중으로 해결할 것!!**



#### 0819

- server, alertmanager - pending & exporter, pushgateway Imagepullbackoff 고치기!
- **프로메테우스 helm으로 설치완료**



#### 0820

- 그라파나 설치하기
  - 일단 prometheus yaml 파일들 수정 안하고 그라파나 먼저 설치 후 잘 돌아가는지 확인하고 진행
  - **helm 설치 지우고 yaml 파일 직접 작성하여 적용시켰음**



#### 0821

- 프로메테우스, 그라파나 설치 내용 정리하기
- 프로메테우스 및 그라파나 개념 정리
- 프로메테우스 및 그라파나에서 사용할 수 있는 데이터 정리해서 보고



#### 0824

- 내용 정리 : 
  - Grafana, Prometheus 에서 모니터링 가능한 내용 정리하기
- 문제 해결 : 
  - swapoff 모든 컴퓨터에서 다시 해주어야 돌아가는데 고정하는 방법?
  - ~~ImgPullOff 도 수동으로 해주었어야하는데 지금은 작동됨~~
  - 결론 : 껐다 켰을 때 자동으로 셋업되게 하는 방법



#### 0825

- k8s 의 마스터노드를 통해서 워커노드에게 명령 내릴수 잇도록

  (vlc rstp 명령)

- 진행해야할 순서

  1. Container 만드는데 OpenCV로 카메라 URL 열어서 받은 데이터가 있는지 없는지 
  2. Camera 에 대한 CRD 작성하기
  3. FLASK로 MJPEG/HTTP만들어서 전송해주기
  4. 서비스 오픈하게끔
  5. 웹서비스 구현



#### 0826

- python, vs code 설치 완료
- openCV 활용하여 비디오 끌어오기 완료 - python 예제 opencv1.py
- container 만들어보기



#### 0831

- git 연동완료
- Contatiner 만들고 OpenCV 사용하는거 연습



#### 0901

- Container 작성하는거 완성하기



#### 0907

- ~~네트워크 연결~~
  - **앞으로는 이더넷은 연결 끊고 와이파이만 사용하다가 필요시 이더넷 사용**
- ~~네트워크 복구 및 기존 했던것들 진행~~
  - 복구 완료
  - **docker hub** 통해서 image 배포까지 완료
- ~~도커 허브 사용해서 이미지를 워커노드에 배포하고 서비스까지 구성 완료~~
  - **localhost:31137 로 연결 가능**
- 이제 openCV 를 컨테이너에 담아서 배포하기



#### 0908

- openCV 컨테이너에 담아서 배포하기
  - 두개 rtsp 주소 받은거로 진행하면 됨!!



#### 0909 

- rtsp 주소 받은 거로 앞으로 개발 진행하면 됨
  - opencv  는 열리는 것 확인 됨



#### 0911

- opencv 컨테이너화 시키기
- 후 배포
- 오늘 오전은 nvidia 드라이버를 미니컴에 설치하는 바람에 재부팅이 안되서 시간을 다 사용했다. 처음에는 난생 처음 보는 에러에 컴퓨터가 켜지지를 않아서 이제까지 한 모든게 날라가나 싶었는데 세시간정도 붙잡고 서칭하면서 겨우 고쳤다. 오후는 opencv  를 도커라이징하는데 문서는 제대로 없고 잘 만들어놓은 Dockerfile 을 찾아서 이미지로 저장하고 실행시켜봤다. 완벽하게 실행되지는 않지만...잘되길..



#### 0914

- opencv 컨테이너화 시키기



#### 0915

- opencv 컨테이너 환경에서 출력 완료
- 다음 작업 시작



#### 0916

- 컨테이너 환경에서 opencv-python을 다시 다운받아야 실행 가능, 왜?
- Docker Images : 
  - opencv-docker1 : 처음으로 open 적용된
  - opencv-docker2 : 워크스페이스 추가
  - opencv-python3 : kubectl 배포중 CrashLoopBackOff 오류 발생 제거
  - opencv-python4 : 워크스페이스에서 열리지 않은것들 수정, 파일들 복사
  - opencv-python5 : CrashLoopBackOff 다시 발생, deployment 에 천천히 만드는 sleep 명령어 삽입



#### 0917

- 이제까지 과정 정리 후 pdf 변환
- 질문 정리



#### 0918

- docker image : sehooh5/opencv-python7 이 제대로된 이미지 = 작동 가능
  - opencv-python 을 재 컴파일한 것이 아닌 전부 받아서 했더니 됐다



#### 0919

- 외국인 개발자 코드를 가지고 실행시켜보기 - flask 는 설치 되었고 카메라 연동하면 됨



#### 0922

- Flask 를 활용하여 MPEG/HTTP Streaming 하는 파일 만들기
- 현재 미구엘 코드 사용중
  -  app.py, camera_opencv.py 사용
  -  rtsp주소를 수동으로 입력하여 웹페이지에 스트리밍되게 완료
     - 사이즈 조절
     - 여러개 동시에 스트리밍? 



#### 0923

- Miguel 코드로 카메라 이미지 가져오기 완료
  -  주소를 Terminal에 직접 입력해줘야한다..
- 앞으로 해야할 것?
  - 사이즈 조절
  - 여러개 동시에 스트리밍
  - 노드포트로 외부 연결하는 것?
- ing
  - ~~버튼 두개(C1, C2) 각 카메라 페이지로 연결시키기 (잘 되면 ajax 까지)~~
    - ~~한개 rtsp는 연결되었는데 두개를 어떻게 나누어서 연결할지 ...?~~
  - ~~Flask 사용법 / 웹 프로젝트 리뷰하면서 연결하는 방법 찾아보기~~
- done
  - 버튼 두개 만들기
  - 버튼으로 카메라 연결 완료
  - 버튼별로 카메라 연결 완료 - 파라미터 no 에따라 환경변수 및 템플릿을 바꿔서 전달



#### 0924

- NodePort 사용법
- curl 사용법 
- ing
  - 해당 앱을 도커라이징 하는중
    - 문제점 : 도커라이징 하면 기존 flask가 d사용하던 포트 5000 을 인식못한다...
  - 일단 배포 완료했으니 확인해보기 6000으로 노드포트(기존 5000 expose)



#### 0925

- NodePort 사용해서 streaming 앱 배포하기\
  - ~~배포해도 도커에서도 안열렸는데 포트를 5000:5000 으로 했더니 열린다!~~
    - 6000:5000 으로 설정했을 때는 localhost:6000으로 해야 열린다... 하지만 카메라 또한 url 을 localhost:6000을 줘야하는데 이 부분은 select.html 에 button 태그에 설정이 0.0.0.0:5000으로 되어있어서 실행되지 않는다...<mark>**어떻게 해야할까?**</mark>
      - 아마도 .. url 입력에 따라 button 설정 값에 들어가는 것도 바뀌어 설정되게끔....?
  - 일단 k8s 배포는 안되서 패쓰
- 그라파나 프로메테우스 잘 돌아가는지 확인(월요일 확인할것)



#### 0928

- 해결하기

  - 6000:5000 으로 설정했을 때는 localhost:6000으로 해야 열린다... 하지만 카메라 또한 url 을 localhost:6000을 줘야하는데 이 부분은 select.html 에 button 태그에 설정이 0.0.0.0:5000으로 되어있어서 실행되지 않는다...

    어떻게 해야할까?

    - 아마도 .. url 입력에 따라 button 설정 값에 들어가는 것도 바뀌어 설정되게끔....?

- 그라파나 30004(import 10000), 프로메테우스 30003  창 켜두기



#### 1005

- 추석 후 이미지 작업 진행
- 위에 내용은 내일부터 다시 해결하기



#### 1006

- 김책임님 출장
  - 07(수), 금책임님께 여쭤볼 것 정리하기
- 내가 한거 다시 정리해서 앞으로 진행 어떻게 할지 찾아보기 



#### 1007

- flask-video-streaming 쿠버네티스에 배포 완료
- 앞으로 방향 회의
  - 1번 REST API 사용 / 2번 CRD 사용
  - 일단 REST API 사용
  - 배포할 때는 ReplicaSet 말고 Demonset 혹은 노드별 Deploy



#### 1008

- ~~Demonset 혹은 노드별 Deploy 배포방법 공부~~
- ~~REST API 공부~~
- ~~공부는 약 1주일~~    
- 현재 새로운 폴더를 만들어서 manager / viewer 나누어서 실행 중
  - 배포 해봤는데 방법을 좀 다르게 해야함
  - ~~지금은 camera_opencv.py 에서 Camera class 를 다르게 지정하는 방법 하는중~~
  - 지금은 manager 에 url 값을 바로 카메라 주소 써서 보내는데 이것도 안될듯



#### 1012

- ~~POST 방법으로 form date 보내고 받는거로 해보기(url 이 변경되지 않음)~~
  - 로컬 환경에서는 제대로 작동하지만, 매니저 화면은 바뀌는 형태로만 됨
  - 우리가 마지막에 구현할 것은 매니저 화면 고정+워커노드의 화면만 바뀌어야함
- SSE 에 관한 내용 더 살펴보고 공부하기



#### 1013

- SSE 에 관한 내용 더 살펴보고 공부하기

- flask-socketio 로 진행했음
  - 지금 예제 구현은 완료 했고 앞으로 어떻게 할지 생각해보기



#### 1014

- ~~Flask-socketio 익숙해지기~~
- 현재는 WebSocket 으로 변경해서 진행하고있음
  - button 형식으로 눌러서, 서버에서  url 값을 os.environ 에 설정하는 방식으로 하는중
  - 현재 생각하는 방식은 client(1개)에서 값을 넘겨주는데, Streaming app 의 서버를 3개 열어주는형식



#### 1015

- Websocket  방법
  - 클라이언트에서 여러 port 로 넘길수 있는지?
- ~~[이 방법으로 구현하기 - flask socketio](https://learn.alwaysai.co/build-your-own-video-streaming-server-with-flask-socketio)~~
- 기존 test  폴더에 flask-socketio 로 다시 진행중 (main.py - session.html + manager.html, viewer.html)



#### 1019

- ~~기존 test  폴더에 flask-socketio 로 다시 진행중 (main.py - session.html + manager.html, viewer.html)~~
- ~~**현재**, LiveStream 폴더로 진행중~~
- 일단 socket 사용 중지!!,,,,,,,,
  1. 기존 방식으로 진행하되 stop 기능이 들어가서 **카메라 전환**이 잘 될 수 있도록!
  2. 카메라 스트리밍 크기 조절할 수 있도록 알아두기
  3. **UI 디자인** 깔끔하게



#### 1020

- 어떻게든 돌아가는 형태 완성 - <u>검사받기</u>
  - /manager - manager.html, app.py
  - /viewer -  cam1.html, cam2.html, cam1-1.py, cam1-2.py (+ camera_opencv.py, base_camera.py * 2개씩)
- 할 것
  1. 카메라 스트리밍 크기 조절할 수 있게
  2. UI 디자인 깔끔하게
- 완료
  - 매니저 UI - 1.1



#### 1021

- ~~마스터 서버 버튼 배열 가로로~~
- ~~워커 서버 버튼별로 테두리~~ **완료**
- ~~상태바, 주소창 가릴수 있는지?~~
  - 주소창 가리기는 아직 못찾음
  - 대신, 듀얼 모니터 가능
- ~~opencv 사이즈 조절하기~~ **완료**
- 우분투 동영상 캡쳐 가능한지 : Ctrl +Alt +Shift + r
- **쿠버네티스에 앱 배포하기!!**
  - 도커환경에서 실행되는 것 확인했음



#### 1022

- ~~k8s 에 배포 실패, 수정하기~~
  - **k8s 에 배포 완료!!** 
    - manager : 30000
    - viewer1 : 30021
    - viewer2 : 30022
- **Grafana - Prometheus** 작동 확인
  - Granfana : 30004
  - Prometheus : 30003



#### 1023

- 김책임님 가이드 주시면 개발 내용 정리하기!

=======

- 개발 내용 정리하기!



#### 1026

- 환경 설정 부분 내부 촬영하기



#### 1027

- 중간 점검까지 내용 정리
- k8s, 프로메테우스, 그라파나 우리 UI 다룰 수 있을 정도로 공부



#### 1028

- 오전만/ 프로메테우스 그라파나 공부



#### 1029

- 프로메테우스