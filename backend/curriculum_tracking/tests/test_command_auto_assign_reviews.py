from django.utils import timezone
from curriculum_tracking.models import AgileCard, ContentItem
from curriculum_tracking.management.commands.auto_assign_reviewers import (
    REQUIRED_REVIEWERS_PER_CARD,
    get_cards_needing_reviewers,
    get_possible_reviewers,
)
from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
    RecruitProjectFactory,
)
from django.test import TestCase
from typing import List

JAVASCRIPT = "js"
TYPESCRIPT = "ts"


class get_cards_needing_reviewers_Tests(TestCase):
    def setUp(self):
        AgileCardFactory(
            content_item=ContentItemFactory(content_type=ContentItem.TOPIC),
            recruit_project=None,
        )

        project_cards: List(AgileCard) = [
            AgileCardFactory() for i in range(REQUIRED_REVIEWERS_PER_CARD + 2)
        ]

        for n, card in enumerate(project_cards):
            assert card.assignees.count()
            for i in range(n):
                card.add_collaborator(UserFactory(), add_as_project_reviewer=True)

        self.project_cards_needing_review = [
            o
            for o in project_cards
            if o.reviewers.count() < REQUIRED_REVIEWERS_PER_CARD
        ]
        self.assertGreater(len(self.project_cards_needing_review), 0)

    def test_counts_work(self):

        result = get_cards_needing_reviewers()
        self.assertEqual(
            sorted([o.id for o in result]),
            sorted([o.id for o in self.project_cards_needing_review]),
        )

    def test_skip_inactive_users(self):
        for card in self.project_cards_needing_review:
            user = card.assignees.first()
            user.active = False
            user.save()

        result = get_cards_needing_reviewers()
        self.assertEqual(list(result), [])


class get_possible_reviewers_Tests(TestCase):
    def test_that_only_competent_people_get_returned(self):

        competent_project = RecruitProjectFactory(
            complete_time=timezone.now(), flavours=[JAVASCRIPT]
        )
        content_item = competent_project.content_item
        nyc_project = RecruitProjectFactory(
            complete_time=None, flavours=[JAVASCRIPT], content_item=content_item
        )
        wrong_flavour_project = RecruitProjectFactory(
            complete_time=timezone.now(),
            flavours=[TYPESCRIPT],
            content_item=content_item,
        )

        card = AgileCardFactory(
            recruit_project=RecruitProjectFactory(
                complete_time=None, flavours=[JAVASCRIPT], content_item=content_item
            )
        )
        result = list(get_possible_reviewers(card))
        self.assertEqual(result, [competent_project.recruit_users.first()])

    def test_that_it_works_with_flavourless_projects(self):
        competent_project = RecruitProjectFactory(
            complete_time=timezone.now(), flavours=[]
        )
        content_item = competent_project.content_item
        nyc_project = RecruitProjectFactory(
            complete_time=None, flavours=[], content_item=content_item
        )
        wrong_flavour_project = RecruitProjectFactory(
            complete_time=timezone.now(),
            flavours=[TYPESCRIPT],
            content_item=content_item,
        )

        card = AgileCardFactory(
            recruit_project=RecruitProjectFactory(
                complete_time=None, flavours=[], content_item=content_item
            )
        )
        result = list(get_possible_reviewers(card))
        self.assertEqual(result, [competent_project.recruit_users.first()])

    def test_that_reviewers_returned_in_order(self):
        content_item = ContentItemFactory()
        competent_projects = [
            RecruitProjectFactory(
                complete_time=timezone.now(), flavours=[], content_item=content_item
            )
            for i in range(3)
        ]

        for n, project in enumerate(competent_projects):
            reviews_to_add = 5 - n
            for i in range(reviews_to_add):
                nyc_card = AgileCardFactory(
                    recruit_project=RecruitProjectFactory(
                        complete_time=None, flavours=[], content_item=content_item
                    )
                )
                project_user = project.recruit_users.first()
                nyc_card.reviewers.add(project_user)
                nyc_card.recruit_project.reviewer_users.add(project_user)

        card = AgileCardFactory(
            recruit_project=RecruitProjectFactory(
                complete_time=None, flavours=[], content_item=content_item
            )
        )
        expected_result = [
            project.recruit_users.first() for project in competent_projects[::-1]
        ]
        assert expected_result
        result = list(get_possible_reviewers(card))
        self.assertEqual(
            result,
            expected_result,
        )

        # add some more duties to first person and make sure order is still correct
        project_user = expected_result[0]
        for i in range(5):

            nyc_card = AgileCardFactory(
                recruit_project=RecruitProjectFactory(
                    complete_time=None, flavours=[], content_item=content_item
                )
            )
            nyc_card.reviewers.add(project_user)
            nyc_card.recruit_project.reviewer_users.add(project_user)

        expected_result = expected_result[1:] + [expected_result[0]]
        result = list(get_possible_reviewers(card))
        self.assertEqual(
            result,
            expected_result,
        )

        # test_that_if_a_user_is_already_a_reviewer_they_are_skipped(self)

        card.reviewers.add(expected_result[0])
        card.recruit_project.reviewer_users.add(expected_result[0])
        card.reviewers.add(expected_result[-1])
        card.recruit_project.reviewer_users.add(expected_result[-1])
        result = list(get_possible_reviewers(card))
        self.assertEqual(
            result,
            expected_result[1:-1],
        )
