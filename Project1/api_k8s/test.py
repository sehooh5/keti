import subprocess

ips = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
ip = ips.split(' ')[0]

print(ips, "\n", ip)
