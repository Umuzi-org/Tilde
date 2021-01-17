from core import permissions
from django.core.management.base import BaseCommand
from core.models import User, Team
from guardian.shortcuts import assign_perm


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("permission", type=str)
        parser.add_argument("team", type=str)

    def handle(self, *args, **options):
        user = User.objects.get(email=options["email"])
        team = Team.objects.get(name=options["team"])
        permission = options["permission"]

        assign_perm(permission, user, team)
        assert user.has_perm(permission, team)
