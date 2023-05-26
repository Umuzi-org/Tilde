#!/bin/sh

if [ -z "${AUTO_MARKER_CONFIGURATION_REPO_PATH}" ]
then
    echo "Please set the AUTO_MARKER_CONFIGURATION_REPO_PATH environment variable"
    exit 1
fi


../staging_cluster/use-cluster.sh
./build_and_push_image_staging.sh

kubectl delete -f automarker-staging-Deployment.yaml
kubectl apply -f automarker-staging-Deployment.yaml

kubectl get pods -w