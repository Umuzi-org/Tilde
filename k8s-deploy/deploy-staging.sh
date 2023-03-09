#!/bin/sh

./build-and-push-image-staging.sh

gcloud container clusters get-credentials tillde-cluster-staging  --zone europe-west2-a --project umuzi-staging

kubectl delete -f tilde-staging-Deployment.yaml
kubectl apply -f tilde-staging-Deployment.yaml
kubectl delete -f tilde-dramatiq-worker-staging-Deployment.yaml
kubectl apply -f tilde-dramatiq-worker-staging-Deployment.yaml

