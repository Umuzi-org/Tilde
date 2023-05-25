#!/bin/sh

if [ -z "${AUTO_MARKER_CONFIGURATION_REPO_PATH}" ]
then
    echo "Please set the AUTO_MARKER_CONFIGURATION_REPO_PATH environment variable"
    exit 1
fi



cd ../../automarker

GIT_COMMIT="$(git show --format="%h" --no-patch)"
DATE_STR=$(date '+%Y-%m-%d-t-%H-%M')

cp -r $AUTO_MARKER_CONFIGURATION_REPO_PATH project_config

docker build \
-t gcr.io/umuzi-staging/automarker:$GIT_COMMIT-$DATE_STR \
-t gcr.io/umuzi-staging/automarker:latest .

docker push gcr.io/umuzi-staging/automarker:$GIT_COMMIT-$DATE_STR
docker push gcr.io/umuzi-staging/automarker:latest

rm -rf project_config


