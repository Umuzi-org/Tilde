#!/bin/sh

../staging_cluster/use-cluster.sh
./build_and_push_image_staging.sh


kubectl delete -f mini-frontend-staging-Deployment.yaml
kubectl apply -f mini-frontend-staging-Deployment.yaml