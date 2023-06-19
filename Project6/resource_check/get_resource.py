import sys
import subprocess

if sys.argv[1] == 'd':
    print("docker resources check")
    output = subprocess.check_output("docker stats",shell=True)
    print(output)
elif sys.argv[1] == 'kp':
    print("k8s pod resources check")
    output = subprocess.check_output("kubectl top po",shell=True)
    print(output)
elif sys.argv[1] == 'kn':
    print("k8s node resources check")
    output = subprocess.check_output("kubectl top no",shell=True)
    print(output)