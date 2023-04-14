#!/bin/sh

cd ../../frontend-mini-challenge

GIT_COMMIT="$(git show --format="%h" --no-patch)"
DATE_STR=$(date '+%Y-%m-%d-t-%H-%M')

export API_BASE_URL=https://backend-staging.tilde.umuzi.org


docker build \
-t gcr.io/umuzi-staging/tilde-frontend-mini-challenge:$GIT_COMMIT-$DATE_STR \
-t gcr.io/umuzi-staging/tilde-frontend-mini-challenge:latest \
--build-arg API_BASE_URL  .

docker push gcr.io/umuzi-staging/tilde-frontend-mini-challenge:$GIT_COMMIT-$DATE_STR
docker push gcr.io/umuzi-staging/tilde-frontend-mini-challenge:latest



