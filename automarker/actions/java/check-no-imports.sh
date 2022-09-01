cd $DESTINATION_PATH

grep --exclude-dir=.git -r './' -e 'import'
