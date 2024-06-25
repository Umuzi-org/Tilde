"""
Project review weight estimates can be seen here: https://docs.google.com/spreadsheets/d/17XRN7Zg6QZzpIdlRPGy0Gw2Q6HAU-RDgsQxkvwmV58c/edit#gid=0 

For now we are just using these values. In future we would like to calculate them automatically.
"""

from google_helpers.utils import fetch_sheet
from django.core.management.base import BaseCommand
from project_review_pricing.models import ProjectReviewAgileWeight

def process_row(row):
    content_item_id = int(row["id"])
    flavour_names = row["flavours"].split() 
    weight = int(row["review weight"])
    ProjectReviewAgileWeight.set_review_weight(content_item_id,flavour_names,weight)

class Command(BaseCommand):
    def handle(self, *args, **options):
        df = fetch_sheet(
            url="https://docs.google.com/spreadsheets/d/17XRN7Zg6QZzpIdlRPGy0Gw2Q6HAU-RDgsQxkvwmV58c/edit#gid=0 "
        )
        df = df.dropna(subset=["id"])
        df.apply(process_row, axis=1)