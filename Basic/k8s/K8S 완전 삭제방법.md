# K8S 완전 삭제방법

- k8s 설치된 모든 설정을 완전 삭제하는 방법



### 1. **`kubeadm reset` 실행**

Kubernetes 클러스터를 초기화하고 관련 설정을 제거하려면 `kubeadm reset` 명령을 실행하세요.

```bash
sudo kubeadm reset
```

이 명령은 Kubernetes가 생성한 리소스, 인증서, API 서버 설정 등을 삭제합니다. 삭제 후에는 아래 메시지가 표시될 수 있습니다:

```
[reset] WARNING: changes made to this host by 'kubeadm init' or 'kubeadm join' will be reverted.
```

### 2. **CNI (네트워크 플러그인) 삭제**

플래널(Flannel) 또는 칼리코(Calico)와 같은 CNI 플러그인 파일을 삭제해야 합니다.

```bash
sudo rm -rf /etc/cni/net.d
sudo rm -rf /var/lib/cni/
sudo rm -rf /var/run/flannel
```

### 3. **Kubelet, Kubeadm 및 kubectl 삭제**

Kubernetes 패키지를 제거하려면 다음 명령어를 실행하세요.

**Ubuntu/Debian:**

```bash
sudo apt-get purge kubeadm kubectl kubelet kubernetes-cni kube*
```

**CentOS/RHEL:**

```bash
sudo yum remove kubeadm kubectl kubelet kubernetes-cni kube*
```

그런 다음 패키지 캐시를 정리합니다:

```bash
sudo apt-get autoremove
sudo apt-get autoclean
```

### 4. **Docker 및 컨테이너 런타임 정리**

컨테이너 런타임(Docker, containerd 등)이 Kubernetes와 함께 사용되었다면, 관련 파일과 컨테이너들을 삭제해야 합니다.

**모든 컨테이너 중지 및 삭제:**

```bash
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
```

**모든 Docker 이미지 삭제:**

```bash
sudo docker rmi $(sudo docker images -q)
```

**containerd 데이터 삭제:**

```bash
sudo rm -rf /var/lib/containerd/
```

### 5. **kubelet 서비스 및 설정 삭제**

kubelet 관련 설정 및 시스템 서비스를 삭제합니다:

```bash
sudo systemctl stop kubelet
sudo systemctl disable kubelet
sudo rm -rf /etc/systemd/system/kubelet.service.d
sudo rm -rf /etc/systemd/system/kubelet.service
sudo rm -rf /usr/bin/kubelet
sudo rm -rf /var/lib/kubelet
```

### 6. **Kubernetes 설정 파일 삭제**

Kubernetes가 사용하는 설정 파일 및 디렉토리를 삭제하세요:

```bash
sudo rm -rf ~/.kube
sudo rm -rf /etc/kubernetes
sudo rm -rf /var/lib/etcd
```

### 7. **IPTables 규칙 삭제**

Kubernetes 네트워크 설정이 남아있을 수 있으므로, `iptables` 규칙을 초기화합니다:

```bash
sudo iptables -F
sudo iptables -t nat -F
sudo iptables -t mangle -F
sudo iptables -X
```

### 8. **재부팅**

모든 설정 및 패키지가 정상적으로 삭제된 후, 시스템을 재부팅하는 것이 좋습니다:

```bash
sudo reboot
```

이 과정을 통해 Kubernetes 클러스터가 완전히 제거됩니다.