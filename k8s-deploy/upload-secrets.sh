#!/bin/sh 

# Cloud SQL secrets
kubectl create secret generic cloudsql-oauth-credentials --from-file=credentials.json=$GOOGLE_APPLICATION_CREDENTIALS 

kubectl create secret generic cloudsql --from-literal=TILDE_SQL_USER=$TILDE_SQL_USER --from-literal=TILDE_SQL_PASS=$TILDE_SQL_PASS

# Misc Django secrets 
kubectl create secret generic miscbackend --from-literal=PROD_SECRET_KEY=$PROD_SECRET_KEY 

# Git Real secrets
kubectl create secret generic gitreal --from-literal=GITHUB_CLIENT_ID=$GITHUB_CLIENT_ID --from-literal=GITHUB_CLIENT_SECRET=$GITHUB_CLIENT_SECRET
kubectl create secret generic gitrealwebhook --from-literal=GIT_REAL_WEBHOOK_SECRET=$GIT_REAL_WEBHOOK_SECRET

# LOGIN WITH GOOGLE
kubectl create secret generic google-oauth-onetime-creds --from-file=google-oauth-onetime-creds.json=$GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE 

