import os


def making(kubeconfig_path):
    os.system(f"kubectl create ns monitoring")
    os.system(f"kubectl --kubeconfig={kubeconfig_path} apply -f prometheus.yaml")
    os.system(f"kubectl --kubeconfig={kubeconfig_path} apply -f state_metrics.yaml")
    os.system(f"kubectl --kubeconfig={kubeconfig_path} apply -f grafana.yaml")

    return "Created!!"


def namespace():
    os.system(f"kubectl --kubeconfig={kubeconfig_path} create ns monitoring")

    return "Created!!"


def prometheus(filename):
    os.system(f"kubectl --kubeconfig={kubeconfig_path} apply -f ./k8s/{filename}")

    return "Created!!"


def grafana():
    os.system(f"kubectl --kubeconfig={kubeconfig_path} apply -f grafana.yaml")

    return "Created!!"
