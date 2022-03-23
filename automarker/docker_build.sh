#!/bin/sh

echo "Building docker image for automark backend"

docker build -t eu.gcr.io/umuzi-prod/automarker:latest .
