#!/bin/sh

cd ../backend 

GIT_COMMIT="$(git show --format="%h" --no-patch)"
DATE_STR=$(date '+%Y-%m-%d-t-%H-%M')

docker build -t gcr.io/umuzi-prod/tilde-backend:$GIT_COMMIT-$DATE_STR -t gcr.io/umuzi-prod/tilde-backend:latest .
docker push gcr.io/umuzi-prod/tilde-backend:$GIT_COMMIT-$DATE_STR
docker push gcr.io/umuzi-prod/tilde-backend:latest
