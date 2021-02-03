from django.test import TestCase
from .factories import (
    AgileCardFactory,
    ContentItemFactory,
    RecruitProjectReviewFactory,
    ReviewTrustFactory,
)
from core.tests.factories import UserFactory
from curriculum_tracking.models import AgileCard, ContentItem

from curriculum_tracking.constants import (
    RED_FLAG,
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
)


class ReviewTrust_update_previous_reviews_Tests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def make_card_and_review(self, flavours=None, content_item=None):
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
            reviewer_user=self.user,
        )
        return card, review

    def test_that_recent_competent_reviews_become_trusted_and_cards_move(self):
        card, review = self.make_card_and_review()
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

        card_none, review_none = self.make_card_and_review(
            content_item=content_item, flavours=[]
        )
        card_js, review_js = self.make_card_and_review(
            content_item=content_item, flavours=[JAVASCRIPT]
        )
        card_ts, review_ts = self.make_card_and_review(
            content_item=content_item, flavours=[TYPESCRIPT]
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