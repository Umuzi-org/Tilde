""" Exports basic data about all the cards of all the active users

Originally requested by Ant in January 2023
"""

from django.core.management.base import BaseCommand
from curriculum_tracking.models import AgileCard
import csv
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_cards = AgileCard.objects.filter(assignees__active=True)

        headings = [
            "email",
            "teams",
            "title",
            "flavours",
            "card status",
            "card_url",
            "user_url",
        ]

        today = timezone.now().date()

        total = all_cards.count()
        with open(
            f"gitignore/export_all_active_learner_cards_{today.strftime('%a %d %b %Y')}.csv",
            "w",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(headings)

            for i, card in enumerate(all_cards):
                print(f"card {i+1}/{total}")

                user = card.assignees.first()
                team_names = ", ".join([o.name for o in user.teams()])
                user_url = f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/users/{user.id}/board"
                card_url = f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card.id}"

                row = [
                    user.email,
                    team_names,
                    card.title,
                    card.flavour_names,
                    card.status,
                    card_url,
                    user_url,
                ]
                writer.writerow(row)
