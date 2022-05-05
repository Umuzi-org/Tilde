#!/bin/bash

cd $CLONE_PATH


if [ ! -f "requirements.txt" ]; then
    echo "<error>requirements.txt doesn't exist</error>"
    exit 1
fi

if [ ! -f "setup.py" ]; then
    echo "<error>setup.py doesn't exist</error>"
    exit 1
fi

if [ -d "venv" ]; then
    echo "<error>venv file found in repo</error>"
    exit 1
fi

# Create a virtual env if it doesn't exist

if [ ! -f "automarker_venv" ]; then
    echo "creating venv"
    python3 -m venv automarker_venv
fi

source automarker_venv/bin/activate
# install the package

python setup.py develop 2>&1
pip install -r requirements.txt 2>&1

# run their tests

echo "<their-tests>"
pytest 2>&1
echo "</their-tests>"

# replace their tests with the reference project tests and make sure it all still works

cp -r  $REFERENCE_PROJECT_PATH/tests .
echo "<our-tests>"
pytest  2>&1
echo "</our-tests>"

# and put the tests back

rm -rf tests
git reset --hard HEAD

