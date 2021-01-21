from django.core.management.base import BaseCommand
from core.models import User, Team
from guardian.shortcuts import assign_perm


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)
        parser.add_argument("permission", type=str)
        parser.add_argument("team", type=str)

    def handle(self, *args, **options):

        who = options["who"]
        if "@" in who:
            assign_to = User.objects.get(email=who)
        else:
            assign_to = Team.objects.get(name=who)
        team = Team.objects.get(name=options["team"])
        permission = options["permission"]

        assert team.active
        assign_perm(permission, assign_to, team)
        # assert assign_to.has_perm(permission, team)
