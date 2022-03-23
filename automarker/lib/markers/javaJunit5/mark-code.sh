#!/bin/bash

cd $CLONE_PATH

chmod +x gradlew
cp "$REFERENCE_PROJECT_PATH/build.gradle" .


echo "<their-tests>"

./gradlew clean test --console=plain 2>&1

echo "</their-tests>"

cp -r "$REFERENCE_PROJECT_PATH/src/test" src/


echo "<our-tests>"

./gradlew clean test --console=plain 2>&1

echo "</our-tests>"


# and put the tests back

rm -rf src/test
git reset --hard HEAD

