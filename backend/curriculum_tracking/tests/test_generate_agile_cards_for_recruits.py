from django.test import TestCase
from curriculum_tracking import models
from curriculum_tracking.tests import factories

from curriculum_tracking.card_generation_helpers import (
    _recurse_generate_ordered_content_items,
    create_or_update_content_cards_for_user,
    _get_or_create_or_update_card,
)
from core.tests import factories as core_factories
from taggit.models import Tag


JAVASCRIPT = "JAVASCRIPT"
PYTHON = "PYTHON"


class get_or_create_or_update_card_Test(TestCase):
    defaults = {"is_hard_milestone": True, "is_soft_milestone": False}

    def setUp(self):
        self.javascript = Tag.objects.get_or_create(name=JAVASCRIPT)[0]
        self.python = Tag.objects.get_or_create(name=PYTHON)[0]

        self.content_item = factories.ContentItemFactory()
        models.ContentAvailableFlavour.objects.create(
            content_item=self.content_item, tag=self.javascript
        )
        models.ContentAvailableFlavour.objects.create(
            content_item=self.content_item, tag=self.python
        )
        self.user = core_factories.UserFactory()

    def test_that_cant_make_two_cards_that_are_the_same__no_flavours(self):
        _get_or_create_or_update_card(
            user=self.user,
            content_item=self.content_item,
            defaults=self.defaults,
            overrides={},
            flavours=[],
        )
        _get_or_create_or_update_card(
            user=self.user,
            content_item=self.content_item,
            defaults=self.defaults,
            overrides={},
            flavours=[],
        )
        self.assertEqual(models.AgileCard.objects.count(), 1)

    def test_that_cant_make_two_cards_that_are_the_same__with_one_flavour(self):
        _get_or_create_or_update_card(
            user=self.user,
            content_item=self.content_item,
            defaults=self.defaults,
            overrides={},
            flavours=[self.python],
        )
        _get_or_create_or_update_card(
            user=self.user,
            content_item=self.content_item,
            defaults=self.defaults,
            overrides={},
            flavours=[self.python],
        )
        self.assertEqual(models.AgileCard.objects.count(), 1)

    def test_that_cant_make_two_cards_that_are_the_same__with_two_flavours(self):
        _get_or_create_or_update_card(
            user=self.user,
            content_item=self.content_item,
            defaults=self.defaults,
            overrides={},
            flavours=[self.python, self.javascript],
        )
        _get_or_create_or_update_card(
            user=self.user,
            content_item=self.content_item,
            defaults=self.defaults,
            overrides={},
            flavours=[self.python, self.javascript],
        )
        self.assertEqual(models.AgileCard.objects.count(), 1)

    def test_that_it_makes_multiple_cards_when_flavours_dont_match(self):
        _get_or_create_or_update_card(
            user=self.user,
            content_item=self.content_item,
            defaults=self.defaults,
            overrides={},
            flavours=[self.python],
        )
        _get_or_create_or_update_card(
            user=self.user,
            content_item=self.content_item,
            defaults=self.defaults,
            overrides={},
            flavours=[self.javascript],
        )
        self.assertEqual(models.AgileCard.objects.count(), 2)

        _get_or_create_or_update_card(
            user=self.user,
            content_item=self.content_item,
            defaults=self.defaults,
            overrides={},
            flavours=[self.javascript, self.python],
        )
        self.assertEqual(models.AgileCard.objects.count(), 3)


class recurse_generate_ordered_content_items_Tests(TestCase):
    def setUp(self):

        curriculum_content = factories.CurriculumContentRequirementFactory()
        self.curriculum = curriculum_content.curriculum
        self.content_item = curriculum_content.content_item
        # self.trusted_user = core_factories.UserFactory(is_staff=True)

    def test_get_single_hard_milestone(self):
        content_requirements = models.CurriculumContentRequirement.objects.filter(
            curriculum=self.curriculum
        ).order_by("order")

        items = list(_recurse_generate_ordered_content_items(content_requirements))
        # (content_item, is_hard_milestone, is_soft_milestone)
        assert items == [(self.content_item, True, False, [])], items

    def test_hard_milestone_and_prereq_two_level_and_branch(self):
        order1 = factories.ContentItemOrderFactory(
            post=self.content_item, hard_requirement=True
        )

        order2 = factories.ContentItemOrderFactory(
            post=self.content_item, hard_requirement=True
        )

        content_requirements = models.CurriculumContentRequirement.objects.filter(
            curriculum=self.curriculum
        ).order_by("order")

        items = list(_recurse_generate_ordered_content_items(content_requirements))
        # (content_item, is_hard_milestone, is_soft_milestone)
        assert items == [
            (order1.pre, False, False, []),
            (order2.pre, False, False, []),
            (self.content_item, True, False, []),
        ], items

        order3 = factories.ContentItemOrderFactory(
            post=order2.pre, hard_requirement=True
        )

        order4 = factories.ContentItemOrderFactory(
            post=order2.pre, hard_requirement=True
        )
        items = list(_recurse_generate_ordered_content_items(content_requirements))

        self.assertEqual(
            items,
            [
                (order1.pre, False, False, []),
                (order3.pre, False, False, []),
                (order4.pre, False, False, []),
                (order2.pre, False, False, []),
                (self.content_item, True, False, []),
            ],
        )

        # add a repeated requirement (not circular). The order should change

        order5 = factories.ContentItemOrderFactory(
            post=order1.pre, pre=order4.pre, hard_requirement=True
        )

        items = list(_recurse_generate_ordered_content_items(content_requirements))

        self.assertEqual(
            items,
            [
                (order4.pre, False, False, []),
                (order1.pre, False, False, []),
                (order3.pre, False, False, []),
                (order2.pre, False, False, []),
                (self.content_item, True, False, []),
            ],
        )


class create_or_update_content_cards_for_user_Tests(TestCase):
    def setUp(self):
        # self.team_membership = core_factories.TeamMembershipFactory()
        # self.recruit = self.team_membership.user
        # self.recruit = core_factories.UserFactory()
        # self.curriculum = self.team_membership.cohort.cohort_curriculum
        self.content_item = factories.ContentItemFactory()
        self.card = factories.AgileCardFactory(
            status=models.AgileCard.READY,
            # assignees=[self.recruit],
            content_item=self.content_item,
        )
        # self.card.assignees.add(self.recruit)
        self.recruit = self.card.assignees.first()

    def test_can_block_cards_that_were_ready(self):

        # adding a soft requirement. The user doesn't HAVE to do this one
        item_order = factories.ContentItemOrderFactory(
            post=self.content_item, hard_requirement=True
        )
        ordered_content_items = [
            # (content_item, is_hard_milestone, is_soft_milestone)
            (item_order.pre, False, False, []),
            (self.content_item, True, False, []),
        ]
        create_or_update_content_cards_for_user(self.recruit, ordered_content_items)
        cards = models.AgileCard.objects.all()
        cards = list(cards)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[1], self.card)
        self.assertEqual(cards[0].status, models.AgileCard.READY)
        self.assertEqual(cards[1].status, models.AgileCard.BLOCKED)
        self.assertEqual(list(cards[0].assignees.all()), list(cards[1].assignees.all()))

    def test_can_add_soft_prereq_to_cards_that_were_ready(self):

        # adding a soft requirement. The user doesn't HAVE to do this one
        item_order = factories.ContentItemOrderFactory(
            post=self.content_item, hard_requirement=False
        )
        ordered_content_items = [
            # (content_item, is_hard_milestone, is_soft_milestone)
            (item_order.pre, False, False, []),
            (self.content_item, True, False, []),
        ]
        create_or_update_content_cards_for_user(self.recruit, ordered_content_items)

        cards = models.AgileCard.objects.order_by("-id")
        cards = list(cards)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[1], self.card)
        self.assertEqual(cards[0].status, models.AgileCard.READY)
        self.assertEqual(cards[1].status, models.AgileCard.READY)
        self.assertEqual(list(cards[0].assignees.all()), list(cards[1].assignees.all()))
