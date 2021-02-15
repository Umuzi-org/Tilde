"""
python manage.py assign_repo_collab TEAM_SHUFFLE_REVIEW_SELF $TEAM_NAME $CONTENT_ITEM_TITLE 
python manage.py assign_repo_collab TEAM_SHUFFLE_REVIEW_OTHER $TEAM_NAME $CONTENT_ITEM_TITLE $NAME_OF_GROUP_DOING_THE_REVIEWING
python manage.py assign_repo_collab ADD_USER_TO_REPO_ONLY $TEAM_NAME $CONTENT_ITEM_TITLE $EMAIL_OR_GITHUB_NAME_OF_REVIEWER #can be used to assign people as repo collabs when they aren't Tilde users
python manage.py assign_repo_collab ADD_USER_AS_CARD_REVIEWER $TEAM_NAME $CONTENT_ITEM_TITLE $EMAIL_OF_REVIEWER
"""

from django.core.management.base import BaseCommand
from curriculum_tracking.models import ContentItem
from git_real.constants import PERSONAL_GITHUB_NAME, ORGANISATION

from git_real.helpers import add_collaborator
from social_auth.github_api import Api
import random
from django.contrib.auth import get_user_model
from social_auth.models import SocialProfile
import itertools

from ..helpers import get_team, get_team_cards

User = get_user_model()

TEAM_SHUFFLE_REVIEW_SELF = "TEAM_SHUFFLE_REVIEW_SELF"
TEAM_SHUFFLE_REVIEW_OTHER = "TEAM_SHUFFLE_REVIEW_OTHER"
ADD_USER_TO_REPO_ONLY = "ADD_USER_TO_REPO_ONLY"
ADD_USER_AS_CARD_REVIEWER = "ADD_USER_AS_CARD_REVIEWER"


def has_social_profile(user):
    try:
        user.social_profile
    except SocialProfile.DoesNotExist:
        return False
    return True


def shuffle_project_reviewers(cards, users):
    # print("shuffle")
    cards = list(cards)
    filtered_users = [o for o in users if has_social_profile(o) and o.active]

    user_permutations = list(itertools.permutations(filtered_users))

    # breakpoint()
    random.shuffle(user_permutations)

    for permutation in user_permutations:
        permutation = list(permutation)
        valid = True
        while len(permutation) < len(cards):
            permutation.extend(permutation)

        for (card, user) in zip(cards, permutation):
            if (user in card.assignees.all()) or (user in card.reviewers.all()):
                valid = False
                break

        if valid:
            return zip(cards, permutation)

    raise Exception("No valid permutation")

    #         return shuffle_project_reviewers(cards, users)
    # # we have a winner
    # print("win")
    # return zip(cards, users)


def team_self_review(team_name, content_item, reviewer=None):
    if reviewer:
        raise Exception(
            "Unexpected reviewer argument. When shuffling a team then dont supply a reviewer"
        )
    team = get_team(team_name)
    cards = get_team_cards(team, content_item)
    users = team.active_users
    assign_random_reviewers(cards, users)


def team_review_other(team_name, content_item, reviewer):
    team = get_team(team_name)
    cards = get_team_cards(team, content_item)
    reviewer_team = get_team(reviewer)
    reviewer_users = reviewer_team.active_users
    assign_random_reviewers(cards, reviewer_users)


def assign_random_reviewers(cards, users):
    api = Api(PERSONAL_GITHUB_NAME)
    shuffled_reviewers = list(
        shuffle_project_reviewers(cards, [o for o in users if o.active])
    )

    for card, user in shuffled_reviewers:
        print(user)

        if card.recruit_project:
            project = card.recruit_project
            if project.repository and project.repository.full_name.startswith(
                ORGANISATION
            ):
                add_collaborator(
                    api, project.repository.full_name, user.social_profile.github_name
                )
            project.reviewer_users.add(user)
            project.save()

        if user not in card.reviewers.all():
            card.reviewers.add(user)
            card.save()


def add_reviewer(team, content_item, reviewer, add_as_project_reviewer):
    api = Api(PERSONAL_GITHUB_NAME)

    cards = get_team_cards(team, content_item)

    if "@" in reviewer:
        user = User.objects.get(email=reviewer)
    else:
        user = User.objects.get(social_profile__github_name=reviewer)

    github_name = user.social_profile.github_name

    for card in cards:

        if card.recruit_project and card.repository:
            add_collaborator(api, card.repository.full_name, github_name)
        card.save()
        if add_as_project_reviewer:
            card.reviewers.add(user)
            if card.recruit_project:
                card.recruit_project.reviewer_users.add(user)
        card.save()
        # project.agile_card.reviewers =


def git_user_as_reviewer(team_name, content_item, reviewer):
    team = get_team(team_name)
    add_reviewer(team, content_item, reviewer, add_as_project_reviewer=True)


def git_user_repo_only(team_name, content_item, reviewer):
    team = get_team(team_name)
    add_reviewer(team, content_item, reviewer, add_as_project_reviewer=False)


allowed_commands = {
    ADD_USER_AS_CARD_REVIEWER: git_user_as_reviewer,
    ADD_USER_TO_REPO_ONLY: git_user_repo_only,
    TEAM_SHUFFLE_REVIEW_SELF: team_self_review,
    TEAM_SHUFFLE_REVIEW_OTHER: team_review_other,
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("command", type=str)
        parser.add_argument("cohort", type=str)
        parser.add_argument("content_item", type=str)
        parser.add_argument("reviewer", type=str, nargs="?")

    def handle(self, *args, **options):
        command = options["command"]
        assert (
            command in allowed_commands
        ), f"command '{command}' not allowed. Choose one of {list(allowed_commands.keys())}"
        cohort_name = options["cohort"]
        content_item_name = options["content_item"]
        reviewer = options["reviewer"]

        content_item = ContentItem.objects.get(
            title=content_item_name, content_type=ContentItem.PROJECT
        )

        allowed_commands[command](
            cohort_name, content_item=content_item, reviewer=reviewer
        )
