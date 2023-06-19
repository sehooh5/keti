import sys

if sys.argv[1] == 'd':
    print("docker resource check")
elif sys.argv[1] == 'k':
    print("k8s resource check")