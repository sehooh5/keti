import os
import sys
import paramiko
import getpass
import time


cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# os.system(f"kubectl delete node keti1-worker1")

cli.connect("192.168.0.32", port=22, username="keti1", password="keti")
stdin, stdout, stderr = cli.exec_command(
    "echo y | sudo kubeadm reset", get_pty=True)
stdin.write('keti\n')

stdin.flush()


lines = stdout.readlines()
print(''.join(lines))

time.sleep(2.0)
cli.close()

# wip = ["192.168.0.29", "192.168.0.32", "192.168.0.33"]
# wname = ["keti0", "keti1", "keti2"]
# whname = ["keti0-master", "keti1-worker1", "keti2-worker2"]
# wpwd = ["keti", "keti", "keti"]

# for ip, name, hname, pwd in zip(wip, wname, whname, wpwd):

#     os.system(f"kubectl delete node {hname}")

#     cli.connect(ip, port=22, username=name, password=pwd)
#     print("1")
#     stdin, stdout, stderr = cli.exec_command(
#         "sudo kubeadm reset", get_pty=True)
#     print("2")
#     stdin.write('keti\n')
#     print("3")
#     stdin.flush()
#     print("4")

#     time.sleep(2.0)
#     cli.close()


# cli.connect("192.168.0.29", port=22, username="keti0", password="keti")

# stdin, stdout, stderr = cli.exec_command(
#     "sudo ifconfig", get_pty=True)
# stdin.write('keti\n')
# stdin.flush()

# lines = stdout.readlines()
# print(''.join(lines))

# time.sleep(2.0)
# cli.close()
