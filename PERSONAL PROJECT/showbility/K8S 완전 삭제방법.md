# K8S 완전 삭제방법

- k8s 설치된 모든 설정을 완전 삭제하는 방법



### 1. **kubectl 삭제**

#### `kubectl` 바이너리 삭제:

```bash
sudo rm -f $(which kubectl)
```

#### `kubectl` 설정 파일 삭제:

```bash
sudo rm -rf ~/.kube
```

### 2. **kubeadm 삭제**

#### `kubeadm` 바이너리 삭제:

```bash
sudo rm -f $(which kubeadm)
```

### 3. **kubelet 삭제**

#### `kubelet` 서비스 중지 및 비활성화:

```bash
sudo systemctl stop kubelet
sudo systemctl disable kubelet
```

#### `kubelet` 바이너리 삭제:

```bash
sudo rm -f $(which kubelet)
```

### 4. **추가적으로 관련 패키지 및 디렉토리 삭제**

Kubernetes 관련 패키지들은 대부분 `apt` 또는 `yum`을 통해 설치되었을 수 있습니다. 이에 따라 패키지 관리자를 사용해 삭제할 수도 있습니다.

#### **Ubuntu/Debian 계열:**

```bash
sudo apt-get purge kubeadm kubectl kubelet kubernetes-cni kube*
sudo apt-get autoremove
```

#### **CentOS/RHEL 계열:**

```bash
sudo yum remove kubeadm kubectl kubelet kubernetes-cni kube*
```

### 5. **Kubernetes 관련 디렉토리 삭제**

Kubernetes 관련 디렉토리들도 삭제하여 모든 설정 파일과 데이터 파일을 제거합니다.

```bash
sudo rm -rf /etc/kubernetes
sudo rm -rf /var/lib/etcd
sudo rm -rf /var/lib/kubelet
sudo rm -rf /etc/cni
sudo rm -rf /opt/cni
```

### 6. **Docker Container 및 Network 정리**

Kubernetes는 Docker나 다른 컨테이너 런타임을 사용할 수 있습니다. Docker 관련 설정도 정리하려면 다음 명령어를 실행하세요.

#### Docker 컨테이너 및 네트워크 정리:

```bash
sudo docker system prune -a
sudo docker network prune
```

### 7. **삭제 완료 후 확인**

모든 도구가 제대로 삭제되었는지 확인하려면 다음 명령어들을 실행해 `kubectl`, `kubeadm`, `kubelet`이 더 이상 존재하지 않는지 확인하세요:

```bash
kubectl version
kubeadm version
kubelet --version
```

모두 명령어가 인식되지 않으면 성공적으로 삭제된 것입니다.