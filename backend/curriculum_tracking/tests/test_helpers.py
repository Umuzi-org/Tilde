from django.test import TestCase
from curriculum_tracking import card_generation_helpers as gen_helpers
from curriculum_tracking.tests import factories
from curriculum_tracking import helpers
from curriculum_tracking import models
from django.utils import timezone
from curriculum_tracking.constants import COMPETENT
from backend.settings import REVIEW_SPAM_THRESHOLD

JAVASCRIPT = "js"
TYPESCRIPT = "ts"


from core.models import User


# class get_full_url_from_content_link_param_Tests(TestCase):
#     def test_various(self):
#         for url_part in [
#             "content/workshops/intro-to-ncit/_index.md",
#             "content/workshops/intro-to-ncit/",
#             "/workshops/intro-to-ncit/",
#             "https://umuzi-org.github.io/tech-department/workshops/intro-to-ncit/",
#         ]:

#             result = helpers.get_full_url_from_content_link_param(url_part)

#             self.assertEqual(
#                 result,
#                 constants.RAW_CONTENT_URL.format(
#                     content_sub_dir="content/workshops/intro-to-ncit/_index.md"
#                 ),
#                 url_part,
#             )


class get_ordered_content_items_Tests(TestCase):
    def setUp(self):
        self.curriculum = factories.CurriculumFactory()

    def test_no_cards(self):
        l = gen_helpers.get_ordered_content_items(self.curriculum)
        self.assertEqual(l, [])

    def test_no_prepreq(self):
        requirement1 = factories.CurriculumContentRequirementFactory(
            curriculum=self.curriculum, hard_requirement=True
        )
        requirement2 = factories.CurriculumContentRequirementFactory(
            curriculum=self.curriculum, hard_requirement=False
        )

        l = gen_helpers.get_ordered_content_items(self.curriculum)

        self.assertEqual(l[0].content_item, requirement1.content_item)
        self.assertEqual(l[0].is_hard_milestone, True)
        self.assertEqual(l[0].is_soft_milestone, False)
        self.assertEqual(l[0].flavours, [])

        self.assertEqual(l[1].content_item, requirement2.content_item)
        self.assertEqual(l[1].is_hard_milestone, False)
        self.assertEqual(l[1].is_soft_milestone, True)
        self.assertEqual(l[1].flavours, [])

    def test_prereq_with_no_flavours(self):
        """requirements have flavours and prereq doesnt"""

        content_item = factories.ContentItemFactory()

        requirement1 = factories.CurriculumContentRequirementFactory(
            content_item=factories.ContentItemFactory(flavours=[TYPESCRIPT]),
            curriculum=self.curriculum,
            hard_requirement=True,
            flavours=[TYPESCRIPT],
        )
        requirement2 = factories.CurriculumContentRequirementFactory(
            content_item=factories.ContentItemFactory(flavours=[JAVASCRIPT]),
            curriculum=self.curriculum,
            hard_requirement=False,
            flavours=[JAVASCRIPT],
        )

        factories.ContentItemOrderFactory(
            post=requirement1.content_item, pre=content_item
        )
        factories.ContentItemOrderFactory(
            post=requirement2.content_item, pre=content_item
        )

        # breakpoint()

        l = gen_helpers.get_ordered_content_items(self.curriculum)

        # since content_item has no available flavours, it will only be associated with one card
        self.assertEqual(len(l), 3)

        self.assertEqual(l[0].content_item, content_item)
        self.assertEqual(l[0].is_hard_milestone, False)
        self.assertEqual(l[0].is_soft_milestone, False)
        self.assertEqual(l[0].flavours, [])

        self.assertEqual(l[1].content_item, requirement1.content_item)
        self.assertEqual(l[1].is_hard_milestone, True)
        self.assertEqual(l[1].is_soft_milestone, False)
        self.assertEqual([o.name for o in l[1].flavours], [TYPESCRIPT])

        self.assertEqual(l[2].content_item, requirement2.content_item)
        self.assertEqual(l[2].is_hard_milestone, False)
        self.assertEqual(l[2].is_soft_milestone, True)
        self.assertEqual([o.name for o in l[2].flavours], [JAVASCRIPT])

    def test_prereq_with_flavours(self):
        """requirements have flavours and prereq does too, therefore moar cards"""

        content_item = factories.ContentItemFactory(flavours=[TYPESCRIPT, JAVASCRIPT])

        requirement1 = factories.CurriculumContentRequirementFactory(
            content_item=factories.ContentItemFactory(flavours=[TYPESCRIPT]),
            curriculum=self.curriculum,
            hard_requirement=True,
            flavours=[TYPESCRIPT],
        )
        requirement2 = factories.CurriculumContentRequirementFactory(
            content_item=factories.ContentItemFactory(flavours=[JAVASCRIPT]),
            curriculum=self.curriculum,
            hard_requirement=False,
            flavours=[JAVASCRIPT],
        )

        factories.ContentItemOrderFactory(
            post=requirement1.content_item, pre=content_item
        )
        factories.ContentItemOrderFactory(
            post=requirement2.content_item, pre=content_item
        )

        l = gen_helpers.get_ordered_content_items(self.curriculum)

        # since content_item has available flavours, it will be associated with TWO cards

        self.assertEqual(len(l), 4)

        self.assertEqual(l[0].content_item, content_item)
        self.assertEqual(l[0].is_hard_milestone, False)
        self.assertEqual(l[0].is_soft_milestone, False)
        self.assertEqual([o.name for o in l[0].flavours], [TYPESCRIPT])

        self.assertEqual(l[1].content_item, requirement1.content_item)
        self.assertEqual(l[1].is_hard_milestone, True)
        self.assertEqual(l[1].is_soft_milestone, False)
        self.assertEqual([o.name for o in l[1].flavours], [TYPESCRIPT])

        self.assertEqual(l[2].content_item, content_item)
        self.assertEqual(l[2].is_hard_milestone, False)
        self.assertEqual(l[2].is_soft_milestone, False)
        self.assertEqual([o.name for o in l[2].flavours], [JAVASCRIPT])

        self.assertEqual(l[3].content_item, requirement2.content_item)
        self.assertEqual(l[3].is_hard_milestone, False)
        self.assertEqual(l[3].is_soft_milestone, True)
        self.assertEqual([o.name for o in l[3].flavours], [JAVASCRIPT])


class agile_card_reviews_outstanding_Tests(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()

        self.review_cards = [
            factories.AgileCardFactory(
                reviewers=[self.user],
                status=models.AgileCard.IN_REVIEW,
                recruit_project=factories.RecruitProjectFactory(
                    review_request_time=timezone.now() - timezone.timedelta(days=1),
                ),
            )
            for _ in range(3)
        ]

        in_progress_cards = [
            factories.AgileCardFactory(
                reviewers=[self.user], status=models.AgileCard.IN_PROGRESS
            )
            for _ in range(2)
        ]

        other_cards = [
            factories.AgileCardFactory(status=models.AgileCard.IN_PROGRESS)
            for _ in range(2)
        ]

    def test_empty_review_column(self):
        user = factories.UserFactory()
        self.assertEqual(helpers.agile_card_reviews_outstanding(user), [])

    def test_cards_in_review_column(self):
        queue = helpers.agile_card_reviews_outstanding(self.user)
        self.assertEqual(queue, self.review_cards)

    def test_excluded_if_already_reviewed_by_user(self):
        factories.RecruitProjectReviewFactory(
            recruit_project=self.review_cards[0].recruit_project,
            reviewer_user=self.user,
            status=COMPETENT,
        )
        factories.RecruitProjectReviewFactory(
            recruit_project=self.review_cards[1].recruit_project, status=COMPETENT
        )
        queue = helpers.agile_card_reviews_outstanding(self.user)
        self.assertEqual(queue, self.review_cards[1:])

    def test_excluded_if_has_enough_reviews(self):

        # add some recent reviews to the first card
        for _ in range(REVIEW_SPAM_THRESHOLD):
            factories.RecruitProjectReviewFactory(
                recruit_project=self.review_cards[0].recruit_project, status=COMPETENT
            )

        # add some old reviews to another card
        for _ in range(REVIEW_SPAM_THRESHOLD):
            o = factories.RecruitProjectReviewFactory(
                recruit_project=self.review_cards[1].recruit_project,
                status=COMPETENT,
            )
            o.timestamp = timezone.now() - timezone.timedelta(days=365)
            o.save()

        queue = helpers.agile_card_reviews_outstanding(self.user)
        self.assertEqual(queue, self.review_cards[1:])
