from unittest import mock
from django.utils import timezone
from guardian.shortcuts import assign_perm
from curriculum_tracking.models import AgileCard, ContentItem
from curriculum_tracking.management.auto_assign_reviewers import (
    get_cards_needing_competent_reviewers,
    get_possible_competent_reviewers,
    get_reviewer_users_by_permission,
    CONFIGURATION_NAMESPACE,
)
from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import TeamFactory
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
    RecruitProjectFactory,
)
from django.test import TestCase
from typing import List

from config.models import NameSpace, Value
from core.models import PERMISSION_REVIEW_CARDS, PERMISSION_TRUSTED_REVIEWER

JAVASCRIPT = "js"
TYPESCRIPT = "ts"


def setup_config():
    ns = NameSpace.objects.create(
        name="management_actions/auto_assign_reviewers",
    )
    # step 1: competnet reviewers
    Value.objects.create(
        namespace=ns,
        name="REQUIRED_COMPETENT_REVIEWERS_PER_CARD",
        value=3,
        datatype=Value.INTEGER,
        repeated=False,
    )
    Value.objects.create(
        namespace=ns,
        name="SKIP_CARD_TAGS_ALL_STEPS",
        value="ncit",
        datatype=Value.STRING,
        repeated=True,
    )
    Value.objects.create(
        namespace=ns,
        name="EXCLUDE_TEAMS_FROM_COMPETENT_REVIEW_STEP",
        value="Demo team\nTech Junior Staff\nTech seniors",
        datatype=Value.STRING,
        repeated=True,
    )

    # step 2: review permission
    # EXCLUDE_REVIEWER_PERMISSIONED_USERS_IN_TEAMS
    # REQUIRED_REVIEWER_PERMISSIONED_REVIEWERS_PER_CARD

    # # step 3: trusted reviewer permission
    # TRUSTED_REVIEWER_ADD_POSITIVE_REVIEW_THRESHOLD
    # TRUSTED_REVIEW_WAIT_TIME
    # REQUIRED_TRUSTED_PERMISSIONED_REVIEWERS_PER_CARD


@mock.patch("git_real.helpers.github_user_exists", return_value=True)
class get_reviewer_users_by_permission_Tests(TestCase):
    def test_only_returns_explicitly_permissioned_users(self, _):
        team_managed = TeamFactory()

        PERMISSION_ONE = PERMISSION_REVIEW_CARDS
        team_with_permission_one = TeamFactory()
        user_one_1 = UserFactory()
        team_with_permission_one.user_set.add(user_one_1)
        user_one_2 = UserFactory()
        assign_perm(PERMISSION_ONE, team_with_permission_one, team_managed)
        assign_perm(PERMISSION_ONE, user_one_2, team_managed)

        PERMISSION_TWO = PERMISSION_TRUSTED_REVIEWER
        team_with_permission_two = TeamFactory()
        user_two_1 = UserFactory()
        team_with_permission_two.user_set.add(user_two_1)
        user_two_2 = UserFactory()
        assign_perm(PERMISSION_TWO, team_with_permission_two, team_managed)
        assign_perm(PERMISSION_TWO, user_two_2, team_managed)

        user_super = UserFactory(is_superuser=True, is_staff=True)
        UserFactory()

        result_one = get_reviewer_users_by_permission(team_managed, PERMISSION_ONE)
        result_two = get_reviewer_users_by_permission(team_managed, PERMISSION_TWO)

        self.assertEqual(
            sorted(result_one, key=lambda o: o.id),
            sorted([user_one_1, user_one_2], key=lambda o: o.id),
        )
        self.assertEqual(
            sorted(result_two, key=lambda o: o.id),
            sorted([user_two_1, user_two_2], key=lambda o: o.id),
        )

        assign_perm(PERMISSION_TWO, user_super, team_managed)
        result_two = get_reviewer_users_by_permission(team_managed, PERMISSION_TWO)
        self.assertIn(user_super, result_two)


@mock.patch("git_real.helpers.github_user_exists", return_value=True)
class get_cards_needing_competent_reviewers_Tests(TestCase):
    def setUp(self):

        setup_config()
        config = NameSpace.get_config(CONFIGURATION_NAMESPACE)

        AgileCardFactory(
            content_item=ContentItemFactory(content_type=ContentItem.TOPIC),
            recruit_project=None,
        )

        project_cards: List(AgileCard) = [
            AgileCardFactory()
            for i in range(config.REQUIRED_COMPETENT_REVIEWERS_PER_CARD + 2)
        ]

        for n, card in enumerate(project_cards):
            assert card.assignees.count()
            for i in range(n):
                card.add_collaborator(UserFactory(), add_as_project_reviewer=True)

        self.project_cards_needing_review = [
            o
            for o in project_cards
            if o.reviewers.count() < config.REQUIRED_COMPETENT_REVIEWERS_PER_CARD
        ]
        self.assertGreater(len(self.project_cards_needing_review), 0)

    def test_counts_work(self, _):
        result = get_cards_needing_competent_reviewers()
        self.assertEqual(
            sorted([o.id for o in result]),
            sorted([o.id for o in self.project_cards_needing_review]),
        )

    def test_skip_inactive_users(self, _):
        for card in self.project_cards_needing_review:
            user = card.assignees.first()
            user.active = False
            user.save()

        result = get_cards_needing_competent_reviewers()
        self.assertEqual(list(result), [])

    def test_exclude_teams(self, _):

        config = NameSpace.get_config(CONFIGURATION_NAMESPACE)

        team = TeamFactory(name=config.EXCLUDE_TEAMS_FROM_COMPETENT_REVIEW_STEP[0])
        team.user_set.add(self.project_cards_needing_review[0].assignees.first())

        result = get_cards_needing_competent_reviewers()
        self.assertEqual(
            sorted([o.id for o in result]),
            sorted([o.id for o in self.project_cards_needing_review][1:]),
        )


@mock.patch("git_real.helpers.github_user_exists", return_value=True)
class get_possible_competent_reviewers_Tests(TestCase):
    def setUp(self):
        setup_config()

    def test_that_only_competent_people_get_returned(self, _):
        config = NameSpace.get_config(CONFIGURATION_NAMESPACE)
        competent_project = RecruitProjectFactory(
            complete_time=timezone.now(), flavours=[JAVASCRIPT]
        )

        content_item = competent_project.content_item

        card = AgileCardFactory(
            recruit_project=RecruitProjectFactory(
                complete_time=None,
                flavours=[JAVASCRIPT],
                content_item=content_item,
            ),
            status=AgileCard.IN_PROGRESS,
        )

        team = TeamFactory(name=config.EXCLUDE_TEAMS_FROM_COMPETENT_REVIEW_STEP[0])
        team.user_set.add(competent_project.recruit_users.first())
        result = list(get_possible_competent_reviewers(card))
        self.assertEqual(result, [])

    def test_that_only_competent_people_get_returned(self, _):

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
                complete_time=None,
                flavours=[JAVASCRIPT],
                content_item=content_item,
            ),
            status=AgileCard.IN_PROGRESS,
        )

        assert card.flavours_match(
            card.recruit_project.flavour_names
        ), f"{card.flavour_names} != {card.recruit_project.flavour_names}"
        result = list(get_possible_competent_reviewers(card))
        self.assertEqual(result, [competent_project.recruit_users.first()])

    def test_that_it_works_with_flavourless_projects(self, _):
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
        result = list(get_possible_competent_reviewers(card))
        self.assertEqual(result, [competent_project.recruit_users.first()])

    def test_that_reviewers_returned_in_order(self, _):
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
                    status=AgileCard.IN_PROGRESS,
                    recruit_project=RecruitProjectFactory(
                        complete_time=None, flavours=[], content_item=content_item
                    ),
                )
                project_user = project.recruit_users.first()
                nyc_card.reviewers.add(project_user)
                nyc_card.recruit_project.reviewer_users.add(project_user)

        card = AgileCardFactory(
            status=AgileCard.IN_PROGRESS,
            recruit_project=RecruitProjectFactory(
                complete_time=None, flavours=[], content_item=content_item
            ),
        )
        expected_result = [
            project.recruit_users.first() for project in competent_projects[::-1]
        ]
        assert expected_result
        result = list(get_possible_competent_reviewers(card))
        self.assertEqual(
            result,
            expected_result,
        )

        # add some more duties to first person and make sure order is still correct
        project_user = expected_result[0]
        for i in range(5):

            nyc_card = AgileCardFactory(
                status=AgileCard.IN_PROGRESS,
                recruit_project=RecruitProjectFactory(
                    complete_time=None, flavours=[], content_item=content_item
                ),
            )
            nyc_card.reviewers.add(project_user)
            nyc_card.recruit_project.reviewer_users.add(project_user)

        expected_result = expected_result[1:] + [expected_result[0]]
        result = list(get_possible_competent_reviewers(card))
        self.assertEqual(
            result,
            expected_result,
        )

        # test_that_if_a_user_is_already_a_reviewer_they_are_skipped(self)

        card.reviewers.add(expected_result[0])
        card.recruit_project.reviewer_users.add(expected_result[0])
        card.reviewers.add(expected_result[-1])
        card.recruit_project.reviewer_users.add(expected_result[-1])
        result = list(get_possible_competent_reviewers(card))
        self.assertEqual(
            result,
            expected_result[1:-1],
        )
