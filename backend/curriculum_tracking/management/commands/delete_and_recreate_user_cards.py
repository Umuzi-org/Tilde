from django.core.management.base import BaseCommand
from curriculum_tracking import models
from core import models as core_models
from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
)

from core.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)

    def handle(self, *args, **options):
        user = None
        who = options["who"]
        if who:
            if "@" in who:
                user = User.objects.get(email=who)
                models.AgileCard.objects.filter(assignees__in=[user]).delete()
                generate_and_update_all_cards_for_user(user, None)

            else:
                team = core_models.Team.objects.get(name=who)
                for user in team.users.filter(active=True):
                    models.AgileCard.objects.filter(assignees__in=[user]).delete()
                    generate_and_update_all_cards_for_user(user, None)
