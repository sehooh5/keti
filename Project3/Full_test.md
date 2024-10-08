# Full_test



1. docker 설치

   - https://docs.docker.com/engine/install/ubuntu/
   - 잘 설치되었는지 확인하는 방법
     - $ sudo docker run hello-world

2. nvidia-docker 설치

   - https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html
   - 잘 설치되었는지 확인하는 방법
     - $ sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

3. 도커 이미지 pull (tar 파일 필요 없이 생성 가능)

   - $ docker pull scrin/dev-spconv:f22dd9aee04e2fe8a9fe35866e52620d8d8b3779
   - 이미지 잘 생성되었는지 확인하는 방법
     - docker images

4. 도커 이미지를 사용하여 container 생성

   - $ docker run -e NVIDIA_VISIBLE_DEVICES=0 -i -t -d --runtime=nvidia --shm-size=64gb --name nia-pcdet-test --mount type=bind,source=[해당 디렉토리]/OpenPCDet,target=/workspace/OpenPCDet scrin/dev-spconv:f22dd9aee04e2fe8a9fe35866e52620d8d8b3779
   - 부연설명 : 
     - -e NVIDIA_VISIBLE_DEVICES=0 : 그래픽 카드 개수 1개여서 0으로 설정
     - --name nia-pcdet-test : 컨테이너 name 설정으로 바꿔줄 수 있음
     - --mount type=bind,source=[해당 디렉토리]/OpenPCDet,target=/workspace/OpenPCDet
       - source : 컴퓨터 내에서 docker container 내부로 mount 하고싶은 폴더 위치(저희는 해당 SSD 카드 내에 /OpenPCDet 을 인식시켜주면 됩니다)
       - target : docker container 내부에서 새로 생성될 위치
   - 도커 container 잘 생성되었는지 확인하는 방법
     - docker ps

5. 도커 container 실행시켜 내부로 진입

   - $ docker exec -it nia-pcdet-test /bin/bash
     - 여7기서 "nia-pcdet-test" 는 container 이름으로 해당 container  를 입력해주시면 됩니다

6. 도커 container 내 해당 폴더로 이동 OpenPCDet

   - $ cd /workspace/OpenPCDet (안되면 상위폴더 이동 후 /workspace 찾아서 들어가기)

7. OpenPCDet/ 폴더 내에서 테스트 하기 위한 기본 세팅 하기

   - $ pip install -r requirements.txt
   - $ python setup.py develop

8. Test 진행

   - OpenPCDet/tools 폴더로 이동
     - $ cd /OpenPCDet/tools

   - test 명령어
     - $ python test.py --cfg_file cfgs/kitti_models/pointpillar.yaml --batch_size 1 --ckpt pointpillar_nia.pth —save_to_file
     - $ python test.py --cfg_file cfgs/kitti_models/pointrcnn.yaml --batch_size 1 --ckpt pointrcnn_nia.pth —save_to_file
     - $ python test.py --cfg_file cfgs/kitti_models/pv_rcnn.yaml --batch_size 1 --ckpt pv_rcnn_nia.pth —save_to_file
     - $ python test.py --cfg_file cfgs/kitti_models/second.yaml --batch_size 1 --ckpt second_nia.pth —save_to_file
   - 결과 : 
     - 테스트 결과는 [OpenPCDet/output/kitti_models/{모델}/default/eval/epoch_no_number/val/default]에 위치한다. 