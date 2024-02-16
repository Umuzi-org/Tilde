from django.core.management.base import BaseCommand
from core.models import User, Team
import csv
from pathlib import Path


class Command(BaseCommand):
    def handle(self, *args, **options):
        headings = ["user_id", "user_email", "team_names"]
        with open(Path("gitignore/users.csv"), "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            for user in User.objects.filter(active=True):
                writer.writerow(
                    [
                        user.id,
                        user.email,
                        " | ".join([team.name for team in user.teams()]),
                    ]
                )

        headings = ["team_id", "team"]
        with open(Path("gitignore/teams.csv"), "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            for team in Team.objects.filter(active=True):
                writer.writerow([team.id, team.name])
