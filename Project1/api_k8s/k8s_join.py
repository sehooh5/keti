import os
import sys
import paramiko
import getpass
import time
# token 210809 : k1caaa.ru6kcyp598l0hx6z


# 다른 서버에 명령 보낼때 사용
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

# 임시로 파이썬 실행시 아규먼트로 전달
wip = sys.argv[1]
wname = sys.argv[2]
wpwd = sys.argv[3]
w_input = "sudo kubeadm join 192.168.100.5:6443 --token k1caaa.ru6kcyp598l0hx6z --discovery-token-ca-cert-hash sha256:7f1758ca4cfd117cda27099644cbe4ef672559a47ab33dce8dd87ddf2e8bea1c"
cli.connect(wip, port=22, username=wname, password=wpwd)
stdin, stdout, stderr = cli.exec_command(w_input)
time.sleep(1.0)
cli.close()

# 1. 인터넷사용
# os.system(f"kubeadm join 10.244.0.1 --token k1caaa.ru6kcyp598l0hx6z")

# 2. 이더넷 사용
# os.system(f"kubeadm join 192.168.100.5:6443 --token k1caaa.ru6kcyp598l0hx6z")
