# Kubernetes

## 목차

[TOC]

---

### [쿠버네티스 구성요소](https://kubernetes.io/ko/docs/concepts/overview/components/)

- 쿠버네티스 클러스터는 컴퓨터 집합인 **노드 컴포넌트**와 **컨트롤 플레인 컴포넌트**로 구성



### Kubernetes Object 

- <u>쿠버네티스는 상태를 관리하기 위한 대상</u>을 **오브젝트**로 정의

#### 1. Pod

- 쿠버네티스에서 배포할 수 있는 가장 작은 단위
- 한 개 이상의 컨테이너와 스토리지, 네트워크 속성을 갖는다
- Pod 에 속한 컨테이너는 스토리지와 네트워크를 공유하고 서로 localhost 로 접근 가능하다
- 컨테이너를 하나만 사용하는 경우도 반드시  Pod 으로 감싸서 관리

![image](https://user-images.githubusercontent.com/58541635/89391056-9e304b80-d742-11ea-960a-7ae2f72f6e13.png)



#### 2. ReplicaSet

- Pod 을 여러개(한개 이상) 복제하여 관리하는 오브젝트
- Pod을 생성하고 개수를 유지하려면 반드시 사용해야함
- 복제할 개수, 개수를 체크할 라벨 선택자, 생성할 Pod의 설정값(템플릿) 등을 갖고 있다
- 직접 사용보다는 Deployment 등 다른 오브젝트에 의해서 사용되는 경우가 많다

![image](https://user-images.githubusercontent.com/58541635/89391588-5d850200-d743-11ea-90c9-87e047edfc70.png)



#### 3. Service

- 네트워크와 관련된 오브젝트
- Pod을 외부 네트워크와 연결해주고 여러개의 Pod을 바라보는 내부 로드 밸런서를 생성할 때 사용
- 내부 DNS에 서비스 이름을 도메인으로 등록하기 때문에 서비스 디스커버리 역할도 함



#### 4. Volume

- 저장소와 관련된 오브젝트
- 호스트 디렉토리를 그대로 사용 or EBS 같은 스토리지를 동적으로 생성하여 사용 가능





### Object Spec - YAML 사용

- 오브젝트의 명세는 YAML로 정의한다
- 명세는 생성, 조회, 삭제로 관리할 수 있기 때문에 REST API 로 쉽게 노출 가능





### Kubernetes 배포방식

- 원하는 상태를 다양한 Object에 Label을 붙여 정의(YAML)하고 API 서버에 전달하는 방식

- “컨테이너를 2개 배포하고 80 포트로 오픈해줘”라는 간단한 작업을 위해 다음과 같은 구체적인 명령을 전달해야 합니다.

  > “컨테이너를 Pod으로 감싸고 type=app, app=web이라는 라벨을 달아줘. type=app, app=web이라는 라벨이 달린 Pod이 2개 있는지 체크하고 없으면 Deployment Spec에 정의된 템플릿을 참고해서 Pod을 생성해줘. 그리고 해당 라벨을 가진 Pod을 바라보는 가상의 서비스 IP를 만들고 외부의 80 포트를 방금 만든 서비스 IP랑 연결해줘.”





### Kubernetes Architecture

- 중앙(**Master**)에 API 서버와 상태 저장소를 두고 각 서버(Node)의 에이전트(**Kubelet**)와 통신하는 단순한 구조



#### Master - Node 구조

- 전체 클러스터를 관리하는 Master 와 컨테이너가 배포되는 Node 로 구성
- 모든 명령은 마스터의 API 서버를 호출하고, 노드는 마스터와 통신하면서 필요한 작업을 수행

![image](https://user-images.githubusercontent.com/58541635/89495620-a0061780-d7f3-11ea-9bb0-2adb1c0c1dd7.png)

##### Master

- 마스터 서버는 다양한 모듈이 확장성을 고려하여 기능별로 쪼개져있음
- 관리자만 접속할 수 있도록 보안 설정을 해야 함
- 마스터 서버가 죽으면 클러스터를 관리할 수 없어서 보통 3대를 구성하여 안정성을 높힘
- 개발환경이나 소규모 환경에선 마스터와 노드를 분리하지 않고 같은 서버에 구성
- **마스터의 구성요소 :**

![image](https://user-images.githubusercontent.com/58541635/89495810-0723cc00-d7f4-11ea-8a86-e18c97bc2a21.png)

###### kube-apiserver (API 서버)

- 모든 요청을 처리하는 마스터의 핵심모듈
- kubectl 의 요청뿐 아니라 내부모듈의 요청도 처리하며 권한을 체크하여 요청을 거부할 수 있다
- 원하는 상태를 key-value 저장소에 저장, 저장된 상태를 조회하는 일을 함
- Pod 을 노드에 할당하고 상태를 체크하는 일은 다른 모듈로 분리되어 있음
- 노드에서 실행 중인 컨테이너의 로그를 보여주고 명령을 보내는 등 (디버거 역할 또한 수행)



###### etcd (분산 데이터 저장소 )

- RAFT 알고리즘을 이용한 key-value 저장소
- 여러 개로 분산하여 복제할 수 있기 떄문에 안정성이 높고 속도도 빠른 편
- 클러스터의 모든 설정, 상태 데이터는 여기 저장, 나머지 모듈은 stateless하게 동작하여 etcd만 잘 백업해두면 언제든 클러스터 복구 가능
- 오직 API 서버와 통신하고 다른 모듈을 API 서버 거쳐서 etcd 데이터에 접근



###### Scheduler, Controller

- API 서버는 요청을 받으면 etcd 저장소와 통신할 뿐 실제로 상태를 바꾸는 건 Scheduler 와 Controller

1. kube-scheduler

   - 스케줄러는 할당되지 않은 Pod 을 여러가지 조건(필요한 자원, 라벨)에 따라 적절한 노드서버에 할당

2. kube-controller-manager

   - Kubernetes 내의 거의 모든 Object의 상태를 관리

   - Object별로 철저하게 분업화 : 

     Deployment 는 ReplicaSet을 생성 / ReplicaSet은 Pod 생성 / Pod 은 scheduler 가 관리

3. cloud-controller-manager

   - AWS, GCE, Azure등 클라우드에 특화된 모듈
   - Node 추가삭제와 로드 밸런서를 연결하거나 Volume 붙이기





##### Node

- 노드서버는 마스터 서버와 통신하면서 필요한 Pod을 생성하고 네트워크와 볼륨을 설정
- 실제 컨테이너들이 생성되는 곳으로 수백, 수천대로 확장할 수 있다.
- 각각의 서버에 라벨을 붙여 사용목적(GPU특화, SSD 서버 등)을 정의할 수 있다.



##### Kubectl

- API 서버는 json 또는 protobuf 형식을 이용한 http 통신을 지원
- 그대로 쓰면 불편하여 `kubectl`이라는 명령행 도구를 사용

### [표준 용어집](https://kubernetes.io/ko/docs/reference/glossary/?all=true#term-cluster-architect)

- **Add-ons**

  Resources that extend the functionality of Kubernetes.

- **API Group**

  A set of related paths in Kubernetes API.

- **API 서버**

  또 다른 명칭:*kube-apiserver*
  API 서버는 쿠버네티스 API를 노출하는 쿠버네티스 [컨트롤 플레인](https://kubernetes.io/ko/docs/reference/glossary/?all=true#term-control-plane) 컴포넌트이다. API 서버는 쿠버네티스 컨트롤 플레인의 프론트 엔드이다.

- **Application Architect**

  A person responsible for the high-level design of an application.

- **Application Developer**

  A person who writes an application that runs in a Kubernetes cluster.

- **Approver**

  A person who can review and approve Kubernetes code contributions.

- **cgroup**

  선택적으로 리소스를 격리, 관리, 제한하는 리눅스 프로세스의 그룹.

- **CIDR**

  CIDR (Classless Inter-Domain Routing) is a notation for describing blocks of IP addresses and is used heavily in various networking configurations.

- **CLA (컨트리뷰터 사용권 계약|Contributor License Agreement)**

  [컨트리뷰터](https://kubernetes.io/ko/docs/reference/glossary/?all=true#term-contributor)가 기여한 것에 대한 사용권을 오픈 소스 프로젝트에 허락하는 계약 조건.

- **Cloud Native Computing Foundation (CNCF)**

  The Cloud Native Computing Foundation (CNCF) builds sustainable ecosystems and fosters a community around [projects](https://www.cncf.io/projects/) that orchestrate containers as part of a microservices architecture.Kubernetes is a CNCF project.

- **Cluster Architect**

  A person who designs infrastructure that involves one or more Kubernetes clusters.

- **Cluster Infrastructure**

  The infrastructure layer provides and maintains VMs, networking, security groups and others. 

- **Cluster Operations**

  The work involved in managing a Kubernetes cluster: managing day-to-day operations, and co-ordinating upgrades.

- **Cluster Operator**

  A person who configures, controls, and monitors clusters.

- **Code Contributor**

  A person who develops and contributes code to the Kubernetes open source codebase.

- **Container Lifecycle Hooks**

  The lifecycle hooks expose events in the [Container](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/#why-containers) management lifecycle and let the user run code when the events occur.

- **Container Storage Interface (CSI)**

  The Container Storage Interface (CSI) defines a standard interface to expose storage systems to containers.

- **containerd**

  A container runtime with an emphasis on simplicity, robustness and portability

- **CRI-O**

  A tool that lets you use OCI container runtimes with Kubernetes CRI.

- **Developer (disambiguation)**

  May refer to: [Application Developer](https://kubernetes.io/docs/reference/glossary/?all=true#term-application-developer), [Code Contributor](https://kubernetes.io/docs/community/devel/), or [Platform Developer](https://kubernetes.io/docs/reference/glossary/?all=true#term-platform-developer).

- **Disruption**

  Disruptions are events that lead to one or more [Pods](https://kubernetes.io/docs/concepts/workloads/pods/) going out of service. A disruption has consequences for workload resources, such as [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), that rely on the affected Pods.

- **Downstream (disambiguation)**

  May refer to: code in the Kubernetes ecosystem that depends upon the core Kubernetes codebase or a forked repo.

- **Dynamic Volume Provisioning**

  Allows users to request automatic creation of storage [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/).

- **Endpoints**

  Endpoints track the IP addresses of Pods with matching [selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/).

- **EndpointSlice**

  A way to group network endpoints together with Kubernetes resources.

- **Ephemeral Container**

  A [Container](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/#why-containers) type that you can temporarily run inside a [Pod](https://kubernetes.io/docs/concepts/workloads/pods/).

- **etcd**

  모든 클러스터 데이터를 담는 쿠버네티스 뒷단의 저장소로 사용되는 일관성·고가용성 키-값 저장소.

- **FlexVolume**

  FlexVolume is an interface for creating out-of-tree volume plugins. The [Container Storage Interface](https://kubernetes.io/docs/concepts/storage/volumes/#csi) is a newer interface which addresses several problems with FlexVolumes.

- **Helm Chart**

  A package of pre-configured Kubernetes resources that can be managed with the Helm tool.

- **Horizontal Pod Autoscaler**

  또 다른 명칭:*HPA*
  An API resource that automatically scales the number of [Pod](https://kubernetes.io/docs/concepts/workloads/pods/) replicas based on targeted CPU utilization or custom metric targets.

- **HostAliases**

  A HostAliases is a mapping between the IP address and hostname to be injected into a [Pod](https://kubernetes.io/docs/concepts/workloads/pods/)'s hosts file.

- **Istio**

  마이크로서비스의 통합을 위한 통일된 방법을 제공하는 오픈 플랫폼(쿠버네티스에 특정적이지 않음)이며, 트래픽 흐름을 관리하고, 정책을 시행하고, 텔레메트리 데이터를 모은다.

- **Kops**

  A CLI tool that helps you create, destroy, upgrade and maintain production-grade, highly available, Kubernetes clusters.

- **kube-controller-manager**

  [컨트롤러](https://kubernetes.io/ko/docs/concepts/architecture/controller/)를 구동하는 마스터 상의 컴포넌트.

- **kube-proxy**

  kube-proxy는 클러스터의 각 [노드](https://kubernetes.io/ko/docs/concepts/architecture/nodes/)에서 실행되는 네트워크 프록시로, 쿠버네티스의 [서비스](https://kubernetes.io/docs/concepts/services-networking/service/) 개념의 구현부이다.

- **kube-scheduler**

  [노드](https://kubernetes.io/ko/docs/concepts/architecture/nodes/)가 배정되지 않은 새로 생성된 [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/) 를 감지하고, 실행할 노드를 선택하는 컨트롤 플레인 컴포넌트.

- **Kubeadm**

  A tool for quickly installing Kubernetes and setting up a secure cluster.

- **Kubectl**

  [쿠버네티스 API](https://kubernetes.io/ko/docs/concepts/overview/kubernetes-api/) 서버와 통신하기 위한 커맨드라인 툴.

- **Kubelet**

  클러스터의 각 [노드](https://kubernetes.io/ko/docs/concepts/architecture/nodes/)에서 실행되는 에이전트. Kubelet은 [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/)에서 [컨테이너](https://kubernetes.io/ko/docs/concepts/overview/what-is-kubernetes/#왜-컨테이너인가)가 확실하게 동작하도록 관리한다.

- **Manifest**

  Specification of a Kubernetes API object in JSON or YAML format.

- **Master**

  Legacy term, used as synonym for [nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) hosting the [control plane](https://kubernetes.io/docs/reference/glossary/?all=true#term-control-plane).

- **Member**

  A continuously active [contributor](https://kubernetes.io/docs/reference/glossary/?all=true#term-contributor) in the K8s community.

- **Minikube**

  로컬에서 쿠버네티스를 실행하기 위한 도구.

- **Operator pattern**

  The [operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) is a system design that links a [Controller](https://kubernetes.io/docs/concepts/architecture/controller/) to one or more custom resources.

- **Persistent Volume**

  An API object that represents a piece of storage in the cluster. Available as a general, pluggable resource that persists beyond the lifecycle of any individual [Pod](https://kubernetes.io/docs/concepts/workloads/pods/).

- **Persistent Volume Claim**

  Claims storage resources defined in a [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) so that it can be mounted as a volume in a [container](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/#why-containers).

- **Platform Developer**

  A person who customizes the Kubernetes platform to fit the needs of their project.

- **Pod Disruption Budget**

  또 다른 명칭:*PDB*
  A Pod Disruption Budget allows an application owner to create an object for a replicated application, that ensures a certain number or percentage of Pods with an assigned label will not be voluntarily evicted at any point in time. PDBs cannot prevent an involuntary disruption, but will count against the budget. 

- **Pod Priority**

  Pod Priority indicates the importance of a [Pod](https://kubernetes.io/docs/concepts/workloads/pods/) relative to other Pods.

- **PodPreset**

  An API object that injects information such as secrets, volume mounts, and environment variables into [Pods](https://kubernetes.io/docs/concepts/workloads/pods/) at creation time.

- **Preemption**

  Preemption logic in Kubernetes helps a pending [Pod](https://kubernetes.io/docs/concepts/workloads/pods/) to find a suitable [Node](https://kubernetes.io/docs/concepts/architecture/nodes/) by evicting low priority Pods existing on that Node.

- **Proxy**

  In computing, a proxy is a server that acts as an intermediary for a remote service.

- **QoS 클래스(QoS Class)**

  QoS 클래스(서비스 품질 클래스)는 쿠버네티스가 클러스터 안의 파드들을 여러 클래스로 구분하고, 스케줄링과 축출(eviction)에 대한 결정을 내리는 방법을 제공한다.

- **Quantity**

  A whole-number representation of small or large numbers using SI suffixes.

- **RBAC(역할 기반 엑세스 제어)**

  인가 결정을 관리하며, 운영자가 [쿠버네티스 API](https://kubernetes.io/ko/docs/concepts/overview/kubernetes-api/)를 통해서 동적으로 엑세스 정책을 설정하게 해준다.

- **Reviewer**

  A person who reviews code for quality and correctness on some part of the project.

- **rkt**

  A security-minded, standards-based container engine.

- **Secret**

  Stores sensitive information, such as passwords, OAuth tokens, and ssh keys.

- **Security Context**

  The `securityContext` field defines privilege and access control settings for a [Pod](https://kubernetes.io/docs/concepts/workloads/pods/) or [container](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/#why-containers).

- **Service Broker**

  An endpoint for a set of [Managed Services](https://kubernetes.io/docs/reference/glossary/?all=true#term-managed-service) offered and maintained by a third-party.

- **shuffle sharding**

  A technique for assigning requests to queues that provides better isolation than hashing modulo the number of queues.

- **SIG (special interest group)**

  [Community members](https://kubernetes.io/docs/reference/glossary/?all=true#term-member) who collectively manage an ongoing piece or aspect of the larger Kubernetes open source project.

- **Storage Class**

  A StorageClass provides a way for administrators to describe different available storage types.

- **sysctl**

  `sysctl` is a semi-standardized interface for reading or changing the attributes of the running Unix kernel.

- **UID**

  오브젝트를 중복 없이 식별하기 위해 쿠버네티스 시스템이 생성하는 문자열.

- **Upstream (disambiguation)**

  May refer to: core Kubernetes or the source repo from which a repo was forked.

- **Volume Plugin**

  A Volume Plugin enables integration of storage within a [Pod](https://kubernetes.io/docs/concepts/workloads/pods/).

- **WG (working group)**

  Facilitates the discussion and/or implementation of a short-lived, narrow, or decoupled project for a committee, [SIG](https://github.com/kubernetes/community/blob/master/sig-list.md#master-sig-list), or cross-SIG effort.

- **네임스페이스(Namespace)**

  쿠버네티스에서 동일한 물리 [클러스터](https://kubernetes.io/ko/docs/reference/glossary/?all=true#term-cluster)에서 다중의 가상 클러스터를 지원하기 위해 사용하는 추상화.

- **네트워크 폴리시(Network Policy)**

  파드 그룹들이 서로에 대한 그리고 다른 네트워크 엔드포인트에 대한 통신이 어떻게 허용되는지에 대한 명세이다.

- **노드(Node)**

  노드는 쿠버네티스의 작업 장비(worker machine)이다.

- **데몬셋(DaemonSet)**

  [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/) 복제본을 [클러스터](https://kubernetes.io/ko/docs/reference/glossary/?all=true#term-cluster) 노드 집합에서 동작하게 한다.

- **데이터 플레인(Data Plane)**

  컨테이너가 실행되고 네트워크에 연결될 수 있게 CPU, 메모리, 네트워크, 스토리지와 같은 능력을 제공하는 레이어. 

- **도커(Docker)**

  도커(구체적으로, 도커 엔진)는 운영 시스템 수준의 가상화를 제공하는 소프트웨어 기술이며, [containers](https://kubernetes.io/ko/docs/concepts/overview/what-is-kubernetes/#왜-컨테이너인가) 로도 알려져 있다.

- **디플로이먼트(Deployment)**

  일반적으로 로컬 상태가 없는 파드를 실행하여 복제된 애플리케이션을 관리하는 API 오브젝트.

- **레이블(Label)**

  사용자에게 의미 있고 관련성 높은 특징으로 식별할 수 있도록 오브젝트에 태그를 붙인다.

- **레플리카셋(ReplicaSet)**

  레플리카셋은 (목표로) 주어진 시간에 실행되는 레플리카 파드 셋을 유지 관리 한다.

- **레플리케이션 컨트롤러(ReplicationController)**

  특정한 수의 [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/) 인스턴스가 실행 중인지 확인하면서 복제된 애플리케이션을 관리하는 워크로드 리소스이다.

- **로깅(Logging)**

  로그는 [클러스터](https://kubernetes.io/ko/docs/reference/glossary/?all=true#term-cluster)나 애플리케이션에 의해 로깅된 이벤트의 목록이다.

- **리소스 쿼터(Resource Quotas)**

  [네임스페이스](https://kubernetes.io/ko/docs/concepts/overview/working-with-objects/namespaces)당 전체 리소스 소비를 제한하는 제약을 제공한다.

- **매니지드 서비스**

  타사 공급자가 유지보수하는 소프트웨어.

- **미러 파드(Mirror Pod)**

  Kubelet이 [스태틱 파드](https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/)를 표현하는 [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/) 객체

- **범위 제한(LimitRange)**

  네임스페이스 내에 [컨테이너](https://kubernetes.io/ko/docs/concepts/overview/what-is-kubernetes/#왜-컨테이너인가)나 [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/)당 리소스 소비를 한정하는 제약 조건을 제공한다.

- **볼륨(Volume)**

  데이터를 포함하고 있는 디렉터리이며, [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/)의 [컨테이너](https://kubernetes.io/ko/docs/concepts/overview/what-is-kubernetes/#왜-컨테이너인가)에서 접근 가능하다.

- **서비스 카탈로그(Service Catalog)**

  쿠버네티스 클러스터 내에서 실행되는 응용 프로그램이 클라우드 공급자가 제공하는 데이터 저장소 서비스와 같은 외부 관리 소프트웨어 제품을 쉽게 사용할 수 있도록하는 확장 API이다.

- **서비스(Service)**

  [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/) 집합에서 실행중인 애플리케이션을 네트워크 서비스로 노출하는 추상화 방법

- **서비스어카운트(ServiceAccount)**

  [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/)에서 실행 중인 프로세스를 위한 신원(identity)을 제공한다.

- **셀렉터(Selector)**

  사용자가 [레이블](https://kubernetes.io/ko/docs/concepts/overview/working-with-objects/labels)에 따라서 리소스 리스트를 필터할 수 있게 한다.

- **스태틱 파드(Static Pod)**

  특정 노드의 Kubelet 데몬이 직접 관리하는 [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/)로,

- **스테이트풀셋(StatefulSet)**

  [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/) 집합의 디플로이먼트와 스케일링을 관리하며, 파드들의 *순서 및 고유성을 보장한다* .

- **애그리게이션 레이어(Aggregation Layer)**

  애그리게이션 레이어를 이용하면 사용자가 추가로 쿠버네티스 형식의 API를 클러스터에 설치할 수 있다.

- **애플리케이션(Applications)**

  컨테이너화된 다양한 애플리케이션들이 실행되는 레이어. 

- **앱 컨테이너(App Container)**

  애플리케이션 컨테이너(또는 앱 컨테이너)는 [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/) 내의 모든 [초기화 컨테이너](https://kubernetes.io/ko/docs/reference/glossary/?all=true#term-init-container)가 완료된 후 시작되는 [컨테이너](https://kubernetes.io/ko/docs/concepts/overview/what-is-kubernetes/#왜-컨테이너인가)이다.

- **어노테이션(Annotation)**

  임의의 식별되지 않는 메타데이터를 오브젝트에 첨부할 때 이용하는 키-밸류 쌍.

- **어드미션 컨트롤러(Admission Controller)**

  쿠버네티스 API 서버에서 요청을 처리하여 오브젝트가 지속되기 전에 그 요청을 가로채는 코드 조각.

- **워크로드(Workloads)**

  워크로드는 쿠버네티스에서 구동되는 애플리케이션이다.

- **이름(Name)**

  `/api/v1/pods/some-name`과 같이, 리소스 URL에서 오브젝트를 가리키는 클라이언트 제공 문자열.

- **이미지(Image)**

  [컨테이너](https://kubernetes.io/ko/docs/concepts/overview/what-is-kubernetes/#왜-컨테이너인가)의 저장된 인스턴스이며, 애플리케이션 구동에 필요한 소프트웨어 집합을 가지고 있다.

- **익스텐션(Extensions)**

  익스텐션은 새로운 타입의 하드웨어를 지원하기 위해 쿠버네티스를 확장하고 깊게 통합시키는 소프트웨어 컴포넌트이다.

- **인그레스(Ingress)**

  클러스터 내의 서비스에 대한 외부 접근을 관리하는 API 오브젝트이며, 일반적으로 HTTP를 관리함.

- **인증서(Certificate)**

  암호화된 안전한 파일로 쿠버네티스 클러스터 접근 검증에 사용한다.

- **잡(Job)**

  완료를 목표로 실행되는 유한 또는 배치 작업.

- **장치 플러그인(Device Plugin)**

  장치 플러그인은 워커
  [노드](https://kubernetes.io/ko/docs/concepts/architecture/nodes/)에서 실행되며, 공급자별 초기화 또는 설정 단계가 필요한 로컬 하드웨어와 같은 리소스에 접근할 수 있는 [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/).

- **초기화 컨테이너(Init Container)**

  앱 컨테이너가 동작하기 전에 완료되기 위해 실행되는 하나 이상의 초기화 [컨테이너](https://kubernetes.io/ko/docs/concepts/overview/what-is-kubernetes/#왜-컨테이너인가).

- **커스텀 리소스 데피니션(CustomResourceDefinition)**

  사용자 정의 서버를 완전히 새로 구축할 필요가 없도록 쿠버네티스 API 서버에 추가할 리소스를 정의하는 사용자 정의 코드.

- **컨테이너 네트워크 인터페이스(Container network interface, CNI)**

  컨테이너 네트워크 인터페이스(CNI) 플러그인은 appc/CNI 스팩을 따르는 네트워크 플러그인의 일종이다.

- **컨테이너 런타임**

  컨테이너 런타임은 컨테이너 실행을 담당하는 소프트웨어이다.

- **컨테이너 런타임 인터페이스(Container runtime interface, CRI)**

  컨테이너 런타임 인터페이스(CRI)는 노드의 Kubelet과 컨테이너 런타임을 통합시키기 위한 API이다.

- **컨테이너 환경 변수(Container Environment Variables)**

  컨테이너 환경 변수는 [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/)에서 동작 중인 컨테이너에 유용한 정보를 제공하기 위한 이름=값 쌍이다.

- **컨테이너(Container)**

  소프트웨어와 그것에 종속된 모든 것을 포함한 가볍고 휴대성이 높은 실행 가능 이미지.

- **컨트롤 플레인(Control Plane)**

  컨테이너의 라이프사이클을 정의, 배포, 관리하기 위한 API와 인터페이스들을 노출하는 컨테이너 오케스트레이션 레이어.

- **컨트롤러(Controller)**

  쿠버네티스에서 컨트롤러는 [클러스터](https://kubernetes.io/ko/docs/reference/glossary/?all=true#term-cluster) 의 상태를 관찰 한 다음, 필요한 경우에 생성 또는 변경을 요청하는 컨트롤 루프이다. 각 컨트롤러는 현재 클러스터 상태를 의도한 상태에 가깝게 이동한다.

- **컨트리뷰터(Contributor)**

  쿠버네티스 프로젝트 또는 커뮤니티를 돕기 위해 코드, 문서 또는 시간을 기부하는 사람.

- **컨피그맵(ConfigMap)**

  키-값 쌍으로 기밀이 아닌 데이터를 저장하는 데 사용하는 API 오브젝트이다. [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/)는 [볼륨](https://kubernetes.io/ko/docs/concepts/storage/volumes/)에서 환경 변수, 커맨드-라인 인수 또는 구성 파일로 컨피그맵을 사용할 수 있다.

- **쿠버네티스 API(Kubernetes API)**

  RESTful 인터페이스를 통해서 쿠버네티스 기능을 제공하고 클러스터의 상태를 저장하는 애플리케이션.

- **크론잡(CronJob)**

  주기적인 일정에 따라 실행되는 [잡](https://kubernetes.io/ko/docs/concepts/workloads/controllers/job/)을 관리.

- **클라우드 공급자**

  또 다른 명칭:*Cloud Service Provide*
  클라우드 컴퓨팅 플랫폼을 제공하는 사업자 또는 다른 조직

- **클라우드 컨트롤 매니저**

  클라우드별 컨트롤 로직을 포함하는 쿠버네티스 [컨트롤 플레인](https://kubernetes.io/ko/docs/reference/glossary/?all=true#term-control-plane) 컴포넌트이다. 클라우트 컨트롤러 매니저를 통해 클러스터를 클라우드 공급자의 API에 연결하고, 해당 클라우드 플랫폼과 상호 작용하는 컴포넌트와 클러스터와 상호 작용하는 컴포넌트를 분리할 수 있다.

- **클러스터(Cluster)**

  컨테이너화된 애플리케이션을 실행하는 [노드](https://kubernetes.io/ko/docs/concepts/architecture/nodes/)라고 하는 워커 머신의 집합. 모든 클러스터는 최소 한 개의 워커 노드를 가진다.

- **테인트(Taint)**

  세 가지 필수 속성: 키(key), 값(value), 효과(effect)로 구성된 코어 오브젝트. 테인트는 [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/)가 [노드](https://kubernetes.io/ko/docs/concepts/architecture/nodes/)나 노드 그룹에 스케줄링되는 것을 방지한다.

- **톨러레이션(Toleration)**

  세 가지 필수 속성: 키(key), 값(value), 효과(effect)로 구성된 코어 오브젝트. 톨러레이션은 매칭되는 [테인트(taints)](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)를 가진 노드나 노드 그룹에 파드가 스케줄링되는 것을 활성화한다.

- **파드 라이프사이클(Pod Lifecycle)**

  파드가 수명(lifetime) 동안 통과하는 상태의 순서이다.

- **파드 시큐리티 폴리시(Pod Security Policy)**

  [파드](https://kubernetes.io/ko/docs/concepts/workloads/pods/pod-overview/) 생성과 업데이트에 대한 세밀한 인가를 활성화한다.

- **파드(Pod)**

  가장 작고 단순한 쿠버네티스 오브젝트. 파드는 사용자 클러스터에서 동작하는 [컨테이너](https://kubernetes.io/ko/docs/concepts/overview/what-is-kubernetes/#왜-컨테이너인가)의 집합을 나타낸다.