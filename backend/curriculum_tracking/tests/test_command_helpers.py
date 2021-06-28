from core.tests.factories import UserFactory
from django.test import TestCase
from curriculum_tracking.management.helpers import user_is_competent_for_card_project
from curriculum_tracking.tests.factories import AgileCardFactory, RecruitProjectFactory
from django.utils import timezone

MATCHING_FLAVOURS = ["js"]


class user_is_competent_for_card_project_Test(TestCase):
    def setUp(self):
        self.card = AgileCardFactory()
        self.card.recruit_project.set_flavours(MATCHING_FLAVOURS)
        self.card.set_flavours(MATCHING_FLAVOURS)

        self.project = RecruitProjectFactory(content_item=self.card.content_item)
        self.user = self.project.recruit_users.first()

    def test_is_competent_with_flavours(self):

        self.project.set_flavours(MATCHING_FLAVOURS)
        self.project.complete_time = timezone.now()
        self.project.save()

        self.assertTrue(
            user_is_competent_for_card_project(card=self.card, user=self.user)
        )

    def test_is_competent_with_no_flavours(self):

        self.project.set_flavours([])
        self.card.recruit_project.set_flavours([])
        self.card.set_flavours([])
        self.project.complete_time = timezone.now()
        self.project.save()
        self.assertTrue(
            user_is_competent_for_card_project(card=self.card, user=self.user)
        )

    def test_is_not_competent_because_not_complete(self):

        self.project.set_flavours(MATCHING_FLAVOURS)
        self.project.complete_time = None
        self.project.save()

        self.assertFalse(
            user_is_competent_for_card_project(card=self.card, user=self.user)
        )

    def test_is_not_competent_because_flavour_mismatch(self):

        self.project.set_flavours([])
        self.project.complete_time = timezone.now()
        self.project.save()

        self.assertFalse(
            user_is_competent_for_card_project(card=self.card, user=self.user)
        )

    def test_that_users_with_no_project_not_competent(self):
        self.assertFalse(
            user_is_competent_for_card_project(card=self.card, user=UserFactory())
        )