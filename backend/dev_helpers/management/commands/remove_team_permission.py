from django.core.management.base import BaseCommand
from core.models import User, Team
from guardian.shortcuts import remove_perm

# from curriculum_tracking.models import Team


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("permission", type=str)
        parser.add_argument("team", type=str)

    def handle(self, *args, **options):
        user = User.objects.get(email=options["email"])
        team = Team.objects.get(name=options["team"])
        remove_perm(options["permission"], user, team)
