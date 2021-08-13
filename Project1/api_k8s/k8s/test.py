import deployment_maker
import build

# deploy = deployment_maker.making(
#     "sw", "6001", "5001", "30001", "keti-node", "seho")
build.build("/home/keti0/keti/Project1/api_k8s/manager",
            "Dockerfile", "sehooh5", "manager")
