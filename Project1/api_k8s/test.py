import subprocess

try:
    output = subprocess.check_output(
        "kubectl get ns monitoring", shell=True).decode('utf-8')
except subprocess.CalledProcessError:
    print("error")
