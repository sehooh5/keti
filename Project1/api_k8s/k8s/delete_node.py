import os
import sys
import paramiko
import getpass
import time


arg = sys.argv[1]
os.system(
    f"kubectl delete node {arg}")

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 나중에 입력받는 값으로 바꿔줘야함
wip = sys.argv[1]
wname = sys.argv[2]
wpwd = sys.argv[3]

cli.connect(wip, port=22, username=wname, password=wpwd)

stdin, stdout, stderr = cli.exec_command("sudo kubeadm reset", get_pty=True)
stdin.write('keti\n')
stdin.flush()

lines = stdout.readlines()
print(''.join(lines))

time.sleep(2.0)
cli.close()
