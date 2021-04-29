# README

- 210428 Project start
- AI 학습용 데이터 품질검증(자율주행 분야)
- 사람, 자동차, 자전거 이미지 데이터를 보고 인식하는 학습 
- Docker Image를 window 환경에 linux, Docker Desktop 을 사용하여 진행하였음
  - Window 10 pro
  - Ubuntu 20.04.2 LTS
  - 개발언어 : Python 
  - 프레임워크 : Pytorch



### Spec

---



#### 시험용 데이터

1. 3D object detection
   - 데이터 종류 : image, velodyne lidar pointcloud, camera calibration, annotation(label)
   - 수량 : training 8657 / validation 2166 
   - 어노테이션 종류 : ’Car’, ’Pedestrian’, ’Cyclist’
   - 형식
     - image : .png
     - velodyne : .bin
     - calibration, annotation : .txt







### Daily

---

#### 0428

- Docker Desktop 및 Linux upbuntu 20.04.2 LTS 설치



#### 0429

- 해당 테스트를 진행할 수 있는 Docke Image 를 Window 환경에 build 하기
  - 폴더 내 `pcdet-image.tar` 파일 사용



