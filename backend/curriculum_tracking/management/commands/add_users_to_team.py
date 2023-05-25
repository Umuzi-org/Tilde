from django.core.management.base import BaseCommand
from core.models import Team, User
from ..helpers import get_users


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)
        parser.add_argument("team_name", type=str)

    def handle(self, *args, **options):
        team = Team.objects.get(name=options["team_name"])

        who = options["who"]
        users = get_users(who)

        for user in users:
            team.user_set.add(user)