cd $DESTINATION_PATH
source automarker_venv/bin/activate

SUBMISSION_URL=$SUBMISSION_URL python -m pytest --tb=line  2>&1

