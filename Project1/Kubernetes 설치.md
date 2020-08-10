# Kubernetes 설치

- Version : 1.14



### product_uuid 확인

```
sudo cat /sys/class/dmi/id/product_uuid
```



### 신뢰할 수 있는 APT 키 추가

```bash
$ sudo apt install apt-transport-https
$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```



### Repository 추가 및 Kubernetes 설치

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



### kube-router 설치를 위해

```
# sysctl net.bridge.bridge-nf-call-iptables=1
```





## Master 노드 초기화

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



### 여기서 자꾸 에러가 떠서 진행이 안되엇다

- 도커와 kubernetes간 cgroup 이 일치하지 않아서 그럼, `systemd`로 변경했는데도 안되서 아래 내용을 추가해봤다
- 아래 명령어 실행하여 해당 내용 추가

```
- 10-kobeadm.conf 내용 변경
# vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf 

- 아래 내용 추가
Environment=”KUBELET_CGROUP_ARGS=–cgroup-driver=systemd”

```





### kubectl 권한설정

- 다음 명령어 실행로 `kubectl`권한 설정

  ```bash
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
  ```

- `admin.conf` 파일은 `kubeadm init` 명령어 수행했을 때 생성

- 즉, Master 노드에서만 `kubectl` 명령어를 사용가능하며, 다른 노드에서 사용하고 싶을때는 admin.conf 파일을 복사해서 사용한다



### Pod 네트워크 구성

- Pod 이 서로 통신할 수 있도록 Network Add-on을 설치한다

```
# kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentaion/kube-flannel.yml
```



---

### 설치 실패 시 초기화 방법

```

# docker 초기화

$ docker rm -f `docker ps -aq`

$ docker volume rm `docker volume ls -q`
$ umount /var/lib/docker/volumes
$ rm -rf /var/lib/docker/

$ systemctl restart docker 


# k8s 초기화

$ kubeadm reset

$ systemctl restart kublet



# iptables에 있는 데이터를 청소하기 위해

$ reboot 
```

