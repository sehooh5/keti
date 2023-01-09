wip = ["192.168.0.32", "192.168.0.33"]
wname = ["keti1", "keti2"]
wpwd = ["keti", "keti"]


for ip, name, pwd in zip(wip, wname, wpwd):
    print(ip, name, pwd)
