cd $DESTINATION_PATH
source automarker_venv/bin/activate

python -m pytest --tb=line  2>&1

