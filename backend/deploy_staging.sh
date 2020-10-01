#!/bin/sh

export GAE_SERVICE="tilde"
export GS_BUCKET_NAME="tilde"
export PROD_MODE=0

/bin/sh ./_deploy.sh