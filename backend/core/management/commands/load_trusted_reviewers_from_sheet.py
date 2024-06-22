from django.core.management.base import BaseCommand
from curriculum_tracking.models import ReviewTrust, ContentItem

from google_helpers.utils import fetch_sheet


def process_row(row):
    if bool(int(row["broken"] or 0)):
        return
    if bool(int(row["processed"] or 0)):
        return

    print(f"Processing {row}")

    flavours = [s for s in [s.strip() for s in row["flavour"].split(",")] if s]

    ReviewTrust.add_specific_trust_instances(
        who=row["who"],
        content_item_title=row["content_item_title"],
        flavours=flavours,
        update_previous_reviews=bool(int(row["update_previous_reviews"])),
    )


def check_content_item(row):
    if bool(int(row["broken"] or 0)):
        return
    # print(row["content_item_title"])

    try:
        content_item = ContentItem.objects.get(title=row["content_item_title"])
    except ContentItem.DoesNotExist:
        print(f"DoesNotExist: {row['content_item_title']}")
        return
    if content_item.content_type == ContentItem.PROJECT:
        # print("ok")
        pass
    else:
        print(f"Not a project: {row['content_item_title']}")


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = fetch_sheet(
            url="https://docs.google.com/spreadsheets/d/1DgXzVzD6K_5x44MXP98HkY2fUhj7No5P17T613UcA4o/edit#gid=0"
        )
        df = df.dropna(subset=["content_item_title", "who"])
        df.apply(check_content_item, axis=1)
        df.apply(process_row, axis=1)
