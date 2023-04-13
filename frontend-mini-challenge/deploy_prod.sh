#!/bin/sh

./build_and_push_image.sh

gcloud run deploy frontend-mini-challenge --image gcr.io/umuzi-prod/tilde-frontend-mini-challenge:latest --project umuzi-prod --platform managed --region europe-west1