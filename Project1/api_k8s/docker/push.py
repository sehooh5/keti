import os
import sys

docker_id = sys.argv[1]
sw_name = sys.argv[2]


def push():

    output = os.system(
        f"docker push {docker_id}/{sw_name}:latest .")


push()
