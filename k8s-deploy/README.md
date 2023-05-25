This directory is all about that infrastructure life.

This k8s deployment is based on https://cloud.google.com/python/django/kubernetes-engine

## Useful commands

Get gcloud connected to the right cluster;

```
gcloud container clusters get-credentials tilde-cluster --zone europe-west2-a --project umuzi-prod
```

kubectl get pods
kubectl logs tilde-backend-5fc8f7cdc8-nhwr9 tilde-backend-app -f
kubectl logs tilde-backend-5fc8f7cdc8-kmnvb tilde-backend-app -f

kubectl get services tilde-backend

## To open a shell into a running pod:

kubectl get pods

kubectl exec --stdin --tty tilde-backend-9ddbdb6d-6b9vm -- /bin/bash
