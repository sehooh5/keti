import paramiko

# 다른 서버에 명령 보낼때 사용
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

cli.connect('192.168.0.28', port=22, username="keti2", password="keti")
stdin, stdout, stderr = cli.exec_command("hostname", get_pty=True)
stdin.write('keti\n')
stdin.flush()
lines = stdout.readlines()
print(''.join(lines))

cli.close()