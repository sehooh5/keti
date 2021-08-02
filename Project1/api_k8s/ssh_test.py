import paramiko
import getpass
import time

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)


cli.connect("10.244.1.1", port=22, username="keti1", password="keti")
stdin, stdout, stderr = cli.exec_command("mkdir test01")
# stdin, stdout, stderr = cli.exec_command("rm -rf test01")
lines = stdout.readlines()
print(''.join(lines))

cli.close()
