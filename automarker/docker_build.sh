#!/bin/sh

echo "Building docker image for automark backend"

cp -r $AUTO_MARKER_CONFIGURATION_REPO_PATH automarker-config

docker build -t eu.gcr.io/umuzi-prod/automarker:latest .

yes | rm -r automarker-config