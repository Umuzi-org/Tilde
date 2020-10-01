#!/bin/sh

export GAE_SERVICE="management-info-sys-devtest"
export GS_BUCKET_NAME="managment-information-system-devtest"
export PROD_MODE=0

/bin/sh ./_deploy.sh