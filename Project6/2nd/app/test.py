

str = "/home/edge-master-01/monitoring.zip".split('/')
if str.find("zip") != -1:
    str = str.split('.')[0]

print(str)