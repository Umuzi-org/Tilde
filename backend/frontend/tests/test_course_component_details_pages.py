import datetime

from django.utils import timezone

from core.tests.factories import UserFactory
from .frontend_test_mixin import FrontendTestMixin
from curriculum_tracking.tests import factories
from curriculum_tracking.models import AgileCard


class TestCourseComponent(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(
            email="learner@umuzi.org",
            is_staff=True,
            is_superuser=True,
        )
        self.user.set_password(self.user.email)
        self.user.save()

        self.reviewer_1 = UserFactory(
            email="learner_r1@umuzi.org",
        )
        self.reviewer_1.save()
        self.reviewer_2 = UserFactory(
            email="learner_r2@umuzi.org",
        )
        self.reviewer_2.save()

        self.content_item = factories.ContentItemFactory()
        self.content_item.project_submission_type = "L"
        self.content_item.save()

        self.link_project = factories.RecruitProjectFactory(
            recruit_users=[self.user],
            reviewer_users=[self.reviewer_1, self.reviewer_2],
            content_item=self.content_item,
        )
        self.link_project.start_time = datetime.datetime(
            2024, 2, 12, 14, 6, 17, 373514, tzinfo=timezone.utc
        )
        self.link_project.due_time = datetime.datetime(
            2024, 2, 13, 14, 6, 17, 373514, tzinfo=timezone.utc
        )
        self.link_project.save()

        self.agile_card_for_link_project = factories.AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=self.link_project,
            content_item=self.content_item,
            assignees=[self.user],
        )
        self.agile_card_for_link_project.start_topic()

        self.link_project_url = self.reverse_url(
            "course_component_details", kwargs={"project_id": f"{self.link_project.id}"}
        )

    def test_link_project_page_displays_correct_details(self):
        self.do_login(self.user)
        self.page.goto(self.link_project_url)

        body = self.page.text_content("body")

        self.assertIn("Course Component Details", body)
        self.assertIn("learner@umuzi.org", body)
        self.assertIn("In Progress", body)
        self.assertIn("Feb. 12, 2024, 2:06 p.m.", body)
        self.assertIn("Feb. 13, 2024, 2:06 p.m.", body)
        self.assertIn("learner_r1@umuzi.org", body)
        self.assertIn("learner_r2@umuzi.org", body)
        self.assertIn(
            self.link_project.content_item.url,
            body,
        )
        self.assertIn("No link submitted yet", body)
