import cv2

url = 'rtsp://root:keti@192.168.100.93/onvif-media/media.amp?rofile=profile_1_h264&sessiontimeout=60&streamtype=unicast'
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
