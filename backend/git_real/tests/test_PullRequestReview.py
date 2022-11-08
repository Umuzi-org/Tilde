from django.test import TestCase
from . import factories
from git_real.models import PullRequestReview


class update_recent_validation_flags_Tests(TestCase):
    def test_positive_and_neutral_do_nothing(self):
        positive_1 = factories.PullRequestReviewFactory(
            state=PullRequestReview.POSITIVE_STATES[0]
        )
        pr = positive_1.pull_request
        neutral_1 = factories.PullRequestReviewFactory(
            state=PullRequestReview.NEUTRAL_STATES[0], pull_request=pr
        )
        neutral_1.update_recent_validation_flags()

        positive_2 = factories.PullRequestReviewFactory(
            state=PullRequestReview.POSITIVE_STATES[0]
        )
        positive_2.update_recent_validation_flags()

        positive_1.refresh_from_db()
        self.assertIsNone(positive_1.validated)
        neutral_1.refresh_from_db()
        self.assertIsNone(neutral_1.validated)
        positive_2.refresh_from_db()
        self.assertIsNone(positive_2.validated)

    def test_negatives_update_previous(self):

        for negative_state in PullRequestReview.NEGATIVE_STATES:
            positive_1 = factories.PullRequestReviewFactory(
                state=PullRequestReview.POSITIVE_STATES[0]
            )
            pr = positive_1.pull_request
            neutral_1 = factories.PullRequestReviewFactory(
                state=PullRequestReview.NEUTRAL_STATES[0], pull_request=pr
            )

            negative_1 = factories.PullRequestReviewFactory(
                state=negative_state, pull_request=pr
            )
            negative_1.update_recent_validation_flags()

            positive_1.refresh_from_db()
            self.assertEqual(positive_1.validated, PullRequestReview.CONTRADICTED)
            neutral_1.refresh_from_db()
            self.assertIsNone(neutral_1.validated)
            negative_1.refresh_from_db()
            self.assertIsNone(negative_1.validated)

    def test_negative_State_doesnt_touch_other_prs(self):
        positive_1 = factories.PullRequestReviewFactory(
            state=PullRequestReview.POSITIVE_STATES[0]
        )
        negative_1 = factories.PullRequestReviewFactory(
            state=PullRequestReview.NEGATIVE_STATES[0]
        )
        negative_1.update_recent_validation_flags()

        positive_1.refresh_from_db()
        self.assertIsNone(positive_1.validated)
        negative_1.refresh_from_db()
        self.assertIsNone(negative_1.validated)
