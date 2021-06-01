from typing import Iterable
from core.models import User
from curriculum_tracking.models import AgileCard, ContentItem, RecruitProject
from django.core.management.base import BaseCommand
from django.db.models import Count, OuterRef

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


def filter_by_flavour_match(query, flavours):
    pks = [flavour.id for flavour in flavours]
    query = query.annotate(flavour_count=Count("flavours")).filter(
        flavour_count=len(pks)
    )
    for pk in pks:
        query = query.filter(flavours__pk=pk)
    return query


def get_possible_reviewers(card):
    """
    find active users who are currently competent for that card and flavour
    order by allocated review duties like so:

    count the number of cards with the same content_item and flavours where a user is the reviewer. Order = count ascending
    """

    project = card.recruit_project

    projects: RecruitProject = RecruitProject.objects.filter(
        content_item=project.content_item
    ).filter(recruit_users__active__in=[True])
    projects = filter_by_flavour_match(projects, project.flavours.all())

    complete_projects = projects.filter(complete_time__isnull=False)

    competent_users = User.objects.filter(
        recruit_projects__in=complete_projects
    ).exclude(projects_to_review__in=[project])

    competent_users = competent_users.annotate(duty_count=Count("projects_to_review"))
    competent_users = competent_users.order_by("duty_count")
    for user in competent_users:
        # print(f"{user} - {user.projects_to_review.count()}")
        yield user


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
                print(f"Add collaborator:\n\tcard = {card}\n\tnew reviewer = {user}")
                # card.add_collaborator(user=user, add_as_project_reviewer=True)
