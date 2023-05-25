#!/bin/sh

../prod_cluster/use-cluster.sh
./build_and_push_image_prod.sh

kubectl delete -f automarker-prod-Deployment.yaml
kubectl apply -f automarker-prod-Deployment.yaml

kubectl get pods -w