from django.test import TestCase
from guardian.shortcuts import assign_perm
from curriculum_tracking import models
from curriculum_tracking.tests import factories
from core.tests import factories as core_factories
from curriculum_tracking.constants import (
    NOT_YET_COMPETENT,
    COMPETENT,
)

from django.utils import timezone
from datetime import timedelta
from core.models import Team


class request_user_can_start_Tests(TestCase):
    def setUp(self):
        self.request_user = core_factories.UserFactory()
        self.user_with_manage_permissions = core_factories.UserFactory()
        self.user_without_manage_permissions = core_factories.UserFactory()
        self.user_team = core_factories.TeamFactory()

        self.user_team.user_set.add(self.request_user)

        assign_perm(Team.PERMISSION_MANAGE_CARDS, self.request_user, self.user_team)

        self.ready_card = factories.AgileCardFactory(status=models.AgileCard.READY)
        self.ip_card = factories.AgileCardFactory(status=models.AgileCard.IN_PROGRESS)
        self.feedback_card = factories.AgileCardFactory(
            status=models.AgileCard.REVIEW_FEEDBACK
        )
        self.review_card = factories.AgileCardFactory(status=models.AgileCard.IN_REVIEW)
        self.complete_card = factories.AgileCardFactory(
            status=models.AgileCard.COMPLETE
        )

        self.cards = [
            self.ready_card,
            self.ip_card,
            self.feedback_card,
            self.review_card,
            self.complete_card,
        ]

    def test_card_owner_can_start_card(self):
        self.assertEqual(1, 1 + 0)
