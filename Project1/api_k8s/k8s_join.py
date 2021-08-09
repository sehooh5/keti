import os
import sys
import paramiko
import getpass
import time
# kubeadm join 192.168.0.29:6443 --token m33kvg.xta9556i5lobye1v \
#    --discovery-token-ca-cert-hash sha256:288c16783a76640c705faa77c170272e02b06668d3b8b00732d3bad3c0527cb1

# 다른 서버에 명령 보낼때 사용
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 임시로 파이썬 실행시 아규먼트로 전달
wip = sys.argv[1]
wname = sys.argv[2]
wpwd = sys.argv[3]
w_input = "sudo kubeadm join 192.168.0.29:6443 --token m33kvg.xta9556i5lobye1v \
    --discovery-token-ca-cert-hash sha256:288c16783a76640c705faa77c170272e02b06668d3b8b00732d3bad3c0527cb1"
cli.connect(wip, port=22, username=wname, password=wpwd)

stdin, stdout, stderr = cli.exec_command(w_input, get_pty=True)
stdin.write('keti\n')
stdin.flush()

lines = stdout.readlines()
print(''.join(lines))

time.sleep(2.0)
cli.close()

# 1. 인터넷사용
# os.system(f"kubeadm join 10.244.0.1 --token k1caaa.ru6kcyp598l0hx6z")

# 2. 이더넷 사용
# os.system(f"kubeadm join 192.168.100.5:6443 --token k1caaa.ru6kcyp598l0hx6z")
