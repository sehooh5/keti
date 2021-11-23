import os
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(os.environ['OPENCV_CAMERA_SOURCE'])
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        print("비디오 소스 : ", source, flush=True)
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        else:
            print("Video Streaming On !", flush=True)
        while True:
            _, img = camera.read()
            img = cv2.resize(img, dsize=(1280, 720),
                             interpolation=cv2.INTER_LINEAR)
            yield cv2.imencode('.jpg', img)[1].tobytes()
