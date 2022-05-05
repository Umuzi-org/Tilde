#!/bin/sh

./docker_build.sh
./docker_push.sh
gcloud builds submit --project umuzi-prod
