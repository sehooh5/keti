# Docker,k8s with GPU

- Docker, Kubernetes에서 torch 등 GPU를 사용할때 참고
- 실제로 컨테이너가 작동하는 Worker 노드(k8s환경)에만 설치하면 됨
- 이 설명에서는 Jetson 플랫폼 사용을 기초로함



### 확인

- **JetPack SDK 설치 확인**: Jetson Orin에 **JetPack SDK**가 설치되어 있어야 GPU, CUDA, cuDNN 등의 드라이버와 라이브러리가 올바르게 설정됩니다. NVIDIA Jetson SDK Manager를 사용해 JetPack SDK를 설치했는지 확인하세요.
- **ARM64 호환 이미지 사용**: Jetson Orin은 ARM64 아키텍처 기반이므로, Docker 컨테이너 이미지를 선택할 때 ARM64와 호환되는 이미지를 사용해야 합니다.





### 설치방법

- GPU 사용하는 모든 워커노드에서 `NVIDIA Container Toolkit` 설치

```cmd
# Jetson 설치방법
$ sudo curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
$ sudo curl -s -L https://nvidia.github.io/libnvidia-container/jetson/$(. /etc/nv_tegra_release; echo $JETSON_ARCH)/nvidia-l4t-apt-source.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install the toolkit
$ sudo apt-get update
$ sudo apt-get install -y nvidia-container-toolkit

# Restart Docker
$ sudo systemctl restart docker

# Version check
$ nvidia-container-toolkit --version
```





```powershell
# 공식문서
# 저장소 구성
$ curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

$ sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list    
    
# Install the toolkit
$ sudo apt-get update
$ sudo apt-get install -y nvidia-container-toolkit

# Restart Docker
$ sudo systemctl restart docker

# Version check
$ nvidia-container-toolkit --version

# 이거때매 다 지워졌음 /etc/containerd/config.toml 확인해봐야함
sudo nvidia-ctk runtime configure --runtime=containerd 

sudo systemctl restart containerd
```



- 클러스터전체에 한번만 마스터노드에서 `NVIDIA Device Plugin` 설치

```cmd
# kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.11.0/nvidia-device-plugin.yml

# 공식문서로 재설치함
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.16.2/deployments/static/nvidia-device-plugin.yml
```

