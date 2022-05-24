cd $DESTINATION_PATH

grep --exclude-dir=spec -r './' -e 'require('
grep --exclude-dir=spec -r './' -e 'import'
