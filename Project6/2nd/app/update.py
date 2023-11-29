import subprocess
import os

result = os.system("kubectl get pods | grep monitoring-edge-worker-01")
print(result)

# result = subprocess.run(['whoami'], capture_output=True, text=True)