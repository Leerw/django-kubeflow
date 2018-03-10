#!/bin/bash
cd ~

# create workspace folder
DIR=kubeflow

# delete the foler created last time
rm -rf ${DIR}

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
ks registry add kubeflow github.com/lrwwll/kubeflow/tree/master/kubeflow
ks pkg install kubeflow/core
ks pkg install kubeflow/tf-serving
ks pkg install kubeflow/tf-job

NAMESPACE=kubeflow

if the NAMESPACE is alreay exists, then delete it!
result=$(kubectl get namespace | grep ${NAMESPACE})
if [ "${result}" != "" ]
then
    kubectl delete namespace kubeflow
    sleep 30s
fi

kubectl create namespace ${NAMESPACE}
ks generate core kubeflow-core --name=kubeflow-core --namespace=${NAMESPACE}

ks env add nocloud

KF_ENV=nocloud
ks apply ${KF_ENV} -c kubeflow-core

sleep 20s

ks param set kubeflow-core jupyterHubServiceType LoadBalancer

PODNAME=`kubectl get pods --namespace=${NAMESPACE} --selector="app=tf-hub" --output=template --template="{{with index .items 0}}{{.metadata.name}}{{end}}"`

# port-forward jupyter-notebook to port 6000
kubectl port-forward --namespace=${NAMESPACE} $PODNAME 8888:8000

# remove the workspace folder and stop minikube
# rm -rf /home/$(whoami)/${DIR}
# minikube stop