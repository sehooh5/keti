import sys
import subprocess

if sys.argv[1] == 'd':
    print("docker resources check")
    output = subprocess.check_output("docker stats",shell=True)
    print(output)
elif sys.argv[1] == 'k':
    print("k8s resources check")
    output = subprocess.check_output("kubectl top pod",shell=True)
    print(output)