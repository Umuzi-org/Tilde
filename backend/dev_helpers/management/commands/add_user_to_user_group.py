from django.core.management.base import BaseCommand
from core.models import UserGroup, User, UserGroupMembership


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("group_name", type=str)
        parser.add_argument("roles", type=str, nargs="*")

    def handle(self, *args, **options):
        user = User.objects.get(email=options["email"])
        group = UserGroup.objects.get(name=options["group_name"])

        membership, created = UserGroupMembership.objects.get_or_create(
            user=user, group=group
        )

        if created:
            print("created")

        roles = options["roles"]
        if roles:
            raise Exception(f"Not implemented: roles = {roles}")
