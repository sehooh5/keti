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

