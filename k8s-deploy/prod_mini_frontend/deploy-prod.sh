#!/bin/sh

../prod_cluster/use-cluster.sh
./build_and_push_image_prod.sh


kubectl delete -f mini-frontend-prod-Deployment.yaml
kubectl apply -f mini-frontend-prod-Deployment.yaml