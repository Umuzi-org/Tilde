from django.core.management.base import BaseCommand
from core.models import User
from curriculum_tracking.models import AgileCard
from pathlib import Path
from django.utils import timezone
import csv


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who")

    def handle(self, *args, **options):
        today = timezone.now().date()
        who = options["who"]
        users = User.get_users_from_identifier(who)

        data = []
        for user in users:
            print(f"processing user: {user.email}")
            for card in AgileCard.objects.filter(assignees__in=[user]):
                data.append(
                    {
                        "user.email": user.email,
                        "card.complete_time": card.complete_time,
                        "card.review_request_time": card.review_request_time,
                        "card.start_time": card.start_time,
                        "card.flavour_names": card.flavour_names,
                        "card.content_item.title": card.content_item.title,
                        "card.content_item.id": card.content_item.id,
                    }
                )

        headings = data[0].keys()

        with open(
            Path(f"gitignore/card_export_{who}_{today.strftime('%a %d %b %Y')}.csv"),
            "w",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            writer.writerows([[d[heading] for heading in headings] for d in data])


"""
python manage.py export_card_dates "Cohort 22 + 24 web dev"
python manage.py export_card_dates "Cohort 23 data sci"
python manage.py export_card_dates "Cohort 24 data eng"
python manage.py export_card_dates "Cohort 24 data eng Old Mutual"
python manage.py export_card_dates "Cohort 24 data sci"
python manage.py export_card_dates "Cohort 24 web dev"
python manage.py export_card_dates "Cohort 25 data eng"
python manage.py export_card_dates "Cohort 25 data eng alumni"
python manage.py export_card_dates "Cohort 25 data sci"
python manage.py export_card_dates "Cohort 25 it support"
python manage.py export_card_dates "Cohort 25 java"
python manage.py export_card_dates "Cohort 25 java alumni"
python manage.py export_card_dates "Cohort 25 web dev"
python manage.py export_card_dates "Cohort 25 web dev 1"
python manage.py export_card_dates "Cohort 25 web dev 2"
python manage.py export_card_dates "Cohort 25 web dev alumni"
python manage.py export_card_dates "Cohort 26 data sci"
python manage.py export_card_dates "Cohort 26 java"
python manage.py export_card_dates "Cohort 27 web dev"
"""