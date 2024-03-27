from session_scheduling.session_types import session_types

from django.core.management.base import BaseCommand

from session_scheduling.models import SessionType


def initialise_session_types():
    for session_type in session_types:
        SessionType.objects.get_or_create(
            name=session_type["name"], defaults=session_type["defaults"]
        )
        print(f"Created session type: {session_type}")
    print("Done")


class Command(BaseCommand):
    def handle(self, *args, **options):
        initialise_session_types()
