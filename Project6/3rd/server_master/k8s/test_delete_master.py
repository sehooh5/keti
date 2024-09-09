import os
import sys
import paramiko
import getpass
import time


cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

os.system(f"kubectl delete node keti0-master")

cli.connect("192.168.0.29", port=22, username="keti0", password="keti")

stdin, stdout, stderr = cli.exec_command(
    "echo y | sudo kubeadm reset", get_pty=True)
stdin.write('keti\n')
stdin.flush()

lines = stdout.readlines()
print(''.join(lines))

time.sleep(2.0)
cli.close()
