import os
import sys
import paramiko
import getpass
import time

# 다른 서버에 명령 보낼때 사용
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 임시로 파이썬 실행시 아규먼트로 전달
# 나중에 입력받는 값으로 바꿔줘야함
wip = sys.argv[1]
wname = sys.argv[2]
wpwd = sys.argv[3]
# 나중에 마스터 설정할때 나오는 명령문으로 바꿔줘야함
w_input = "sudo kubeadm join 192.168.0.29:6443 --token iixxe9.0cph4xryuggpkbeu     --discovery-token-ca-cert-hash sha256:b98ec0b1def87c7cffa1b20f2ba37d5c563634cfa0eb9b5ab94e9f79eddb0405"
cli.connect(wip, port=22, username=wname, password=wpwd)

stdin, stdout, stderr = cli.exec_command(w_input, get_pty=True)
stdin.write('keti\n')
stdin.flush()

lines = stdout.readlines()
print(''.join(lines))

time.sleep(2.0)
cli.close()

# 나중에 위 명령문 실행 후 아래 명령문도 실행해줘야된다
# $ mkdir -p $HOME/.kube
# $ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
# $ sudo chown $(id -u):$(id -g) $HOME/.kube/config
# $ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
