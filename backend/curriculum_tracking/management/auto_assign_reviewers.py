from typing import Iterable
from core.models import User
from curriculum_tracking.models import AgileCard, ContentItem, RecruitProject
from django.db.models import Count
from django.db.models import Q
from curriculum_tracking.management.helpers import user_is_competent_for_card_project


from config.models import NameSpace


def get_config():
    config_namespace = NameSpace.objects.get(
        name="management_actions/auto_assign_reviewers",
    )

    REQUIRED_REVIEWERS_PER_CARD = config_namespace.get_value(
        "REQUIRED_REVIEWERS_PER_CARD"
    )  # 3
    SKIP_CARD_TAGS = config_namespace.get_value("SKIP_CARD_TAGS")  # ["ncit"]
    EXCLUDE_TEAMS = config_namespace.get_value("EXCLUDE_TEAMS")  # ["ncit"]

    return REQUIRED_REVIEWERS_PER_CARD, SKIP_CARD_TAGS, EXCLUDE_TEAMS


# EXCLUDE_TEAMS = [  # TODO: put this in the database or something. We shouldn't have this mixed in with the code
#     "Tech seniors",
#     "Staff Data Sci",
#     "Staff Scrum masters",
#     "Staff Web Dev",
#     "Tech Junior Staff",
#     "TechQuest Staff",
#     "Demo team",
#     "Boot",
#     "tech alumni",
# ]

STAFF_ONLY = []  # TODO


def get_cards_needing_reviewers() -> Iterable[AgileCard]:
    """
    cards need reviewers if:
    - they are project cards
    - they belong to active users
    - they don't have enough reviewers added
    """
    REQUIRED_REVIEWERS_PER_CARD, SKIP_CARD_TAGS, EXCLUDE_TEAMS = get_config()

    def card_team_check(card):
        for user in card.assignees.all():
            for team in user.teams():
                if not team.active:
                    continue
                for name in EXCLUDE_TEAMS:
                    if name in team.name:
                        # print(f"team = {team.name}")
                        # print("noop")
                        return
        # print("card ok")
        return True

    for card in (
        AgileCard.objects.filter(assignees__active__in=[True])
        # .exclude(assignees__groups__name__in=EXCLUDE_TEAMS)
        .exclude(content_item__tags__name__in=SKIP_CARD_TAGS)
        .annotate(reviewer_count=Count("reviewers"))
        .filter(content_item__content_type=ContentItem.PROJECT)
        .filter(reviewer_count__lt=REQUIRED_REVIEWERS_PER_CARD)
        .filter(
            Q(status=AgileCard.IN_PROGRESS)
            | Q(status=AgileCard.IN_REVIEW)
            | Q(status=AgileCard.REVIEW_FEEDBACK)
        )
    ):
        if card_team_check(card):
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
    REQUIRED_REVIEWERS_PER_CARD, SKIP_CARD_TAGS, EXCLUDE_TEAMS = get_config()
    projects: RecruitProject = RecruitProject.objects.filter(
        content_item=card.content_item
    ).filter(recruit_users__active__in=[True])
    projects = filter_by_flavour_match(projects, card.flavours.all())

    complete_projects = projects.filter(complete_time__isnull=False)

    competent_users = (
        User.objects.filter(recruit_projects__in=complete_projects)
        .exclude(agile_cards_to_review__in=[card])
        .exclude(groups__name__in=EXCLUDE_TEAMS)
    )

    competent_users = competent_users.annotate(duty_count=Count("projects_to_review"))
    competent_users = competent_users.order_by("duty_count")
    for user in competent_users:
        assert user_is_competent_for_card_project(card, user)
        yield user


def auto_assign_reviewers():
    REQUIRED_REVIEWERS_PER_CARD, SKIP_CARD_TAGS, EXCLUDE_TEAMS = get_config()
    cards = list(get_cards_needing_reviewers())
    total = len(cards)
    for n, card in enumerate(cards):
        number_of_reviewers_to_add = (
            REQUIRED_REVIEWERS_PER_CARD - card.reviewers.count()
        )
        assert number_of_reviewers_to_add > 0
        print(
            f"card {n+1}/{total}\n\t[{card.id}] {card} {card.flavour_names} - {card.assignees.first().email}\n\tneeds {number_of_reviewers_to_add} reviewer(s)"
        )
        possible_reviewers = get_possible_reviewers(card)
        for i, user in enumerate(possible_reviewers):
            if card.reviewers.count() >= REQUIRED_REVIEWERS_PER_CARD:
                print("there are now enough")
                break

            print(f"Add collaborator {i+1}: \n\tnew reviewer = {user}\n")
            card.add_collaborator(user=user, add_as_project_reviewer=True)
        print(f"card now has {card.reviewers.count()} reviewers\n")
