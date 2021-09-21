from typing import Iterable

from django.db.models.fields import IntegerField
from core.models import User
from curriculum_tracking.models import AgileCard, ContentItem, RecruitProject
from core.models import Team
from django.db.models import Count, F, IntegerField
from django.db.models import Q
from curriculum_tracking.management.helpers import user_is_competent_for_card_project
from config.models import NameSpace


"""
Step 1: competent reviewers
if there is a project that has started that has < {REQUIRED_REVIEWERS_PER_CARD} reviewers:
   exclude cards according to settings: SKIP_CARD_TAGS, EXCLUDE_TEAMS
   add random reviewers who have completed the project before until there are enough
   (At this point there may be slow reviewers, or people who are part time or inactive)

Step 2: team reviewer permission
get a list of people who have "reviewer" permission on the team. Add these people as reviewers until there are a maximum of {REQUIRED_REVIEWERS_PER_CARD} of these folks is added as a reviewer to each card
   exclude cards according to settings: SKIP_CARD_TAGS only
   at this point there may be 2 * REQUIRED_REVIEWERS_PER_CARD per card.

Step 3:
get a list of cards in the "review" column that have at least {REQUIRED_REVIEWERS_PER_CARD} smiles OR that have been in the review column for more than {x} days
get a list of people with "trusted reviewer" permission for the team
add a maximum of {y} trusted reviewers to each card
Now there might be a lot of people on a card. But it will move

Missing:
If someone has earned trust then they should probably get added at step 1. But I'll leave that out for now.

@ryan says: Looks good, but am unsure of the below:
Missing:
If someone has earned trust then they should probably get added at step 1. But I'll leave that out for now.

If someone has earned trust should they be added at Step 1 or Step 3 If they are added at step 1 there is a chance they will close a card before another review happens and this may slow the trust propagation, unless we have some front end indication for trusted reviewers so they know not to review first. What are your thought?
"""


def get_config():
    config_namespace = NameSpace.objects.get(
        name="management_actions/auto_assign_reviewers",
    )

    REQUIRED_REVIEWERS_PER_CARD = config_namespace.get_value(
        "REQUIRED_REVIEWERS_PER_CARD"
    )  # 3
    SKIP_CARD_TAGS = config_namespace.get_value("SKIP_CARD_TAGS")
    EXCLUDE_TEAMS = config_namespace.get_value("EXCLUDE_TEAMS")

    return REQUIRED_REVIEWERS_PER_CARD, SKIP_CARD_TAGS, EXCLUDE_TEAMS


def get_cards_needing_regular_reviewers() -> Iterable[AgileCard]:
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


def get_possible_competent_reviewers(card):
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


def auto_assign_competent_reviewers():
    REQUIRED_REVIEWERS_PER_CARD, SKIP_CARD_TAGS, EXCLUDE_TEAMS = get_config()
    cards = list(get_cards_needing_regular_reviewers())
    total = len(cards)
    for n, card in enumerate(cards):
        number_of_reviewers_to_add = (
            REQUIRED_REVIEWERS_PER_CARD - card.reviewers.count()
        )
        assert number_of_reviewers_to_add > 0
        print(
            f"card {n+1}/{total}\n\t[{card.id}] {card} {card.flavour_names} - {card.assignees.first().email}\n\tneeds {number_of_reviewers_to_add} reviewer(s)"
        )
        possible_reviewers = get_possible_competent_reviewers(card)
        for i, user in enumerate(possible_reviewers):
            if card.reviewers.count() >= REQUIRED_REVIEWERS_PER_CARD:
                print("there are now enough")
                break

            print(f"Add collaborator {i+1}: \n\tnew reviewer = {user}\n")
            card.add_collaborator(user=user, add_as_project_reviewer=True)
        print(f"card now has {card.reviewers.count()} reviewers\n")


def get_user_current_review_duty_count(user):
    return user.projects_to_review.filter(
        ~Q(agile_card__status=AgileCard.COMPLETE)
    ).count()


def auto_assign_reviewers_based_on_permission(
    permission, required_card_status, required_positive_reviews=0
):
    from guardian.shortcuts import get_users_with_perms, get_objects_for_user

    REQUIRED_REVIEWERS_PER_CARD, SKIP_CARD_TAGS, EXCLUDE_TEAMS = get_config()

    for team in Team.objects.filter(active=True):
        # for team in [Team.objects.get(pk=162)]:
        print(f"\nTeam: {team.name}")
        user_permissions = get_users_with_perms(
            team, attach_perms=True, with_superusers=False
        )
        reviewer_users = [
            u for u in user_permissions if permission in user_permissions[u]
        ]
        reviewer_users = [
            u
            for u in reviewer_users
            if team in get_objects_for_user(u, permission, Team, with_superuser=False)
        ]
        reviewer_users = [o for o in reviewer_users if o.github_name]
        if not reviewer_users:
            print(f"No users with permission {permission} for team {team}")
            continue
        print(f"users with permission: {reviewer_users}")

        cards = (
            AgileCard.objects.filter(assignees__active__in=[True])
            # .filter(assignees__teams__in=[team])
            .filter(content_item__content_type=ContentItem.PROJECT)
            .annotate(
                positive_reviews=F(
                    "recruit_project__code_review_competent_since_last_review_request",
                )
                + F("recruit_project__code_review_excellent_since_last_review_request")
                # output_field=IntegerField(),
            )
            .filter(positive_reviews__gte=required_positive_reviews)
            .exclude(content_item__tags__name__in=SKIP_CARD_TAGS)
            .filter(assignees__in=team.active_users)
        )

        if required_card_status:
            cards = cards.filter(status=required_card_status)
        else:
            cards = cards.filter(
                Q(status=AgileCard.IN_PROGRESS)
                | Q(status=AgileCard.IN_REVIEW)
                | Q(status=AgileCard.REVIEW_FEEDBACK)
            )

        for card in cards:
            current_reviewers = list(card.reviewers.all())
            matching_reviewers = [u for u in current_reviewers if u in reviewer_users]
            reviewers_needed = REQUIRED_REVIEWERS_PER_CARD - len(matching_reviewers)
            if reviewers_needed > 0:
                reviewer_users.sort(key=get_user_current_review_duty_count)
                for new_reviewer in reviewer_users[:reviewers_needed]:

                    # print(card)
                    print(f"{card}:\n\t{new_reviewer}\n")
                    # breakpoint()
                    card.add_collaborator(
                        user=new_reviewer, add_as_project_reviewer=True
                    )


def auto_assign_reviewers():
    auto_assign_competent_reviewers()
    # auto_assign_reviewers_based_on_permission(permission = Team.PERMISSION_REVIEW_CARDS)
    auto_assign_reviewers_based_on_permission(
        permission=Team.PERMISSION_TRUSTED_REVIEWER,
        required_card_status=AgileCard.IN_REVIEW,
        required_positive_reviews=3,
    )
