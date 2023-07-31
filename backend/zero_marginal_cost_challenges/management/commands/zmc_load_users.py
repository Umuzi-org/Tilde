"""load users from the zmc spreadsheet"""
from django.core.management.base import BaseCommand
from google_helpers.utils import fetch_sheet
from core.models import User, Team

SHEET_URL = "https://docs.google.com/spreadsheets/d/1x_6DcMfwwwG5Mw68MPONHmJw2VHMfU1ep10gC8BXNno/edit#gid=0"
COL_FIRST_NAME = "first name"
COL_LAST_NAME = "last name"
COL_EMAIL = "email"
COL_PILOT_DATE = "pilot date"
COL_PILOT_COURSE = "pilot course"
COL_EXTRA_IDENTIFIERS = "extra identifiers"
COL_LOADED = "loaded"


def process_row(row):
    if bool(int(row[COL_LOADED] or 0)):
        return

    print(f"Processing:\n{row}")

    first_name = row[COL_FIRST_NAME].strip()
    last_name = row[COL_LAST_NAME].strip()
    email = row[COL_EMAIL].strip()
    pilot_date = row[COL_PILOT_DATE].strip()
    pilot_course = row[COL_PILOT_COURSE].strip()
    extra_identifiers = row[COL_EXTRA_IDENTIFIERS].strip()

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    if created:
        user.set_password(email)
    user.save()

    team_name = f"ZMC {pilot_date} {pilot_course} {extra_identifiers}".strip()

    team, _ = Team.objects.get_or_create(name=team_name)
    team.user_set.add(user)


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = fetch_sheet(url=SHEET_URL)
        df = df.dropna(subset=[COL_EMAIL])
        df.apply(process_row, axis=1)
