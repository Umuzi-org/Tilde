from django.core.management.base import BaseCommand

from core.models import User

from core.models import User, Team
from guardian.shortcuts import assign_perm, remove_perm


class Command(BaseCommand):
    def handle(self, *args, **options):
        teams = list(Team.objects.all())
        for user in User.objects.all():
            for team in teams:
                if user.has_perm(Team.PERMISSION_VIEW_ALL, team):
                    remove_perm(Team.PERMISSION_VIEW_ALL, user, team)
                # assign_perm(Team.PERMISSION_VIEW_ALL, user, team)
