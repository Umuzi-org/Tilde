from django.core.management.base import BaseCommand
from google_helpers.utils import fetch_sheet
from core.models import User

email_column = "Email Address"


def process_row(row):
    try:
        user = User.objects.get(email=row[email_column])
    except User.DoesNotExist:
        return
    user.active = False
    user.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        sheet = "https://docs.google.com/spreadsheets/d/1W3TYRS5CUlOUExMJsDepkX0Zw7yIvg0ukRxNQRzeQQQ/"
        df = fetch_sheet(url=sheet)
        df = df.dropna(subset=[email_column])

        df.apply(process_row, axis=1)
