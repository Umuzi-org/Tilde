cd $DESTINATION_PATH
source automarker_venv/bin/activate

cd $REQUIREMENTS_DIRECTORY
pip install -r requirements.txt --use-pep517
pip install pytest --upgrade
