#!/bin/sh

yes | gcloud container clusters resize tillde-cluster-staging-2 --num-nodes=3 --zone europe-west2-a --project umuzi-staging


gcloud sql instances patch staging \
--activation-policy=ALWAYS \
--project umuzi-staging