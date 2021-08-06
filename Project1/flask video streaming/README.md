# Flask-video-streaming

- Flask 를 사용
- Kubernetes 를 사용하여 배포





### 필요한 파이썬 지식

---

- `b` : byte 로 만들어 준다 (ex. b'hello')
- `mimetype` : 파일 변환, 파일을 텍스트로 전환해서 이메일에 전달하기 위해 개발
  - `multipart/x-mixed-replace; boundary=frame` : [server push](https://qaos.com/sections.php?op=viewarticle&artid=272)
    - `multipart` : 복합문서
    - `x-` : 정식으로 표준화되지 않은 형식
    - `boundary` : 복합문서 내의 각 문서들을 구별하는 분리자를 지정
    - 예를 들어 gif 이미지를 MIME 형식에 적용하면 하나의 gif 를 표시하고 다음에 다른 gif 가 그것을 대치하고 여러 파일들이 계속 대체하여 애니메이션 구현
    - 쉽게 말해서 영상이 스트리밍되는 시점이 바로 이 시점(?)
- `os` : 환경설정에 대한 정보를 가져올 수 있다
  - `os.environ['HOME']`
  - `os.environ.get('CAMERA')`
- 터미널에서 `CAMERA=opencv` 로 환경 설정을 해줄 수 있다





### Code

---

#### app.py

- 웹 앱으로 `./templates/index.html` 을 열고 저장되어있는 frame 들을 읽어서 전달

```python
#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

# 1. import camera driver
# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from camera import Camera

# 2. 카메라 opencv 로 처음부터 지정
Camera = import_module('camera_opencv').Camera


# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def select():
    """Video streaming home page."""
    return render_template('select.html')


@app.route('/cam', methods=['GET'])
def camera():
    """Camera1 streaming"""
    # url 의 파라미터 값을 가져오는 방법
    no = request.args.get('no')
    # print('number = '+request.args.get('no'))
    if no == '1':
        os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.70:8810/videoMain'
    elif no == '2':
        os.environ['OPENCV_CAMERA_SOURCE'] = 'rtsp://keti:keti1234@192.168.100.60:8805/videoMain'

    return render_template('camera.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

```



#### camera_opencv.py

- opencv 를 사용하여 영상을 읽어서 이미지를 `.jpg` 로 인코딩해주는 파일
- print 하여 각각 작동하는지 여부 및 어떤 값이 들어오는지 확인하는 코드 수정
- 터미널에서 실행 시 환경변수(이 파일에선 OPENCV_CAMERA_SOURCE) 입력해주어야 한다
  - `CAMERA=opencv OPENCV_CAMERA_SOURCE=rtsp://keti:keti1234@192.168.100.70:8810/videoMain python app.py`

```python
import os
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0
    print("0")

    def __init__(self):
        print("1")
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(os.environ['OPENCV_CAMERA_SOURCE'])
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        print("2")
        Camera.video_source = source

    @staticmethod
    def frames():
        print("3")
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        else:
            print("Video Streaming On !")
        while True:
            # read current frame
            _, img = camera.read()
            # print(img) ... return  decode frame
            # print(_) ... return True or False

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

```



#### base_camera.py

- 기본 카메라에 대한 정보(공부 및 해석 필요)
- 수정한 것 없음

```python
import time
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    event = CameraEvent()

    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            # start background frame thread
            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        BaseCamera.last_access = time.time()

        # wait for a signal from the camera thread
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        """"Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None

```





### Dockerfile

- 도커 이미지 빌드를 위한 Dockerfile
- 기본적인 패키지들과 `requirement.txt` 를 인식을 못해서 직접 인스톨해주었다
- `Working Directory` 를 복사해서 `workspace` 란 폴더로 지정해주었다
- 여기서는 Flask 를 사용하기 때문에 자동으로 포트번호가 5000 이지만, EXPOSE로 다시 지정해주었다
- 도커 실행과 동시에 `app.py` 파일이 실행되게끔 하였다

```dockerfile
FROM python:3.7

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install click Flask itsdangerous Jinja2 MarkupSafe Werkzeug numpy

WORKDIR /
ADD . /workspace
ENV OPENCV_VERSION="4.1.0"
RUN pip install opencv-python
RUN ln -s \
  /usr/local/python/cv2/python-3.7/cv2.cpython-37m-x86_64-linux-gnu.so \
  /usr/local/lib/python3.7/site-packages/cv2.so

EXPOSE 5000
CMD ["python", "workspace/app.py"]


```





### deployment.yaml

- k8s 배포를 위한 `deployment.yaml`

- port 번호는 아직 확실하게 지정하지 않았고, 서비스를 NodePort 를 사용해 외부와 통신 가능

- <mark>1. 앞으로 ReplicaSet 사용하지 않을 것이다..우린 지정해서 사용해야함</mark>

  <mark>2. NodePort 지정 : url 정보 사용할 때 지정된 것 사용하려고..</mark>

  <mark>3. sleep 하는 명령어 있었는데 사용하면 k8s 내 앱 제대로 실행 안되서 지움</mark>

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-opencv-service
spec:
  selector:
    app: flask-opencv
  ports:
    - protocol: "TCP"
      port: 6060
      targetPort: 5000
      nodePort: 30001
  type: NodePort

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-opencv
spec:
  selector:
    matchLabels:
      app: flask-opencv
  replicas: 1
  template:
    metadata:
      labels:
        app: flask-opencv
    spec:
      containers:
        - name: flask-opencv
          image: sehooh5/flask-opencv:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 5000

```





---



## 참고 자료

1. [Python-Flask-Docker 통신 - 네이버](https://m.blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221585566556&proxyReferer=https:%252F%252Fwww.google.com%252F)

2. [Miguel - flask-video-streaming](https://github.com/miguelgrinberg/flask-video-streaming) - 이 전체 앱이 컨테이너화 되는 느낌

3. [Miguel 자료 기초](https://blog.miguelgrinberg.com/post/video-streaming-with-flask)

4. [Miguel 자료 opencv 심화](https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited)
