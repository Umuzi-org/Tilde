from django.test import TestCase
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
    RecruitProjectReviewFactory,
)
from core.tests.factories import UserFactory
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

        projects_user_has_not_reviewed = [
            AgileCardFactory(
                content_item=ContentItemFactory(
                    content_type=ContentItem.PROJECT,
                    project_submission_type=ContentItem.LINK,
                ),
                status=AgileCard.READY,
            )
            for _ in range(2)
        ]

        for project in projects_user_has_not_reviewed:
            project.start_project()
            project.recruit_project.request_review()

        self.projects_in_review = projects_user_has_not_reviewed + [
            self.project_user_has_reviewed
        ]

    def test_get_projects_user_can_review_returns_the_right_projects(self):
        projects__user_can_review = (
            ProjectReviewBundleClaim.get_projects_user_can_review(self.user)
        )

        assert self.project_user_has_reviewed not in projects__user_can_review
        assert len(self.projects_in_review) != len(projects__user_can_review)
