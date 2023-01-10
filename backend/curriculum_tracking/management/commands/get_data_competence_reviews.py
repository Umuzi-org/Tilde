"""
example usage:
python manage.py get_data_competence_reviews "Staff Tech Education"
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User
from pathlib import Path
import csv
from curriculum_tracking.models import RecruitProjectReview, AgileCard


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
            for review in (
                RecruitProjectReview.objects.filter(reviewer_user=user)
                .filter(timestamp__gte=timezone.now() - timezone.timedelta(days=90))
                .order_by("-timestamp")
            ):

                try:
                    card_id = review.recruit_project.agile_card.id
                except AgileCard.DoesNotExist:
                    card_id = None

                data.append(
                    {
                        "user.email": user.email,
                        "review.recruit_project.content_item.title": review.recruit_project.content_item.title,
                        "review.timestamp": review.timestamp,
                        "review.recruit_project.flavour_names": review.recruit_project.flavour_names,
                        "review.status": review.status,
                        "review.validated ": review.validated,
                        "review.recruit_project.agile_card.id": card_id,
                        "url": f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card_id}",
                    }
                )

        headings = data[0].keys()

        with open(
            Path(f"gitignore/review_export_{who}_{today.strftime('%a %d %b %Y')}.csv"),
            "w",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            writer.writerows([[d[heading] for heading in headings] for d in data])
