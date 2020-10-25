from django.core.management.base import BaseCommand
from core.models import UserGroup, User, UserGroupMembership
from curriculum_tracking.models import AgileCard, ContentItem
from ..helpers import get_student_users


def get_ip_project_cards(user):
    return AgileCard.objects.filter(
        assignees__in=[user],
        status=AgileCard.IN_PROGRESS,
        content_item__content_type=ContentItem.PROJECT,
    )


def unstart_project(card):
    project = card.recruit_project
    project.start_time = None
    project.save()

    # fresh_status = AgileCard.derive_status_from_project(project)
    fresh_status = card.status_ready_or_blocked()
    card.status = fresh_status
    assert fresh_status in [AgileCard.READY, AgileCard.BLOCKED], fresh_status
    card.save()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)

    def handle(self, *args, **options):
        users = get_student_users(options["who"])
        for user in users:
            cards = get_ip_project_cards(user)
            for card in cards:
                print(f"{user.email} {card}")
                # breakpoint()
                unstart_project(card)
