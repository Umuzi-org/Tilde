"create a user group if it does not yet exist. If the group was not active then activate it. You can choose not to activate existing Teams by setting the activate command-line parameter to false"

from django.core.management.base import BaseCommand
from core.models import Team


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("group_name", type=str)
        parser.add_argument("activate", type=bool, default=True, nargs="?")

    def handle(self, *args, **options):
        o, created = Team.objects.get_or_create(name=options["group_name"])
        if created:
            print("Created")
        else:
            print("Already exists")

            if options["activate"] and not o.active:
                print("activating group")
                o.active = True
                o.save()
