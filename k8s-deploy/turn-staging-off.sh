#!/bin/sh





yes | gcloud container clusters resize tillde-cluster-staging --num-nodes=0 --zone europe-west2-a --project umuzi-staging



gcloud sql instances patch staging \
--activation-policy=NEVER \
--project umuzi-staging