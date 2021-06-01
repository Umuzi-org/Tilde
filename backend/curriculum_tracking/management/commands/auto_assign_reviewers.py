from typing import Iterable
from core.models import User
from curriculum_tracking.models import AgileCard, ContentItem, RecruitProject
from django.core.management.base import BaseCommand
from django.db.models import Count

REQUIRED_REVIEWERS_PER_CARD = 2
SKIP_CARD_TAGS = ["ncit"]


def get_cards_needing_reviewers() -> Iterable[AgileCard]:
    """
    cards need reviewers if:
    - they are project cards
    - they belong to active users
    - they don't have enough reviewers added
    """

    for card in (
        AgileCard.objects.filter(assignees__active__in=[True])
        .annotate(reviewer_count=Count("reviewers"))
        .filter(content_item__content_type=ContentItem.PROJECT)
        .filter(reviewer_count__lt=REQUIRED_REVIEWERS_PER_CARD)
    ):
        yield card


def get_possible_reviewers(card):
    """
    find active users who are currently competent for that card and flavour
    order by allocated review duties
    """
    project = card.recruit_project

    # User.objects.filter(active=True)
    RecruitProject.objects.filter(content_item=project.content_item).filter(
        complete_time
    ).filter(recruit_users__active__in=[True])


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("skip_teams", type=str, nargs="*")

    def handle(self, *args, **options):

        for card in get_cards_needing_reviewers():
            number_of_reviewers_to_add = (
                card.reviewers.count() - REQUIRED_REVIEWERS_PER_CARD
            )
            possible_reviewers = get_possible_reviewers(card)
            for user in possible_reviewers[:number_of_reviewers_to_add]:
                card.add_collaborator(user=user, add_as_project_reviewer=True)
