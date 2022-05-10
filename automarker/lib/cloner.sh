#!/bin/bash

# expects a few things to be defined:
# CLONE_PATH = the root directory that everything gets cloned to
# REPO_URL = the thing to clone
# DIR_NAME = the name of the thing we are cloning to

# FULL_CLONE_PATH="$CLONE_PATH/$DIR_NAME"


if [ ! -d "$CLONE_PATH" ]; then
  mkdir $CLONE_PATH
fi

if [ -d "$FULL_CLONE_PATH" ]; then
  echo "repo already exists locally, deleting"
  rm -rf $FULL_CLONE_PATH
fi

git clone $REPO_URL $FULL_CLONE_PATH

