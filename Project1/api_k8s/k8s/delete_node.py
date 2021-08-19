import os
import sys
import paramiko
import getpass
import time


cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

mname = sys.argv[1]

wip = ["192.168.0.32", "192.168.0.33"]
wname = ["keti1", "keti2"]
whname = ["keti0-master", "keti1-worker1", "keti2-worker2"]
wpwd = ["keti", "keti"]

for ip, name, pwd in zip(wip, wname, wpwd):

    os.system(f"kubectl delete node {arg}")

    cli.connect(ip, port=22, username=name, password=pwd)

    stdin, stdout, stderr = cli.exec_command(
        "sudo kubeadm reset", get_pty=True)
    stdin.write('keti\n')
    stdin.flush()

    lines = stdout.readlines()
    print(''.join(lines))

    time.sleep(2.0)
    cli.close()
