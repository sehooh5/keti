import os
import sys
import paramiko
import getpass
import time

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 나중에 입력받는 값으로 바꿔줘야함
wip = sys.argv[1]
wname = sys.argv[2]
wpwd = sys.argv[3]

cli.connect(wip, port=22, username=wname, password=wpwd)

stdin, stdout, stderr = cli.exec_command("reboot")
print("rebooting!=====")

time.sleep(2.0)
cli.close()
