#!/bin/sh 

export HOST_FRONTEND_MINI=https://challenge-staging.tilde.umuzi.org
export HOST_BACKEND_API=https://backend-staging.tilde.umuzi.org/api
export HOST_AUTOMARKER=http://34.117.22.208


# for i in {1..5}
# do
#     curl \
#     --request POST \
#     --header "Content-Type: application/json" \
#     --data '{"repoUrl":"https://umuzi-org.github.io/zmc-first-website-automark-demo-site/","contentItemId":867, "flavours": []}' \
#     http://34.117.22.208/mark-project
# done