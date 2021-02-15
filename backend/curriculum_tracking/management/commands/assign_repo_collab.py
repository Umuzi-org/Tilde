"""
python manage.py assign_repo_collab TEAM_SHUFFLE_REVIEW_SELF $TEAM_NAME $CONTENT_ITEM_TITLE 
python manage.py assign_repo_collab TEAM_SHUFFLE_REVIEW_OTHER $TEAM_NAME $CONTENT_ITEM_TITLE $NAME_OF_GROUP_DOING_THE_REVIEWING
python manage.py assign_repo_collab ADD_USER_TO_REPO_ONLY $TEAM_NAME $CONTENT_ITEM_TITLE $EMAIL_OR_GITHUB_NAME_OF_REVIEWER #can be used to assign people as repo collabs when they aren't Tilde users
python manage.py assign_repo_collab ADD_USER_AS_CARD_REVIEWER $TEAM_NAME $CONTENT_ITEM_TITLE $EMAIL_OF_REVIEWER
"""

from django.core.management.base import BaseCommand
from curriculum_tracking.models import ContentItem

from django.contrib.auth import get_user_model

from curriculum_tracking.reviewer_allocation_helpers import (
    bulk_add_user_as_card_reviewer,
    bulk_add_user_to_repo_only,
    team_shuffle_review_self,
    team_shuffle_review_other,
)

User = get_user_model()

TEAM_SHUFFLE_REVIEW_SELF = "TEAM_SHUFFLE_REVIEW_SELF"
TEAM_SHUFFLE_REVIEW_OTHER = "TEAM_SHUFFLE_REVIEW_OTHER"
ADD_USER_TO_REPO_ONLY = "ADD_USER_TO_REPO_ONLY"
ADD_USER_AS_CARD_REVIEWER = "ADD_USER_AS_CARD_REVIEWER"


allowed_commands = {
    ADD_USER_AS_CARD_REVIEWER: bulk_add_user_as_card_reviewer,
    ADD_USER_TO_REPO_ONLY: bulk_add_user_to_repo_only,
    TEAM_SHUFFLE_REVIEW_SELF: team_shuffle_review_self,
    TEAM_SHUFFLE_REVIEW_OTHER: team_shuffle_review_other,
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
