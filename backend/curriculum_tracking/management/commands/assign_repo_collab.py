"""
python manage.py assign_repo_collab GROUP_SELF_REVIEW $USER_GROUP_NAME $CONTENT_ITEM_TITLE 
python manage.py assign_repo_collab GROUP_REVIEW_OTHER $USER_GROUP_NAME $CONTENT_ITEM_TITLE $NAME_OF_GROUP_DOING_THE_REVIEWING
python manage.py assign_repo_collab GIT_USER_REPO_ONLY $USER_GROUP_NAME $CONTENT_ITEM_TITLE $EMAIL_OR_GITHUB_NAME_OF_REVIEWER #can be used to assign people as repo collabs when they aren't Tilde users
python manage.py assign_repo_collab GIT_USER_AS_REVIEWER $USER_GROUP_NAME $CONTENT_ITEM_TITLE $EMAIL_OF_REVIEWER
"""

from django.core.management.base import BaseCommand
from curriculum_tracking.models import ContentItem
from git_real.constants import PERSONAL_GITHUB_NAME, ORGANISATION

from git_real.helpers import add_collaborator
from social_auth.github_api import Api
import random
from django.contrib.auth import get_user_model
from social_auth.models import SocialProfile

from ..helpers import get_group, get_group_project_cards

User = get_user_model()

GROUP_SELF_REVIEW = "GROUP_SELF_REVIEW"
GROUP_REVIEW_OTHER = "GROUP_REVIEW_OTHER"
GIT_USER_REPO_ONLY = "GIT_USER_REPO_ONLY"
GIT_USER_AS_REVIEWER = "GIT_USER_AS_REVIEWER"


def has_social_profile(user):
    try:
        user.social_profile
    except SocialProfile.DoesNotExist:
        return False
    return True


def shuffle_project_reviewers(cards, users):
    print("shuffle")
    cards = list(cards)
    users = [o for o in users if has_social_profile(o) and o.active]
    random.shuffle(users)
    while len(users) < len(cards):
        users.extend(users)

    for (card, user) in zip(cards, users):
        if (user in card.assignees.all()) or (user in card.reviewers.all()):
            return shuffle_project_reviewers(cards, users)
    # we have a winner
    print("win")
    return zip(cards, users)


def group_self_review(group_name, content_item, reviewer=None):
    if reviewer:
        raise Exception(
            "Unexpected reviewer argument. When shuffling a group then dont supply a reviewer"
        )
    group = get_group(group_name)
    cards = get_group_project_cards(group, content_item)
    users = group.active_student_users
    assign_random_reviewers(cards, users)


def group_review_other(group_name, content_item, reviewer):
    group = get_group(group_name)
    cards = get_group_project_cards(group, content_item)
    reviewer_group = get_group(reviewer)
    reviewer_users = reviewer_group.active_student_users
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


def add_reviewer(group, content_item, reviewer, add_as_project_reviewer):
    api = Api(PERSONAL_GITHUB_NAME)

    cards = get_group_project_cards(group, content_item)

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


def git_user_as_reviewer(group_name, content_item, reviewer):
    group = get_group(group_name)
    add_reviewer(group, content_item, reviewer, add_as_project_reviewer=True)


def git_user_repo_only(group_name, content_item, reviewer):
    group = get_group(group_name)
    add_reviewer(group, content_item, reviewer, add_as_project_reviewer=False)


allowed_commands = {
    GIT_USER_AS_REVIEWER: git_user_as_reviewer,
    GIT_USER_REPO_ONLY: git_user_repo_only,
    GROUP_SELF_REVIEW: group_self_review,
    GROUP_REVIEW_OTHER: group_review_other,
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
