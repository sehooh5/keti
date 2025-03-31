# KETI

- KETI 에서 활용했던 자료



## 목차

## Basic

- 기본 IT 용어 및 활용 기술에 대한 기본 Document 적 자료
- 쿠버네티스, PyQt5 등 리서치 자료



## Project1

- kubernetes 활용
  - Docker
  - Prometheus, Grafana
- CCTV 제어
  - REST API 활용
  - opencv활용해 카메라 연동
- rtsp relay server
- k8s 클러스터 구성 및 SW 배포를 위한 API 구성



## Project1-1

- Dockerfile, Deployment 작성 및 배포 기능 웹앱



## Project2

- Python-C++ 간 Socket 통신
- Kinect sdk 영상과 string data을 python(server) 에서 C++(client)로 전송
- **개발환경**
  - Python : 3.6.10
  - Cuda : 10.0
  - Cudnn : 10.0
  - Pytorch : 1.2.0
  - Anaconda : 4.9.1



## Project3

- AI 학습용 데이터 품질검증(자율주행 분야)
- 사람, 자동차, 자전거 이미지 데이터를 보고 인식하는 학습 
- 테스트 내용은 완성된 것을 사용하고 테스트 환경을 구축하는데 주력함
  - Ubuntu 20.04.2 LTS
  - 개발언어 : Python 
  - 프레임워크 : Pytorch



## Project4 

- **동시 지능 연계 시스템**     
  - CCTV 를 실시간 영상 스트리밍 데이터를 활용해, 3개의 Edge 컴퓨터로 구성된 Kubernetes 클러스터에서 동작 
  - 각 Edge는 고유한 역할을 수행하며, 세 가지 지능(Face Detection, Feature Extraction, Member Verification)이 연계되어 결과가 비디오에 오버레이로 표시됨.
-  **Kubernetes 클러스터 구성**    
  - 마스터 노드: `keti2`   
  - 워커 노드 1: `keti0` (GPU 지원)  
  - 워커 노드 2: `keti1` 
- **주요 기능 및 기술**    
  - CCTV 비디오 스트리밍 및 처리    
  - Kubernetes를 활용한 클러스터 관리 (taint, toleration, nodeSelector 설정)
  - Docker 이미지 빌드 및 배포    
  - 실시간 데이터 처리를 위한 ConfigMap 및 Service 설정
  - 모니터링: Prometheus/Flask/Nginx 기반    
  - - MQTT를 통한 데이터 통신   
- **배포 환경**   
  - OS: Ubuntu



## Project5

- **고립지/원격지 지능형 CCTV 시스템 기획**    
  - 고립지 및 원격지 환경에 적합한 무선 기반 지능형 CCTV 시스템 개발을 위한 초기 서베이 단계   
- **키워드**    
  - 무선+엣지 CCTV    
  - 무선 자가망 (LORA, 무료)   
- **주요 활동**    
  - 물리적/엣지 CCTV 및 무선 자가망 기술 자료 조사    
  - 무선 자가망 응용 기술 분석    
  - 견적 정리 및 결과물 도출   
  - **조사 결과**    
    - **기술 보유 현황**: 장거리 통신 대역망 기술을 활용한 공공 시스템 존재 (도회지 중심)    
    - **문제점**: 구축 및 관리 비용 높음
    - **목표**: 고립지/원격지向け 저비용 자가망 보안 시스템 설계



## Project 6
- **엣지 AI 보안지능 및 무선 엣지 영상 보안 시스템 개발**  
  
  - 엣지 AI 보안지능의 지속적 최적화와 엣지 보안 단말 간 연계협업을 지원하는 무선 기반 영상 보안 시스템 기술 개발. 
  
  - 지능형 환경분석 AI와 자동 최적화 시스템을 구현
  
- **주요 기능**  
  
  - NVIDIA Jetson Orin 보드 탑재 지능형 CCTV와 환경분석 AI 모델로 실시간 분석  
  - 환경분석 AI의 Docker 컨테이너화 및 Kubernetes 기반 배포  
  - 환경정보 6종에 특화된 SW 자동 배포  
  - PyQT5 기반 CCTV 영상 스트리밍 및 메타데이터 출력 클라이언트  
  
- **기술 스택**  
  
  - **하드웨어**: NVIDIA Jetson Orin 보드  (JetPack 5.1.2 [L4T 35.4.1])
  - **개발 언어**: Python  
  - **프레임워크**: Flask (API), SQLAlchemy (DB), 배포용 클라이언트 PyQT5
  - **컨테이너/배포**: Docker, Kubernetes  
  - **환경분석 AI**: Pytorch 2.1.0, torchvision 0.16 
  
- **구성 요소**  

  - **등록/설정 서버**: AI 및 SW DB (SQLAlchemy), 설정 파일 업로드  
  - **마스터 서버**: 환경분석 AI 배포 관리  
  - **최적화 서버**: 환경 변화에 따른 SW 자동 배포 파이프라인  
  - **워커 서버**: 엣지 보드 탑재 CCTV에 환경분석 AI 실행 (Orin 보드 탑재 CCTV 제작/사용)

- **개발 목표**  
  - 환경분석 결과 기반 최적화 소프트웨어 자동 배포  
  - 무선 엣지 환경에서의 실시간 보안 지능 구현  



## Project 7
- **신규 과제 1차년도: 엣지 클러스터링 및 배포 시스템**  
  - Kubernetes와 Docker를 활용한 클러스터링 및 배포 시스템 구축을 목표로 하는 신규 과제의 1차년도 프로젝트. 
- **주요 기술**  
  - Kubernetes (k8s) 클러스터링  
  - Docker 컨테이너화  
  - Python 모듈 사용 예정  
  - Docker Private Repository 활용 예정  
- **환경 구성**  
  - **마스터 노드**  
    - 운영체제/시스템: Ubuntu / AMD  
    - 이름: `edge-master-01`  
  - **워커 노드**  
    - 운영체제/시스템: Ubuntu / AMD  
    - 이름: `edge-worker-01`
  - **CCTV**  
    - RTSP 스트리밍 지원  
- **개발 목표**  
  - 엣지 환경에서의 클러스터링 시스템 구현  
  - CCTV 연동 및 배포 자동화  
