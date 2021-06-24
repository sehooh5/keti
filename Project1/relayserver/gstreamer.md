# gstreamer

- gstremaer 를 사용하여 영상 relay server 구축
- 개발환경 : 
  - ubuntu
  - rtsp camera
  - python





## 개발내용

1. Gstreamer 및 Gst RTSP server 설치
2. Gstreamer RTSP server 를 python 을 이용하여 스트리밍



### Gstreamer 및 Gst RTSP server 설치

---



#### 1. GStreamer 설치

- 설치 확인 우분투의 경우 GStreamer가 기본으로 깔려 있는 경우가 있어서 설치 확인

  ```shell
  $ which gst-launch-1.0
  
  -> /usr/bin/gst-launch-1.0 뜨면 설치 되어있는것
  ```

  

- 패키지 설치 

  - GStreamer 라이브러리 설치

    ```shell
    sudo apt-get install libgstreamer1.0-0 
    sudo apt-get install gstreamer1.0-plugins-base gstreamer1.0-plugins-good 
    sudo apt-get install gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly 
    sudo apt-get install gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools 
    ```

     

  - python  패키지 설치

    ```shell
    sudo apt-get install python-gst-1.0 python3-gst-1.0
    ```

     

  - dev-packages 설치

    ```shell
    sudo apt-get install libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev 
    sudo apt-get install libfontconfig1-dev libfreetype6-dev libpng-dev 
    sudo apt-get install libcairo2-dev libjpeg-dev libgif-dev 
    sudo apt-get install libgstreamer-plugins-base1.0-dev
    ```

     

- 설치 확인

  ```shell
  $ gst-launch-1.0 videotestsrc ! autovideosink
  
  -> 화면이 뜨면 설치완료!
  ```

  



#### 2.Gst RTSP server 설치

- gir1.2-gst-rtsp-server-1.0 패키지를 설치해야 GstRtspServer이 가동이 가능하게 됩니다.

  ```shell
  $ sudo apt-get install gir1.2-gst-rtsp-server-1.0
  ```

  





### Gstreamer RTSP server 를 python 을 이용하여 스트리밍

---



#### 1. Streaming server 예제소스 분석 [소스 출처](https://github.com/tamaggo/gstreamer-examples/blob/master/test_gst_rtsp_subtitles_server.py)

```python
#import 하는 부분은 다들 아실테니 넘어가고
import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GstRtspServer, GObject
#메인이 시작됩니다.
if __name__ == '__main__':
    #루프를 선언하는데 이게 GstRtspServer의 루프입니다.
	loop = GObject.MainLoop()
	GObject.threads_init()
	Gst.init(None)

	class MyFactory(GstRtspServer.RTSPMediaFactory):
		def __init__(self):
			GstRtspServer.RTSPMediaFactory.__init__(self)
        #팩토리에 들어갈 영상의 파이프라인을 설정하는 부분입니다.
        #아래에서 해당 함수를 콜하는 부분이 없지만 init 될때와 서버가
        #기동해서 루프돌고 있을때 참조해서 가동하게 됩니다.
		def do_create_element(self, url):
			#여기에 파이프라인을 형성할 영상의 주소와 그 설정을 넣게 됩니다.
            spec = """
			filesrc location=test.mp4 ! qtdemux name=demux
			demux.video_0 ! queue ! rtph264pay pt=96 name=pay0
			demux.audio_0 ! queue ! rtpmp4apay pt=97 name=pay1
			demux.subtitle_0 ! queue ! rtpgstpay pt=98 name=pay2
			"""
			return Gst.parse_launch(spec)

  	class GstServer():
		def __init__(self):
            #GstRtspServer를 클래스 내에서 선언하고
			self.server = GstRtspServer.RTSPServer()
            #포트를 지정해줍니다.
			self.server.set_service("3002")
            #팩토리를 생성하는데 이 부분은 위의 MyFactory 클래스에서 설명하겠습니다.
			f = MyFactory()
            #이 팩토리를 공유 할것이라 설정하고
			f.set_shared(True)
            #서버 마운트 포인트를 선언하고
			m = self.server.get_mount_points()
            #마운트 포인트에 주소와 공유할 팩토리를 넣어줍니다.
			m.add_factory("/test", f)
			self.server.attach(None)

    # GstServer 클래스로 서버 설정을 마치고
	s = GstServer()
    #서버 루프를 돌립니다.
	loop.run()
```

- 자꾸 gi 모듈이 없다고 에러남

  ```
  $ pip install PyGObject 
  
  -> 입력해서 설치해주니 일단 넘어가는데 또 에러!
  ```

  

