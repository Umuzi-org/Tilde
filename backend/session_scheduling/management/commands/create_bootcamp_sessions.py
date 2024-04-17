"""
Run this script at least weekly if there is an active bootcamp
"""

from django.core.management.base import BaseCommand
from session_scheduling.models import Session, SessionType
from session_scheduling.session_types import SESSION_BOOTCAMP_ASSESSMENT
from selection_bootcamps.models import Bootcamp
from curriculum_tracking.models import RecruitProject
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


TASK_10_ID = 754
TASK_9_ID = 761
TASK_8_ID = 762

bootcamp_project_content_item_ids = [TASK_10_ID, TASK_9_ID, TASK_8_ID]

DUE_DAYS = 21  # If a session is created today, it is expected to be complete within {DUE_DAYS} days


def get_users_needing_sessions(bootcamp):
    """
    Get users who need sessions to be booked. We check what projects have been completed, and what sessions have already been booked. We just return people who still need something booked.
    """
    users = bootcamp.team.active_users

    completed_projects = (
        RecruitProject.objects.filter(
            recruit_users__in=users,
        )
        .filter(content_item_id__in=bootcamp_project_content_item_ids)
        .filter(complete_time__isnull=False)
    )

    users_who_should_have_sessions = [
        project.recruit_users.first() for project in completed_projects
    ]

    users_with_sessions = get_users_with_sessions(bootcamp)

    final = [
        user
        for user in set(users_who_should_have_sessions)
        if user not in users_with_sessions
    ]
    return final


def get_users_with_sessions(bootcamp):
    """
    List the bootcamp attendees who already have sessions for this bootcamp
    If the session is cancelled it does not count
    """
    session_type = SessionType.objects.get(name=SESSION_BOOTCAMP_ASSESSMENT)

    sessions = (
        Session.objects.filter(session_type=session_type)
        # .filter(related_to=bootcamp)
        .filter(is_cancelled=False)
        .filter(related_object_content_type=ContentType.objects.get_for_model(bootcamp))
        .filter(related_object_id=bootcamp.id)
        .prefetch_related("attendees")
    )

    attendees = [session.attendees.first() for session in sessions]
    return attendees


def create_sessions(bootcamp):
    """
    Create sessions for the bootcamp
    """
    session_type = SessionType.objects.get(name=SESSION_BOOTCAMP_ASSESSMENT)

    users = get_users_needing_sessions(bootcamp)
    for user in users:
        session = Session.objects.create(
            session_type=session_type,
            due_date=timezone.now() + timezone.timedelta(days=DUE_DAYS),
        )
        session.attendees.add(user)
        session.related_object = bootcamp
        flavours = bootcamp.stream.flavour_names
        session.set_flavours(flavours)
        session.save()


def create_bootcamp_sessions():
    bootcamps = Bootcamp.objects.filter(active=True)
    for bootcamp in bootcamps:
        create_sessions(bootcamp)
        print(f"Created sessions for {bootcamp}")


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_bootcamp_sessions()
        print("Done")
