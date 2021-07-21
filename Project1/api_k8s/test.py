

# NAME STATUS ROLES AGE VERSION
# keti0-master Ready master 336d v1.18.8
# keti1-worker1 Ready 336d v1.18.6
# keti2-worker2 Ready 336d v1.18.6

s = """NAME STATUS ROLES AGE VERSION
keti0-master Ready master 336d v1.18.8
keti1-worker1 Ready 336d v1.18.6
keti2-worker2 Ready 336d v1.18.6"""

s_split = s.split('\n')
len_s = len(s_split)

node_list = s_split[1:len_s]

print(node_list)

a = []
for x in node_list:
    nx = {"name" : x.split(' ')[0]}
    a.append(nx)
    
print(a)


# 랜덤 id 만들기

import string 
import random 

_LENGTH = 4 # 12자리 # 숫자 + 대소문자 
string_pool = string.ascii_letters + string.digits 

# 랜덤한 문자열 생성 
result = ""
for i in range(_LENGTH) :
    result += random.choice(string_pool) # 랜덤한 문자열 하나 선택 
    
print(result)



