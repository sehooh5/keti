import os


def making():
    os.system("kubectl create ns monitoring")
    os.system("kubectl --kubeconfig=/home/keti2/.kube/config apply -f prometheus.yaml")
    os.system("kubectl --kubeconfig=/home/keti2/.kube/config apply -f state_metrics.yaml")
    os.system("kubectl --kubeconfig=/home/keti2/.kube/config apply -f grafana.yaml")

    return "Created!!"


def namespace():
    os.system("kubectl --kubeconfig=/home/keti2/.kube/config create ns monitoring")

    return "Created!!"


def prometheus(filename):
    os.system(f"kubectl --kubeconfig=/home/keti2/.kube/config apply -f ./k8s/{filename}")

    return "Created!!"


def grafana():
    os.system("kubectl --kubeconfig=/home/keti2/.kube/config apply -f grafana.yaml")

    return "Created!!"
