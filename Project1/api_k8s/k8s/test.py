import os
import sys
import paramiko
import getpass
import time
import subprocess

# 다른 서버에 명령 보낼때 사용
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

w_input = "sudo kubeadm join 192.168.0.29:6443 --token ccwbg2.mxandio4t3xw70tc \
    --discovery-token-ca-cert-hash sha256:3634571886e38e3bb79c21e39b1c4ce974d9b9fc4ba8d8f61e2cb22487128f20"
wip = "192.168.0.32"
wname = "keti1"
wpwd = "keti"
print(wip, wname, wpwd)
### 여기서 wlist 로 wid 차례대로 가져와서 원격으로 접속한 뒤 w_input 입력해주기 ###
cli.connect(wip, port=22, username=wname, password=wpwd)
stdin, stdout, stderr = cli.exec_command(w_input, get_pty=True)
stdin.write('keti\n')
stdin.flush()
lines = stdout.readlines()
print(''.join(lines))
time.sleep(2.0)
cli.close()
print(f"마스터노드와 {wname} 노드 연결...ip 주소 : {wip}")

# s = os.system(
#     f"yes | sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
# s.stdin.write("y")
