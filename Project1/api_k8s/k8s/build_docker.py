import os
import sys


url = sys.argv[1]
file = sys.argv[2]
docker_id = sys.argv[3]
sw_name = sys.argv[4]


def build():

    output = os.system(
        f"docker build -f {url}/{file} -t {docker_id}/{sw_name}:latest .")


build()
