from django.core.management.base import BaseCommand

from playwright.sync_api import sync_playwright
import os
from pathlib import Path
import csv
from django.contrib.auth import get_user_model
import datetime

from coderbyte_tests.models import CoderbyteTestResult
import re

CODERBYTES_EMAIL = os.environ["CODERBYTES_EMAIL"]
CODERBYTES_PASSWORD = os.environ["CODERBYTES_PASSWORD"]
CODERBYTES_ORG = os.environ["CODERBYTES_ORG"]


SAVE_PATH = Path(f"gitignore/coderbyte_export.csv")


COL_EMAIL = "Email"  # we will match this to a User
COL_REPORT_LINK = "Report Link"
COL_STATUS = "Status"  # Eg Submitted
COL_DATE_JOINED = (
    "Date Joined"  # when they started the test. eg '04/12/24' 03/12/24 MM/DD/YY
)
COL_DATE_INVITED = "Date Invited"
COL_ASSESSMENT_NAME = "Assessment Name"  # Eg 'Problem solving 2.2'
COL_ASSESSMENT_ID = "Assessment ID"  # Eg: 'software-engine-uy5ishc13z'
COL_PLAGIARISM = "Plagiarism"  # Eg: Likely
COL_TIME_TAKEN = "Time Taken"  # eg: 20m
COL_CHALLENGES_COMPLETED = "Challenges Completed"  # int
COL_CHALLENGE_SCORE = "Challenge Score"
COL_MULTIPLE_CHOICE_SCORE = "Multiple Choice Score"
COL_FINAL_SCORE = "Final Score"

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        download_csv()
        save_results()
        delete_csv()


def delete_csv():
    os.remove(SAVE_PATH)


def save_results():
    """Take the CB results and save them to the database"""

    with open(SAVE_PATH, "r") as f:
        reader = csv.reader(f)
        lines = [l for l in reader]
        header = lines[0]

        for line in lines[1:]:
            result_row = dict(zip(header, line))
            _save_single_result(result_row)


def _save_single_result(result_row: dict):
    """result_row is a dict with the keys being the column names and the values being the data for that row"""

    email = result_row[COL_EMAIL]

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # if the user isn't in our database then they are not a learner. Nothing to do
        return

    report_link = result_row[COL_REPORT_LINK]
    status = result_row[COL_STATUS]
    date_joined = _get_date_or_none(result_row[COL_DATE_JOINED])
    date_invited = _get_date_or_none(result_row[COL_DATE_INVITED])
    assessment_name = result_row[COL_ASSESSMENT_NAME]
    assessment_id = result_row[COL_ASSESSMENT_ID]

    plagiarism = result_row[COL_PLAGIARISM]
    if plagiarism == "null":
        plagiarism = None

    time_taken = _get_minutes_or_none(result_row[COL_TIME_TAKEN])
    challenges_completed = int(result_row[COL_CHALLENGES_COMPLETED])
    challenge_score = _get_score_or_none(result_row[COL_CHALLENGE_SCORE])

    multiple_choice_score = _get_score_or_none(result_row[COL_MULTIPLE_CHOICE_SCORE])

    final_score = _get_score_or_none(result_row[COL_FINAL_SCORE])

    defaults = {
        "status": status,
        "date_joined": date_joined,
        "date_invited": date_invited,
        "assessment_name": assessment_name,
        "assessment_id": assessment_id,
        "plagiarism": plagiarism,
        "time_taken_minutes": time_taken,
        "challenges_completed": challenges_completed,
        "challenge_score": challenge_score,
        "multiple_choice_score": multiple_choice_score,
        "final_score": final_score,
    }

    result_instance, created = CoderbyteTestResult.objects.get_or_create(
        report_link=report_link, user=user, defaults=defaults
    )
    if not created:
        for key, value in defaults.items():
            setattr(result_instance, key, value)
        result_instance.save()


def _get_score_or_none(score_str):
    if score_str == "N/A":
        return None
    return int(score_str)


def _get_date_or_none(date_str):
    if date_str == "N/A":
        return None
    return datetime.datetime.strptime(date_str, "%m/%d/%y").date()


def _get_minutes_or_none(time_str):
    """
    eg 2h 30m
    eg 30m
    """
    if time_str == "N/A":
        return None

    found = re.search(r"(\d+)h (\d+)m", time_str)
    if found:
        hours, minutes = found.groups()
        return int(hours) * 60 + int(minutes)
    found = re.search(r"(\d+)h", time_str)
    if found:
        hours = found.groups()[0]
        return int(hours) * 60
    found = re.search(r"(\d+)m", time_str)
    if found:
        minutes = found.groups()[0]
        return int(minutes)


def download_csv() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://coderbyte.com/sl-org")
        page.get_by_role("textbox").click()
        page.get_by_role("textbox").fill(CODERBYTES_EMAIL)
        page.get_by_role("button", name="Next →").click()
        page.locator('input[type="password"]').click()
        page.locator('input[type="password"]').fill(CODERBYTES_PASSWORD)
        page.get_by_role("button", name="Log in").click()
        page.get_by_role("link", name="Assessments").click()

        page.goto(
            f"https://coderbyte.com/dashboard/{CODERBYTES_ORG}#screening-analytics"
        )

        with page.expect_download() as download_info:
            page.get_by_role("button", name="CSV Export").click()
        download = download_info.value

        # now = datetime.datetime.now()
        download.save_as(SAVE_PATH)

        # ---------------------
        context.close()
        browser.close()
