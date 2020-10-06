from google_helpers.sheets_attendance import (
    get_sheet_as_df,
    AFTERNOON,
    COL_EMAIL,
    COL_TIMESTAMP,
)
from attendance.models import AfternoonAttendance
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

User = get_user_model()


def save_row(row):
    print(f"afternoon - {row[COL_EMAIL]}")
    user, _ = User.objects.get_or_create(email=row[COL_EMAIL])
    AfternoonAttendance.objects.get_or_create(
        user=user,
        date=row[COL_TIMESTAMP].date(),
        defaults={
            "still_on_track": row["still_on_track"],
            "reason_for_not_on_track": row["reason_for_not_on_track"],
            "comments": row["comments"],
            "late_reason": row["late_reason"],
            "score": row["score"],
            "timestamp": row[COL_TIMESTAMP],
        },
    )


def pull_afternoon_attendance(days):
    df = get_sheet_as_df(AFTERNOON)
    df = df[df["Timestamp"].dt.date == datetime.now().date() - timedelta(days=days)]
    df.apply(save_row, axis=1)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("days", type=int, nargs="?", default=0)

    def handle(self, *args, **options):
        pull_afternoon_attendance(options["days"])
