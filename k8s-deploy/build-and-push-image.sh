#!/bin/sh

cd ../backend 

docker build -t gcr.io/umuzi-prod/tilde-backend .
docker push gcr.io/umuzi-prod/tilde-backend
