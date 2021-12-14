# README

- Project 4
- 동시 지능 연계
- 타 프로젝트를 현 프로젝트에 리빌딩
- CCTV video 가 존재하고 Edge 컴퓨터가 3개인 클러스터가 있다. 각 Edge 는 역할이 나누어져있는데, 세개의 지능이 연계되며 그 값이 video 에 overlay 되어 Display 에 표출되게 된다



### k8s 참고 자료

---

- node의 taint 확인 :
  -  `kubectl get nodes -o json | jq '.items[].spec.taints' `
- node에 taint 추가 및 삭제 :
  - 추가 : `kubectl taint nodes <nodename> <key>=<value>:<effect>`
  - 삭제 : `kubectl taint nodes <nodename> <key>-`
- pod 종료시 계속 terminating 될 때 강제 종료 : 
  - `kubectl -n <namespace> delete pods --grace-period=0 --force <pod_name>`
- 각 노드에 대한 labeling 해주기
  - `kubectl label nodes [nodename] [key]=[value]`



### 작업 일지

---

#### 1018

- 금책임님팀 자료 받고 우리 쿠버네티스 클러스터 구성해서 실행시켜보는 작업
- 일단 우분투 서버 3개 구성
  - keti2 : 마스터노드 / 192.168.0.28
  - keti0 : 그래픽카드 좋은 워커노드 / 192.168.0.71
  - keti1 : 기타 워커노드 / 192.168.0.25



#### 1019

- 쿠버네티스 설치



#### 1020

- 쿠버네티스 클러스터링 후 해당 프로그램 진행시켜보기
  - 쿠버네티스 클러스터링 완료
- 전달받은 자료(이미지, yaml 등) 마스터로 이동 및 설치
- 마스터에 vscode 설치 후 파일들 해석하기
- image 파일들은 tar 로 build 완료
  - keti2 마스터 : all images
  - keti0 워커 : all images
  - keti1 워커 : all images



#### 1025

- 각 노드에 이미지파일 build 상태 확인

- yaml 파일 해석해보기

- 배포 진행해보기

  - service, configmap 은 배포 완료

    - service 는 수정 x
    - **conifgmap 의 처음 실시간 카메라 입력데이터 맨 밑의 주소로 고쳐줫음**

  - deployment 배포시 에러

    - **nodeSelector 부분 전부 수정해줬음**

    - [같은 에러 해결한 한국 예시](https://nevido.tistory.com/315)

    - nodeselector 대문자 혹은 true, false 오류여서 다른거로 바꿔줌

    - taint, tolerate 에러

      - kubectl taint nodes [nodename] [taint]- 로 삭제했더니 배포되는거 같은데

      - 계쏙 Pending.....삭제도 terminating 에서 멈춤

        - terminating 강제 종료 : 

          ```kubectl -n <namespace> delete pods --grace-period=0 --force <pod_name>```

- image 파일들은 tar 로 build 완료

  - keti2 마스터
  - keti0 워커 : facedetactor / feature extractor / monitoring-flask / monitoring-nginx / mqtt
  - keti1 워커 : member-verifier

- 먼저 각 노드에 대한 labeling 해주기

  - kubectl label nodes [nodename] [key]=[value]



#### 1026

- deploy 할때 계속적으로 taint, toleration 문제인지 pending 됨...오류 수정 필요
- 계속 안됨 지속적 수정 필요



#### 1027

- deploy 문제 해결중
- schedule 원리 확인중



#### 1028

- deploy taint, toleration 지정 후에도 해결이 되지않고 계속 진행
  - 오류메시지 : 0/3 nodes are available: 1 node(s) didn't match Pod's node affinity/selector, 2 node(s) had taint {node.kubernetes.io/unreachable: }, that the pod didn't tolerate.
  - [똑같은 에러 해결하는 블로그](https://waspro.tistory.com/563)
- 원래 5G 과제 worker nodes 에는 taint 가 none 이다.. 지금 프로젝트 worker 에도 taint 없애기
  - 지우면 자꾸 자동으로 생김..
  - **노드 전부 지우고 다시 클러스터링 구성하니 taint 문제 해결**
- **mv pod만 keti1(그래픽카드 없음)에 배포하려 했는데, CrushLoopBackOff 에러떠서 그냥 모든 pod keti0(gpu O)에 배포했더니 모두 잘 돌아감**



#### 1029

- 현 상황 : 
  - pod 은 모두 running 상태
  - ~~port 30001 : nginx monitoring - start 눌러도 face detect 를 못함~~
  - ~~port 30002 : flask monitoring - start 눌러도 face detect 를 못함~~
  - 화면에 뿌려지는 UI 주소 : 182.252.132.39:9000
  - re-deploy 두 번정도 해주고, 화면에 얼굴을 가까이 위치시키니 전부다 잘 **작동**
  - 다만 화면에 보여지는 UI 가 연동이 안되는데 어떻게 연동되는지 월요일에 확인



#### 1101

- 영기씨 가능하면 UI 연동 가능한지 확인 후 말씀드리기
- 프로젝트 전체 주소 :
  - UI : 182.252.132.39:9000
  - flask : 192.168.0.28:30002
  - nginx : 192.168.0.28:30001



#### 1209

- AXIS M3026 카메라 복구
  - 일단 겨우 공장초기화 성공 
    - 주소 : https://169.254.213.166/operator/videostream.shtml?nbr=0&id=49
  - 내일 mjpg 설정해서 카메라 스트리밍 가능한지 확인하고 
  - config 파일 수정 후 배포해보기



#### 1214

- 10/29 상황과 같은 상황..pods running but dont face detect

- pod running 상태

  ![image](https://user-images.githubusercontent.com/58541635/145916715-b39e5d00-b3e0-47bd-9636-2989ae4f4556.png)

- monitoring wep app 확인 - 아래 상태에서 멈춤(FD 안됨)

  ![image](https://user-images.githubusercontent.com/58541635/145919379-da21c465-83c4-43de-880d-72e16be58b61.png)

- log 확인

  - fd log - pod 생성 직후

    ```
    Start server
    Dec 14 01:27:06 program_name [10]: BaseClass Init called
    Dec 14 01:27:06 program_name [10]: load_ai_model called
     * Serving Flask app "decenter.ai.flask" (lazy loading)
     * Environment: production
    Dec 14 01:27:06 program_name [10]: set_model_Status : loading
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
    Dec 14 01:27:06 program_name [10]: Starting new HTTP connection (1): 182.252.132.39:5000
    Dec 14 01:27:06 program_name [10]:  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    Dec 14 01:27:08 program_name [10]: http://182.252.132.39:5000 "GET /model_download?model_name=UC4_FaceDetector&model_version=1.1&model_split=Split_No&split_number=0& HTTP/1.1" 200 123661198
    Dec 14 01:27:48 program_name [10]: calling MyClass - load_ai_model()
    Dec 14 01:27:49 program_name [10]: extracting files...
    WARNING:tensorflow:From /MyModel.py:51: The name tf.gfile.GFile is deprecated. Please use tf.io.gfile.GFile instead.
    
    Dec 14 01:27:49 program_name [10]: From /MyModel.py:51: The name tf.gfile.GFile is deprecated. Please use tf.io.gfile.GFile instead.
    
    WARNING:tensorflow:From /MyModel.py:52: The name tf.GraphDef is deprecated. Please use tf.compat.v1.GraphDef instead.
    
    Dec 14 01:27:49 program_name [10]: From /MyModel.py:52: The name tf.GraphDef is deprecated. Please use tf.compat.v1.GraphDef instead.
    
    WARNING:tensorflow:From /MyModel.py:57: The name tf.placeholder is deprecated. Please use tf.compat.v1.placeholder instead.
    
    Dec 14 01:27:49 program_name [10]: From /MyModel.py:57: The name tf.placeholder is deprecated. Please use tf.compat.v1.placeholder instead.
    
    WARNING:tensorflow:From /MyModel.py:63: The name tf.image.resize_image_with_pad is deprecated. Please use tf.compat.v1.image.resize_image_with_pad instead.
    
    Dec 14 01:27:49 program_name [10]: From /MyModel.py:63: The name tf.image.resize_image_with_pad is deprecated. Please use tf.compat.v1.image.resize_image_with_pad instead.
    
    WARNING:tensorflow:From /MyModel.py:69: The name tf.ConfigProto is deprecated. Please use tf.compat.v1.ConfigProto instead.
    
    Dec 14 01:27:49 program_name [10]: From /MyModel.py:69: The name tf.ConfigProto is deprecated. Please use tf.compat.v1.ConfigProto instead.
    
    WARNING:tensorflow:From /MyModel.py:71: The name tf.Session is deprecated. Please use tf.compat.v1.Session instead.
    
    Dec 14 01:27:49 program_name [10]: From /MyModel.py:71: The name tf.Session is deprecated. Please use tf.compat.v1.Session instead.
    
    2021-12-14 01:27:49.913989: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
    2021-12-14 01:27:49.933954: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 3699850000 Hz
    2021-12-14 01:27:49.934420: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x70dff70 initialized for platform Host (this does not guarantee that XLA will be used). Devices:
    2021-12-14 01:27:49.934432: I tensorflow/compiler/xla/service/service.cc:176]   StreamExecutor device (0): Host, Default Version
    2021-12-14 01:27:49.935207: W tensorflow/stream_executor/platform/default/dso_loader.cc:55] Could not load dynamic library 'libcuda.so.1'; dlerror: /usr/lib/x86_64-linux-gnu/libcuda.so.1: file too short; LD_LIBRARY_PATH: /usr/local/nvidia/lib:/usr/local/nvidia/lib64
    2021-12-14 01:27:49.935217: E tensorflow/stream_executor/cuda/cuda_driver.cc:318] failed call to cuInit: UNKNOWN ERROR (303)
    2021-12-14 01:27:49.935227: I tensorflow/stream_executor/cuda/cuda_diagnostics.cc:156] kernel driver does not appear to be running on this host (face-detector): /proc/driver/nvidia/version does not exist
    WARNING:tensorflow:From /MyModel.py:72: calling crop_and_resize_v1 (from tensorflow.python.ops.image_ops_impl) with box_ind is deprecated and will be removed in a future version.
    Instructions for updating:
    box_ind is deprecated, use box_indices instead
    Dec 14 01:27:49 program_name [10]: From /MyModel.py:72: calling crop_and_resize_v1 (from tensorflow.python.ops.image_ops_impl) with box_ind is deprecated and will be removed in a future version.
    Instructions for updating:
    box_ind is deprecated, use box_indices instead
    WARNING:tensorflow:From /MyModel.py:74: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.
    
    Dec 14 01:27:49 program_name [10]: From /MyModel.py:74: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.
    
    Dec 14 01:27:49 program_name [10]: model loading done
    Dec 14 01:27:49 program_name [10]: set_model_Status : loaded
    Dec 14 01:27:49 program_name [10]: Connecting to a dest
    Dec 14 01:27:49 program_name [10]: using mqtt protocol for output
    Dec 14 01:27:49 program_name [10]: output-connect
    Dec 14 01:27:49 program_name [10]: Connecting to a dest
    Dec 14 01:27:49 program_name [10]: using mqtt protocol for output
    Dec 14 01:27:49 program_name [10]: output-connect
    Dec 14 01:27:49 program_name [10]: Connecting to a dest
    Dec 14 01:27:49 program_name [10]: using mqtt protocol for output
    Dec 14 01:27:50 program_name [10]: get_autostart : true
    Dec 14 01:27:50 program_name [10]: AUTOSTART = :true
    http://182.252.132.39:5000/model_download?model_name=UC4_FaceDetector&model_version=1.1&model_split=Split_No&split_number=0&
    Download URL: http://182.252.132.39:5000/model_download?model_name=UC4_FaceDetector&model_version=1.1&model_split=Split_No&split_number=0&
    UC4_FaceDetector_1.1.zip
    UC4_FaceDetector_1.1.zip is stored on local storage.
    Dec 14 01:27:50 program_name [10]: output-connect
    
    ```

  - fd log - 모니터링 툴 시작 후

    ```
    Dec 14 02:07:08 program_name [9]: Connecting to a dest
    Dec 14 02:07:08 program_name [9]: using mqtt protocol for output
    Dec 14 02:07:08 program_name [9]: output-connect
    Dec 14 02:07:08 program_name [9]: Connecting to a dest
    Dec 14 02:07:08 program_name [9]: using mqtt protocol for output
    Dec 14 02:07:09 program_name [9]: get_autostart : true
    Dec 14 02:07:09 program_name [9]: AUTOSTART = :true
    Dec 14 02:07:09 program_name [9]: get_autostart : true
    Dec 14 02:07:09 program_name [9]: starting compute_ai, HTTP and AUTOSTART
    Dec 14 02:07:09 program_name [9]: get_model_Status : loaded
    Dec 14 02:07:09 program_name [9]: compute_ai called
    Dec 14 02:07:09 program_name [9]: retrieven input source from: http://169.254.213.166:5000/mjpg/1/video.mjpg
    Dec 14 02:07:09 program_name [9]: calling MyClass - compute_ai()
    Dec 14 02:07:10 program_name [9]: output-connect
    Dec 14 02:07:11 program_name [9]: ------------starting image thread-------------
    Dec 14 02:07:11 program_name [9]: reading input queue: 0
    Dec 14 02:07:11 program_name [9]: video device open...
    Dec 14 02:07:16 program_name [9]: processing a frame in a thread
    Dec 14 02:07:16 program_name [9]: ***remaining input queue size: 0
    Dec 14 02:07:18 program_name [9]: 1639447638.066611
    Dec 14 02:07:18 program_name [9]: <class 'list'>
    Dec 14 02:07:18 program_name [9]: result size: 45417
    Dec 14 02:07:18 program_name [9]: Processing Time : 74.382 ms
    Dec 14 02:07:18 program_name [9]: reading input queue: 0
    Dec 14 02:07:19 program_name [9]: image proceesed, returning result
    Dec 14 02:07:19 program_name [9]: fire_notification called
    Dec 14 02:07:19 program_name [9]: Starting new HTTP connection (1): uc4-mnt.default:8001
    Dec 14 02:07:44 program_name [9]: get fps received 
    Dec 14 02:07:44 program_name [9]: get_fps: 30.0
    Dec 14 02:07:44 program_name [9]: 10.244.2.17 - - [14/Dec/2021 02:07:44] "GET /get_fps HTTP/1.1" 200 -
    Dec 14 02:07:51 program_name [9]: get fps received 
    Dec 14 02:07:51 program_name [9]: get_fps: 30.0
    Dec 14 02:07:51 program_name [9]: 10.244.2.17 - - [14/Dec/2021 02:07:51] "GET /get_fps HTTP/1.1" 200 -
    http://182.252.132.39:5000/model_download?model_name=UC4_FaceDetector&model_version=1.1&model_split=Split_No&split_number=0&
    Download URL: http://182.252.132.39:5000/model_download?model_name=UC4_FaceDetector&model_version=1.1&model_split=Split_No&split_number=0&
    UC4_FaceDetector_1.1.zip
    UC4_FaceDetector_1.1.zip is stored on local storage.
    input source scheme : http
    input source scheme is http
    GENERATOR type returned
    
    ```

- **일단 30001 에서 됐음**

  - 카메라 주소 https 아닌 **http**사용
  - 앱은 **30001** 포트로 실행했는데 아마 상관 없을듯
  - 카메라 연결은 유선 사용하지 않고, 공유기 한 대를 공유하여 네트워크 구성