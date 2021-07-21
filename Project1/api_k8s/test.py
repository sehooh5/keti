

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

