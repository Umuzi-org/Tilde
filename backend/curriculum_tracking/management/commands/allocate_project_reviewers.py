from django.core.management.base import BaseCommand
from curriculum_tracking.models import ContentItem
from git_real.constants import PERSONAL_GITHUB_NAME, ORGANISATION

from git_real.helpers import add_collaborator
from social_auth.github_api import Api
import random

from ..helpers import get_user_cards

from core.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("assignee", type=str)
        parser.add_argument("reviewer", type=str)
        parser.add_argument("content_item", type=str)
        parser.add_argument("reviewer_count", type=int, default=1)

    def handle(self, *args, **options):
    
        api = Api(PERSONAL_GITHUB_NAME)

        assignee = options['assignee']
        reviewer = options['reviewer']
        content_item_name = options['content_item']
        reviewer_count = options['reviewer_count']

        assignee_users = User.get_users_from_identifier(assignee)
        reviewer_users = User.get_users_from_identifier(reviewer) if reviewer !=assignee else assignee_users 

        content_item = ContentItem.objects.get(
            title=content_item_name, content_type=ContentItem.PROJECT
        )

        cards = get_user_cards(users=assignee_users,content_item=content_item)
        reviewer_users = list(reviewer_users)
        total_cards = len(cards)



        for i,card in enumerate(cards):
            print(f"card {i+1}/{total_cards}: {card}")
            random.shuffle(reviewer_users)

            reviewers_added = 0 
            for user in reviewer_users:
                if (user in card.assignees.all()) or (user in card.reviewers.all()):
                    continue 
                reviewers_added += 1 
                print(f"adding reviewer {reviewers_added}: {user}")
                add_reviewer(card,user,api)
                if reviewers_added >= reviewer_count:
                    break 


def add_reviewer(card,user,api):
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