import os


def select(file, nodename):
    path = os.path.abspath('..')

    with open(f"{file}", "r") as f:
        data = f.read()
        # print(data.replace("nodeselect", "keti1-worker1"))
        data = data.replace("nodeselect", nodename)

        with open("./k8s/prometheuswithmetrics.yaml", "w") as f:
            f.write(data)

    return print("complited!!")


# select("prometheuswithmetrics_backup.yaml", "keti1-worker1")
