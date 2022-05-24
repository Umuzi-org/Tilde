cd $DESTINATION_PATH

# we exclude the tests directory here just so this works when we are testing the configuration. The configured perfect projects will always have imports in the tests dir
grep --exclude-dir=tests -r './' -e 'import'
