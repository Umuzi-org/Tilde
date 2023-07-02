#!/bin/sh

../prod_cluster/use-cluster.sh

./build-and-push-image-prod.sh


kubectl delete -f tilde-prod-Deployment.yaml
kubectl apply -f tilde-prod-Deployment.yaml
kubectl delete -f tilde-dramatiq-worker-prod-Deployment.yaml
kubectl apply -f tilde-dramatiq-worker-prod-Deployment.yaml

kubectl get pods -w