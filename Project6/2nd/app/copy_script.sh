#!/bin/bash

# "yes"를 통해 "yes"를 입력하고 
yes | sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
