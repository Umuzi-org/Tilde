#!/bin/bash

cd $CLONE_PATH


if [ -d "node_modules" ]; then
    echo "<error>You added node_modules to your git repo. Please clean up your repo. You might need to learn about .gitignore</error>"
    exit 1
fi

rm package-lock.json
npm install
npm i jasmine-reporters

if [ ! -d "node_modules" ]; then
    echo "<error>npm install didn't work</error>"
    exit 1
fi

echo "<their-tests>"

npm run test 2>&1
# npx jasmine 2>&1

echo "</their-tests>"


cp -r $REFERENCE_PROJECT_PATH/spec .

echo "<our-tests>"

# npm run test 2>&1
npx jasmine  2>&1

echo "</our-tests>"

# and put the tests back

rm -rf spec
rm -rf node_modules
git reset --hard HEAD
