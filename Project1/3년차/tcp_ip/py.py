e_ip = "192.168.0.60"
print('cvlc -vvv rtp://%s:5004 --sout="#rtp{sdp=rtsp://:8554/videoMain}" --no-sout-all --sout-keep'%e_ip)
