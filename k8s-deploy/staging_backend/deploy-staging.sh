#!/bin/sh

../staging_cluster/use-cluster.sh

./build-and-push-image-staging.sh


kubectl delete -f tilde-staging-Deployment.yaml
kubectl apply -f tilde-staging-Deployment.yaml
kubectl delete -f tilde-dramatiq-worker-staging-Deployment.yaml
kubectl apply -f tilde-dramatiq-worker-staging-Deployment.yaml

kubectl get pods -w