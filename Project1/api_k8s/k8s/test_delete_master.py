import os
import sys
import paramiko
import getpass
import time


os.system(f"kubectl delete node keti0-master")


os.system("echo y | sudo kubeadm reset")
stdin.write('keti\n')
stdin.flush()

lines = stdout.readlines()
print(''.join(lines))

time.sleep(2.0)
cli.close()
