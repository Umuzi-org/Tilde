from django.test import TestCase
from .factories import (
    AgileCardFactory,
    ContentItemFactory,
    RecruitProjectReviewFactory,
    ReviewTrustFactory,
)
from core.tests.factories import UserFactory
from curriculum_tracking.models import AgileCard, ContentItem, RecruitProjectReview

from curriculum_tracking.constants import (
    RED_FLAG,
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
)


def make_card_and_review(reviewer_user, flavours=None, content_item=None):
    content_item = content_item or ContentItemFactory(
        content_type=ContentItem.PROJECT,
        project_submission_type=ContentItem.LINK,
    )
    flavours = flavours or []
    card = AgileCardFactory(
        content_item=content_item,
        status=AgileCard.READY,
        recruit_project=None,
        flavours=flavours,
    )
    card.assignees.set([UserFactory()])
    card.start_project()
    card.recruit_project.request_review()
    review = RecruitProjectReviewFactory(
        status=COMPETENT,
        recruit_project=card.recruit_project,
        reviewer_user=reviewer_user,
    )
    return card, review


class ReviewTrust_update_previous_reviews_Tests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_that_recent_competent_reviews_become_trusted_and_cards_move(self):
        card, review = make_card_and_review(reviewer_user=self.user)
        self.assertEqual(card.status, AgileCard.IN_REVIEW)

        self.assertFalse(review.trusted)

        trust = ReviewTrustFactory(user=self.user, content_item=card.content_item)
        trust.update_previous_reviews()

        review.refresh_from_db()
        card.refresh_from_db()

        self.assertTrue(review.trusted)
        self.assertEqual(card.status, AgileCard.COMPLETE)

    def test_works_on_cards_of_correct_flavour(self):
        TYPESCRIPT = "ts"
        JAVASCRIPT = "js"

        content_item = ContentItemFactory(
            content_type=ContentItem.PROJECT,
            project_submission_type=ContentItem.LINK,
            flavours=[TYPESCRIPT, JAVASCRIPT],
        )

        card_none, review_none = make_card_and_review(
            reviewer_user=self.user, content_item=content_item, flavours=[]
        )
        card_js, review_js = make_card_and_review(
            reviewer_user=self.user, content_item=content_item, flavours=[JAVASCRIPT]
        )
        card_ts, review_ts = make_card_and_review(
            reviewer_user=self.user, content_item=content_item, flavours=[TYPESCRIPT]
        )

        trust = ReviewTrustFactory(user=self.user, content_item=content_item)
        trust.update_previous_reviews()

        card_none.refresh_from_db()
        review_none.refresh_from_db()
        card_js.refresh_from_db()
        review_js.refresh_from_db()
        card_ts.refresh_from_db()
        review_ts.refresh_from_db()

        self.assertEqual(card_none.status, AgileCard.COMPLETE)
        self.assertTrue(review_none.trusted)

        self.assertEqual(card_js.status, AgileCard.IN_REVIEW)
        self.assertFalse(review_js.trusted)

        self.assertEqual(card_ts.status, AgileCard.IN_REVIEW)
        self.assertFalse(review_ts.trusted)

        trust = ReviewTrustFactory(
            user=self.user, content_item=content_item, flavours=[JAVASCRIPT]
        )
        trust.update_previous_reviews()

        card_none.refresh_from_db()
        review_none.refresh_from_db()
        card_js.refresh_from_db()
        review_js.refresh_from_db()
        card_ts.refresh_from_db()
        review_ts.refresh_from_db()

        self.assertEqual(card_none.status, AgileCard.COMPLETE)
        self.assertTrue(review_none.trusted)

        self.assertEqual(card_js.status, AgileCard.COMPLETE)
        self.assertTrue(review_js.trusted)

        self.assertEqual(card_ts.status, AgileCard.IN_REVIEW)
        self.assertFalse(review_ts.trusted)

    def test_that_previous_review_validated_gets_updated(self):
        card, review = make_card_and_review(reviewer_user=UserFactory())

        user = UserFactory()
        review.refresh_from_db()
        self.assertEqual(review.validated, None)

        # add another review
        new_review = RecruitProjectReviewFactory(
            reviewer_user=user, recruit_project=card.recruit_project, status=COMPETENT
        )

        # then make it trusted
        trust = ReviewTrustFactory(
            user=user, content_item=card.content_item, flavours=[]
        )

        review.refresh_from_db()
        self.assertEqual(review.validated, None)

        trust.update_previous_reviews()

        review.refresh_from_db()
        self.assertEqual(review.validated, RecruitProjectReview.CORRECT)


class CreatingAReviewUpdatesValidationFieldOnPreviousReviews(TestCase):
    def setUp(self):
        self.card, self.review = make_card_and_review(reviewer_user=UserFactory())
        self.trusted_user = UserFactory(is_superuser=True)
        self.untrusted_user = UserFactory(is_superuser=False)

    def test_adding_trusted_competent_review_to_untrusted_competent_marks_review_correct(
        self,
    ):
        RecruitProjectReviewFactory(
            recruit_project=self.card.recruit_project,
            reviewer_user=self.trusted_user,
            status=COMPETENT,
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.validated, RecruitProjectReview.CORRECT)

    def test_adding_trusted_excellent_review_to_untrusted_competent_marks_review_correct(
        self,
    ):
        RecruitProjectReviewFactory(
            recruit_project=self.card.recruit_project,
            reviewer_user=self.trusted_user,
            status=EXCELLENT,
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.validated, RecruitProjectReview.CORRECT)

    def test_adding_trusted_nyc_review_to_untrusted_competent_marks_review_incorrect(
        self,
    ):
        RecruitProjectReviewFactory(
            recruit_project=self.card.recruit_project,
            reviewer_user=self.trusted_user,
            status=NOT_YET_COMPETENT,
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.validated, RecruitProjectReview.INCORRECT)

    def test_adding_trusted_red_flag_review_to_untrusted_competent_marks_review_incorrect(
        self,
    ):
        RecruitProjectReviewFactory(
            recruit_project=self.card.recruit_project,
            reviewer_user=self.trusted_user,
            status=RED_FLAG,
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.validated, RecruitProjectReview.INCORRECT)

    def test_adding_untrusted_competent_review_to_untrusted_competent_makes_no_change(
        self,
    ):
        RecruitProjectReviewFactory(
            recruit_project=self.card.recruit_project,
            reviewer_user=self.untrusted_user,
            status=COMPETENT,
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.validated, None)

    def test_adding_untrusted_excellent_review_to_untrusted_competent_makes_no_change(
        self,
    ):
        RecruitProjectReviewFactory(
            recruit_project=self.card.recruit_project,
            reviewer_user=self.untrusted_user,
            status=EXCELLENT,
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.validated, None)

    def test_adding_untrusted_nyc_review_to_untrusted_competent_marks_review_contradicted(
        self,
    ):
        RecruitProjectReviewFactory(
            recruit_project=self.card.recruit_project,
            reviewer_user=self.untrusted_user,
            status=NOT_YET_COMPETENT,
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.validated, RecruitProjectReview.CONTRADICTED)

    def test_adding_untrusted_nyc_review_to_untrusted_competent_marks_review_contradicted(
        self,
    ):
        RecruitProjectReviewFactory(
            recruit_project=self.card.recruit_project,
            reviewer_user=self.untrusted_user,
            status=RED_FLAG,
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.validated, RecruitProjectReview.CONTRADICTED)