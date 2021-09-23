import os
import sys


def push(docker_id, sw_name):

    output = os.system(
        f"docker push {docker_id}/{sw_name}:latest .")


push()
