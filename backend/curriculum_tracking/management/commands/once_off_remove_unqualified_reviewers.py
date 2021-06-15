from django.core.management.base import BaseCommand
from curriculum_tracking.models import AgileCard, ContentItem
from curriculum_tracking.management.helpers import user_is_competent_for_card_project

from .auto_assign_reviewers import EXCLUDE_TEAMS, SKIP_CARD_TAGS


def remove_reviewer(card, user):
    print(f"removing: {user}")
    if card.recruit_project:
        card.recruit_project.reviewer_users.remove(user)
    card.reviewers.remove(user)


class Command(BaseCommand):
    def handle(self, *args, **options):
        cards = (
            AgileCard.objects.filter(assignees__active__in=[True])
            .exclude(assignees__groups__name__in=EXCLUDE_TEAMS)
            .exclude(content_item__tags__name__in=SKIP_CARD_TAGS)
            .filter(content_item__content_type=ContentItem.PROJECT)
        )
        total = cards.count()
        for i, card in enumerate(cards):
            print(f"{i+1}/{total}: {card} {card.flavour_names}")
            reviewers = card.reviewers.all()
            for reviewer in reviewers:
                if reviewer in card.assignees.all():
                    remove_reviewer(card, reviewer)
                    continue
                if card.is_trusted_reviewer(reviewer):
                    print(f"{reviewer} is trusted")
                    continue
                if not user_is_competent_for_card_project(card=card, user=reviewer):
                    remove_reviewer(card, reviewer)
