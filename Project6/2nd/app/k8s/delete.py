import os
import sys


url = sys.argv[1]
file = sys.argv[2]


def delete():

    output = os.system(f"kubectl delete -f {url}/{file}")


delete()
