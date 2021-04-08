from django.core.management.base import BaseCommand
from curriculum_tracking.models import ReviewTrust

from google_helpers.utils import fetch_sheet


def process_row(row):
    if bool(int(row["broken"] or 0)):
        return

    ReviewTrust.add_specific_trust_instances(
        who=row["who"],
        content_item_title=row["content_item_title"],
        flavours=row["flavour"].split(","),
        update_previous_reviews=bool(int(row["update_previous_reviews"])),
    )


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = fetch_sheet(
            url="https://docs.google.com/spreadsheets/d/1DgXzVzD6K_5x44MXP98HkY2fUhj7No5P17T613UcA4o/edit#gid=0"
        )
        df.apply(process_row, axis=1)
