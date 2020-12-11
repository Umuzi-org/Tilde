from django.core.management.base import BaseCommand
from core.models import Team, User, TeamMembership


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("group_name", type=str)

    def handle(self, *args, **options):
        group = Team.objects.get(name=options["group_name"])

        members = TeamMembership.objects.filter(group=group, permission_student=True)

        for member in members:
            print(member.user.email)
