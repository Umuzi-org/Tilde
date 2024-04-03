from django.core.management.base import BaseCommand
from core.models import User, Team
import csv
from pathlib import Path
from session_scheduling.models import Session, SessionType


class Command(BaseCommand):
    def handle(self, *args, **options):
        headings = [
            "session.id",
            "session.session_type.name",
            "session.get_title_copy()",
            "session.session_type.duration_minutes",
            "flavours",
            "attendee.email",
        ]
        with open("gitignore/technical_sessions.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            for session in Session.objects.all():
                flavours = ", ".join(session.flavour_names)
                for attendee in session.attendees.all():
                    writer.writerow(
                        [
                            session.id,
                            session.session_type.name,
                            session.get_title_copy(),
                            session.session_type.duration_minutes,
                            flavours,
                            attendee.email,
                        ]
                    )
