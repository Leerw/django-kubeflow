#!/bin/bash
cd /home/$(whoami)/

# create workspace folder
DIR=kubeflow
mkdir ${DIR}
cd ${DIR}

# start minikube
minikube start
sleep 10s

# init kubeflow
WORKSPACE=my-kubeflow
ks init ${WORKSPACE}
cd ${WORKSPACE}
ks registry add kubeflow github.com/kubeflow/kubeflow/tree/master/kubeflow
ks pkg install kubeflow/core
ks pkg install kubeflow/tf-serving
ks pkg install kubeflow/tf-job

NAMESPACE=kubeflow
kubectl create namespace ${NAMESPACE}
ks generate core kubeflow-core --name=kubeflow-core --namespace=${NAMESPACE}

ks env add nocloud

KF_ENV=nocloud
ks apply ${KF_ENV} -c kubeflow-core

sleep 10s

ks param set kubeflow-core jupyterHubServiceType LoadBalancer

PODNAME=`kubectl get pods --namespace=${NAMESPACE} --selector="app=tf-hub" --output=template --template="{{with index .items 0}}{{.metadata.name}}{{end}}"` 

PODNAME=`kubectl get pods --namespace=${NAMESPACE} --selector="app=tf-hub" --output=template --template="{{with index .items 0}}{{.metadata.name}}{{end}}"`

## remove the workspace folder and stop minikube
# rm -rf /home/$(whoami)/${DIR}
# minikube stop