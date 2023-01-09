import paramiko
import getpass
import time
import sys

cam_no = sys.argv[1]

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

cli.connect("192.168.0.32", port=22, username="keti1", password="keti")

del_url = "sudo sed -i '/OPENCV_CAMERA_SOURCE/d' ~/.bashrc"
del_stop = "sudo sed -i '/CAMERA_STOP/d' ~/.bashrc"
refresh = "source ~/.bashrc"

if cam_no == "1":
    new_url = "sudo echo 'export OPENCV_CAMERA_SOURCE=rtsp://keti:keti1234@192.168.100.70:8810/videoMain' >> ~/.bashrc"
    new_stop = "sudo echo 'export CAMERA_STOP=None' >> ~/.bashrc"
    stdin, stdout, stderr = cli.exec_command(w_input, get_pty=True)
    stdin.write('keti\n')
    stdin.flush()

elif cam_no == "2":
    cam_url = "rtsp://keti:keti1234@192.168.100.60:8805/videoMain"
    cam_stop = "None"
elif cam_no == 'stop':
    cam_stop = "stop"


stdin, stdout, stderr = cli.exec_command(w_input, get_pty=True)
stdin.write('keti\n')
stdin.flush()
lines = stdout.readlines()
print(''.join(lines))

cli.close()
