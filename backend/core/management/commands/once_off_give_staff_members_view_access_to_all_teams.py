from django.core.management.base import BaseCommand

from core.models import User

from core.models import User, Team
from guardian.shortcuts import assign_perm, remove_perm


class Command(BaseCommand):
    def handle(self, *args, **options):
        teams = list(Team.objects.filter(active=True))
        for user in User.objects.filter(is_staff=True):
            print(user)
            for team in teams:
                print(team)
                # if user.has_perm(Team.PERMISSION_VIEW_ALL, team):
                #     remove_perm(Team.PERMISSION_VIEW_ALL, user, team)
                assign_perm(Team.PERMISSION_VIEW_ALL, user, team)
