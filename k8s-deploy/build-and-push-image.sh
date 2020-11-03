#!/bin/sh

cd ../backend 

GIT_COMMIT="$(git show --format="%h" --no-patch)"

docker build -t gcr.io/umuzi-prod/tilde-backend:$GIT_COMMIT -t gcr.io/umuzi-prod/tilde-backend:latest .
docker push gcr.io/umuzi-prod/tilde-backend:$GIT_COMMIT
docker push gcr.io/umuzi-prod/tilde-backend:latest
