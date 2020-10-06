from django.core.management.base import BaseCommand
from social_auth.github_api import Api
from git_real.constants import PERSONAL_GITHUB_NAME

from pprint import pprint


class Command(BaseCommand):
    def handle(self, *args, **options):
        api = Api(PERSONAL_GITHUB_NAME)
        who = api.who_am_i()
        pprint(who)
