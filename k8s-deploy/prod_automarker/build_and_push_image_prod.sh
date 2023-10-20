#!/bin/sh

cd ../../automarker

GIT_COMMIT="$(git show --format="%h" --no-patch)"
DATE_STR=$(date '+%Y-%m-%d-t-%H-%M')

cp -r $AUTO_MARKER_CONFIGURATION_REPO_PATH project_config

docker build --no-cache \
-t gcr.io/umuzi-prod/automarker:$GIT_COMMIT-$DATE_STR \
-t gcr.io/umuzi-prod/automarker:latest .

docker push gcr.io/umuzi-prod/automarker:$GIT_COMMIT-$DATE_STR
docker push gcr.io/umuzi-prod/automarker:latest

rm -rf project_config


