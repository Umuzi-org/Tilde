git clone https://github.com/GoogleCloudPlatform/click-to-deploy.git googleCloudPlatformClickToDeploy
git checkpt d367a22a0daa93082c14e7f9c63b45960375ddcc


kubectl apply -f "https://raw.githubusercontent.com/GoogleCloudPlatform/marketplace-k8s-app-tools/master/crd/app-crd.yaml"

cd  googleCloudPlatformClickToDeploy/k8s/rabbitmq

```
export APP_INSTANCE_NAME=tilde-rabbitmq
export NAMESPACE=default
export REPLICAS=1
export RABBITMQ_STORAGE_CLASS="standard"
export RABBITMQ_PERSISTENT_DISK_SIZE="5Gi"
export RABBITMQ_ERLANG_COOKIE=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1 | tr -d '\n' | base64)
export RABBITMQ_DEFAULT_USER=rabbit
export RABBITMQ_DEFAULT_PASS=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1 | tr -d '\n' | base64)
export METRICS_EXPORTER_ENABLED=true
export TAG="3.7.28-20210103-154152"
export IMAGE_RABBITMQ=marketplace.gcr.io/google/rabbitmq
export IMAGE_RABBITMQ_INIT=marketplace.gcr.io/google/rabbitmq/debian9:${TAG}
export IMAGE_METRICS_EXPORTER="marketplace.gcr.io/google/rabbitmq/prometheus-to-sd:${TAG}"
export RABBITMQ_SERVICE_ACCOUNT=$APP_INSTANCE_NAME-rabbitmq-sa

echo $RABBITMQ_DEFAULT_PASS
```

```
# Expand rbac.yaml
envsubst '$APP_INSTANCE_NAME' < scripts/rbac.yaml > "../../../rabbitmq/${APP_INSTANCE_NAME}_rbac.yaml"

helm template "$APP_INSTANCE_NAME" chart/rabbitmq --namespace "$NAMESPACE" --set rabbitmq.image.repo="$IMAGE_RABBITMQ" --set rabbitmq.image.tag="$TAG" --set rabbitmq.initImage="$IMAGE_RABBITMQ_INIT" --set rabbitmq.replicas="$REPLICAS" --set rabbitmq.persistence.storageClass="$RABBITMQ_STORAGE_CLASS" --set rabbitmq.persistence.size="$RABBITMQ_PERSISTENT_DISK_SIZE" --set rabbitmq.erlangCookie="$RABBITMQ_ERLANG_COOKIE" --set rabbitmq.user="$RABBITMQ_DEFAULT_USER" --set rabbitmq.password="$RABBITMQ_DEFAULT_PASS" --set rabbitmq.serviceAccount="$RABBITMQ_SERVICE_ACCOUNT" --set metrics.image="$IMAGE_METRICS_EXPORTER" --set metrics.exporter.enabled="$METRICS_EXPORTER_ENABLED" > "../../../rabbitmq/${APP_INSTANCE_NAME}_manifest.yaml"
```

```
# rbac.yaml
kubectl apply -f "${APP_INSTANCE_NAME}_rbac.yaml" --namespace "${NAMESPACE}"
# manifest.yaml
kubectl apply -f "${APP_INSTANCE_NAME}_manifest.yaml" --namespace "${NAMESPACE}"
```

kubectl get secret $APP_INSTANCE_NAME-rabbitmq-secret \
  --namespace $NAMESPACE \
  --output=jsonpath='{.data.rabbitmq-pass}' | base64 --decode


kubectl port-forward svc/$APP_INSTANCE_NAME-rabbitmq-svc --namespace $NAMESPACE 15672 25672 56720:5672 5671 43690:4369