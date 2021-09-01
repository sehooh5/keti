import os
import sys
import paramiko
import getpass
import time


cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# mname = sys.argv[1]

wip = ["192.168.100.5", "192.168.100.6", "192.168.100.7"]
wname = ["keti0", "keti1", "keti2"]
whname = ["keti0-master", "keti1-worker1", "keti2-worker2"]
wpwd = ["keti", "keti", "keti"]

for ip, name, hname, pwd in zip(wip, wname, whname, wpwd):

    os.system(f"kubectl delete node {hname}")

    cli.connect(ip, port=22, username=name, password=pwd)

    stdin, stdout, stderr = cli.exec_command(
        "echo y | sudo kubeadm reset", get_pty=True)
    stdin.write('keti\n')
    stdin.flush()

    lines = stdout.readlines()
    print(''.join(lines))

    time.sleep(2.0)
    cli.close()
