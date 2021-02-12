# Setting up and accessing rabbit mq

We followed intructions to set up rabbit MQ from here. Started from this repo:

```
git clone https://github.com/GoogleCloudPlatform/click-to-deploy.git googleCloudPlatformClickToDeploy
git checkpt d367a22a0daa93082c14e7f9c63b45960375ddcc
```

This happens once in order to define the Application type.

```
kubectl apply -f "https://raw.githubusercontent.com/GoogleCloudPlatform/marketplace-k8s-app-tools/master/crd/app-crd.yaml"
```

Please Note: the passwords generated here are random. If you use tis in multiple shells you would just need to be sure that you get the right values.

```
cd  googleCloudPlatformClickToDeploy/k8s/rabbitmq
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

```

Now generate our yaml files:

```
# Expand rbac.yaml
envsubst '$APP_INSTANCE_NAME' < scripts/rbac.yaml > "../../../rabbitmq/${APP_INSTANCE_NAME}_rbac.yaml"

helm template "$APP_INSTANCE_NAME" chart/rabbitmq --namespace "$NAMESPACE" --set rabbitmq.image.repo="$IMAGE_RABBITMQ" --set rabbitmq.image.tag="$TAG" --set rabbitmq.initImage="$IMAGE_RABBITMQ_INIT" --set rabbitmq.replicas="$REPLICAS" --set rabbitmq.persistence.storageClass="$RABBITMQ_STORAGE_CLASS" --set rabbitmq.persistence.size="$RABBITMQ_PERSISTENT_DISK_SIZE" --set rabbitmq.erlangCookie="$RABBITMQ_ERLANG_COOKIE" --set rabbitmq.user="$RABBITMQ_DEFAULT_USER" --set rabbitmq.password="$RABBITMQ_DEFAULT_PASS" --set rabbitmq.serviceAccount="$RABBITMQ_SERVICE_ACCOUNT" --set metrics.image="$IMAGE_METRICS_EXPORTER" --set metrics.exporter.enabled="$METRICS_EXPORTER_ENABLED" > "../../../rabbitmq/${APP_INSTANCE_NAME}_manifest.yaml"
```

And apply them:

```
# rbac.yaml
kubectl apply -f "${APP_INSTANCE_NAME}_rbac.yaml" --namespace "${NAMESPACE}"
# manifest.yaml
kubectl apply -f "${APP_INSTANCE_NAME}_manifest.yaml" --namespace "${NAMESPACE}"
```

To grab the password from the k8s secret:

```
kubectl get secret $APP_INSTANCE_NAME-rabbitmq-secret \
  --namespace $NAMESPACE \
  --output=jsonpath='{.data.rabbitmq-pass}' | base64 --decode
```

To access any part of the rabbit mq deployment, do some port forwarding:

```
kubectl port-forward svc/$APP_INSTANCE_NAME-rabbitmq-svc --namespace $NAMESPACE 15672 25672 56720:5672 5671 43690:4369
```

Now the rabbitmq gui is accessable at: `http://127.0.0.1:15672/#/`
And you can add stuff to the queue (to be consumed by our live dramatiq worker) by interacting here