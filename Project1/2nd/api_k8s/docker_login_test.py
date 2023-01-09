import os
import subprocess

# 도커 로그인 되어있는지 확인
try:
    print("Docker login status is Checking...")
    subprocess.check_output("docker info | grep Username", shell=True).decode('utf-8')
except subprocess.CalledProcessError:
    print("Docker login status : none")
    print("Docker login..")
    os.system("docker login -u sehooh5 -p @Dhtpgh1234")




# 로그인 시도
# os.system("docker login -u sehooh5 -p @Dhtpgh1234")

