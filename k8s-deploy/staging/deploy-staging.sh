#!/bin/sh

gcloud container clusters get-credentials tillde-cluster-staging-2  --zone europe-west2-a --project umuzi-staging

./build-and-push-image-staging.sh


kubectl delete -f tilde-staging-Deployment.yaml
kubectl apply -f tilde-staging-Deployment.yaml
# kubectl delete -f tilde-dramatiq-worker-staging-Deployment.yaml
# kubectl apply -f tilde-dramatiq-worker-staging-Deployment.yaml

