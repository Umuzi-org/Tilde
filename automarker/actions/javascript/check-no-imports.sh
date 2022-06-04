cd $DESTINATION_PATH

grep --exclude-dir=spec --exclude-dir=.git -r './' -e 'require('
grep --exclude-dir=spec --exclude-dir=.git -r './' -e 'import'
