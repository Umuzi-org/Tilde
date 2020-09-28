import os
from pathlib import Path

# from backend.settings import BASE_DIR

GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE = Path(
    os.environ.get(
        "GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE",
        "GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE MISSING",
    )
)

# if not GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE.exists():
#     GOOGLE_OAUTH_ONE_TIME_CLIENT_SECRET_FILE(
#         BASE_DIR / "google-oauth-onetime-creds.json"
#     )
