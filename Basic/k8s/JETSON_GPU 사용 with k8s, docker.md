### 1. **추가로 설치해야 할 프로그램**

#### **마스터 노드**

- ~~**Kubernetes Server**: Master 노드에 Kubernetes 서버가 설치 및 설정되어야 합니다.~~
- ~~**kubectl**: Kubernetes 클라이언트를 통해 워커 노드와 클러스터를 관리.~~
- ~~**Docker (GPU 지원 불필요)**: 컨테이너 관리용으로 Docker만 설치 필요.~~

#### **워커 노드**

- NVIDIA GPU Device Plugin  **----> 설치되었는데 잘 안됨 처음부터 다시 설치**
  - [설치 가이드](https://github.com/NVIDIA/k8s-device-plugin)
- **NVIDIA Container Toolkit**: GPU 지원을 위해 이미 설치되어 있으므로 문제 없음.
- ~~**PyTorch**: 워커 노드 컨테이너 내부에 AI 작업용으로 설치.   **----> Cuda 11.4 에 맞게 설치, 로컬에도 필요한지 확인 필요**~~**도커 내부에서 사용하므로 설치 안하고 Docker 에서만 잘 설치해서 진행**

### 2. **버전 정보 일치**

- ~~**Kubernetes 버전**  **----> 동일한 버전 설치 필요 **~~**1.30.9 설치 완료**
  - ~~클러스터 내 **마스터 노드와 워커 노드의 Kubernetes 버전**이 호환되어야 합니다.~~
  - ~~현재 마스터 노드의 `kubectl`은 `v1.30.5`입니다. 워커 노드의 Kubernetes와 동일하거나 하위 호환 버전이어야 합니다.~~
- **CUDA, PyTorch**
  - ~~PyTorch는 CUDA 11.4를 지원하는 버전으로 설치해야 합니다. `PyTorch 1.12.x`가 CUDA 11.4와 호환됩니다.~~
  - ~~Docker 컨테이너 내부에서도 CUDA, PyTorch 버전이 일치하도록 해야 합니다.~~   **----> NVIDIA PyTorch 이미지 사용docker run --rm --gpus all -it nvcr.io/nvidia/pytorch:23.02-py3 **
- ~~**Docker**~~
  - ~~클러스터 내 노드들에서 Docker 버전은 서로 달라도 상관없지만, 최신 버전일수록 안정적입니다.~~
  - ~~Master: `27.3.1`, Worker: `24.0.5`는 호환 가능.   **----> 내부에서 pytorch, cuda 사용하는데 지장없는지 확인 필요 -- 괜찮**~~

### 3. **Docker 컨테이너로 실행 후 Pod 배포**

- **단계적으로 테스트 권장**:
  1. Docker 컨테이너를 먼저 워커 노드에서 실행해 GPU 작동 여부 확인.
     - `docker run --rm --gpus all nvidia/cuda:11.4-base nvidia-smi`
  2. Dockerfile을 기반으로 Pod을 구성하고 Kubernetes로 배포.
- **직접 Pod 배포도 가능**:
  - NVIDIA GPU Device Plugin 및 Toolkit 설정이 올바르면 Pod으로 바로 배포 가능.
  - Docker 이미지 생성 후 Kubernetes YAML 파일 작성.

### 4. **그 외 설정 및 실행**

- **마스터 노드의 클러스터 네트워크 구성**:

  - `kubeadm`을 통해 마스터 노드와 워커 노드 클러스터를 구성해야 합니다.
  - 네트워크 플러그인 설치 필요(Calico, Flannel 등).

- **워커 노드의 GPU 지원 확인**:

  - NVIDIA Container Runtime 및 GPU가 Pod 내에서 정상 동작하는지 `nvidia-smi`를 통해 확인.

- **Persistent Volume**:

  - 데이터를 저장해야 한다면 Kubernetes의 Persistent Volume 설정 필요.

- **리소스 요청 및 제한 설정**:

  - AI 모델이 GPU를 사용할 수 있도록 YAML 파일에 리소스 요청 설정:

    ```yaml
    resources:
      limits:
        nvidia.com/gpu: 1
    ```

- **헬름 차트 사용**:

  - Kubernetes 작업을 자동화하려면 Helm 차트를 사용해 Pod 배포.

필요한 설정 스크립트나 자세한 명령어가 필요하면 알려주세요!