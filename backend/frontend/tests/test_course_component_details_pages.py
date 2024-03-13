import datetime

from django.utils import timezone

from core.tests.factories import UserFactory
from .frontend_test_mixin import FrontendTestMixin
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
    RecruitProjectFactory,
)
from curriculum_tracking.models import AgileCard, ContentItem


class TestLinkProjectDetailsPage(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(
            email="learner_1@umuzi.org",
            is_staff=True,
            is_superuser=True,
        )
        self.user.set_password(self.user.email)
        self.user.save()
        self.do_login(self.user)

    def make_ip_project_card(self, project_submission_type):
        content_item = ContentItemFactory(
            content_type=ContentItem.PROJECT,
            project_submission_type=project_submission_type,
        )

        learner_reviewer = UserFactory(
            email="learner_reviewer@umuzi.org",
        )

        self.recruit_project = RecruitProjectFactory(
        self.recruit_project = RecruitProjectFactory(
            recruit_users=[self.user],
            reviewer_users=[learner_reviewer],
            content_item=content_item,
            start_time=datetime.datetime(
                2024, 2, 12, 14, 6, 17, 373514, tzinfo=timezone.utc
            ),
            due_time=datetime.datetime(
                2024, 2, 13, 14, 6, 17, 373514, tzinfo=timezone.utc
            ),
        )

        AgileCardFactory(
            content_item=content_item,
            status=AgileCard.IN_PROGRESS,
            recruit_project=self.recruit_project,
        )

    def test_link_project_page_displays_correct_details(self):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            "course_component_details",
            kwargs={"id": self.recruit_project.id, "type": "project"},
            "course_component_details", kwargs={"project_id": self.recruit_project.id}
        )
        self.page.goto(self.link_project_url)

        body = self.page.text_content("body")

        self.assertIn("Course Component Details", body)
        self.assertIn("learner_1@umuzi.org", body)
        self.assertIn("In Progress", body)
        self.assertIn("Feb. 12, 2024, 2:06 p.m.", body)
        self.assertIn("Feb. 13, 2024, 2:06 p.m.", body)
        self.assertIn("learner_reviewer@umuzi.org", body)
        self.assertIn(
            self.recruit_project.content_url,
            body,
        )
        self.assertIn("No link submitted yet", body)
