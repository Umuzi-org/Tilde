cd $DESTINATION_PATH
source automarker_venv/bin/activate

cd $REQUIREMENTS_DIRECTORY
pip install -r requirements.txt
pip install pytest --upgrade
