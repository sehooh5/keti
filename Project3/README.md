# README

- 210428 Project start
- AI 학습용 데이터 품질검증(자율주행 분야)
- 사람, 자동차, 자전거 이미지 데이터를 보고 인식하는 학습 
- Docker Image를 window 환경에 linux, Docker Desktop 을 사용하여 진행하였음
  - Window 10 pro
  - Ubuntu 20.04.2 LTS
  - 개발언어 : Python 
  - 프레임워크 : Pytorch



## Process

#### 1. Docker Desktop 설치



#### 2. Ubuntu 설치

- cmd 창에서 Docker 설치되엇는지 -v 확인 후 
- apt-get ubuntu 실행
  - 사실 그냥 진행되는데 git bash, power shell, cmd 창에서 docker 사용 가능



#### 3. 3D_Object_detection_1차변환

- zip 파일 둘다 풀고 진행
  - 1번에는 `drive 데이터`
  - 2 번에는 `main.py`



#### 4. 3D_Object_detection_2차변환

- conda 실행시에는 작업자 권한으로 실행할 것!

- 아래 명령어로 설정
  - conda env create --file environment.yaml
                                             (environment.yaml에 명시된 가상환경을 만듭니다.)
  - conda activate NIA_test                                   (NIA_test 가상환경을 실행합니다.)
  - pip insta ll --user opencv-python                           (명시된 라이브러리를 설치합니다.)
  - pip install --user open3d
  - pip install --user pypcd
  - pip install --user natsort
- python 파일 data 위치 폴더 생성 및 변경 후 위치 설정 제대로 해줌
- `python NIA_data_convert.py` 실행
  - 폴더들은 생성되는데 제대로 된 이미지들이 없어서 데이터들은 텅 빈상태 아래 에러
  - ![image](https://user-images.githubusercontent.com/58541635/116641226-3fcd8c00-a9a7-11eb-9d0a-7406512d4223.png)



#### 5. OpenPCDet 진행

- 로컬환경에 옴긴 후 도커라이징할 것

- ```
  $ docker run -e NVIDIA_VISIBLE_DEVICES=0,1,2,3 -i -t -d --shm-size=64gb --name pcdet-test5 --mount type=bind,source=C:\Windows,target=/workspace scrin/dev-spconv:f22dd9aee04e2fe8a9fe35866e52620d8d8b3779
  ```

  - `source=` 설정만 제대로해주면 될듯



#### 6. 도커 run 명령어

- ```
  docker run -e NVIDIA_VISIBLE_DEVICES=0 -i -t -d --runtime=nvidia --shm-size=64gb --name pcdet-test --mount type=bind,source=/mnt/usb/TTA_01/docker_images/OpenPCDet,target=/workspace/OpenPCDet scrin/dev-spconv:f22dd9aee04e2fe8a9fe35866e52620d8d8b3779
  ```

- ```
  nvidia-docker run -e NVIDIA_VISIBLE_DEVICES=0 -i -t -d --shm-size=64gb --name nia-pcdet-test --mount type=bind,source=/ndata/sanghun,target=/workspace scrin/dev-spconv:f22dd9aee04e2fe8a9fe35866e52620d8d8b3779
  ```





## Spec



#### 시험용 데이터

1. 3D object detection
   - 데이터 종류 : image, velodyne lidar pointcloud, camera calibration, annotation(label)
   - 수량 : training 8657 / validation 2166 
   - 어노테이션 종류 : ’Car’, ’Pedestrian’, ’Cyclist’
   - 형식
     - image : .png
     - velodyne : .bin
     - calibration, annotation : .txt



E:\TTA_01\docker_images

scrin/dev-spconv



## Daily

#### 0428

- Docker Desktop 및 Linux upbuntu 20.04.2 LTS 설치



#### 0429

- 해당 테스트를 진행할 수 있는 Docke Image 를 Window 환경에 build 하기
  - 폴더 내 `pcdet-image.tar` 파일 사용



#### 0430

- 두번째 주신 과제
  - test 폴더 환경구성 완료 
  - 테스트 진행햇는데 데이터가 없어서 실패
- 첫번째 과제 - 컴퓨터 바꿔서 진행
  - 환경설정은 완료했고 폴더를 로컬로 옴긴 후 실행(다음주)



#### 0503

- 오늘 진행 순서

  1. 박사님 컴퓨터에서 새로 들어온 데이터 테스트 컴퓨터로 옮기기(혹은 그 자리에서 테스트?)

  2. 옮기고 변환툴 사용해서 데이터 변환시키기(두번째 주신 과제)

  3. 변환된 데이터를 사용해서 첫번째 과제 진행

     - 데이터는 새로 받은 데이터

     - 컨테이너 생성 시 옮겨놓은 워킹 디렉토리 옮겨서 사용

     - 명령어 변경(`--runtime=nvidia` 안됨)

       ```
       docker run -e NVIDIA_VISIBLE_DEVICES=0,1,2,3 -i -t -d --shm-size=64gb --name pcdet-test5 --mount type=bind,source=C:\Windows,target=/workspace scrin/dev-spconv:f22dd9aee04e2fe8a9fe35866e52620d8d8b3779
       ```

       

- 현재 내 컴퓨터에서 다시 데이터 생성하는 작업 진행중

  - 테스트환경은 완성 되어있고
  - 테스트 돌리고 나오는 데이터들 (calib, image_2, label_2, velodyne 의 폴더) 테스팅 컴퓨터로 옮겨서 사용
    - 데이터 사이즈가 클거같은데.. 일단 테스트 돌려보기
    - 네개의 폴더로 데이터들 잘 생성되는중
      - 1분에 4개 데이터 처리중(총 728개 182분 예정)
    - **!! 1883번 진행중 pct_to_bin 명령어에서 오류 발생하고 진행멈춤!!**
      - `NIA` 폴더에 `data_done` 폴더 생성 후 1882번까지의 데이터 옴긴 후 
      - 1883번부터 다시 진행중
      - 오류 자세한 내용은 python 파일 위치의 폴더에 캡쳐해서 저장해놓았음



#### 0504

- 테스트 컴퓨터에 nvidia driver 설치하고 진행해보기

  - ```
     sudo docker run --gpus all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark
    ```

    명령해보기

  - 내컴퓨터 크롬 마지막 1,2번 블로그 보면서 해결해보기

- [nvidia-docker 설치(공식문서 url)](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

  - docker 설치도 중간에 url 있음

- 한글파일 명령어 모음

  - ```
    o 알고리즘 학습 방법
    
    - 본 과제에서 제안된 모델을 학습하기 위해서는 Docker Hub나 AIHub에서 Docker Image를 받아 설치할 환경과, 학습된 모델, Kitti format으로 변형한 데이터 셋의 다운로드가 필요하다.
    
    - [docker pull scrin/dev-spconv:f22dd9aee04e2fe8a9fe35866e52620d8d8b3779] 을 통해 spconv가 설치 완료된 docker 이미지를 받거나, AIHub의 [139.특수환경 자율주행 3D/03.AI모델/1.라이다 기반 주변 차량 인식 기술/3. 도커 이미지/pcdet-image.tar]를 받아 spconv가 설치 완료된 docker 이미지를 받는다.
    
    - 받은 도커 이미지를 컨테이너로 실행 시킨다. 사용자의 GPU할당 방식과 서버 storage 방식에 따라 명령어는 달라질 수 있다. 예시 명령어는 다음과 같다.
    [docker run -e NVIDIA_VISIBLE_DEVICES=0,1,2,3 -i -t -d --runtime=nvidia --shm-size=64gb --name nia-pcdet-test --mount type=bind,source=/ndata/sanghun,target=/workspace scrin/dev-spconv:f22dd9aee04e2fe8a9fe35866e52620d8d8b3779]
    
    - [docker attach pcdet] 또는 [docker exec -it pcdet /bin/bash]으로 컨테이너에 접속한다.
    
    - [139.특수환경 자율주행 3D/03.AI모델/1. 라이다 기반주변 차량 인식 기술/3. 도커 이미지/OpenPCDet.zip] 서 벤치마크 코드와 학습 모델이 포함된 알집 파일을 다운받아 압축 해제한다.
    
    - [139.특수환경 자율주행 3D/03.AI모델/4. 전체 데이터셋/Object_Detection_Dataset.zip]의 Dataset을 다운 받아 [OpenPCDet/data/kitti/training/]에 다음과 같은 형태가 되도록 압축을 해제해 위치시킨다
    
    - [OpenPCDet/]로 이동해 [pip install -r requirements.txt]를 실행한다.
    
    - [python setup.py develop]를 실행한다.
    
     
    
    
    
    
    
    - Test
    [OpenPCDet/tools/]로 이동하여 각 모델에 대해 아래의 명령어를 실행시킨다.
    python test.py --cfg_file cfgs/kitti_models/pointpillar.yaml --batch_size 1 --ckpt pointpillar_nia.pth —save_to_file
    python test.py --cfg_file cfgs/kitti_models/pointrcnn.yaml --batch_size 1 --ckpt pointrcnn_nia.pth —save_to_file
    python test.py --cfg_file cfgs/kitti_models/pv_rcnn.yaml --batch_size 1 --ckpt pv_rcnn_nia.pth —save_to_file
    python test.py --cfg_file cfgs/kitti_models/second.yaml --batch_size 1 --ckpt second_nia.pth —save_to_file
    
    - 테스트 결과는 [OpenPCDet/output/kitti_models/{모델명}/default/eval/epoch_no_number/val/default]에 위치한다. 테스트 결과의 예시는 다음과 같다.
    ```

  - 