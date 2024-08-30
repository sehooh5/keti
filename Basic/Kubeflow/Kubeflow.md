# Kubeflow



## Basic

- 엔드투엔드(End-to-End) AI 플랫폼
-  머신러닝 워크플로우의 `[End]머신러닝 모델 학습`부터 `[End]배포` 단계까지 모든 작업에 필요한 도구와 환경을 쿠버네티스(Kubernetes) 위에서 쿠브플로우 컴포넌트로 제공



## 구조

![image](https://github.com/user-attachments/assets/5a3c6224-6808-48e4-b4b9-7035918c5846)



### Central Dashboard

- 웹브라우저를 통해 **대시보드 UI**로 각종 컴포넌트를 이용
- 컴포넌트 : Notebooks, Experiments (AutoML), Experiments (KFP)  등



### Notebooks

- 웹브라우저에서 **파이썬 코드를 작성하고 실행**할 수 있는 주피터 Notebook 개발 도구를 제공
- 사용자는 생성한 Notebook을 이용해 데이터 전처리와 탐색적 데이터 분석 등을 수행하여 머신러닝 모델 코드를 개발할 수 있음



### Training Operators

- TensorFlow, PyTorch, MXNet 등 다양한 **딥러닝 프레임워크에 대해 분산 학습 지원**
- 사용자가 분산 학습 명세서(YAML)를 작성하여 쿠버네티스에 배포하면 쿠브플로우 Training Operator는 명세서에 따라 워크로드를 실행



### Experiments(AutoML)

- AutoML은 머신러닝 모델의 예측 정확도와 성능을 높이기 위한 **반복 실험을 자동화하는 도구**(쿠브플로우에서는 Katib를 사용)
- Katib는 하이퍼 파라미터 튜닝(Hyper Parameter Tuning), 뉴럴 아키텍처 탐색(Neural Architecture Search, NAS) 기능을 갖고있음
  - Hyper Parameter Tuning : 모델의 하이퍼 파라미터를 최적화하는 작업
  - Neural Architecture Search, NAS : 모델의 구조, 노드 가중치 등 뉴럴 네트워크 아키텍처를 최적화하는 작업
- 명세서를 작성한 후 쿠버네티스에 배포하면 카티브가 명세서에 정의한 하이퍼 파라미터와 병렬 처리 설정에 따라 실험을 동시에 수행하여 가장 성능이 좋은 하이퍼 파라미터를 찾음



### KServe

- 쿠버네티스에 **머신러닝 모델을 배포**하고 추론 기능을 제공
- Endpoint, Transformer, Predictor, Explainer로 구성
- Endpoint가 Predictor에 데이터를 전달하면 Predictor는 데이터를 예측하거나 분류
- Explainer는 데이터를 예측하거나 분류한 결과에 대해 판단 이유를 제시하는 설명 가능한 인공지능(eXplainable Artificial Intelligence, XAI) 역할
- Transformer는 데이터 전처리, 후처리 기능을 제공



### Kubeflow Pipelines(KFP)

- 머신러닝 **워크플로우를 구축하고 배포하기 위한 ML Workflow Orchestration 도구**
- KFP의 목적은 Pipelines과 Pipeline Components를 재사용하여 다양한 실험을 빠르고 쉽게 수행하는 것