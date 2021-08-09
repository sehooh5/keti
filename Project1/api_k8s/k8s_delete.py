import os
import sys

arg = sys.argv[1]
os.system(
    f"kubectl delete node {arg}")
