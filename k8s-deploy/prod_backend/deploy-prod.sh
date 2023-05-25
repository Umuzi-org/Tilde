#!/bin/sh

./build-and-push-image-prod.sh

gcloud container clusters get-credentials tilde-cluster --zone europe-west2-a --project umuzi-prod

kubectl delete -f tilde-prod-Deployment.yaml
kubectl apply -f tilde-prod-Deployment.yaml
kubectl delete -f tilde-dramatiq-worker-prod-Deployment.yaml
kubectl apply -f tilde-dramatiq-worker-prod-Deployment.yaml

