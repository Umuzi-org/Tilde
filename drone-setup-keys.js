'use strict';

const fs = require('fs');

const data = {
    "type": "service_account",
    "project_id": "umuzi-prod",
    "private_key_id": process.env.GCLOUD_PRIVATE_KEY_ID,
    "private_key": process.env.GCLOUD_PRIVATE_KEY,
    "client_email": "drone-io-deploy@umuzi-prod.iam.gserviceaccount.com",
    "client_id": "117897706003738993064",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/drone-io-deploy%40umuzi-prod.iam.gserviceaccount.com"
}

fs.writeFileSync("/root/.key/gcloud-service-key.json",JSON.stringify(data))