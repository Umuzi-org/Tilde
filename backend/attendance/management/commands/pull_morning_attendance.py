from google_helpers.sheets_attendance import (
    get_sheet_as_df,
    MORNING,
    COL_EMAIL,
    COL_TIMESTAMP,
)
from attendance.models import MorningAttendance
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

User = get_user_model()


def save_row(row):
    # print(f"morning - {row[COL_EMAIL]}")
    user, _ = User.objects.get_or_create(email=row[COL_EMAIL])
    MorningAttendance.objects.get_or_create(
        user=user,
        # timestamp=row[COL_TIMESTAMP],
        date=row[COL_TIMESTAMP].date(),
        defaults={
            "plan_of_action": row["plan_of_action"],
            "problems_forseen": row["problems_forseen"],
            "requests": row["requests"],
            "late_reason": row["late_reason"],
            "score": row["score"],
            "timestamp": row[COL_TIMESTAMP],
        },
    )


def pull_morning_attendance(days):
    df = get_sheet_as_df(MORNING)
    df = df[df["Timestamp"].dt.date == datetime.now().date() - timedelta(days=days)]
    df.apply(save_row, axis=1)
    print(df.head())


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("days", type=int, nargs="?", default=0)

    def handle(self, *args, **options):
        pull_morning_attendance(options["days"])
