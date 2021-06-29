from core.tests.factories import TeamFactory, UserFactory
from django.test import TestCase
from curriculum_tracking.models import ReviewTrust, RecruitProjectReview
from curriculum_tracking.tests.factories import (
    ContentItemFactory,
    RecruitProjectFactory,
    RecruitProjectReviewFactory,
)
from backend.settings import (
    CURRICULUM_TRACKING_TRUST_STREAK_LENGTH,
)


class propagate_trust_signal_Tests(TestCase):
    def test(self):
        user = UserFactory()
        content_item = ContentItemFactory(flavours=["js"])

        for i in range(CURRICULUM_TRACKING_TRUST_STREAK_LENGTH - 1):
            project = RecruitProjectFactory(content_item=content_item, flavours=["js"])
            RecruitProjectReviewFactory(
                recruit_project=project,
                reviewer_user=user,
                validated=RecruitProjectReview.CORRECT,
            )
            trust_count = ReviewTrust.objects.all().count()
            self.assertEqual(trust_count, 0)

        # add one more and the user should be trusted
        project = RecruitProjectFactory(content_item=content_item, flavours=["js"])
        RecruitProjectReviewFactory(
            recruit_project=project,
            reviewer_user=user,
            validated=RecruitProjectReview.CORRECT,
        )
        trust_count = ReviewTrust.objects.all().count()
        self.assertEqual(trust_count, 1)

        trust = ReviewTrust.objects.first()
        self.assertEqual(trust.content_item, content_item)
        self.assertEqual(trust.user, user)
        self.assertTrue(trust.flavours_match(["js"]))


class get_validated_streak_Tests(TestCase):
    def setUp(self):
        content_item = ContentItemFactory()

        self.project_js_1 = RecruitProjectFactory(
            flavours=["js"], content_item=content_item
        )

        self.project_js_2 = RecruitProjectFactory(
            flavours=["js"], content_item=content_item
        )

        self.project_js_3 = RecruitProjectFactory(
            flavours=["js"], content_item=content_item
        )

        self.project_js_4 = RecruitProjectFactory(
            flavours=["js"], content_item=content_item
        )

        self.project_ts_1 = RecruitProjectFactory(
            flavours=["ts"], content_item=content_item
        )

        self.project_ts_2 = RecruitProjectFactory(
            flavours=["ts"], content_item=content_item
        )

        self.project_ts_3 = RecruitProjectFactory(
            flavours=["ts"], content_item=content_item
        )

        self.user_1 = UserFactory()
        self.user_2 = UserFactory()

    def test_different_statuses(self):
        review = RecruitProjectReviewFactory(reviewer_user=self.user_1, validated=None)
        self.assertEqual(review.get_validated_streak(), 0)

        review = RecruitProjectReviewFactory(
            reviewer_user=self.user_1, validated=RecruitProjectReview.INCORRECT
        )
        self.assertEqual(review.get_validated_streak(), 0)
        review = RecruitProjectReviewFactory(
            reviewer_user=self.user_1, validated=RecruitProjectReview.CONTRADICTED
        )
        self.assertEqual(review.get_validated_streak(), 0)
        review = RecruitProjectReviewFactory(
            reviewer_user=self.user_1, validated=RecruitProjectReview.CORRECT
        )
        self.assertEqual(review.get_validated_streak(), 1)

    def test_blacklist(self):
        team = TeamFactory(name="tghyj TechQuest dfghj")
        review = RecruitProjectReviewFactory(
            reviewer_user=self.user_1, validated=RecruitProjectReview.CORRECT
        )
        assignee = review.recruit_project.recruit_users.first()
        team.user_set.add(assignee)

        self.assertEqual(review.get_validated_streak(), 0)

    def test_streak_adds_up_per_flavour(self):
        review_js_1 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_1,
            validated=RecruitProjectReview.CORRECT,
        )

        review_ts_1 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_ts_1,
            validated=RecruitProjectReview.CORRECT,
        )

        review_js_2 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_2,
            validated=RecruitProjectReview.CORRECT,
        )

        review_ts_2 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_ts_2,
            validated=RecruitProjectReview.CORRECT,
        )

        review_js_3 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_3,
            validated=RecruitProjectReview.CORRECT,
        )

        review_ts_3 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_ts_3,
            validated=RecruitProjectReview.CORRECT,
        )

        self.assertEqual(review_js_1.get_validated_streak(), 1)
        self.assertEqual(review_js_2.get_validated_streak(), 2)
        self.assertEqual(review_js_3.get_validated_streak(), 3)

        self.assertEqual(review_ts_1.get_validated_streak(), 1)
        self.assertEqual(review_ts_2.get_validated_streak(), 2)
        self.assertEqual(review_ts_3.get_validated_streak(), 3)

    def test_interrupted_streak(self):

        review_js_1 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_1,
            validated=RecruitProjectReview.CORRECT,
        )

        review_js_2 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_2,
            validated=RecruitProjectReview.INCORRECT,
        )

        review_js_3 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_3,
            validated=RecruitProjectReview.CORRECT,
        )

        review_js_4 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_4,
            validated=RecruitProjectReview.CORRECT,
        )

        self.assertEqual(review_js_1.get_validated_streak(), 1)
        self.assertEqual(review_js_2.get_validated_streak(), 0)
        self.assertEqual(review_js_3.get_validated_streak(), 1)
        self.assertEqual(review_js_4.get_validated_streak(), 2)

    def test_only_grabs_last_review_for_project(self):
        """otherwise people can try to cheat the system by adding extra reviews to the same thing"""

        review_js_1 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_1,
            validated=RecruitProjectReview.CORRECT,
        )

        review_js_2 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_1,
            validated=RecruitProjectReview.CORRECT,
        )

        review_js_3 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_2,
            validated=RecruitProjectReview.CORRECT,
        )
        review_js_4 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_1,
            validated=RecruitProjectReview.CORRECT,
        )

        self.assertEqual(review_js_1.get_validated_streak(), 1)
        self.assertEqual(review_js_2.get_validated_streak(), 1)
        self.assertEqual(review_js_3.get_validated_streak(), 2)
        self.assertEqual(review_js_4.get_validated_streak(), 2)

    def test_that_different_users_get_different_streaks(self):
        review_js_1 = RecruitProjectReviewFactory(
            reviewer_user=self.user_1,
            recruit_project=self.project_js_1,
            validated=RecruitProjectReview.CORRECT,
        )

        review_js_2 = RecruitProjectReviewFactory(
            reviewer_user=self.user_2,
            recruit_project=self.project_js_2,
            validated=RecruitProjectReview.CORRECT,
        )

        self.assertEqual(review_js_1.get_validated_streak(), 1)
        self.assertEqual(review_js_2.get_validated_streak(), 1)
