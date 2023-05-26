#!/bin/sh

if [ -z "${AUTO_MARKER_CONFIGURATION_REPO_PATH}" ]
then
    echo "Please set the AUTO_MARKER_CONFIGURATION_REPO_PATH environment variable"
    exit 1
fi

../prod_cluster/use-cluster.sh
./build_and_push_image_prod.sh

kubectl delete -f automarker-prod-Deployment.yaml
kubectl apply -f automarker-prod-Deployment.yaml

kubectl get pods -w