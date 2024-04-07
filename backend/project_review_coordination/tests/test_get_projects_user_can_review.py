from guardian.shortcuts import assign_perm
from django.test import TestCase
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
    RecruitProjectReviewFactory,
)
from core.models import Team
from core.tests.factories import UserFactory, TeamFactory
from curriculum_tracking.models import ContentItem, AgileCard
from curriculum_tracking.constants import COMPETENT

from project_review_coordination.models import ProjectReviewBundleClaim


class get_projects_user_can_review_with_permission_check_Tests(TestCase):
    def setUp(self) -> None:
        self.superuser = UserFactory(is_superuser=True)
        
        self.learner_a = UserFactory()
        self.learner_b = UserFactory()
        self.reviewer = UserFactory()

        self.permissioned_team = TeamFactory()
        self.permissioned_team.user_set.add(self.learner_a)
        assign_perm(
            Team.PERMISSION_VIEW_ALL,
            self.reviewer,
            self.permissioned_team,
        )

        self.restricted_team = TeamFactory()
        self.restricted_team.user_set.add(self.learner_b)

        self.learner_a_card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.READY
        )

        self.learner_a_card.assignees.set([self.learner_a])
        self.learner_a_card.recruit_project.recruit_users.set([self.learner_a])
        self.learner_a_card.start_project()
        self.learner_a_card.recruit_project.request_review()

        self.learner_b_card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.READY
        )
        self.learner_b_card.assignees.set([self.learner_b])
        self.learner_b_card.recruit_project.recruit_users.set([self.learner_b])
        self.learner_b_card.start_project()
        self.learner_b_card.recruit_project.request_review()

        self._setup_already_reviewed_card()

    def _setup_already_reviewed_card(self):
        self.already_reviewed_card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.READY
        )
        self.already_reviewed_card.start_project()
        self.already_reviewed_card.recruit_project.request_review()

        RecruitProjectReviewFactory(
            status=COMPETENT,
            recruit_project=self.already_reviewed_card.recruit_project,
            reviewer_user=self.reviewer,
        )

        self.already_reviewed_card.assignees.set([self.learner_a])
        self.already_reviewed_card.recruit_project.recruit_users.set([self.learner_a])

    def test_get_projects_user_can_review_as_superuser(self):
        projects_user_can_review = (
            ProjectReviewBundleClaim.get_projects_user_can_review(self.superuser)
        )

        self.assertEqual(len(projects_user_can_review), 3) # All
    

    def test_get_projects_user_can_review_as_reviewer(self):
        projects_user_can_review = (
            ProjectReviewBundleClaim.get_projects_user_can_review(self.reviewer)
        )

        self.assertEqual(len(projects_user_can_review), 1)
        self.assertNotIn(self.learner_b_card, projects_user_can_review)
        self.assertIn(self.learner_a_card, projects_user_can_review)

    def test_get_projects_user_can_review_excludes_already_reviewed(self):
        projects_user_can_review = (
            ProjectReviewBundleClaim.get_projects_user_can_review(self.reviewer)
        )

        self.assertEqual(len(projects_user_can_review), 1)
        self.assertNotIn(self.already_reviewed_card, projects_user_can_review)
        self.assertIn(self.learner_a_card, projects_user_can_review)