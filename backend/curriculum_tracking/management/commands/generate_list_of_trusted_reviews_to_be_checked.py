from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q
from curriculum_tracking.models import RecruitProjectReview, AgileCard
from core.models import User
from pathlib import Path
import csv
from curriculum_tracking.constants import COMPETENT, EXCELLENT
from django.utils import timezone


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who")

    def handle(self, *args, **options):
        who = options["who"]
        users = User.get_users_from_identifier(who)

        data = []

        for user in users:
            # trusts = ReviewTrust.objects.filter(user=user)
            # for trust in trusts:
            print(user.email)

            reviews = (
                RecruitProjectReview.objects.filter(trusted=True)
                .filter(reviewer_user=user)
                .filter(Q(status=COMPETENT) | Q(status=EXCELLENT))
                .filter(timestamp__gte=timezone.now() - timezone.timedelta(days=30))
                .order_by("-timestamp")
                .prefetch_related("recruit_project__agile_card")
            )

            for review in reviews:
                project = review.recruit_project
                try:
                    project.agile_card
                except AgileCard.DoesNotExist:
                    continue
                card_id = project.agile_card.id
                card_url = f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card_id}"
                # content_item_id = project.content_item_id
                title = project.content_item.title
                flavours = project.flavour_names

                data.append(
                    {
                        "reviewer email": user.email,
                        "content title": title,
                        "flavours": ", ".join(flavours),
                        "card url": card_url,
                        "content url": project.content_item.url,
                        "review time": review.timestamp,
                    }
                )

        headings = data[0].keys()

        with open(
            Path(f"gitignore/trusted_reviews.csv"),
            "w",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            writer.writerows([[d[heading] for heading in headings] for d in data])
