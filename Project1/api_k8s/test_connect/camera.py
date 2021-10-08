import cv2
import os

print("카메라 설정 : ", os.environ['OPENCV_CAMERA_SOURCE'])


def open():
    cap = cv2.VideoCapture(os.environ['OPENCV_CAMERA_SOURCE'])

    while True:

        # Image read
        ret, image = cap.read()
        # image show
        cv2.imshow('stream', image)
        # q 키를 누르면 종료
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


open()
