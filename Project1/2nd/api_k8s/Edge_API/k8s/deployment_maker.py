import os
import sys

# 이 부분은 나중에 들어오는 값들을 받아와야함
#sw_name = sys.argv[1]
#port = sys.argv[2]
#target_port = sys.argv[3]
#node_port = sys.argv[4]
#node_name = sys.argv[5]
# docker_id = sys.argv[6]  # 나중에 로컬끼리 주고받는거면 필요없을수도잇음


def making(sw_name, port, target_port, node_port, node_name, docker_id):

    deployment = f"""
apiVersion: v1
kind: Service
metadata:
  name: {sw_name}-service
spec:
  selector:
    app: {sw_name}
  ports:
    - protocol: "TCP"
      port: {port}
      targetPort: {target_port}
      nodePort: {node_port}
  type: NodePort

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {sw_name}
spec:
  selector:
    matchLabels:
      app: {sw_name}
  template:
    metadata:
      labels:
        app: {sw_name}
    spec:
      nodeName: {node_name}
      containers:
        - name: {sw_name}
          image: {docker_id}/{sw_name}:latest
          imagePullPolicy: Always
          ports:
            - containerPort: {target_port}"""
    # print(deployment)

    with open(f"{sw_name}.yaml", "w") as f:
        f.write(deployment)

    return f"{sw_name}.yaml"
