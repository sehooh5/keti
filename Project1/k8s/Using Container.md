# Using Container

- k8s 를 이용해서 컨테이너를 실행
- 여기서는 yaml 사용이 아닌 `kubectl` 명령어로 nginx 컨테이너 실행



1. nginx 를 컨테이너로 실행

```bash
$ kubectl create deployment nginx --image=nginx

# 처음 방법 사용하면 deployment not found 에러가 떴음
# $ kubectl run nginx --image nginx --port=80
```



2. nginx가 제대로 실행 됐는지 확인하기 위해 상태 확인

```bash
$ kubectl get pods
$ kubectl get deployments
$ kubectl get servcie
```



3. deployment 를 이용하여 포드 개수 늘리기

```bash
$ kubect scale deploy nginx --replicas=2
```



4. k8s 내부에서 띄운 컨테이너를 외부에서 접근 가능하게 하기위해 service 사용
   - service 종류 : ClusterIP, NodePort, LoadBalancer, ExteralName
   - port 는 80 으로 지정

```bash
$ kubectl expose deployment nginx --port 80 --type=NodePort
```



5. service 확인하여 연결하기
   - 해당 서비스를 보면 내부 포트번호와 외부 번호를 사용하여 연동
   - `localhost:32741` 로 연결 가능

```bash
$ kubectl get services

NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP        11d
nginx        NodePort    10.99.161.36   <none>        80:32741/TCP   9s


# describe 로 자세한 내용 확인
# Endpoint : service 에 두개의 컨테이너가 연결된 것을 확인
$ kubectl describe service nginx
Name:                     nginx
Namespace:                default
Labels:                   app=nginx
Annotations:              <none>
Selector:                 app=nginx
Type:                     NodePort
IP:                       10.99.161.36
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  32741/TCP
Endpoints:                10.244.1.32:80,10.244.2.23:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>

```



6. 배포 롤백 및 사용한 자원들 삭제

   - 배포 롤백

     ```bash
     $ kubectl rollout history deploy nginx(이름)
     
     # 아래 버전이 여러개 뜸
     ~~
     ~~~
     
     # 6번 자세히 보기
     $ kubectl rollout history deploy nginx(이름) --revision=6
     
     # 직전 버전으로 돌아가기
     $ kubectl rollout undo deploy nginx
     
     # 특정 버전으로 돌아가기
     $ kubectl rollout undo deploy nginx --to-revision=3
     ```

     

   - 삭제

     ```bash
     $ kubectl delete deployment nginx
     $ kubectl delete service nginx
     ```



