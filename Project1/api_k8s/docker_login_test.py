import os
import subprocess

# 로그인 되어있는지 확인
d_login_status=subprocess.check_output("docker info | grep Username", shell=True, errors=None).decode('utf-8')
#print(d_login_status)

# 로그인 시도
# os.system("docker login -u sehooh5 -p @Dhtpgh1234")

