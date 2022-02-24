#!/bin/bash

TEST_RUNNER_PATH=$PWD/lib/markers/javascriptJasmine/testRunner.js

cd $CLONE_PATH


if [ -d "node_modules" ]; then
    echo "<error>You added node_modules to your git repo. Please clean up your repo. You might need to learn about .gitignore</error>"
    exit 1
fi

npm install

if [ ! -d "node_modules" ]; then
    echo "<error>npm install didn't work</error>"
    exit 1
fi

cp $TEST_RUNNER_PATH .


echo "<their-tests>"

node testRunner.js
cat test_output


echo "</their-tests>"


cp -r $REFERENCE_PROJECT_PATH/spec .

echo "<our-tests>"

node testRunner.js
cat test_output

echo "</our-tests>"

# and put the tests back

rm -rf spec
rm -rf node_modules
git reset --hard HEAD
