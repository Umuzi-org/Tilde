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


class get_projects_user_can_review_Tests(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.project_user_has_reviewed = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.READY,
        )

        self.project_user_has_reviewed.start_project()
        self.project_user_has_reviewed.recruit_project.request_review()

        RecruitProjectReviewFactory(
            status=COMPETENT,
            recruit_project=self.project_user_has_reviewed.recruit_project,
            reviewer_user=self.user,
        )

        self.projects_user_has_not_reviewed = [
            AgileCardFactory(
                content_item=ContentItemFactory(
                    content_type=ContentItem.PROJECT,
                    project_submission_type=ContentItem.LINK,
                ),
                status=AgileCard.READY,
            )
            for _ in range(2)
        ]

        for project in self.projects_user_has_not_reviewed:
            project.start_project()
            project.recruit_project.request_review()

        self.projects_in_review = self.projects_user_has_not_reviewed + [
            self.project_user_has_reviewed
        ]

    def test_get_projects_user_can_review_returns_the_right_projects(self):
        projects_user_can_review = (
            ProjectReviewBundleClaim.get_projects_user_can_review(self.user)
        )

        assert self.project_user_has_reviewed not in projects_user_can_review
        assert len(projects_user_can_review) == len(self.projects_user_has_not_reviewed)


class get_projects_user_can_review_with_permission_check_Tests(TestCase):
    def setUp(self) -> None:
        self.superuser = UserFactory(is_superuser=True)
        
        self.learner_a = UserFactory(email="learner_a@umuzi.org")
        self.learner_b = UserFactory(email="learner_b@umuzi.org")
        
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
            status=AgileCard.READY,
        )
        self.learner_a_card.assignees.set([self.learner_a])
        self.learner_a_card.start_project()
        self.learner_a_card.recruit_project.request_review()

        self.learner_b_card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.READY,
        )
        self.learner_b_card.assignees.set([self.learner_b])
        self.learner_b_card.start_project()
        self.learner_b_card.recruit_project.request_review()


    def test_get_projects_user_can_review_as_superuser(self):
        projects_user_can_review = (
            ProjectReviewBundleClaim.get_projects_user_can_review(self.superuser)
        )

        assert len(projects_user_can_review) == 2 # All
    

    def test_get_projects_user_can_review_as_reviewer(self):
        projects_user_can_review = (
            ProjectReviewBundleClaim.get_projects_user_can_review(self.reviewer)
        )

        assert len(projects_user_can_review) == 1
        assert self.learner_a_card in projects_user_can_review
        assert self.learner_b_card not in projects_user_can_review