#!/bin/sh 

cd ../backend
python manage.py collectstatic --noinput
gsutil -m rsync -r ./collectstatic gs://tilde-backend-collectstatic/static
