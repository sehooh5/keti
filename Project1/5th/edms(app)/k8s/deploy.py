import os
import sys


url = sys.argv[1]
file = sys.argv[2]


def deploy():

    output = os.system(f"kubectl apply -f {url}/{file}")


deploy()