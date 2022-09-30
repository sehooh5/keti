import os
import subprocess

# 로그인 되어있는지 확인
pipe= subprocess.Popen("docker info | grep Username",stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
if "" == pipe.stdout.readline():
    print("Success")
    self.isCommandExectutionSuccessful = True

if not "" == pipe.stderr.readline():
    print("Error")
    self.isCommandExectutionSuccessful = True

print("  --------------  ")
# d_login_status=subprocess.check_output("docker info | grep Username", shell=True).decode('utf-8')
#print(d_login_status)

# 로그인 시도
# os.system("docker login -u sehooh5 -p @Dhtpgh1234")

