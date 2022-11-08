#!/bin/sh
# echo REACT_APP_GOOGLE_CLIENT_ID=$REACT_APP_GOOGLE_CLIENT_ID

# REACT_APP_API_BASE_URL="https://tilde-dot-umuzi-prod.nw.r.appspot.com" \
npm i



REACT_APP_API_BASE_URL="https://backend.tilde.umuzi.org" \
REACT_APP_FEATURE_AUTHENTICATION=1 \
REACT_APP_FEATURE_BACKEND_API_ON=1 \
REACT_APP_GOOGLE_CLIENT_ID=$REACT_APP_GOOGLE_CLIENT_ID \
npm run build

yes | gcloud app deploy --project umuzi-prod --appyaml app-staging.yaml
