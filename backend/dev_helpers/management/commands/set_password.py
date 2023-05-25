from django.core.management.base import BaseCommand
from core.models import User


def generate_password():
    import string
    import random

    PASSWORD_LENGTH = 8
    characters = string.ascii_letters + string.digits + string.punctuation

    password = "".join([random.choice(characters) for _ in range(PASSWORD_LENGTH)])
    print(f"Generated string password (length={PASSWORD_LENGTH}):\n{password}")
    return password


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("--password", type=str)

    def handle(self, *args, **options):
        password = options["password"] or generate_password()
        user = User.objects.get(email=options["email"])
        user.set_password(password)
        user.save()
        print("password updated")
