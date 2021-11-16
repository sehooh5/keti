import os


def making():
    os.system("kubectl create ns monitoring")
    os.system("kubectl apply -f prometheus.yaml")
    os.system("kubectl apply -f state_metrics.yaml")
    os.system("kubectl apply -f grafana.yaml")

    return "Created!!"


def namespace():
    os.system("kubectl create ns monitoring")

    return "Created!!"


def prometheus(filename):
    os.system(f"kubectl apply -f {filename}")

    return "Created!!"


def grafana():
    os.system("kubectl apply -f grafana.yaml")

    return "Created!!"
