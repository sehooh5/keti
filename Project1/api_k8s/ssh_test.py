import paramiko
import getpass
import time

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

# 1. 주소 혹은 서버이름, 2. port 22, 3. 사용자 이름, 4. 비밀번호
cli.connect("keti1-worker1", port=22, username="keti1", password="keti")
# cli.connect("10.244.1.1", port=22, username="keti1", password="keti") 윈도우-리눅스 실행 안됨
stdin, stdout, stderr = cli.exec_command("mkdir test01")
# stdin, stdout, stderr = cli.exec_command("rm -rf test01")
lines = stdout.readlines()
print(''.join(lines))

cli.close()
