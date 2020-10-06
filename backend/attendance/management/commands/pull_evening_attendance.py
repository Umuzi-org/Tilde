from google_helpers.sheets_attendance import (
    get_sheet_as_df,
    EVENING,
    COL_EMAIL,
    COL_TIMESTAMP,
)
from attendance.models import EveningAttendance
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

User = get_user_model()


def save_row(row):
    print(f"evening - {row[COL_EMAIL]}")
    user, _ = User.objects.get_or_create(email=row[COL_EMAIL])
    EveningAttendance.objects.get_or_create(
        user=user,
        date=row[COL_TIMESTAMP].date(),
        defaults={
            "plan_completed_sucessfully": row["plan_completed_sucessfully"],
            "reason_not_completed": row["reason_not_completed"],
            "comments": row["comments"],
            "late_reason": row["late_reason"],
            "score": row["score"],
            "timestamp": row[COL_TIMESTAMP],
        },
    )


def pull_evening_attendance(days):
    df = get_sheet_as_df(EVENING)
    df = df[df["Timestamp"].dt.date == datetime.now().date() - timedelta(days=days)]
    df.apply(save_row, axis=1)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("days", type=int, nargs="?", default=0)

    def handle(self, *args, **options):
        pull_evening_attendance(options["days"])
