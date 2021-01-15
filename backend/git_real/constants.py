import os
from pathlib import Path
from backend.settings import GITHUB_BOT_USERNAME

# TODO: this should all be in settings.py
# import pytz

ORGANISATION = os.environ.get("GIT_REAL_ORG", "Umuzi-org")
PROJECT_REVIEWER_TEAM = os.environ.get(
    "GIT_REAL_PROJECT_REVIEWER_TEAM", "project_reviewers"
)

CLONE_DESTINATION = Path(os.environ.get("GIT_REAL_CLONE_DIR", "gitignore/sync_git"))

GITHUB_BASE_URL = "https://api.github.com"
GITHUB_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"  #'2017-02-11T15:09:20Z'

PERSONAL_GITHUB_NAME = os.environ.get("GIT_REAL_PERSONAL_GITHUB_NAME")


# https://developer.github.com/v3/#timezones
GITHUB_DEFAULT_TIMEZONE = "utc"


# GITHUB_BOT_USERNAME = "umuzibot"
# Note: this needs to be associated with an actual User in the db
# and has to be logged in.
# this should really be in settings.py