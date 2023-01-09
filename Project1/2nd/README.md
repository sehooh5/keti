# Project 1 2년차

- 5G 기반 협력 대응 과제
- 전체 내용 `5G`  파일에 정리



### 사용 툴 버전

---

- ubuntu : 18.04
- kubernetes : 1.14
- docker : 최신버전 19.03.12 (현, 2020.08.04)
- Prometheus
- Grafana
- OpenCV
- VLC
- RTSP
- Flask : 1.0.2



## 진행 단계(daily)

#### 0618

- UI 초안 및 추가기능 완료
- 새롭게 시작 :
  - 영상,메타정보를 전달하는 릴레이서버 구성
    - `CCTV(server) - Edge(client+server) - VMS(client)` 형태의 구성



#### 0622

- 전체 회의 내용 토대로 릴레이서버 구성하는 테스트 하기(요번주내)
  - 영상,메타정보를 전달하는 릴레이서버 구성
    - `CCTV(server) - Edge(client+server) - VMS(client)` 형태의 구성



#### 0623

- 릴레이서버 구축 : 
  - Wowza  찾아보는중
    - 와우자는 완성된 프로그램인듯?
  - Gstreamer - python(ubuntu 기반)
    - https://dkant.net/2019/05/17/Gstreamer01/
    - 이 서버내용대로 worker1, 2 딴에서 relay server 가 돌아가면 될듯 
      - 먼저 테스트해서 위 내용대로 잘 작동하는지 master 에서 구현 후
      - relay server 도커로 만든 후 k8s 로 worker1,2 에 배포
  - [관련 논문](http://koreascience.or.kr/article/CFKO200724737420524.pdf)



#### 0624

- 위 내용 중 Gstreamer 개념으로 테스트배드 구축하기
  - [내 작업 내용](https://github.com/sehooh5/keti/blob/master/Project1/relayserver/gstreamer.md)
- 잘 안됨



#### 0625

- 일단 쉘에서는 카메라 켜짐, 파이선파일도 에러는 고친듯
- 그다음 파이썬 예제 찾아보고 이어서해보기
- ~~깃허브에  rtsp-simple-server 보고 하는중~~
  - ~~주소 : https://github.com/aler9/rtsp-simple-server~~ 일단 보류
- version 오류 뜨는거는 무시해도 되는거같은데, 일단 텍스트파일로 저장하면 에러 해결
- 지금은 일단 돌아는 가는거같은데 ..... server 구동되는지 확인 + 클라이언트 연결하는거 하면될듯



#### 0701

- gstreamer 다시 시작
- `relayserver` repository
  - server_test2.py : test video on -> auto off
  - server_test.py : stopped in CLI
- CLI using : OK





#### 0702

- Wowza start
- Using CLI improve



#### 0705

- wowza start with developer license
  - made basic
    - vod sample check
    - live... how to connect my rtsp address to wowza
  - improve about JAVA environ
  - [refo blog](https://m.blog.naver.com/PostView.naver?blogId=woliver&logNo=221833439445&targetKeyword=&targetRecommendationCode=1)



#### 0706

- Wowza keep going
- what shoud i use for relay server?



#### 0707

- meeting for next step
- [와우자 기본적 내용 잘 정리된 블로그](https://help.iwinv.kr/manual/read.html?idx=679)
- wowza ing
  - 다시 rtsp 사용하는 예제 보면서 시작해보기
  - rtsp://192.168.0.29:1935/live/test01.stream 주소로 vlc 플레이어 사용해서 보여지는데 된건가?
    - https://www.wowza.com/docs/how-to-re-stream-video-from-an-ip-camera-rtsp-rtp-re-streaming 이거보고 따라함
    - [해당 내용으로 유튜브 스트리밍 하는 방법](https://www.youtube.com/watch?v=9AYCwibnjDE) : 내일부터 스트리밍 가능
    - [페북 라이브로 스트리밍 성공](https://www.youtube.com/watch?v=ZRWTnmHof_g)
  - **페북 라이브로 스트리밍 넘기는거까지 완성햇음!!**
- git push default setting
- [HLS 멀티뷰 시스템 관련 논문](https://www.koreascience.or.kr/article/JAKO201734963727796.pdf)
- [와우자 리스트리밍 관련 논문](http://koreascience.kr/article/CFKO201130533389393.pdf)



#### 0708

- 페북 라이브 스트리밍 한것 토대로 진



#### 0709

- wowaz improve
- rtsp://keti:keti1234@192.168.100.60:8805/videoMain 새로운 카메라까지 동시 연결하는중
  - 연결 완료 후 두개의 카메라 두개의 클라이언트로 따로 전송 완료



#### 0712

- 완성된것 박사님 보여드리고 연결이 어떻게 구성되어있는지 보고드리기!
- 그 전에 live edge 사용하는거 진행해보고 다음단계로
- **릴레이서버 STOP**
- **2차년도 본격적으로 시작**
  - 클러스터 구성 등에 필요한 Open API 파라미터, 아규먼트 전달드리기



#### 0713

- SW 동작, 중지하는 부분부터 정리하고 책임님께 전달 및 질의
  - 완료 후 컨펌 ok
  - 배포시 설정하는 포트들 어디서 사용하는 포트인지 ? (master or worker)
- OPEN API 종류보고 공부해보기
  - 진행
- 진행 범위는 "DEMS 연동 인터페이스 설계서"의 26쪽 부터



#### 0714

-   에이피아이 구성 시작
- 피피티 및 한글파일 참고
  - 한글파일에는 내꺼 관련한 목록은 없음
  - 일단 작동이 가능하게끔만 프레임 짜두라는 말이신듯



#### 0716

- 기본적으로 내가 생각하는 방향의 API 만들고 있기



#### 0719

- 엣지 클러스터 추가부터 시작..

- DB 만들고 시작해보기 

  - flask-sqlalchemy 로 시작

- 기능 STOP!! 일단 껍데기만 먼저 만들기!!

- 누나 예제

  - get

    ```python
    app.get("/get_edgeInfo", function (req, res) {
        dbclient.connect(url, function (err, db) {
            if (err) throw err;
            db.collection("edgeserver").findOne({
                id: req.query.id
            }, function (err, result) {
                if (result != null) {
                    res.json({
                        code: "0000",
                        message: "처리 성공",
                        id: result.id,
                        name: result.name,
                        type: result.type,
                        ip: result.ip,
                        port: result.port,
                        gps: result.gps
                    })
                } else {
                    res.json(error_code.error9999d);
                }
            })
            db.close()
        })
    });
    ```

  - post

    ```python
    app.post("/add_newEdge", function (req, res) {
        dbclient.connect(url, function (err, db) {
            if (err) throw err;
            let doc = db.collection("edgeserver").update({
                id: req.body.id,
                name: req.body.name,
                type: req.body.type,
                ip: req.body.ip,
                port: req.body.port,
                gps: req.body.gps
            }, req.body, {
                upsert: true
            }, function (err, result) {
                res.json({
                    code: "0000",
                    message: "처리성공",
                    id: req.body.id
                })
            })
            db.close()
        })
    });
    ```



#### 0720

- 껍데기는 다 만들어놨으니 

- flask - **DB 연동**하는 부분부터 다시 공부하면서 시작

  - sqlalchemy (ORM) 방식 사용

    -  특징
       1) 장점

         -  개발자는 DBMS에 대한 큰 고민없이, ORM에 대한 이해만으로 웬만한 CRUD를 다룰 수 있기 때문에,

             비즈로직에 집중할 수 있으므로 개발 생산성을 증가시킬 수 있다.

         - 객체를 통하여 대부분의 데이터를 접근 및 수정을 진행하므로, 코드 가독성이 좋다.

         -  데이터 구조 변경시, 객체에 대한 변경만 이루어지면 되므로, 유지보수성이 좋다.

       

      2) 단점: 

       - 복잡한 쿼리 작성시, ORM 사용에 대한 난이도가 급격히 증가한다.

       - 호출 방식에 따라, 성능이 천차만별이다.

       -  DBMS 고유의 기능을 전부 사용하지는 못한다.

- **postman 사용**하는 방법 진행 - 나중에 

- 질문 : 

  - 2.16~ , 3.4~ 의  사용가능한 포트 조회하는 부분은 같은 내용인데 필요한지?

- 디비 연동부터 시작



#### 0721

- 질문 : 

  - 2.16~ , 3.4~ 의  사용가능한 포트 조회하는 부분은 같은 내용인데 필요한지?

- 외부 api 와 연동해보고 해당 정보가 어떻게 들어오는지(아마도 json) 확인하고 어떻게 사용할 것인지?

  - [urllib.request 사용하여 json 불러오는 예제](https://da-nika.tistory.com/14)
  - [json data 사용하는 예제](https://devpouch.tistory.com/33)
  - [sqlalchemy 사용](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=sys3948&logNo=221624837865)

- 진행 : 

  - SW DB 두개 만들기

    - | 이름        | 타입   | 필수 | 예제값                 | 설명               |
      | ----------- | ------ | ---- | ---------------------- | ------------------ |
      | sid         | String |      | “0xs1”                 | 소프트웨어 고유 ID |
      | name        | String |      | “분석 SW”              | 소프트웨어 명      |
      | fname       | String |      | “content”              | 소프트웨어 파일 명 |
      | copyright   | String |      | “KETI”                 | 저작권자           |
      | type        | String |      | “Container”            | 타입               |
      | description | String |      | “영상 분석 소프트웨어” | 설명               |
      | datetime    | String |      | “2021-07-08”           | 업로드 날자        |

    - | 이름 | 타입   | 필수 | 예제값 | 설명                  |
      | ---- | ------ | ---- | ------ | --------------------- |
      | sid  | String |      | “0xs1” | Master/Worker 서버 ID |
      | wid  | String |      | “0xw1” | 소프트웨어 id         |

  - 포스트맨 사용해보기 - 못함

  - DB에 들어가는거는 확인햇다 DB browser for sqlite 설치함

- 질문 : 

  - api 들이 실행될때 직접적인 기능들이 실행되어야 하는것인지? 기능 실행부분은 다른곳에? (ex 1번기능)



#### 0722

- 2.7 그대로진행하고 sid 만드는 부분했으니 그 다음부터 진행



#### 0726

- [sqlalchemy engine 추가하고 사용하기](https://yujuwon.tistory.com/entry/SQLAlchemy-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0)
- [sqlalchemy 사용](https://edykim.com/ko/post/getting-started-with-sqlalchemy-part-1/)
- [실질적으로 select 찾아서 사용한 부분](https://lowelllll.github.io/til/2019/04/19/TIL-flask-sqlalchemy-orm/)
- API 완성목록
  - 2.1 : 아직 k8s 기능 구현 안됨
  - 2.2 : O, k8s 구현했지만 쿠버네티스에서 사용안해봄
  - 2.3 : ㅁ
  - 2.4 : ㅁ
  - 2.5 : O
  - 2.6 : O
  - 2.7 : O
  - 2.8 : O
  - 2.9 : O
  - 2.10 : O
  - 2.11 : O
  - 2.12 : O
  - 아래부터 포트조회
    - server_sw db에 랜덤한 숫자 부여하는 방식으로
    - 배포될 때 port 3개의 정보를 함께 저장
    - server id 로 POST 전달하면 해당 서버에서 사용 가능한 port 번호 전달
  - 2.13 : O
  - 2.14 : O
  - 2.15 : O



#### 0727

- 2.5부터 시작하면 될듯? 완료
- Datetime 넣기 - 완료



#### 0728

- 포트찾기 완료
  - 수정 : 포트에 대한 DB 를 추가했음(server_sw 3개의 column으로 추가)



#### 0729

- 디바이스 연결 부분 생각하고 API 작성하기 - 내일이후
- 내일까지 쿠버네티스 교육



#### 0802

- 디바이스 연결부분 시작 - 타 API 연동 후 작동하는지 여부 확인하면서 더 진행
- 2.1 클러스터 추가할 때 원격으로 워커노드 cli 명령 보내는 작업 진행중
  - OpenSSH 서버 설치 
    -  [참고1](https://dora-guide.com/ssh-%EC%A0%91%EC%86%8D/)
    - [참고2](https://jootc.com/p/201808031462)
  -  keti0에서 keti1 로 ssh 접속 성공...이내용 대로 명령 할 수 있게 python 코드 구성하면 될듯
  - 코드구성 완료
- 전체적인 틀 및 구현가능하게 완성 app.py 
  - 내일 회의 후에 연동 가능하게 한 후에 작동시켜보면서 작업하기



#### 0803

- 전체 회의
- 엣지 클러스터 추가 시 ssh 연결하는 동작 구현



#### 0804

- 전체 api 검토
- api 연결사례 등 보면서 시뮬레이션



#### 0805

- 06일에는 워크스테이션 글카 채우기 



#### 0806 

- 글카 설치 완료
  - 추후에 워크스테이션 잘 돌아가는지 확인하고 우분투 설치하기
- api 연동사례 진행해보기
  - using_API.py 파일 만들어서 기존 app.py 를 서버로 돌리면서 연동해봤음



#### 0809

- 쿠버네티스 파이썬으로 실행시켜보기
  - 쿠버네티스 노드 join 을 파이썬으로하면 pwd 입력하는 부분을 처리못해서 안넘어가는듯
    - 해결 : exec_command에 get_pty=True 아규먼트 추가
- 쿠버네티스 다시 시작하는중....
  - 정상적으로 설치는 됨
- 서버에 그래픽카드 설치했으니 우분투 설치하고 서버 옮기기?



#### 0810

- 09일 파이썬으로 k8s 노드 연결하는 부분 추가해서 진행하면 될듯
- 이전일과 마찬가지로 노드 재연결 join 시 멈춤현상 발생............
  - 6443 포트 방화벽 풀어줘서 해결



#### 0811

- 앱 배포하는 부분 파이썬으로 가능하게끔 만들면 될듯



#### 0812

- 전체적인 진도 관리 및 앱 배포부분 정리
- 파이썬으로 모든 동작 작동 가능하게



#### 0813

- docker image가 마스터 노드에 잇을때 배포가 가능한지 (docker hub 에 올리지 않음)
  - 역시나 imagePullBackOff
  - 
    - 모든 노드에 이미지가 pull 되어잇어야한다....
  - 일단은 도커허브에 올려서 사용하는 방향으로..
- k8s 폴더에 배포, 삭제하는 기능 추가
- deployment_maker.py 파일 기능 수정 완료
- docker, k8s 폴더 나누고 각자 기능추가
  - 이 기능들로 작용 가능하게 `app.py`에서 사용하면 될듯?



#### 0817

- `app.py` 에서 모든 기능이 작동가능하게끔 연동해보기
- git 관련하여 token 이슈 및 자동로그인 해결
- API 응답코드 관련하여 처리방법 서베이해보고 구현하기
  - 응답코드 입력하면 메시지 출력하는 `response.py` 만들고 사용되는지 확인
  - 이 응답처리를 어떻게 사용할 것인가....?에 대한 질문 필요



#### 0818

- 앱 작동여부 세부사항 체크



#### 0819

- add_newEdgeCluster 와 연동되는 기능 수정 및 테스트
  -  join 기능 `join.py` 에서 완벽하게 3개의 서버 클러스터링 완료
  - 해당 기능에서도 추가하였음
  - 하지만 나중에 list 받아와서 처리해야함
- `delete_node.py` 수정중에 있음
  - whname 이 3개로 다른변수들과 숫자가 달라서 처리 어떻게할지 `test.py` 에서 테스트중
  - `test.py` 의 kubeadm reset 부분이 잘 작동하지 않음



#### 0820

- kubeadm reset 부분 수정



#### 0823

- reset 계속 수정



#### 0824

- 일단 그라파나 연동해서 주소 받아오기
- 그라파나, 프로메테우스 연동 완료



#### 0830

- 전체 프로젝트 진행상황 정리
- 디바이스연결(=카메라 연결) 확인
  - 확인 후 연결하고 끊는 API 구성하기



#### 0831

- 카메라 60:8805 만 살아있고 직접 같은 라우터에 연결했을때만 사용가능...
  - 일단은 이 카메라로만 진행..
- 카메라 70:8810 은 직접 연결해도 "Codec `h264' (H264 - MPEG-4 AVC (part 10)) is not supported" 에러가 뜸
- 스위치 새로왓으니 전체 유선랜선 한꺼번에 사용하기
- sudo + y 전달하는거 `echo y | sudo kubeadm reset` 으로 해결
  - 현재는 노드1,2 삭제+리셋 완료 
  - 마스터 삭제하는거 실행해보고(test_delete_master.py) 다시 조인하기..
    - 조인할때 무선 말고 유선으로 다시 하는게 나을듯?



#### 0901

- 스위치 설치, 카메라는 여전히 60:8805 만 작동
- 마스터 삭제 진행 후 다시 조인
- **중간에 계속 마스터노드에서 localhost:nodePort> 실행이 안됐었는데...겨우겨우 해결**
  - 방법 : `sudo iptables -F`
- kube-state-metrics 오류가 계속났는데 일단...넘겨...
- 그라파나 보입니다...!!
- 다음 디바이스 연결부분 진행!!
  - 일단....다시 localhost 안뜨는데..기본 python app은 노드포트에서 실행이됨..일단 진행?



#### 0903

- 새로운 카메라앱 구성
  - 기능 : API 로 주어진 url 을 가지고 해당 노드에 해당 카메라 연결
  - 배포 : 각 노드에 배포
  - 참고 : flask video streaming 앱 구동이 되고있고 이 앱을 변형시켜서 제작할 예정
- 소켓서버로 다시 구성해야할듯...
  - socket flask server 시작
  - [flask-soketio server-client 예제](https://heodolf.tistory.com/125)
  - [기본 다큐먼트](https://flask-socketio.readthedocs.io/en/latest/getting_started.html) : 이거보고 간단한 프로그램 만듬
- 소켓서버로 구성 완료 : `connect_device` 폴더에 있음
- 현재 구성 : 
  - CLIENT(`socket_test` 폴더) : 
    - index.html : nodeport, device_url 을 입력할수 있음
    - client_flask.py : flask 로 구성된 client 로 최종 `app.py` 의 connect_device API 를 수행
  - SERVER(`connect_device` 폴더) :
    - device_app.py : 소켓 서버로 client 에서 오는 정보를 계속 받고, 그 정보로 camera 연결
- 궁극적인 구성 : 
  - `app.py` : socketio 에서는 클라이언트 개념으로 connect_device API 작동하면 해당 nodeport와 device_url 을 서버에 전달
  - 새로운 카메라앱 : 서버 개념으로 계속 노드포트에 켜져있을 것이며 `app.py`에서 해당 정보들이 넘어오면 해당 카메라를 연결하게 된다
- 카메라 disconnect 기능 구현중
  - 서버에서 카메라가 계속 구동중이면 socketio 로 연결이 안되서 stop 명령을 보낼수가 없음..어떻게..?
  - 멀티쓰레드 소켓 쓰면 될까?



#### 0906

- 카메라 disconnect 기능 구현중
  - 서버에서 카메라가 계속 구동중이면 socketio 로 연결이 안되서 stop 명령을 보낼수가 없음..어떻게..?
  - 멀티쓰레드 소켓 쓰면 될까?
  - 시나리오1 : 
    - 워커노드에 앱 두개
      - 앱1 : 소켓으로 os.environ 설정만
      - 앱2 : os.environ으로 실질적으로 카메라 구동하는 앱\
      - 안됨
  - 시나리오2
    - 그냥 지금처럼 하고 영상 나오는 클라이언트에서 disconnect하는 방법.. 은 의미가없는데..
  - 시나리오3
    - 카메라마다 앱이 한대씩 있어서 계속 영상이 틀려져있고
    - 마스터에서 명령을 보내면 그 영상을 틀어주기?
  - **시나리오4** 이거로 진행!!
    - 기존처럼 진행하되 버튼형식 -> 지금 UI 처럼 선택해서 커넥트, 디스커넥트 하는 방식으로?
    - cam1,2.html / app1,2.py / manager_app.html 으로 실행중
    - **여기서 render_template 이 아닌 그냥 정보만 보내는식으로? 하면 될듯...??**
    - **Disconnect 부분도 만들어야함**



#### 0907

- **manager_app.py 에 /test 부분은 포스트명령을 다른 포트로 보내기 성공**
  - **사실상 이 방법이 api 에는 적합..다만 명령은 보내지는데 그 명령을 대상 서버에서 사용을 못함**
  - 그런데 그 명령으로 실행시킬수는 없음..
  - 이벤트 핸들링 서버를 만들어야 하나..?
- **클라이언트 단에서 명령 보내서 해당 카메라 앱을 실행하는 방식으로..**
  - worker node 당 모든 카메라에 대한 앱이 존재함 (cam1,2_no1.py)
  - 클라이언트에서 worker id+camera app id 를 사용해 해당 camera app의 nodeport 를 찾아와서 연결
- **타 API 와 연결 테스트 실시 /test_connect/socket_test/test_server.py** 
  - 연결 도중 json 으로 받아오는것을 이제 알았음 
  - <mark>**다른 API들도 json 파싱해서 진행하는 방법으로 다 바꿔줘야함**</mark>
- <mark>**궁극적 목표 : 1. 마스터->워커로 device 연결/해제 가 가능해야한다..   2. 여러대 device 연결 **</mark>
  - device 의 해당 url 주소가 전달되서 워커에서 사용되고 또 해지되게끔... : 이벤트 헨들링?
  - [여러대 디바이스 연결 참고1](https://www.python2.net/questions-951811.htm)
  - [여러대 디바이스 연결 참고2](https://www.python2.net/questions-1174062.htm)



#### 0908

- 디바이스 서버 단에서 while if 로 진행해보기
  - manager_app.py - /test
  - 새롭게 app1.py 변경하든지 해서 진행해보기
  - manager_app.py  /  open_cam1,2.py  / manager_app2.html 로 진행중
    - post request 보내면 해당정보 받아서 각 port 에서 카메라 url 정보로 카메라 실행
    - **하지만.. 한번 전달하면 카메라 구동중이여서 다른 전달을 받을수가 없음**
      - 이부분 어떻게 해결할지가 관건...
- 기본 api app.py 구동 되게끔 만들기
  - 완료
  - json 데이터로 받아오는거까지 완료
  - 처리메시지 나중에 전체적으로 처리 필요!



#### 0909

-   카메라 실행시 포스트로 전달 가능하게 만들기
- 다른 API에서 데이터베이스 사용해서 연동해놓기
-   멀티 쓰레드 이용해서 opencv 돌리는 방법으로 진행
    - [참고 깃허브](https://gist.github.com/allskyee/7749b9318e914ca45eb0a1000a81bf56)



#### 0910

- 작동 안되는 4개의 에이피아이 수정



#### 0913

- API 전달메시지 전체적으로 수정 및 완성시키기
  - 디바이스 연결부분은 일단 가능한데까지 해놓기\
  - **응답코드는 아직 전체완성은 아니고 부분완성**
- 포트포워딩 
  - 192.168.0.1 접속해서 열어주는거로 해결
  - 주소 : http://123.214.186.231:5000
- 현재 디바이스 연결/해제 부분 빼고는 연동완료



#### 0914

- 디바이스 연결부분 완성시키기!
  - 일단 1개 노드에 여러대 카메라 연결하는거는 보류
  - 기존방법사용...
    - 워커노드에서 실행되고있는 viewer 웹앱에 명령을 보내는식..
    - app.py - test_connect/app.py 와 연동중 // 잠깐 멈춤
- 다시 기본 토대
  - Master에서 디바이스 연결/해제 API 작동시 Worker는 영상 릴레이서버 역할만 함
  - Client(VMS)는 본인의 명령어로 추후에 릴레이된 데이터를 읽어서 스트리밍!
  - 마지막에는 여러 카메라의 데이터를 릴레이 시킬수 있는 멀티 릴레이서버
- [Yield, generator 기본 참고](https://tech.ssut.me/what-does-the-yield-keyword-do-in-python/)
- [Yield, generator 기본 참고2 - 정리잘됨](https://yeomko.tistory.com/11)
- **새롭게 M-W 로는 CAM에 대한 정보만 넘겨서 Worker 의 환경변수를 저장하는 방향으로 진행중**
- 작동 완성 : 
  - k8s/delete_node.py
  - app.py - add_newEdgeCluster



#### 0915

- **새롭게 M-W 로는 CAM에 대한 정보만 넘겨서 Worker 의 환경변수를 저장하는 방향으로 진행중**
  - 환경변수를 어떻게 영구적으로 등록하는지 
    - [환경변수 설정 정리](https://blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=koromoon&logNo=220793570727)
    - [리눅스 환경변수 정리](https://wooono.tistory.com/73)
    - .bashrc 에 있는 환경변수 덮어쓰기
    - sed 로 파일내 특정문자 찾아서 삭제 가능
    - 삭제 : `sudo sed -i '/OPENCV_CAMERA_SOURCE/d' ~/.bashrc`
    - 추가 : `sudo echo "export OPENCV_CAMERA_SOURCE=test1" >> ~/.bashrc`
    - 등록하는 거 완료 
  - ssh 명령으로 Worker 의 OPENCV, STOP 환경변수 설정해주기 : `ssh_device.py`
    - request_device.py, /test_connect/response_device.py
    - 위 파일들로 정보 보내서 환경변수 설정하는건 됨
      - source ~/.bashrc 명령어는 실행 안되는데 파일은 잘 바뀜
    - 다만 sudo 입력시 비밀번호 없이하는거 좀 더 연구해봐야함
  - 정보 넘겨서 VMS서버 역할하는 앱 따로 구동해서 연결되는지 확인



#### 0916

- **다만 sudo 입력시 비밀번호 없이하는거 좀 더 연구해봐야함**
  - pexpect 모듈 연구
- 정보 넘겨서(완) VMS서버 역할하는 앱 따로 구동해서 연결되는지 확인



#### 0917

- sudo 연결 확인



#### 0923

- sudo 연결 확인
- 소프트웨어 API 확인 후 내일 연동
  - docker login 이 되었다는 가정하에
  - upload = docker image build + push / 해당 정보 데이터베이스에 저장
  - deploy = k8s deployment making + deploy / 해당 정보 데이터 베이스에 저장



#### 0924

- sudo 작업 계속 진행
  - 실제로 제대로 환경설정이 되는지
  - 환경 설정 후 VMS 앱 실행 시 실제로 영상이 틀리는지도 확인해야함
- 수정 및 추가해야할 것 : 
  - 클라이언트 구성 시! **모니터링 구성 기능** 추가해야함
    - yaml 파일이 이미 Master 서버에 있다는 가정하에 시작
  - 파일 트랜스퍼



#### 0927

- 체크해야할 것 : 
  - 모니터링 기능 잘 되는지
    - 그라파나 띄워짐 : 192.168.0.29:30006
    - /add_newMonitoring(GET) -> json 응답값 : key=url 
  - **파일 트랜스퍼** 기능 어떻게 진행할지?
  - sudo 작업 계속 진행해야함...
    - sudo 는 잘 진행됨
    - os.environ 설정은 잘 되는데, 아래 작업들 더 고민해봐야함
      - 영상 보여주는 작업(계속 os.environ 이 바뀌지 않음)
      - **영상 data relay server**
        - **영상 데이터를 주고받는 형식이 되려면 어떻게 해야하는지 알아야할듯**
    - 다 좋은데 데이터 넘길때 지금은 cam_no 로 넘어가는데, device_url 정보가 넘어가야함



#### 0928

- connect_device ---- response_device.py 부분은 완료
  - disconnect_device 해야함
- 영상처리 어떻게할지
- 파일트랜스퍼부분



#### 0930

- connect_device, disconnect_device API 일단 구성
  - 구성은 해놨는데 연결 잘 되는지 확인해봐야함.....
  - 확인하면서 API 부분의 server ip, port 설정 잘해줘야 전달될듯?
  - 나중에 server ip,port 는 sw deploy 됐을때 번호로 바꿔줘야하는거같은데 추후에 고민
- 영상처리 어떻게할지 진행
  - 기존 처리방식에서 relayserver 방식으로 전체적 변경 필요할듯
  - relayserver 방식으로 하면 기존(1개 카메라만 연결)방식에서 다수 카메라 url 연결후 데이터 보관이 가능한지... 그렇다면 궁극적 목표 달성일듯
  - **기존 socket server-client 끼리 영상스트리밍데이터 주고받은것 처럼 릴레이서버 만들어보기(테스트로 다른폴더에 먼저 진행)**
  - **아니면 기존 response_device.py 로 진행하는데 gen부분으로 생성된 데이터를 다른서버에서 사용할 수 있는지 알아보고 사용**
  - **아니면 CAM 당 APP이 한개씩 배포되기...APP의 기능은 CAM 데이터를 저장하는기능.... VMS 에서는 해당 APP 의 데이터만 전달받으면 됨...**
- 파일 트랜스퍼 찾아보고 진행 - 예지누나가 진행중





#### 1001

- 영상처리 진행 -> 작년 결과처럼만 보여지게끔 하면될듯 = 다른 app 필요없이 app.py 에서 실행되게끔
  - **1. 기존 socket server-client 끼리 영상스트리밍데이터 주고받은것 처럼 릴레이서버 만들어보기(테스트로 다른폴더에 먼저 진행)**
  - **2. 기존 response_device.py 로 진행하는데 gen부분으로 생성된 데이터를 다른서버에서 사용할 수 있는지 알아보고 사용**
  - **3. CAM 당 APP이 한개씩 배포되기...APP의 기능은 CAM 데이터를 저장하는기능.... VMS 에서는 해당 APP 의 데이터만 전달받으면 됨...**
- **CAM 선택하는 SW 의 노트포트가 필요함...내가 아는정보는  server_id 뿐**
- 파일 전송될때 받아야하는 파일
  - Dockerfile (ex, app - Dockerfile)
  - 실제 SW file (ex, app.py)
- 체크 해야할 것
  1. response_device 가 노드포트사용X 이고 그냥 포트로 사용될 때 되는지
  2. sw 노드포트 알아오는 작업
     - 메모해둔대로 진행

- 완료
  - 예지누나 : 파일전송 윈도우-윈도우 가능/ 윈도우-리눅스 안됨 ERR_ADDRESS_UNREACHABLE 에러



#### 1006

- sw 노드포트 알아오는 작업(이거 먼저 진행해보기 - test.py 에서 진행 완료)
  - 메모해둔대로 진행
- **내일까지 완료해야 할 사항들 : ** 
  - **이전년도와 같이(방법은 변경될 수 있음) 카메라 보여지게끔** 
  - **sw노드포트 알아오는작업 진행**(완료) - **/test/test_nodeport.py -> connectdevice API에 사용중**
- 지금은 카메라 os.environ 설정부분 하고잇음 (response_device.py)
  - response_device 가 노드포트사용X 이고 그냥 포트로 사용될 때 되는지**(현재 진행중)**



#### 1007

- 지금은 카메라 os.environ 설정부분 하고잇음 (response_device.py)
  - response_device 가 노드포트사용X 이고 그냥 포트로 사용될 때 되는지**(현재 진행중)**
  - 현재 카메라 스탑, 실행은 되는데 컴퓨터 메모리 사용량 과부하로 너무 버벅됨...
    - ~~70 은 잘되는거같고, 60은 렉이 심함~~
    - 현재 60은 잘되고, 70 은 카메라 코덱 decode 에러..(h264)
      - 일단 vlc 에서 안되고 그냥 opencv 하면 되니까 그거로 진행
  - 일단 컴퓨터 다시 재부팅해서 실행해보고 다시 진행해보기
- 파일 전달하는거 리눅스에서 사용가능 **완료**
  - 현재는 기본 디렉토리 "다운로드"에 저장되는데 app.py 와 같은 위치의 폴더에 저장되게끔 변경 혹은 디렉토리 지정해주어야함
- 처음에 index 로 카메라 선택 사용할때 nodeport 를 전달해주어야하는데 어떻게..?



#### 1008

- UI 생각해보고 진행해야할 부분
  - 처음에 index 로 카메라 선택 사용할때 nodeport 를 전달해주어야하는데 어떻게..?
  - ~~그냥 opencv 창으로 띄워줘?~~
- ~~환경변수 설정때 source refresh 안되는거 해결방법 잇나?~~
  - **"/bin/bash -c 'source ~/.bashrc'" 이렇게 해결**
- 현재 다운로드는 파일 다운로드인데 폴더전체를 다운로드 할 수 있는지?
  - 다운받은다음 도커 이미지 빌딩할때, 위치도 해당 fname 따라서 지정해줘야함..?
    - type 에 따라 지정해줘도 될듯..도커파일은?
  - deploy할때 deployment 파일은 app.py 에 잇어야하나? - 이건 맞는듯 나중에 확인 가능
  - **일단 upload 시 zip 파일(docker+files)으로 받으면 압축풀고 도커이미지 생성까지 완료**
- **UI**
  - Index :
    - 위치 : Master 노드
    - 기능 : Master 에서 Worker1,2 로 카메라 켜주는 역할
    - 필요조건 : Worker 노드에 배포된 Camera select 앱의 **nodeport** 를 알고 있어야함
    - [버튼 CSS site](http://rwdb.kr/interactionbutton/)
  - Camer select :
    - 위치 : 각 Worker 노드
    - 기능 : VMS 에서 전달된 Cam 정보를 전달받고 / 스트리밍 해주는 역할



#### 1012

- 전체적으로 잘 돌아가는지 테스트해야함....
  - 예지누나랑 같이 진행 해야할듯
  - 내일 13일 다시 시작
- k8s 관련한 새로운 과제 시작 : 금승우책임님
  - 이 과제는 추후에 금책임님이 자료주시면 진행할 수 잇음
  - 다음주 영기씨랑 시작



#### 1013

- index.py 의 노드포트 연결부분
  - 지금은 지정된 노드포트 사용하는데, **client 단에서 API 호출 후 가져오는방안 구현하기**
    1. nodeport 및 nodename 찾아와서 index.html 에 뿌려주기
       - list 라는 데이터로 nodename, nodeport 보내줌(현재는 2개 데이터)
    2. 받아온 node 숫자대로 화면에 버튼만들기
       - 완벽하게 동적인 버튼은 아니지만 list 순서대로 2개 버튼 생성하기 완료
- 전체 연동 잘 되는지 테스트
  - 예지누나랑 같이 진행 해야할듯 - 10월동안 다른과제 진행, 내 파트 따로 임시데이터로 진행!
- 연동 전까지 필요한 작업들 완벽하게 완성시켜놓기 



#### 1014

- 연동 전까지 필요한 작업들 정리 후 완성해 나가기 시작



#### 1015

- 블록체인
- 연동전 작업들 정리



#### 1018

- 금책임님팀 자료 받고 우리 쿠버네티스 클러스터 구성해서 실행시켜보기
  - **타 k8s 프로젝트를 새로운 환경에 적용시키는 작업** : Project4 에서 실행



#### 1104

- 다시 프로젝트 재개..
  - 일단 내꺼 잘 돌아가는지 확인
  - index 부분에 json 데이터가 넘어온다고 명시되어있는데..어떻게 넘어오는건지?
    - 만약 데이터 전달이 어렵다면.. 해당 방법 말고 다른 방법을 사용할수 있는지 확인
- connect / disconnect 500 ERROR 뜨는데 해결 필요함
  - 카메라오면 가능하게끔 만들기
- index 부분 불러오는데 json 데이터 넘어오게끔,,, 설계서 수정해서 예지누나 전달드리기
- ~~add monitoring 부분 반환값에 url 고정인지? 고정이면 바꿔줘야함~~





#### 1105

- 책임님께 전달사항 전달드리고 4일 내용 진행 계속
- connect / disconnect 500 ERROR
  - 현재 nodeport 를 찾아와서 실행시켜야하는데 여기서 에러가 나는듯
    - 실제로 파일 배포해보면서 수정해야할듯?
- ~~add_newUploadSw 500 ERROR~~
  - ~~vms download api~~



#### 1108

- index 부분 불러오는데 json 데이터 사용하지말고.. worker 이름들은 사용 가능하니까 ~~worker 이름으로 예지누나 db 접근해서 찾아올수잇게끔..?~~
  - DB사용은 안하고 get_edgeList API 호출해서, nodename 으로 ID 찾아서 진행하는거로 완성
- connect / disconnect 500 ERROR
  - 현재 nodeport 를 찾아와서 실행시켜야하는데 여기서 에러가 나는듯
    - 실제로 파일 배포해보면서 수정진행
- SW upload 부분 `_` 사용이 안되서 수정해서 진행
- SW deploy 부분 배포는 되는데 에러나서...다시 진행해야함



#### 1110

- 배포부분 배포는 되는데 error 계속 생김 수정필요!
  - port 맞춰주는데도 계속 에러...
  - 계속 수정해보기
  - dockerfile build 중 python 실행파일의 위치를 찾지못해서 그랬음 해결!
  - 현재 잘 배포되고 running 되는데 잘 실행되는지 확인해야함
    - ~~**디바이스 연결도중 예지누나 서버가 다운됏는지 실행이안됨.. 내일 해결보기*~~*
- device connect, disconnect 부분 - 배포한 후에 계속 진행하기
- 카메라 연결이 안됨...
  - **내일 해결보기**



#### 1111

- 배포 완료, connect/disconnect 완료, 카메라 1대 연결 완료
- 
- 제대로 camera 정보도 nodeport 사용해서 넘어가는데.. 스트리밍이 안됨
  - exec 명령어로 pod 들어가서 확인해보기
  - ~~안됨쓰..황ㄴ경변수는 설정 잘 하는데 streaming 시작을 안함...~~
- 카메라 작동 확인
  - select-cam 폴더로 사용!
  - `kubectl logs -f [pod name]` 으로 pod 내에서 어떻게 동작하고 있는지 확인 가능



#### 1112

- 일단 완성한 부분 시연 보여드리고...
- 보완해야하는 부분
  - ~~지금은 마스터서버에서 카메라 스트리밍이 보여지는데 ..~~
  - ~~궁극적으로는 다른 컴퓨터에서 스트리밍이 되어야하는 부분...~~
  - ~~어떻게 할지~~ 
- DEMS 에서 카메라 연결하면 바로 카메라 구동 앱 보여지게끔 다음주 진행
- 에러 고치고 다시 보여드리기 완료!



#### 1115

- 할것 : A4 용지에 잘 적어놓았으니 그대로 시작해보기
  - DEMS 에서 카메라 연결하면 바로 카메라 구동 앱 보여지게끔 다음주 진행
    - UI 상에서 url+노드포트 찾아서 창 열어주는 방법으로 일단 진행
  - 프로메테우스 앱 업로드, 배포 하는 과정 보여주기 
  - 카메라 한대 더 추가해야함...need help
  
- print 해주는 내용들 채워주는중...

- 프로메테우스 업로드, 배포부분 업데이트 완료..실제 작동하는지 확인해야함

- 전체적 연동하는 과정에서 누나부분 /get_edgeInfo 부분 불러올때 에러가 나는데 확인 필요 내일!

  - 에러내용 

    ```ubu
    requests.exceptions.ConnectionError: HTTPConnectionPool(host='123.214.186.231', port=4882): Max retries exceeded with url: /get_edgeInfo?id=61404604ee9585d76f6f9479 (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7fc835715b90>: Failed to establish a new connection: [Errno 113] No route to host'))
    ```



#### 1116

- ~~연동에서 에러나는 부분 고치고~~  완료(컴퓨터 IP, 즉 API IP 가 자꾸 변경되서..IP 고정 : 192.168.0.69)
- 프로메테우스 앱 배포하는 과정부터 확인 <mark>**완성**</mark>
  - 프로메테우스, 스테이트 메트릭스 어디에 있는 파일이 실시되는지 확인
    - /k8s 에 있는 파일을 backup file 처리했음
    - 현재 node_selector.py - select 메소드 작업중인데..
      - 파일 경로를 /k8s 에 할지, 상위폴더에 할지...? **이거는 deployment maker.py 도 해당되는 내용**
      - 파일경로는 
        - **기본적으로 app.py 가 실행되는 위치에서 실행된다**



#### 1117

- prometheus 배포는 되니까, 배포삭제하는 부분도 백그라운드에서 실행되게끔 !!
  - remove_deploy API 에서 지워주게끔 했음
- UI 없이 카메라 화면 열어주는 작업 진행
  - connect_device, disconnect_device 에서 응답값에 url 추가해주면 될듯? (add_newMonitoring과 같음)
  - **다만 서버가 3대로 늘어났을때...카메라 바뀌는것을 어떻게 보여줄것인가...**



#### 1118

- **깃 다시 둘다 시작하기!!**
  - 깃 클론이 안됨..........
- UI 없이 카메라 화면 열어주는 작업 이대로 진행해보고...두번째꺼는 고민
  - connect_device, disconnect_device 에서 응답값에 url 추가해주면 될듯? (add_newMonitoring과 같음)
  - **다만 서버가 3대로 늘어났을때...카메라 바뀌는것을 어떻게 보여줄것인가...**
  - cam-select.py server 에서 
    - streaming 기능을 connect 기능에 합쳐서
    - post 명령이 오면 새롭게 refresh 가능하게끔...?
    - app.py ----> connect/disconcnect 변경했고
    - cam-select-test.py         두 파일로 진행



#### 1119

- cam 화면 auto refresh 하는 기능 구현중
  - html head 에 `<meta http-equiv="refresh" content="5" />` 추가
    - 5초마다 화면을 reload해줌
    - ~~top은 되는데 , stop 에서 다시 streaming 이 안됨..~~
  - 이제 구현은 되었는데 5초가 아닌 데이터가 변경되엇을때 reload되게끔
    - ajax 통신 + jquery setinterval()....안됨
    - socket 을 사용해야할것같은데........해보기



#### 1122

- socket 사용해서 웹 페이지 refresh 비동기통신 해보기

  - cam.html --- select-cam-test.py 두개로 테스트중

    ```javascript
    function show_article() {
        $('#articleBox').empty();
    
        $.ajax({
            type: "GET",
            url: "/api/top",
            data: {},
            success: function (response) {
              let articles = response['articles_list']
              for (let i = 0; i < articles.length; i++) {
                let article = articles[i];
    
                let code = article['category_code'];
                let body = article['article_body'];
                
                let append_one = make_article(code, body);
                
                $('#articleBox').append(append_one);
            }
        });
    }
    ```

- **화면 Refresh**

  - ajax 로 1초마다 데이터 불러와서
  - global 변수에 들어가있는 값과 다르면 refresh 해주기로 완성
  - 완성된 내용 쿠버네티스로 배포해보기
  - **내일 소켓으로 구현하는 방법 해보기.......**

- **DEMS UI -  `디바이스 연결설정` 에 추가해야하는 내용**

  - 연결 눌렀을 때 첫번째 클릭시에만
    - return 되는 json data `url` 로 화면 띄우기
  - 이후 클릭 시
    - 기존과 같은 형태여도 괜찮음



#### 1123

- 화면 refresh
  - ~~**내일 소켓으로 구현하는 방법 해보기.......**~~ 일단 지금 된거로 k8s 배포확인해보기
  - ~~점심먹고 서버->클라이언트 명령보내는거 해보기..~~ 일단 ajax 기존꺼로 진행
- - - 
- 김책임님 카메라연결부분 진행
  - 192.168.100.70:88 카메라 연결 완료
  - 현재 무선으로 2대 카메라와 AP 가 연결되어있음



#### 1124

- 추가된 카메라 추가하고 연결 잘되는지 확인
- **DEMS UI -  `디바이스 연결설정` 에 추가해야하는 내용**
  - 연결 눌렀을 때 첫번째 클릭시에만
    - return 되는 json data `url` 로 화면 띄우기
  - 이후 클릭 시
    - 기존과 같은 형태여도 괜찮음



#### 1125

- 추가된 카메라 연결 완료
  - cam1 : rtsp://keti:keti1234@192.168.0.60:8805
  - cam2 : rtsp://keti:keti1234@192.168.0.70:88
- 추가 카메라 한대 더 있는데 혼자 힘으로 연결해보기
  - 다음주 진행!
- `디바이스 연결설정` UI 창 뜨는부분 전달 완료..예지누나 작업중



#### 1129

- 커넥트, 디스커넥트부분 수정
- 자동클릭



#### 1130

- 오후에 책임님 보여드리기
  - 1안 : YES/NO 로 구분하여 딱 한번만 창이 켜지게끔
    - 만약 추가구현을 한다면 UI 밑부분에 연결된 node 누르면 화면 다시켜서 확인할 수 있게끔?
  - 2안 : 지금처럼 화면이 계속 켜지게끔
- 브라우저가 켜져있고 꺼져있음을 알수있게끔 하는 .. 무언가 있을까?
  - onunload 로 일단 구현완료

- 도커 build 시 pip install 오류가 있어서 지금 안되느중....해결plz..
  - `# systemctl restart docker ` **로 해결!!:)**




#### 1201

- 카메라 연결 이더넷-무선 충돌나는거 해결하는 방법잇나 찾아보기
  - 되면 거의 완벽하게 구현이 됨..
- 카메라 잘 작동되는지 확인



#### 1202

- **카메라 연결 이더넷-무선 충돌나는거 해결한듯!**
  - https://logon.tistory.com/747 : 18.04 버전에서는 ui로 변경이 안되서 command 로 변경
  - `/etc/NetworkManager/system-connections/` 에 위치한 '유선랜 설정' 파일에서 [ip4] 에 추가
    - `never-default=true`



#### 1203

- 예지누나 변경사항이랑 잘 연동되는지 전체적인 구동되는 거 확인



- 1207
  - onunload 가 작동이 안될때가 많아서........고쳐야함.......왜안되는걸까
    - 계속 될때도잇고 안될때도잇음
    - 카메라 켜진상태에선 안됨..
    - 왜?
    - 내생각에 ajax 통신이 1초에 한번씩 전달되서 그런듯..?
      - 2초로 늘려도 잘 안됨...일단 그대로 진행
      - <mark>아마도 ajax-async : false, 하면 될거같은데..일단 안됐었음</mark>




#### 1208

- 금책임님 이미그레이션 한 과제도 정리가 필요함
  - 카메라 연결 문제
  - UI 관련 문제
- 5G 과제 한거 일단 완료.. 내일 보여드리기!



#### 1209

- 금책임님 과제
  - 카메라 reset 해서 url  교체 후 ->> config 수정 후 재배포!
- 5G 과제 회의
  - 전체 보고서 작성 위한 영상촬영 : 16(금) 까지
  - DEMS operation synario :14(화) 까지
  - 카메라 지능관련-금책임님  또한 :16(금) 까지



#### 1210

- Axis 카메라 url 설정 완료하기
  - 월요일 추가로..
- 완료한 url로 config 수정 후 재배포
- ~~시나리오 받았으니 수정 및 추가할 부분 엑셀파일에 추가 + 스크립트도 생각해놓기~~
  - 1차적 완료, 화요일에 말씀 드린 후 더 추가할 부분 추가하기



#### 1213

- 영기씨 질문 (네트워크 구성)
  - ~~방법 1 (기존방식) : 지금 서버에서 카메라를 외부로 연결 가능하게 만들어, 해당 서버에서 사용가능하게~~
    - 현재 카메라 주소를 외부에서도 연결 가능하게 하는 방법?
  - 방법 2 : 유선으로 각 서버에 연결해서 지금 사용하는 url 을 사용(?)
    - 지금 사용하는 https://192.168.0.9/mjpg/1/video.mjpg 은 사용이 가능한지? (http -> https)
- 진행 과정
  - 현재 사용하는 무선 공유기1 과 공유기2(new)를 유선 LAN 선으로 연결 
  - 공유기2를 hub 로 사용하기위해 설정 변경
    - 참고 : https://mirunamuman.tistory.com/11
  - 공유기2 에 카메라 연결 
    - 공유기2 주소 : 192.168.0.208
    - 카메라 주소 : 169.254.213.166



#### 1214

- 일단 project4 는 실행 완료
  - 캡쳐해서 전달 완료
- console 창에 뿌려줄 내용들 project4 참고하여 추가해보기
  - app.py 에 print  내용들은 전부 수정해줌
- 시연 촬영
  - 오늘은 DEM UI 파트 촬영 완료 후
  - 내일부터 console 창 파트 촬영 진행하기
    - console 창 콘티 먼저 짜서 진행



#### 1215

- DEMS 콘솔 화면 촬영 완료



#### 1216

- 촬영 편집 의뢰 완료
- 촬영 편집 완료되는대로 확인 받고 스크립트 구성하기



#### 0308

- 이사 후 컴퓨터 resetting 및 원격
- 원격이 잘 연결이 안됨
  - keti0 : 아예 원격 연결이 안됨
    - 192.168.0.29
    - xrdp, xorg,  xfce4 설치
  - keti1 : 빈화면만 뜸
    - 192.168.0.32
    - xrdp, xfce4 설치, xorg 등등 설치하니까 시작은 됨
    - 그런데 너무 느려서 사용하기 힘듬
      - **해상도 낮추니 해결!**
  - keti2 : ~~접속안되고 튕김~~ **xrdp, xorg,  xfce4 모두 설치하고 해결!**
    - 192.168.0.33
    - xrdp, xorg  만 설치
    - xfce4는 설치 했는데 계속 튕김



#### 0314

- keti0 도 원격 가능하게 만든 뒤 
- 카메라 연결 하기