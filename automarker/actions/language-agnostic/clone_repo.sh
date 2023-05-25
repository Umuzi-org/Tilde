# expects a few things to be defined:

# CLONE_PATH = the root directory that everything gets cloned to. This gets created if it doesn't exist 
# REPO_URL = the thing to clone
# FULL_CLONE_PATH = the full path to the destination of the clone

if [ ! -d "$CLONE_PATH" ]; then
  mkdir $CLONE_PATH
fi

if [ -d "$FULL_CLONE_PATH" ]; then
  echo "repo already exists locally, deleting"
  rm -rf $FULL_CLONE_PATH
fi


echo "cloning---------"
echo "git clone $REPO_URL $FULL_CLONE_PATH"


git clone $REPO_URL $FULL_CLONE_PATH

