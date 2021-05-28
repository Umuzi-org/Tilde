import logging
import pandas as pd
import gspread

# from functools import lru_cache
import re
from timezone_helpers import timestamp_str_to_tz_aware_datetime
from google_helpers.constants import TIMESTAMP_FORMAT, TIMEZONE_NAME


def timestamp_to_datetime(timestamp):

    return timestamp_str_to_tz_aware_datetime(
        timestamp=timestamp, zone_name=TIMEZONE_NAME, dt_format=TIMESTAMP_FORMAT
    )


def fetch_sheet(sheet: str = None, url: str = None):
    print(f"Fetching sheet: {sheet} {url}")
    service = get_gspread_service()
    if sheet:
        book = service.open(sheet)
    elif url:
        book = service.open_by_url(url)
    logging.info(f"fetched sheet {sheet}")
    sheet = book.sheet1  # choose the first sheet
    return pd.DataFrame(sheet.get_all_records())


def authorize_creds():
    import json
    from oauth2client.client import SignedJwtAssertionCredentials
    import os

    SCOPE = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    SECRETS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")

    if not SECRETS_FILE:
        raise Exception(
            "Missing environmental variable: GOOGLE_SHEETS_CREDENTIALS_FILE"
        )

    # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
    # Load in the secret JSON key in working directory (must be a service account)
    json_key = json.load(open(SECRETS_FILE))

    # Authenticate using the signed key
    credentials = SignedJwtAssertionCredentials(
        json_key["client_email"], json_key["private_key"], SCOPE
    )
    return credentials


def get_gspread_service():
    credentials = authorize_creds()
    ret = gspread.authorize(credentials)
    return ret


# def date_from_args(date): # Not tz aware
#     if type(date) is datetime.datetime:
#         return date.date()

#     for dt_format in [
#         "%m/%d/%Y %H:%M:%S",
#         "%m/%d/%Y %H:%M",
#         "%m/%d/%Y",
#         "%d/%m/%Y",
#         "%d/%m/%Y %H:%M",
#         "%d/%m/%Y %H:%M:%S",
#         "%Y/%m/%d %H:%M:%S",
#     ]:
#         try:
#             return datetime.datetime.strptime(date, dt_format).date()
#         except ValueError:
#             pass

#     raise Exception(f"date '{date}' not allowed")


# def timestamp_to_date(timestamp): # Not tz aware
#     return timestamp_to_datetime(timestamp).date()


def clean_project_url_part(df, source_col, dest_col):
    def mapper(row):
        found = re.match(".*(projects/.*$)", str(row[source_col]))
        if found:
            return found.groups()[0]
        return ""

    df[dest_col] = df.apply(mapper, axis=1)
    df = df[df[source_col].str.contains("projects/")]
    return df
