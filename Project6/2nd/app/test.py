# file path 및 zip 파일에서 fname 추출하는 방법 테스트
str = "/home/edge-master-01/monitoring.zip".split('/')[-1]
if str.find("zip") != -1:
    str = str.split('.')[0]

print(str)