cd $DESTINATION_PATH
source automarker_venv/bin/activate

python -m pytest 2>&1
