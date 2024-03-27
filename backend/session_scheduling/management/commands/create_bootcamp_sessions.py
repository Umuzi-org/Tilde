"""
Run this script weekly if there is an active bootcamp
"""

from django.core.management.base import BaseCommand
from session_scheduling.models import Session
from session_scheduling.session_types import SESSION_BOOTCAMP_ASSESSMENT
from selection_bootcamps.models import Bootcamp
from curriculum_tracking.models import RecruitProject
from django.utils import timezone


TASK_10_ID = 754
TASK_9_ID = 761
TASK_8_ID = 762

task_ids = [TASK_10_ID, TASK_9_ID, TASK_8_ID]

DUE_DAYS = 7  # If a session is created today, it is expected to be complete within {DUE_DAYS} days


def get_users_needing_sessions(bootcamp):
    """
    Get users who need sessions to be booked. We check what projects have been completed, and what sessions have already been booked. We just return people who still need something booked.
    """
    users = bootcamp.team.active_users

    completed_projects = RecruitProject.objects.filter(
        user__in=users, content_item_id__in=task_ids, complete_time__isnull=False
    )

    users_who_should_have_sessions = [
        project.recruit_users.first() for project in completed_projects
    ]

    users_with_sessions = get_users_with_sessions()

    final = [
        user
        for user in users_who_should_have_sessions
        if user not in users_with_sessions
    ]
    return final


def get_users_with_sessions(bootcamp):
    """
    List the bootcamp attendees who already have sessions for this bootcamp
    If the session is cancelled it does not count
    """

    sessions = (
        Session.objects.filter(session_type=SESSION_BOOTCAMP_ASSESSMENT)
        .filter(related_to=bootcamp)
        .filter(cancelled=False)
        .prefetch_related("attendees")
    )

    attendees = [session.attendees.first() for session in sessions]
    return attendees


def create_sessions(bootcamp):
    """
    Create sessions for the bootcamp
    """
    users = get_users_needing_sessions(bootcamp)
    for user in users:
        session = Session.objects.create(session_type=SESSION_BOOTCAMP_ASSESSMENT)
        session.attendees.add(user)
        session.flavour  # TODO, get from stream
        session.due_date = timezone.now() + timezone.timedelta(days=DUE_DAYS)
        session.related = bootcamp.TODO
        session.save()


def create_bootcamp_sessions():
    bootcamps = Bootcamp.objects.filter(active=True)
    for bootcamp in bootcamps:
        bootcamp.create_sessions()
        print(f"Created sessions for {bootcamp}")

    print("Done")


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_bootcamp_sessions()
