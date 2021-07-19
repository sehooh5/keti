#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response, request
import os
import subprocess

app = Flask(__name__)


@app.route('/')
def select():
    return render_template('manager.html')


@app.route('/writeFile')
def write_file():
    test = """
    [init] Using Kubernetes version: v1.16.3
[preflight] Running pre-flight checks
	[WARNING IsDockerSystemdCheck]: detected "cgroupfs" as the Docker cgroup driver. The recommended driver is "systemd". Please follow the guide at <https://kubernetes.io/docs/setup/cri/>
	[WARNING SystemVerification]: this Docker version is not on the list of validated versions: 19.03.4. Latest validated version: 18.09
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
...
...
[bootstrap-token] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy
Your Kubernetes control-plane has initialized successfully!
To start using your cluster, you need to run the following as a regular user:
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  <https://kubernetes.io/docs/concepts/cluster-administration/addons/>
Then you can join any number of worker nodes by running the following on each as root:
kubeadm join 192.168.99.102:6443 --token fnbiji.5wob1hu12wdtnmyr \
    --discovery-token-ca-cert-hash sha256:701d4da5cbf67347595e0653b31a7f6625a130de72ad8881a108093afd06188b
    """
    print(test.split('root:')[-1])
    return render_template('write_doc.html')


@app.route('/saveFile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.form['file']
        folder_name = request.form['folder']
        file_name = request.form['fileName']

        # file 작성부분
        f = open(os.getcwd().replace(
            "manager", f'{folder_name}/{file_name}'), 'w')
        f.write(file)
        f.close()
    return render_template('apply_doc.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():

    if request.method == 'POST':
        file_name = request.form['fileName']
        folder_name = request.form['folder']

        if folder_name == 'manager':
            os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")
            os.system(f"kubectl apply -f {file_name}")
        else:
            os.chdir("/home/keti0/keti/Project1-1/REST_API/viewer")
            os.system(f"kubectl apply -f {file_name}")
        os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")
        os.system("echo %s" % file_name)

    return render_template('apply_doc.html')


@ app.route('/signin', methods=['POST'])
def signin():

    pass

    return render_template('docker_login.html')


@ app.route('/login', methods=['POST'])
def login():

    docker_id = request.form['docker_id']
    docker_pwd = request.form['docker_pwd']
    os.system(f"docker login -u {docker_id} -p {docker_pwd}")

    return render_template('apply_doc.html')


@ app.route('/logout', methods=['POST'])
def logout():

    os.system("docker logout")

    return render_template('apply_doc.html')


@ app.route('/build', methods=['GET', 'POST'])
def build():
    print("========= docker build start =========")

    if request.method == 'POST':
        folder_name = request.form['folder']
        file_name = request.form['fileName']
        docker_name = request.form['dockerName']

        if folder_name == 'manager':
            os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")
            os.system(
                f"docker build -f {file_name} -t sehooh5/{docker_name}:latest {path}")
        else:
            os.chdir("/home/keti0/keti/Project1-1/REST_API/viewer")
            os.system(
                f"docker build -f {file_name} -t sehooh5/{docker_name}:latest {path}")
        os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")

    print("========= docker build success =========")
    return render_template('apply_doc.html')


@ app.route('/push', methods=['GET', 'POST'])
def push():

    folder_name = request.form['folder']
    docker_name = request.form['dockerName']

    if folder_name == 'manager':
        os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")
        os.system(f"docker push sehooh5/{docker_name}:latest")
    else:
        os.chdir("/home/keti0/keti/Project1-1/REST_API/viewer")
        os.system(f"docker push sehooh5/{docker_name}:latest")
    os.chdir("/home/keti0/keti/Project1-1/REST_API/manager")

    return render_template('apply_doc.html')


if __name__ == '__main__':
    app.run()
