import cv2
import os

url = "rtsp://keti:keti1234@192.168.100.70:8810/videoMain"
print(os.environ['OPENCV_CAMERA_SOURCE'])


def open(url):
    print("Camera url :", url)
    cap = cv2.VideoCapture(url)

    while True:

        # Image read
        ret, image = cap.read()
        # image show
        cv2.imshow('stream', image)
        # q 키를 누르면 종료
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


# open(url)
