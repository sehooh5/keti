import subprocess
import os

result1 = os.system("kubectl get pods | grep monitoring-edge-worker-01")
print(result1)

result2 = os.system("kubectl get pods | grep monitoring-edge-worker-02")
print(result2)

result3 = os.system("kubectl get pods | grep monitoring-edge-worker-03")
print(result3)

# result = subprocess.run(['whoami'], capture_output=True, text=True)