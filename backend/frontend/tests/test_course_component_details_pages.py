from django.utils import timezone
from playwright.sync_api import expect
from datetime import datetime, timedelta
from unittest.mock import patch
from activity_log.models import LogEntry

from core.tests.factories import UserFactory
from .frontend_test_mixin import FrontendTestMixin
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
    RecruitProjectFactory,
    TopicProgressFactory,
)
from curriculum_tracking.models import (
    AgileCard,
    ContentItem,
)


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

    def make_topic_card(self):
        content_item = ContentItemFactory(content_type=ContentItem.TOPIC)

        self.topic = TopicProgressFactory(
            user=self.user,
            content_item=content_item,
            start_time=datetime(2024, 2, 12, 14, 6, 17, 373514, tzinfo=timezone.utc),
            due_time=datetime(2024, 2, 13, 14, 6, 17, 373514, tzinfo=timezone.utc),
        )

        AgileCardFactory(
            content_item=content_item,
            status=AgileCard.IN_PROGRESS,
            topic_progress=self.topic,
        )

    def make_ip_project_card(self, project_submission_type):
        content_item = ContentItemFactory(
            content_type=ContentItem.PROJECT,
            project_submission_type=project_submission_type,
        )

        learner_reviewer = UserFactory(
            email="learner_reviewer@umuzi.org",
        )

        self.recruit_project = RecruitProjectFactory(
            recruit_users=[self.user],
            reviewer_users=[learner_reviewer],
            content_item=content_item,
            start_time=datetime(2024, 2, 12, 14, 6, 17, 373514, tzinfo=timezone.utc),
            due_time=datetime(2024, 2, 13, 14, 6, 17, 373514, tzinfo=timezone.utc),
        )

        self.agile_card = AgileCardFactory(
            content_item=content_item,
            status=AgileCard.IN_PROGRESS,
            recruit_project=self.recruit_project,
        )

    def test_course_component_page_displays_correct_details_for_link_project(self):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            "course_component_details_project",
            kwargs={"id": self.recruit_project.id},
        )
        self.page.goto(self.link_project_url)

        body = self.page.text_content("body")

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

    def test_link_submission_form_correctly_updates_link_submission(
        self,
    ):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            "course_component_details_project",
            kwargs={"id": self.recruit_project.id},
        )
        self.page.goto(self.link_project_url)

        body = self.page.text_content("body")

        self.assertIn("learner_1@umuzi.org", body)
        self.assertIn("In Progress", body)
        self.assertIn("Feb. 12, 2024, 2:06 p.m.", body)
        self.assertIn("Feb. 13, 2024, 2:06 p.m.", body)
        self.assertIn(
            self.recruit_project.content_url,
            body,
        )
        self.assertIn("No link submitted yet", body)

        self.page.get_by_label("Link submission").fill("https://google.com")

        self.page.click("text=Submit Link")
        self.page.wait_for_load_state("networkidle")

        body = self.page.text_content("body")
        self.assertIn("https://google.com", body)

    def test_link_submission_form_disappears_after_successful_submission(
        self,
    ):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            "course_component_details_project",
            kwargs={"id": self.recruit_project.id},
        )
        self.page.goto(self.link_project_url)

        link_submission_form = self.page.locator('[id="link_submission_form"]')
        expect(link_submission_form).to_be_visible()

        expect(
            self.page.get_by_role("button", name="Edit link submission")
        ).not_to_be_visible()

        self.page.get_by_label("Link submission").fill("https://google.com")
        self.page.click("text=Submit Link")
        self.page.wait_for_load_state("networkidle")

        link_submission_form = self.page.locator('[id="link_submission_form"]')
        expect(link_submission_form).to_be_hidden()

        expect(
            self.page.get_by_role("button", name="Edit link submission")
        ).to_be_visible()

    def test_link_submission_form_appears_after_edit_link_submission_button_is_clicked(
        self,
    ):
        self.make_ip_project_card(ContentItem.LINK)
        self.recruit_project.link_submission = "https://google.com"
        self.recruit_project.save()

        self.link_project_url = self.reverse_url(
            "course_component_details_project",
            kwargs={"id": self.recruit_project.id},
        )
        self.page.goto(self.link_project_url)

        link_submission_form = self.page.locator('[id="link_submission_form"]')
        expect(link_submission_form).not_to_be_visible()

        expect(
            self.page.get_by_role("button", name="Edit link submission")
        ).to_be_visible()

        self.page.click("text=Edit link submission")
        self.page.wait_for_load_state("networkidle")

        link_submission_form = self.page.locator('[id="link_submission_form"]')
        expect(link_submission_form).to_be_visible

        expect(
            self.page.get_by_role("button", name="Edit link submission")
        ).not_to_be_visible()

    def test_link_submission_form_displays_correct_error_message_when_form_is_submitted_with_no_input(
        self,
    ):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            "course_component_details_project",
            kwargs={"id": self.recruit_project.id},
        )
        self.page.goto(self.link_project_url)

        self.page.get_by_label("Link submission").fill("")
        self.page.click("text=Submit Link")
        self.page.wait_for_load_state("networkidle")

        body = self.page.text_content("body")
        self.assertIn("This field is required", body)

    def test_link_submission_form_displays_correct_error_message_when_form_is_submitted_with_invalid_input(
        self,
    ):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            "course_component_details_project",
            kwargs={"id": self.recruit_project.id},
        )
        self.page.goto(self.link_project_url)

        self.page.get_by_label("Link submission").fill("http://google")
        self.page.click("text=Submit Link")
        self.page.wait_for_load_state("networkidle")

        body = self.page.text_content("body")
        self.assertIn("Enter a valid URL", body)


class TestTopicDetailsPage(FrontendTestMixin):
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

    def make_topic_card(self, card_status):
        content_item = ContentItemFactory(content_type=ContentItem.TOPIC)

        self.topic = TopicProgressFactory(
            user=self.user,
            start_time=datetime(2024, 2, 12, 14, 6, 17, 373514, tzinfo=timezone.utc),
            due_time=datetime(2024, 2, 13, 14, 6, 17, 373514, tzinfo=timezone.utc),
        )

        self.card = AgileCardFactory(
            content_item=content_item,
            status=card_status,
            topic_progress=self.topic,
        )

        self.card.assignees.set([self.user])

    def test_course_component_page_displays_correct_details_for_topic(self):
        self.make_topic_card(AgileCard.IN_PROGRESS)

        self.topic_url = self.reverse_url(
            "course_component_details_topic",
            kwargs={"id": self.topic.id},
        )
        self.page.goto(self.topic_url)

        body = self.page.text_content("body")

        self.assertIn("learner_1@umuzi.org", body)
        self.assertIn("In Progress", body)
        self.assertIn("Feb. 12, 2024, 2:06 p.m.", body)
        self.assertIn("Feb. 13, 2024, 2:06 p.m.", body)
        self.assertIn(
            self.topic.content_url,
            body,
        )

    def test_course_component_page_displays_duration_details_for_topic(self):
        self.make_topic_card(AgileCard.READY)

        link_card_element = self.page.locator(
            f"div#column_RB > div#card_{self.card.id}"
        )

        details_link_element = link_card_element.get_by_role("button", name="Start")
        details_link_element.click()
        self.page.wait_for_load_state("networkidle")

        self.assertEqual(
            LogEntry.objects.filter(object_1_id=self.card.topic_progress.id)[
                0
            ].timestamp,
            None,
        )
        self.assertEqual(LogEntry.objects.count(), 1)

        with patch.object(
            LogEntry._meta.get_field("timestamp"), "auto_now_add", True
        ), patch(
            "django.utils.timezone.now",
            side_effect=[
                timezone.now(),
                timezone.now() + timedelta(hours=3),
            ],
        ):

            link_card_element = self.page.locator(
                f"div#column_IP > div#card_{self.card.id}"
            )

            details_link_element = link_card_element.get_by_role("link", name="Details")
            details_link_element.click()
            self.page.wait_for_load_state("networkidle", timeout=450000)

            body = self.page.text_content("body")

            self.assertRegex(
                body,
                r"(\d{1,2})\s*days?,\s*(\d{1,2})\s*hours?,\s*(\d{1,2})\s*minutes?",
            )

            self.assertIn("0 days, 3 hours, 0 minutes", body)
