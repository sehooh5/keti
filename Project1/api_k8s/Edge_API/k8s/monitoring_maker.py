import os


def making():
    os.system("kubectl create ns monitoring")
    os.system("kubectl apply -f prometheus.yaml")
    os.system("kubectl apply -f state_metrics.yaml")
    os.system("kubectl apply -f grafana.yaml")

    return
