from django.core.management.base import BaseCommand
from core.models import User 
from pprint import pprint

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)

    def handle(self, *args, **options):
        user = User.objects.get(email=options['email'])
        pprint(user.get_permissions())
