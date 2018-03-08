#!/bin/bash
cd /home/$(whoami)/

# create workspace folder
DIR=kubeflow
mkdir ${DIR}
cd ${DIR}

# start minikube
result=$(minikube status | grep "minikube: Stopped")
if [ "${result}" != "" ]
then
    minikube start
fi

# init kubeflow
WORKSPACE=my-kubeflow
ks init ${WORKSPACE}
cd ${WORKSPACE}
ks registry add kubeflow github.com/leerw/kubeflow/tree/master/kubeflow
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

# port-forward jupyter-notebook to port 6000
kubectl port-forward --namespace=${NAMESPACE} $PODNAME 8888:8000

# remove the workspace folder and stop minikube
# rm -rf /home/$(whoami)/${DIR}
# minikube stop