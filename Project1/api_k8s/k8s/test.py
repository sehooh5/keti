import deployment_maker


def hi():
    print("hi")


deploy = deployment_maker.making(
    "sw", "6001", "5001", "30001", "keti-node", "seho")
