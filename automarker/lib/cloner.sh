#!/bin/bash

# expects a few things to be defined:
# CLONE_PATH = the root directory that everything gets cloned to
# REPO_URL = the thing to clone
# DIR_NAME = the name of the thing we are cloning to

FULL_PATH="$CLONE_PATH/$DIR_NAME"


if [ ! -d "$CLONE_PATH" ]; then
  mkdir $CLONE_PATH
fi

if [ -d "$FULL_PATH" ]; then
  echo "repo already exists locally, pulling changes"
  cd $FULL_PATH
  git pull
else
  git clone $REPO_URL $FULL_PATH
  if [  -d "$FULL_PATH" ]; then
    cd $FULL_PATH
  fi
fi

