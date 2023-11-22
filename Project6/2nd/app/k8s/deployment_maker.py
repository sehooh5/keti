import os
import sys


def making(sw_name, node_name, docker_id, version):

    deployment = f"""
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
          image: {docker_id}/{sw_name}:{version}
          imagePullPolicy: Always
          ports:
            - containerPort: 80"""

    with open(f"{sw_name}-{node_name}.yaml", "w") as f:
        f.write(deployment)

    return deployment
