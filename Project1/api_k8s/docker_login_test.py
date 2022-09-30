import os
import subprocess

# 로그인 되어있는지 확인
try:
    subprocess.check_call(["docker","info","|", "grep", "Username"])
except subprocess.CalledProcessError:
    print(" Non-zero status  ")

# d_login_status=subprocess.check_output("docker info | grep Username", shell=True).decode('utf-8')
#print(d_login_status)

# 로그인 시도
# os.system("docker login -u sehooh5 -p @Dhtpgh1234")

