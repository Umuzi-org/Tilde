docker run \
  -v $GOOGLE_APPLICATION_CREDENTIALS:/config \
  -p 127.0.0.1:5437:5432 \
  gcr.io/cloudsql-docker/gce-proxy:1.12 /cloud_sql_proxy \
  -instances=$SQL_CONNECTION_NAME=tcp:0.0.0.0:5432 -credential_file=/config
