import os
import sys


def making(sw_name, port, target_port, node_port, node_name, docker_id):

    deployment = f"""
apiVersion: v1
kind: Service
metadata:
  name: {sw_name}-{node_name}-service
spec:
  selector:
    app: {sw_name}-{node_name}
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
  name: {sw_name}-{node_name}
spec:
  selector:
    matchLabels:
      app: {sw_name}-{node_name}
  template:
    metadata:
      labels:
        app: {sw_name}-{node_name}
    spec:
      nodeName: {node_name}
      containers:
        - name: {sw_name}-{node_name}
          image: {docker_id}/{sw_name}:latest
          imagePullPolicy: Always
          ports:
            - containerPort: {target_port}"""

    with open(f"{sw_name}-{node_name}.yaml", "w") as f:
        f.write(deployment)

    return deployment
