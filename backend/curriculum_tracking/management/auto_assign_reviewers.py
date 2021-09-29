import datetime
from typing import Iterable
from django.utils import timezone
from django.db.models import Count, F
from django.db.models import Q
from guardian.shortcuts import get_users_with_perms, get_objects_for_user
from core.models import User, Team
from curriculum_tracking.models import AgileCard, ContentItem, RecruitProject
from curriculum_tracking.management.helpers import user_is_competent_for_card_project
from config.models import NameSpace

CONFIGURATION_NAMESPACE = "management_actions/auto_assign_reviewers"

"""
# Step 1: competent reviewers

if there is a project that has started that has < {REQUIRED_COMPETENT_REVIEWERS_PER_CARD} reviewers:
   exclude cards according to settings: SKIP_CARD_TAGS_ALL_STEPS, EXCLUDE_TEAMS_FROM_COMPETENT_REVIEW_STEP
   add random reviewers who have completed the project before until there are enough.
   If possible, don't add multiple reviewers from the same team
   At this point there may be slow reviewers, or people who are part time or inactive

# Step 2: team reviewer permission

get a list of people who have "reviewer" permission on the team.
exclude people in EXCLUDE_REVIEWER_PERMISSIONED_USERS_IN_TEAMS teams
(eg: this can be used to give seta assessors review access to a team without actually adding them to any cards)

Add these people as reviewers until there are a maximum of {REQUIRED_REVIEWER_PERMISSIONED_REVIEWERS_PER_CARD} of these folks is added as a reviewer to each card

exclude cards according to settings: SKIP_CARD_TAGS_ALL_STEPS only

At this point there will be a maximum of REQUIRED_REVIEWER_PERMISSIONED_REVIEWERS_PER_CARD + REQUIRED_COMPETENT_REVIEWERS_PER_CARD per card.

# Step 3: add people who have trusted reviewer permission

Get a list of cards in the "review" column that have at least {TRUSTED_REVIEWER_ADD_POSITIVE_REVIEW_THRESHOLD} smiles OR that have been in the review column for more than {TRUSTED_REVIEW_WAIT_TIME} days
get a list of people with "trusted reviewer" permission for the team
add a maximum of {REQUIRED_TRUSTED_PERMISSIONED_REVIEWERS_PER_CARD} trusted reviewers to each card

At this point there will be a maximum of REQUIRED_REVIEWER_PERMISSIONED_REVIEWERS_PER_CARD + REQUIRED_COMPETENT_REVIEWERS_PER_CARD + REQUIRED_TRUSTED_PERMISSIONED_REVIEWERS_PER_CARD reviewers on the card



TODO Later:
people who have earned trust



Missing:
If someone has earned trust then they should probably get added at step 1. But I'll leave that out for now.

@ryan says: Looks good, but am unsure of the below:
Missing:
If someone has earned trust then they should probably get added at step 1. But I'll leave that out for now.

If someone has earned trust should they be added at Step 1 or Step 3 If they are added at step 1 there is a chance they will close a card before another review happens and this may slow the trust propagation, unless we have some front end indication for trusted reviewers so they know not to review first. What are your thought?
"""


# def get_config():

# config_namespace = NameSpace.objects.get(
#     name="management_actions/auto_assign_reviewers",
# )

# return config_namespace.values()

# REQUIRED_COMPETENT_REVIEWERS_PER_CARD = config_namespace.get_value(
#     "REQUIRED_COMPETENT_REVIEWERS_PER_CARD"
# )  # 3
# SKIP_CARD_TAGS_ALL_STEPS = config_namespace.get_value("SKIP_CARD_TAGS_ALL_STEPS")
# EXCLUDE_TEAMS_FROM_COMPETENT_REVIEW_STEP = config_namespace.get_value("EXCLUDE_TEAMS_FROM_COMPETENT_REVIEW_STEP")

# return (
#     REQUIRED_COMPETENT_REVIEWERS_PER_CARD,
#     SKIP_CARD_TAGS_ALL_STEPS,
#     EXCLUDE_TEAMS_FROM_COMPETENT_REVIEW_STEP,
# )


def get_cards_needing_competent_reviewers() -> Iterable[AgileCard]:
    """
    cards need reviewers if:
    - they are project cards
    - they belong to active users
    - they don't have enough reviewers added
    """

    config = NameSpace.get_config(CONFIGURATION_NAMESPACE)

    def card_team_check(card):
        for user in card.assignees.all():
            for team in user.teams():
                if not team.active:
                    continue
                for name in config.EXCLUDE_TEAMS_FROM_COMPETENT_REVIEW_STEP:
                    if name.lower() in team.name.lower():
                        # print(f"team = {team.name}")
                        # print("noop")
                        return
        # print("card ok")
        return True

    for card in (
        AgileCard.objects.filter(assignees__active__in=[True])
        .exclude(content_item__tags__name__in=config.SKIP_CARD_TAGS_ALL_STEPS)
        .annotate(reviewer_count=Count("reviewers"))
        .filter(content_item__content_type=ContentItem.PROJECT)
        .filter(reviewer_count__lt=config.REQUIRED_COMPETENT_REVIEWERS_PER_CARD)
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


def get_possible_competent_reviewers(card):
    """
    find active users who are currently competent for that card and flavour
    order by allocated review duties like so:

    count the number of cards with the same content_item and flavours where a user is the reviewer. Order = count ascending
    """
    config = NameSpace.get_config(CONFIGURATION_NAMESPACE)

    projects: RecruitProject = RecruitProject.objects.filter(
        content_item=card.content_item
    ).filter(recruit_users__active__in=[True])
    projects = filter_by_flavour_match(projects, card.flavours.all())

    complete_projects = projects.filter(complete_time__isnull=False)

    competent_users = (
        User.objects.filter(recruit_projects__in=complete_projects)
        .exclude(agile_cards_to_review__in=[card])
        .exclude(groups__name__in=config.EXCLUDE_TEAMS_FROM_COMPETENT_REVIEW_STEP)
    )

    competent_users = competent_users.annotate(duty_count=Count("projects_to_review"))
    # TODO: this will be unfair to people who work hard.
    # The duty count should be a combination of recent reviews done and projects to review
    competent_users = competent_users.order_by("duty_count")

    # TODO: check teams. Order stuff so that we don't end up with 2 users in a row who have the same team

    for user in competent_users:
        assert user_is_competent_for_card_project(card, user)
        yield user


def auto_assign_competent_reviewers():
    config = NameSpace.get_config(CONFIGURATION_NAMESPACE)

    cards = list(get_cards_needing_competent_reviewers())
    total = len(cards)
    for n, card in enumerate(cards):
        add_reviewers_to_card_until_enough(
            card,
            config.REQUIRED_COMPETENT_REVIEWERS_PER_CARD,
            reviewer_users=get_possible_competent_reviewers(card),
        )


def add_reviewers_to_card_until_enough(
    card, total_matching_reviewers_needed, reviewer_users
):
    if card.content_item.project_submission_type in [
        ContentItem.REPOSITORY,
        ContentItem.CONTINUE_REPO,
    ]:
        reviewer_users = [o for o in reviewer_users if o.github_name]

    current_reviewers = list(card.reviewers.all())
    matching_reviewers = [u for u in current_reviewers if u in reviewer_users]
    reviewers_needed = total_matching_reviewers_needed - len(matching_reviewers)
    if reviewers_needed > 0:
        reviewer_users = sorted(reviewer_users, key=get_user_current_review_duty_count)
        for new_reviewer in reviewer_users[:reviewers_needed]:
            print(f"{card}:\n\t{new_reviewer}\n")
            card.add_collaborator(user=new_reviewer, add_as_project_reviewer=True)


def get_user_current_review_duty_count(user):
    return user.projects_to_review.filter(
        ~Q(agile_card__status=AgileCard.COMPLETE)
    ).count()


def get_reviewer_users_by_permission(team, permission):
    user_permissions = get_users_with_perms(
        team, attach_perms=True, with_superusers=False
    )
    reviewer_users = [u for u in user_permissions if permission in user_permissions[u]]
    reviewer_users = [
        u
        for u in reviewer_users
        if team in get_objects_for_user(u, permission, Team, with_superuser=False)
    ]
    return reviewer_users


def get_cards_needing_trusted_reviewer_allocation(team):
    config = NameSpace.get_config(CONFIGURATION_NAMESPACE)

    threshold_time = timezone.now() - datetime.timedelta(
        days=config.TRUSTED_REVIEW_WAIT_TIME
    )

    return (
        AgileCard.objects.filter(assignees__active__in=[True])
        .filter(content_item__content_type=ContentItem.PROJECT)
        .annotate(
            positive_reviews=F(
                "recruit_project__code_review_competent_since_last_review_request",
            )
            + F("recruit_project__code_review_excellent_since_last_review_request")
        )
        .filter(
            Q(
                positive_reviews__gte=config.TRUSTED_REVIEWER_ADD_POSITIVE_REVIEW_THRESHOLD
            )
            | Q(recruit_project__review_request_time__lt=threshold_time)
        )
        .exclude(content_item__tags__name__in=config.SKIP_CARD_TAGS_ALL_STEPS)
        .filter(assignees__in=team.active_users)
        .filter(status=AgileCard.IN_REVIEW)
    )


def get_cards_needing_reviewer_allocation(team):
    config = NameSpace.get_config(CONFIGURATION_NAMESPACE)
    return (
        AgileCard.objects.filter(assignees__active__in=[True])
        .filter(content_item__content_type=ContentItem.PROJECT)
        .exclude(content_item__tags__name__in=config.SKIP_CARD_TAGS_ALL_STEPS)
        .filter(assignees__in=team.active_users)
        .filter(
            Q(status=AgileCard.IN_REVIEW)
            | Q(status=AgileCard.IN_PROGRESS)
            | Q(status=AgileCard.REVIEW_FEEDBACK)
        )
    )


def auto_assign_reviewers_based_on_reviewer_team_permission():
    config = NameSpace.get_config(CONFIGURATION_NAMESPACE)

    exclude_users_nested = [
        Team.objects.get(name=name).users.all()
        for name in config.EXCLUDE_REVIEWER_PERMISSIONED_USERS_IN_TEAMS
    ]
    exclude_users = [user for subset in exclude_users_nested for user in subset]

    for team in Team.objects.filter(active=True):
        print(f"\nTeam: {team.id} {team.name}")
        reviewer_users = get_reviewer_users_by_permission(
            team=team, permission=Team.PERMISSION_REVIEW_CARDS
        )
        reviewer_users = [o for o in reviewer_users if o not in exclude_users]

        if not reviewer_users:
            print(
                f"No users with permission {Team.PERMISSION_REVIEW_CARDS} for team {team}"
            )
            continue

        print(f"users with permission: {reviewer_users}")
        cards = get_cards_needing_reviewer_allocation(team)
        for card in cards:

            add_reviewers_to_card_until_enough(
                card=card,
                total_matching_reviewers_needed=config.REQUIRED_REVIEWER_PERMISSIONED_REVIEWERS_PER_CARD,
                reviewer_users=reviewer_users,
            )


def auto_assign_reviewers_based_on_trusted_team_permission():

    config = NameSpace.get_config(CONFIGURATION_NAMESPACE)

    for team in Team.objects.filter(active=True):
        print(f"\nTeam: {team.id} {team.name}")
        reviewer_users = get_reviewer_users_by_permission(
            team=team, permission=Team.PERMISSION_TRUSTED_REVIEWER
        )

        if not reviewer_users:
            print(
                f"No users with permission {Team.PERMISSION_TRUSTED_REVIEWER} for team {team}"
            )
            continue

        print(f"users with permission: {reviewer_users}")

        cards = get_cards_needing_trusted_reviewer_allocation(team)

        for card in cards:

            add_reviewers_to_card_until_enough(
                card=card,
                total_matching_reviewers_needed=config.REQUIRED_TRUSTED_PERMISSIONED_REVIEWERS_PER_CARD,
                reviewer_users=reviewer_users,
            )


def auto_assign_reviewers():
    auto_assign_reviewers_based_on_trusted_team_permission()
    auto_assign_competent_reviewers()
    auto_assign_reviewers_based_on_reviewer_team_permission()
