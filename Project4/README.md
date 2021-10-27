# README

- Project 4
- 동시 지능 연계
- 타 프로젝트를 현 프로젝트에 리빌딩
- CCTV video 가 존재하고 Edge 컴퓨터가 3개인 클러스터가 있다. 각 Edge 는 역할이 나누어져있는데, 세개의 지능이 연계되며 그 값이 video 에 overlay 되어 Display 에 표출되게 된다



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

- deploy taint, toleration 지정 후에도 해결이 되지않고 계속 진행해봐야할듯..?