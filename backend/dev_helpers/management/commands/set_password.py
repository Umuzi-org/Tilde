from django.core.management.base import BaseCommand
from core.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)

    def handle(self, *args, **options):
        user = User.objects.get(email=options["email"])
        user.set_password(options["password"])
        user.save()
        print("password updated")