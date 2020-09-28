from django.test import TestCase
from curriculum_tracking import models
from curriculum_tracking.tests import factories
from core.tests import factories as core_factories
from curriculum_tracking.constants import (
    RED_FLAG,
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
)


class RecruitProjectReviewCreationTests(TestCase):
    def setUp(self):
        self.trusted_user = core_factories.UserFactory(
            is_staff=True
        )  # TODO: trust different people for diferent reasons
        self.untrusted_user = core_factories.UserFactory(
            is_staff=False
        )  # TODO: trust different people for diferent reasons

        self.ready_card = factories.AgileCardFactory(status=models.AgileCard.READY)
        self.ip_card = factories.AgileCardFactory(status=models.AgileCard.IN_PROGRESS)
        self.feedback_card = factories.AgileCardFactory(
            status=models.AgileCard.REVIEW_FEEDBACK
        )
        self.cards = [
            self.ready_card,
            self.ip_card,
            self.feedback_card,
        ]

    def test_review_knows_it_it_is_trusted_or_not(self):
        trusted = factories.RecruitProjectReviewFactory(
            reviewer_user=self.trusted_user,
        )
        untrusted = factories.RecruitProjectReviewFactory(
            reviewer_user=self.untrusted_user,
        )
        self.assertTrue(trusted.trusted)
        self.assertFalse(untrusted.trusted)

    def test_adding_trusted_competent_moves_card_to_complete(self):

        for card in self.cards:
            project = card.recruit_project
            factories.RecruitProjectReviewFactory(
                recruit_project=project,
                reviewer_user=self.trusted_user,
                status=COMPETENT,
            )

        for card in self.cards:
            card.refresh_from_db()
            self.assertEqual(card.status, models.AgileCard.COMPLETE)

    def test_adding_untrusted_competent_does_not_move_card(self):
        for card in self.cards:
            project = card.recruit_project
            factories.RecruitProjectReviewFactory(
                recruit_project=project,
                reviewer_user=self.untrusted_user,
                status=COMPETENT,
            )

        for card in self.cards:
            card.refresh_from_db()

        # nothing moved
        self.assertEqual(self.ready_card.status, models.AgileCard.READY)
        self.assertEqual(self.ip_card.status, models.AgileCard.IN_PROGRESS)
        self.assertEqual(self.feedback_card.status, models.AgileCard.REVIEW_FEEDBACK)

    def test_adding_nyc_untrusted_moves_card_to_review_feedback(self):
        for card in self.cards:
            project = card.recruit_project
            factories.RecruitProjectReviewFactory(
                recruit_project=project,
                reviewer_user=self.untrusted_user,
                status=NOT_YET_COMPETENT,
            )

        for card in self.cards:
            card.refresh_from_db()
            self.assertEqual(card.status, models.AgileCard.REVIEW_FEEDBACK)


class RecruitProjectTests(TestCase):
    def setUp(self):
        self.blocked_card = factories.AgileCardFactory(status=models.AgileCard.BLOCKED)
        self.ready_card = factories.AgileCardFactory(status=models.AgileCard.READY)
        self.ip_card = factories.AgileCardFactory(status=models.AgileCard.IN_PROGRESS)
        self.review_card = factories.AgileCardFactory(status=models.AgileCard.IN_REVIEW)
        self.feedback_card = factories.AgileCardFactory(
            status=models.AgileCard.REVIEW_FEEDBACK
        )
        self.complete_card = factories.AgileCardFactory(
            status=models.AgileCard.COMPLETE
        )

        self.cards = [
            self.blocked_card,
            self.ready_card,
            self.ip_card,
            self.review_card,
            self.feedback_card,
            self.complete_card,
        ]

    def test_that_requesting_a_review_moves_the_card_to_in_review_when_it_should(self):
        self.blocked_card.recruit_project.request_review()
        self.ready_card.recruit_project.request_review()
        self.ip_card.recruit_project.request_review()
        self.review_card.recruit_project.request_review()
        self.feedback_card.recruit_project.request_review()
        # self.complete_card.recruit_project.request_review()

        for card in self.cards:
            card.refresh_from_db()
            card.recruit_project.refresh_from_db()

        self.assertEqual(self.blocked_card.status, models.AgileCard.BLOCKED)
        self.assertEqual(self.ready_card.status, models.AgileCard.READY)
        self.assertEqual(self.ip_card.status, models.AgileCard.IN_REVIEW)
        self.assertEqual(self.review_card.status, models.AgileCard.IN_REVIEW)
        self.assertEqual(self.feedback_card.status, models.AgileCard.IN_REVIEW)
        # self.assertEqual(self.complete_card.status, models.AgileCard.COMPLETE)

    def test_review_failed_then_rerequested_flow(self):
        card = self.ip_card
        untrusted_user = core_factories.UserFactory(
            is_staff=False
        )  # TODO: trust different people for diferent reasons
        trusted_user = core_factories.UserFactory(
            is_staff=True
        )  # TODO: trust different people for diferent reasons

        project = card.recruit_project


        project.request_review()

        card.refresh_from_db()
        project.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.IN_REVIEW)

        # add NCY review
        factories.RecruitProjectReviewFactory(
            recruit_project=project,
            reviewer_user=untrusted_user,
            status=NOT_YET_COMPETENT,
        )

        card.refresh_from_db()
        project.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.REVIEW_FEEDBACK)

        # the recruit asks for another review...
        project.request_review()

        card.refresh_from_db()
        project.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.IN_REVIEW)

        # a staff member add a review
        factories.RecruitProjectReviewFactory(
            recruit_project=project,
            reviewer_user=trusted_user,
            status=NOT_YET_COMPETENT,
        )

        card.refresh_from_db()
        project.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.REVIEW_FEEDBACK)

        # the recruit asks for another review...
        project.request_review()

        card.refresh_from_db()
        project.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.IN_REVIEW)
