from django.test import TestCase
from django.contrib.auth import get_user_model

from curriculum_tracking import models
from curriculum_tracking import constants
from curriculum_tracking import helpers
from curriculum_tracking import card_generation_helpers as gen_helpers
from curriculum_tracking.tests import factories

JAVASCRIPT = "js"
TYPESCRIPT = "ts"


User = get_user_model()


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

    def test_prereq_with_no_available_flavours(self):
        """ requirements have flavours and prereq doesnt """

        content_item = factories.ContentItemFactory()

        requirement1 = factories.CurriculumContentRequirementFactory(
            content_item=factories.ContentItemFactory(available_flavours=[TYPESCRIPT]),
            curriculum=self.curriculum,
            hard_requirement=True,
            flavours=[TYPESCRIPT],
        )
        requirement2 = factories.CurriculumContentRequirementFactory(
            content_item=factories.ContentItemFactory(available_flavours=[JAVASCRIPT]),
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

    def test_prereq_with_available_flavours(self):
        """ requirements have flavours and prereq does too, therefore moar cards """

        content_item = factories.ContentItemFactory(
            available_flavours=[TYPESCRIPT, JAVASCRIPT]
        )

        requirement1 = factories.CurriculumContentRequirementFactory(
            content_item=factories.ContentItemFactory(available_flavours=[TYPESCRIPT]),
            curriculum=self.curriculum,
            hard_requirement=True,
            flavours=[TYPESCRIPT],
        )
        requirement2 = factories.CurriculumContentRequirementFactory(
            content_item=factories.ContentItemFactory(available_flavours=[JAVASCRIPT]),
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
