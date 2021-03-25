""" look at all the ContentItems and create/update cards as needed"""
from django.core.management.base import BaseCommand
from core import models as core_models
from django.db.models import Q
from curriculum_tracking.models import Curriculum

from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
    generate_all_content_cards_for_team,
)

from core.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)
        parser.add_argument("curriculum", type=str, default=None)

    def handle(self, *args, **options):
        user = None
        who = options["who"]

        name = options["curriculum"]
        if name:
            curriculum = Curriculum.objects.get(Q(short_name=name) | Q(name=name))
        else:
            curriculum = None

        if who:
            if "@" in who:
                user = User.objects.get(email=who)
                generate_and_update_all_cards_for_user(user, curriculum)

            else:
                team = core_models.Team.objects.get(name=who)
                generate_all_content_cards_for_team(team, curriculum)
