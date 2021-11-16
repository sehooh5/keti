
import requests, json
import random
import time
import datetime

## application/json 으로 보내기
# http://ptsv2.com/t/ucjg5-158907602/post
# "http://127.0.0.1:9000"+"/result"
# "http://182.252.132.39:9000"+"/result"
#url = "http://localhost:9000"+"/result"
url = "http://182.252.132.39:9000/result"
# http://localhost/result


# {"confidence":0.92,"groupName":"A","result":True,"timeStamp":"2020-05-25 10:31:41"}

group = ["A","B"]
#date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
while(True):
    ran = random.randrange(2)
    f = random.uniform(0.8, 1) 
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(today)
    data = {"confidence":f,"groupName":group[ran],"result":"True","timeStamp":today}
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    
    #r = requests.post(url, data = json.dumps(data), headers=headers)    
    r = requests.post(url, data = str(data))
    print(r.text)
    time.sleep(0.2)


## 그냥 몸체 통으로 보내기
#url = "http://182.252.132.39:9000"+"/result"
#data = {'groupName':'B','confidence':0.9}
#headers = {'Content-Type': 'application/json; charset=utf-8'}
#r = requests.post(url, data = data)#,headers=headers)    
#print(r.text)
