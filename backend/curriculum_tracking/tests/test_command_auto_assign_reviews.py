from curriculum_tracking.models import AgileCard, ContentItem
from curriculum_tracking.management.commands.auto_assign_reviewers import (
    REQUIRED_REVIEWERS_PER_CARD,
    get_cards_needing_reviewers,
)
from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import AgileCardFactory, ContentItemFactory
from django.test import TestCase
from typing import List


class get_cards_needing_reviewers_Tests(TestCase):
    def setUp(self):
        AgileCardFactory(
            content_item=ContentItemFactory(content_type=ContentItem.TOPIC),
            recruit_project=None,
        )

        project_cards: List(AgileCard) = [
            AgileCardFactory() for i in range(REQUIRED_REVIEWERS_PER_CARD + 2)
        ]

        for n, card in enumerate(project_cards):
            assert card.assignees.count()
            for i in range(n):
                card.add_collaborator(UserFactory(), add_as_project_reviewer=True)

        self.project_cards_needing_review = [
            o
            for o in project_cards
            if o.reviewers.count() < REQUIRED_REVIEWERS_PER_CARD
        ]
        self.assertGreater(len(self.project_cards_needing_review), 0)

    def test_counts_work(self):

        result = get_cards_needing_reviewers()
        self.assertEqual(
            sorted([o.id for o in result]),
            sorted([o.id for o in self.project_cards_needing_review]),
        )

    def test_skip_inactive_users(self):
        for card in self.project_cards_needing_review:
            user = card.assignees.first()
            user.active = False
            user.save()

        result = get_cards_needing_reviewers()
        self.assertEqual(list(result), [])
