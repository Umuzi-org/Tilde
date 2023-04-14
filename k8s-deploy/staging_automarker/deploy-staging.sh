#!/bin/sh

../staging_cluster/use-cluster.sh
./build_and_push_image_staging.sh

kubectl delete -f automarker-staging-Deployment.yaml
kubectl apply -f automarker-staging-Deployment.yaml

kubectl get pods