import os
import subprocess


    os.system("echo yes | sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
    command = "sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config"
    result = subprocess.run(f"echo yes | {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if result.returncode == 0:
        print("명령어 실행 성공.")
    else:
        print(f"오류 발생: {result.returncode}")
        print(result.stderr)
