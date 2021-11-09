#!/bin/sh

./build-and-push-image.sh
kubectl delete -f tilde-prod-Deployment.yaml
kubectl apply -f tilde-prod-Deployment.yaml
kubectl delete -f tilde-dramatiq-worker-prod-Deployment.yaml
kubectl apply -f tilde-dramatiq-worker-prod-Deployment.yaml

