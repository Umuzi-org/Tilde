""" look at all the ContentItems and create/update cards as needed"""
from django.core.management.base import BaseCommand
from curriculum_tracking import helpers
from core import models as core_models

from core.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str, nargs="?")

    # TODO allow command line parameters
    # default: run for all cohorts
    # optional: run for a single cohort
    def handle(self, *args, **options):
        user = None
        cohort = None
        who = options["who"]
        if who:
            if "@" in who:
                user = User.objects.get(email=who)
            else:
                cohort = core_models.Cohort.get_from_short_name(who)
        helpers.generate_project_cards(cohort=cohort, user=user)
