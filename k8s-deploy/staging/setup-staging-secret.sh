#!/bin/sh

# rabbitmq stuff 
export APP_INSTANCE_NAME=tilde-rabbitmq
export NAMESPACE=default 

export RABBITMQ_ERLANG_COOKIE=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1 | tr -d '\n' | base64)
export RABBITMQ_DEFAULT_PASS=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1 | tr -d '\n' | base64)


TODO: look at secrets.yaml in rabbitmq dir. 


# everything else
../upload-secrets.sh