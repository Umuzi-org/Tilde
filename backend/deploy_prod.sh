#!/bin/sh

echo "DEPLOYING TO GAE - DEPRICATED!! use k8s deployment instead"
exit 

export GAE_SERVICE="tilde"
export GS_BUCKET_NAME="tilde"



export BASE_URL="https://tilde-dot-umuzi-prod.nw.r.appspot.com"

export PROD_MODE=1

cp $GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE google-oauth-onetime-creds.json

/bin/sh ./_deploy.sh


rm google-oauth-onetime-creds.json

