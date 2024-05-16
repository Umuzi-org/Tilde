from django.core.management.base import BaseCommand
from core.models import User, Team
import csv
from pathlib import Path
from session_scheduling.models import Session, SessionType


class Command(BaseCommand):
    def handle(self, *args, **options):
        headings = [
            "id",
            "session_type name",
            "Event title",
            "facilitator",
            "duration_minutes",
            "flavours",
            "attendee_emails",
            "attendee_board_links",
        ]
        with open("gitignore/technical_sessions_for_team.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            for session in (
                Session.objects.exclude(is_complete=True)
                .exclude(is_cancelled=True)
                .order_by("pk")
            ):
                print(session.id)
                flavours = ", ".join(session.flavour_names)
                writer.writerow(
                    [
                        session.id,
                        session.session_type.name,
                        session.get_title_copy(),
                        session.facilitator.email,
                        session.session_type.duration_minutes,
                        flavours,
                        "\n".join(u.email for u in session.attendees.all()),
                        "\n".join(
                            f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/users/{u.id}/board"
                            for u in session.attendees.all()
                        ),
                    ]
                )
