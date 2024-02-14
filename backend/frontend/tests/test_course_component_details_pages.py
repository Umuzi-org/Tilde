from core.tests.factories import UserFactory
from .frontend_test_mixin import FrontendTestMixin
from curriculum_tracking.tests import factories
from curriculum_tracking.models import AgileCard
import datetime
from django.utils import timezone


class TestCourseComponent(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(
            email="learner@umuzi.org",
        )
        self.user.set_password(self.user.email)
        self.user.save()

        self.reviewer_1 = UserFactory(
            email="learner_r1@umuzi.org",
        )
        self.reviewer_2 = UserFactory(
            email="learner_r2@umuzi.org",
        )

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

        self.link_project_url = f"{self.live_server_url}/project/{self.link_project.id}"

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
            "https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/projects/tdd/simple-calculator/part-465/_index.md",
            body,
        )
        self.assertIn("No link submitted yet", body)
