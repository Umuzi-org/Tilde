#!/bin/bash

# expects a few things to be defined:
# CLONE_PATH = the root directory that everything gets cloned to
# REPO_URL = the thing to clone
# DIR_NAME = the name of the thing we are cloning to

FULL_PATH="$CLONE_PATH/$DIR_NAME"
HTTP_STATUS=$(curl -I ${REPO_URL:0:-4} | head -n 1)

if [[ $HTTP_STATUS == *"404"* ]]; then
  exit 404
fi

if [ ! -d "$CLONE_PATH" ]; then
  mkdir $CLONE_PATH
fi

if [ -d "$FULL_PATH" ]; then
  echo "repo already exists locally, pulling changes"
  cd $FULL_PATH
  git pull
else
  git clone $REPO_URL $FULL_PATH
  cd $FULL_PATH
fi
