"""if a usergroup is supplied, then remove the students in that group from all review requests, this student or group of students needs to focus on their own stuff for a while because they are behind"""
from django.core.management.base import BaseCommand
from ..helpers import get_student_users
from curriculum_tracking.models import AgileCard


def get_all_cards_user_is_reviewing(user):
    return AgileCard.objects.filter(reviewers__in=[user])


def remove_reviewer(card, user):
    if card.recruit_project:
        card.recruit_project.reviewer_users.remove(user)
    card.reviewers.remove(user)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)

    def handle(self, *args, **options):
        users = get_student_users(options["who"])
        for user in users:
            cards = get_all_cards_user_is_reviewing(user)
            for card in cards:
                if card.status in [
                    AgileCard.IN_PROGRESS,
                    AgileCard.BLOCKED,
                    AgileCard.READY,
                    AgileCard.IN_REVIEW,
                ]:
                    remove_reviewer(card, user)
