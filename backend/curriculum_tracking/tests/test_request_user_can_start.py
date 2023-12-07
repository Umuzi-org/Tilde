from django.test import TestCase
from guardian.shortcuts import assign_perm
from curriculum_tracking.models import AgileCard
from curriculum_tracking.tests import factories
from core.tests import factories as core_factories
from core.models import Team


class request_user_can_start_Tests(TestCase):
    def setUp(self):
        self.assignee_user = core_factories.UserFactory()
        self.user_with_manage_permissions = core_factories.UserFactory()
        self.user_without_manage_permissions = core_factories.UserFactory()
        self.user_team = core_factories.TeamFactory()

        self.user_team.user_set.add(self.assignee_user)
        self.user_team.save()

        assign_perm(
            Team.PERMISSION_MANAGE_CARDS,
            self.user_with_manage_permissions,
            self.user_team,
        )

        self.ready_card = factories.AgileCardFactory(status=AgileCard.READY)
        self.ip_card = factories.AgileCardFactory(status=AgileCard.IN_PROGRESS)
        self.feedback_card = factories.AgileCardFactory(
            status=AgileCard.REVIEW_FEEDBACK
        )
        self.review_card = factories.AgileCardFactory(status=AgileCard.IN_REVIEW)
        self.complete_card = factories.AgileCardFactory(status=AgileCard.COMPLETE)

        self.cards = [
            self.ready_card,
            self.ip_card,
            self.feedback_card,
            self.review_card,
            self.complete_card,
        ]

        for card in self.cards:
            card.assignees.set([self.assignee_user])

    def test_assignee_can_start_card(self):
        for card in self.cards:
            if card.status == AgileCard.READY:
                self.assertTrue(card.request_user_can_start(self.assignee_user))
            else:
                self.assertFalse(card.request_user_can_start(self.assignee_user))

    def test_user_with_team_manage_permissions_can_start_card(self):
        for card in self.cards:
            if card.status == AgileCard.READY:
                self.assertTrue(
                    card.request_user_can_start(self.user_with_manage_permissions)
                )
            else:
                self.assertFalse(
                    card.request_user_can_start(self.user_with_manage_permissions)
                )

    def test_user_without_team_manage_permissions_cannot_start_card(self):
        for card in self.cards:
            self.assertFalse(
                card.request_user_can_start(self.user_without_manage_permissions)
            )
