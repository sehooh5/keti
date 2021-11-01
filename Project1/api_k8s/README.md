# README

- 5G 과제 클러스터 구성 및 SW 배포부분 API 작성
- 환경
  - 마스터, 워커 공통
    - ubuntu : 18.04 이상
    - kubernetes : 1.14 이상
    - docker : 19.03.12 이상
  - 마스터에서만
    - Prometheus 
    - Grafana 
    - Python package and module
      - flask
      - flask_cors
      - sqlite - sqlalchemy
      - requests
      - paramiko
      - subprocess
      - zipfile





### `API_K8S` directory

- `app.py` : 작성한 API 전체 내용
- `models.py` : sqlalchemy 사용한 DB 내용
- `ssh_test.py` : ssh 명령을 다른 컴퓨터에 전달하는 테스트 내용
- `ssh_reboot.py` : ssh 리부팅 명령
- `using_API.py` : API 를 직접적으로 사용해보는 예제
- `response.py` : API 응답코드에 대한 메시지 처리 기능
- `k8s` directory : 
  - `delete_node.py` : k8s 노드 삭제하는 기능
  - `join.py` : k8s 노드 추가하는 내용
  - `deployment_maker.py` : deployment 를 전달받은 값으로 만들어주는 기능
  - `deploy.py` : 만들어진 deployment.yaml 으로 배포하는 내용
  - `delete.py` : 배포된 yaml 파일로 삭제하는 내용
- `docker` directory : 
  - `build.py` : 도커 이미지 생성
  - `push.py` : 도커 이미지 도커허브로 push 

