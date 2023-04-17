#!/bin/sh

npm i

REACT_APP_API_BASE_URL="https://backend-staging.tilde.umuzi.org" \
REACT_APP_FEATURE_AUTHENTICATION=1 \
REACT_APP_FEATURE_BACKEND_API_ON=1 \
REACT_APP_GOOGLE_CLIENT_ID=$REACT_APP_GOOGLE_CLIENT_ID \
npm run build && \
yes | gcloud app deploy --project umuzi-staging --appyaml app-staging.yaml
