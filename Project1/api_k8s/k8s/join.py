import os
import sys
import paramiko
import getpass
import time
import subprocess


# 임시로 파이썬 실행시 아규먼트로 전달
# 나중에 입력받는 값으로 바꿔줘야함
# wip = sys.argv[1]
# wname = sys.argv[2]
# wpwd = sys.argv[3]
# # 나중에 마스터 설정할때 나오는 명령문으로 바꿔줘야함
# w_input = "sudo kubeadm join 192.168.0.29:6443 --token iixxe9.0cph4xryuggpkbeu     --discovery-token-ca-cert-hash sha256:b98ec0b1def87c7cffa1b20f2ba37d5c563634cfa0eb9b5ab94e9f79eddb0405"
# cli.connect(wip, port=22, username=wname, password=wpwd)

# stdin, stdout, stderr = cli.exec_command(w_input, get_pty=True)
# stdin.write('keti\n')
# stdin.flush()

# lines = stdout.readlines()
# print(''.join(lines))

# time.sleep(2.0)
# cli.close()


mip = "192.168.0.29"
# sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=192.168.0.29
# 마스터 엣지 구성
m_output = os.popen(
    f"sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address={mip}").read()
print("print : ", m_output)
# 마스터 - 워커 연결해주는 명령어
w_input = m_output.split('root:')[-1].lstrip()
print("print : ", w_input)
# 마스터에서 설정해줘야 하는 내용
os.system("mkdir -p $HOME/.kube")
time.sleep(2.0)
os.system("yes | sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
time.sleep(2.0)
os.system("sudo chown $(id -u):$(id -g) $HOME/.kube/config")
time.sleep(2.0)
os.system("kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml")
time.sleep(2.0)


# 다른 서버에 명령 보낼때 사용
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

wip = ["192.168.0.32", "192.168.0.33"]
wname = ["keti1", "keti2"]
wpwd = ["keti", "keti"]
w_input = f"sudo {w_input}"

for ip, name, pwd in zip(wip, wname, wpwd):
    ### 여기서 wlist 로 wid 차례대로 가져와서 원격으로 접속한 뒤 w_input 입력해주기 ###
    cli.connect(ip, port=22, username=name, password=pwd)
    stdin, stdout, stderr = cli.exec_command(w_input, get_pty=True)
    stdin.write('keti\n')
    stdin.flush()
    lines = stdout.readlines()
    print(''.join(lines))
    time.sleep(2.0)
    cli.close()

print(f"마스터노드와 {wname} 노드 연결...ip 주소 : {wip}")
os.system("kubectl get node")
