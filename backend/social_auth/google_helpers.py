from . import constants
from oauth2client import client
from pathlib import Path


def get_email_from_one_time_code(auth_code):
    from backend.settings import BASE_DIR

    GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE = (
        constants.GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE
    )

    if not GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE.exists():
        GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE = (
            Path(BASE_DIR) / "google-oauth-onetime-creds.json"
        )

    assert GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE.exists()

    credentials = client.credentials_from_clientsecrets_and_code(
        GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE, [], auth_code,
    )

    # Get profile info from ID token
    # userid = credentials.id_token["sub"]
    email = credentials.id_token["email"]
    return email
