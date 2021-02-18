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


class RecruitProjectReviewCreationTests(TestCase):
    def setUp(self):
        self.trusted_user = core_factories.UserFactory()
        self.untrusted_user = core_factories.UserFactory()

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

        for card in self.cards:
            factories.ReviewTrustFactory(
                content_item=card.content_item,
                user=self.trusted_user,
                flavours=card.recruit_project.flavour_names,
            )
            assert card.recruit_project.is_trusted_reviewer(self.trusted_user)

    def test_review_knows_it_it_is_trusted_or_not_using_trust_obj(self):
        trusted = factories.RecruitProjectReviewFactory(
            reviewer_user=self.trusted_user,
            recruit_project=self.ip_card.recruit_project,
        )
        untrusted = factories.RecruitProjectReviewFactory(
            reviewer_user=self.untrusted_user,
            recruit_project=self.ip_card.recruit_project,
        )
        self.assertTrue(trusted.trusted)
        self.assertFalse(untrusted.trusted)

    def test_that_user_given_permission_trusted_reviewer_makes_trusted_review(self):
        user = core_factories.UserFactory()

        recruit_team = core_factories.TeamFactory()
        assign_perm(Team.PERMISSION_TRUSTED_REVIEWER, user, recruit_team)

        untrusted = factories.RecruitProjectReviewFactory(
            reviewer_user=user, recruit_project=self.ip_card.recruit_project
        )
        self.assertFalse(untrusted.trusted)

        # now add the recruit to the team and make another review

        recruit_team.user_set.set(self.ip_card.recruit_project.recruit_users.all())

        trusted = factories.RecruitProjectReviewFactory(
            reviewer_user=user, recruit_project=self.ip_card.recruit_project
        )
        self.assertTrue(trusted.trusted)
        self.assertFalse(untrusted.trusted)

    def test_that_superuser_always_trusted(self):
        superuser = core_factories.UserFactory(is_superuser=True)
        review = factories.RecruitProjectReviewFactory(
            reviewer_user=superuser, recruit_project=self.ip_card.recruit_project
        )
        self.assertTrue(review.trusted)

    def test_adding_trusted_competent_moves_card_to_complete(self):
        for card in self.cards:
            card.refresh_from_db()

            project = card.recruit_project

            review = factories.RecruitProjectReviewFactory(
                recruit_project=project,
                reviewer_user=self.trusted_user,
                status=COMPETENT,
            )
            self.assertIsNotNone(review.timestamp)
            self.assertEqual(review.trusted, True)

            # for card in self.cards:
            card.refresh_from_db()
            project.refresh_from_db()

            project = models.RecruitProject.objects.get(pk=project.id)
            # project = card.recruit_project
            # print("AFTER SIGNAL")

            # print(f"card.id:   {card.id}")
            # print(f"card.status:   {card.status}")
            # print(f"project:   {project}")
            # print(f"project.id: {project.id}")
            # print(f"project.complete_time:{project.complete_time}")

            self.assertEqual(card.status, models.AgileCard.COMPLETE)
            self.assertIsNotNone(project.complete_time)

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

        self.ip_card.recruit_project.start_time = timezone.now() - timedelta(days=15)
        self.review_card.recruit_project.start_time = timezone.now() - timedelta(
            days=15
        )
        self.feedback_card.recruit_project.start_time = timezone.now() - timedelta(
            days=15
        )
        self.complete_card.recruit_project.start_time = timezone.now() - timedelta(
            days=15
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

        # self.blocked_card.recruit_project.request_review()
        # self.ready_card.recruit_project.request_review()

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

        project.start_time = timezone.now() - timedelta(days=15)
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
