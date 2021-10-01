
cam_url = "rtsp://keti:keti1234"
p = f"echo keti | sudo echo 'export OPENCV_CAMERA_SOURCE={cam_url}' >> ~/.bashrc"
