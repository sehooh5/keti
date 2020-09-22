# Flask-video-streaming

- Flask 를 사용, 도커 컨테이너를 만들어 웹 서비스를 Get, Post 방식으로 전달



## Miguel 개발자 자료 해석

### 필요한 파이썬 지식

---

- `b` : byte 로 만들어 준다 (ex. b'hello')
- `mimetype` : 파일 변환, 파일을 텍스트로 전환해서 이메일에 전달하기 위해 개발
  - `multipart/x-mixed-replace; boundary=frame` : [server push](https://qaos.com/sections.php?op=viewarticle&artid=272)
    - `multipart` : 복합문서
    - `x-` : 정식으로 표준화되지 않은 형식
    - `boundary` : 복합문서 내의 각 문서들을 구별하는 분리자를 지정
    - 예를 들어 gif 이미지를 MIME 형식에 적용하면 하나의 gif 를 표시하고 다음에 다른 gif  가 그것을 대치하고 여러 파일들이 계속 대체하여 애니메이션 구현
    - 쉽게 말해서 영상이 스트리밍되는 시점이 바로 이 시점(?)
- `os` : 환경설정에 대한 정보를 가져올 수 있다
  - `os.environ['HOME']`
  - `os.environ.get('CAMERA')`
- 터미널에서 `CAMERA=opencv` 로 환경 설정을 해줄 수 있다





### Code

---

#### app.py

```python

```



#### camera_opencv.py

```python

```



#### base_camera.py

```python

```





## 문제점

1. Flask 의 웹서버를 사용하는 경우 한번에 하나의 연결만 처리 가능..한개의 스트림만 작동 가능

---

## 참고 자료

1. [Python-Flask-Docker 통신 - 네이버](https://m.blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221585566556&proxyReferer=https:%252F%252Fwww.google.com%252F)

2. [Miguel - flask-video-streaming](https://github.com/miguelgrinberg/flask-video-streaming) - 이 전체 앱이 컨테이너화 되는 느낌

3. [Miguel 자료 기초](https://blog.miguelgrinberg.com/post/video-streaming-with-flask)

4. [Miguel 자료 opencv 심화](https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited)

   

