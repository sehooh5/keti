# Docker, Kubernetes 리소스 사용량 확인 방법

​    

## **실행 절차**

#### 1. Docker, Kubernetes 설치

​    

#### 2. Kubernetes 리소스 확인을 위한 metrics-server 설치(배포)

- 명령어 실행으로 metrics-server 디플로이먼트 파일 다운로드 :  

  ```
   $ wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
  ```

- metrics-server의 디플로이먼트 파일 수정 :

  ```
  # 편집기 실행
  $ vi components.yaml    
  
  # 추가 옵션 1  
  spec:     
  	containers:       
  	- args:         
  	--cer-dir=/tmp        
  	--secure-port=4443        
  	--kublet-insecure-tls # 추가 옵션1
  - 생략 -     
  
  # 추가 옵션 2
  apiVersion: rbac.authorization.k8s.io/v1
  kind: ClusterRole
  - 생략 -
  rules:
  	- apiGroups:  
  	- “” 
  	resources:  
  	- nodes/metrics  
  	- nodes/stats # 추가옵션2
  ```

- 디플로이먼트 파일을 명령어로 설치(배포) : 

  ```
  kubectl apply –f components.yaml
  ```

  

#### 3. Python 실행 파일 작성 후 Docker, Kubernetes 리소스 확인 방법에 따라 실행

​    



## 실행 파일(get_resource.py)

```python
import sys
import subprocess

if sys.argv[1] == 'd': # docker 명령어
    print("docker resources check")
    output = subprocess.check_output("docker stats --no-stream",shell=True)
    print(output)
elif sys.argv[1] == 'kp': # k8s 명령어 – pod
    print("k8s pod resources check")
    output = subprocess.check_output("kubectl top po",shell=True)
    print(output)
elif sys.argv[1] == 'kn': # k8s 명령어 – Node
    print("k8s node resources check")
    output = subprocess.check_output("kubectl top no",shell=True)
    print(output)
else:
    print("argument not available")
```

​    

   

## **실행 결과**



#### 1. Docker 리소스 확인 명령어 및 결과 :

```
# 명령어
$ python3 get_resource.py d    

# 결과
b'CONTAINER ID   NAME  CPU %     MEM USAGE / LIMIT     MEM %     NET I/O   BLOCK I/O         PIDS\n
7f4e45cc7993k8s_coredns_coredns-78fcd69978-8gt2g_kube-system_5380fe1d-dc62-41a7-b806-b2c65ff395ce_15   0.30%     22.34MiB / 170MiB     13.14%    0B / 0B   21MB / 0B         10\n“
```



#### 2. Kubernetes Pod 리소스 확인 명령어 및 결과 :

```
명령어
$ python3 get_resource.py kp    

# 결과
b'NAME                                CPU(cores)   MEMORY(bytes)  \n
select-cam-keti1-5dc4bcd4b4-cvd8n   1m           41Mi            \n'
```



​    

#### 3. Kubernetes Node 리소스 확인 명령어 및 결과 :

```
명령어
$ python3 get_resource.py kn    

# 결과
b'NAME    CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   \n
keti1   626m         15%    3065Mi          39%       \nketi2   583m         14%    4356Mi          56%       \n'
```

