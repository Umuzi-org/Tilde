
# expects a few things to be defined:
# CLONE_PATH = the root directory that everything gets cloned to
# REPO_URL = the thing to clone
# DIR_NAME = the name of the thing we are cloning to

# FULL_CLONE_PATH="$CLONE_PATH/$DIR_NAME"

echo CLONE_PATH=$CLONE_PATH
echo DESTINATION_PATH=$DESTINATION_PATH
echo PERFECT_PROJECT_PATH=$PERFECT_PROJECT_PATH



if [ ! -d "$CLONE_PATH" ]; then
  mkdir $CLONE_PATH
fi

if [ -d "$DESTINATION_PATH" ]; then
  echo "directory already exists, deleting"
  rm -rf $DESTINATION_PATH
fi

echo "cp -r $PERFECT_PROJECT_PATH $DESTINATION_PATH"
cp -r $PERFECT_PROJECT_PATH $DESTINATION_PATH

