from django.core.management.base import BaseCommand
from core.models import Team, User, TeamMembership


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("team_name", type=str)

    def handle(self, *args, **options):
        user = User.objects.get(email=options["email"])
        team = Team.objects.get(name=options["team_name"])

        membership, created = TeamMembership.objects.get_or_create(user=user, team=team)

        if created:
            print("created")
