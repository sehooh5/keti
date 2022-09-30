import os
import subprocess

# 로그인 되어있는지 확인
try:
    print("try!!")

except subprocess.CalledProcessError:
    print("docker login status : none")
    os.system("docker login -u sehooh5 -p @Dhtpgh1234")

d_login_status = subprocess.check_output("docker info | grep Username", shell=True).decode('utf-8')
print("docker status : ", d_login_status)


# 로그인 시도
# os.system("docker login -u sehooh5 -p @Dhtpgh1234")

