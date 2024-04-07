import datetime
from math import exp

from django.utils import timezone
from playwright.sync_api import expect

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

        self.agile_card = AgileCardFactory(
            content_item=content_item,
            status=AgileCard.IN_PROGRESS,
            recruit_project=self.recruit_project,
        )

    def test_link_project_page_displays_correct_details(self):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            "course_component_details", kwargs={"project_id": self.recruit_project.id}
        )
        self.page.goto(self.link_project_url)

        self.page.wait_for_load_state()
        
        self.assertEqual(self.page.url, self.link_project_url)

        body = self.page.locator("body")

        expect(body).to_contain_text("learner_1@umuzi.org")
        expect(body).to_contain_text("In Progress")
        expect(body).to_contain_text("Feb. 12, 2024, 2:06 p.m.")
        expect(body).to_contain_text("Feb. 13, 2024, 2:06 p.m.")
        expect(body).to_contain_text("learner_reviewer@umuzi.org")
        expect(body).to_contain_text(self.recruit_project.content_url)
        expect(body).to_contain_text("No link submitted yet")

    def test_link_submission_form_correctly_updates_link_submission(
        self,
    ):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            "course_component_details", kwargs={"project_id": self.recruit_project.id}
        )
        self.page.goto(self.link_project_url)

        self.assertEqual(self.page.url, self.link_project_url)

        body = self.page.locator("body")

        expect(body).to_contain_text("No link submitted yet")

        self.page.get_by_label("Link submission").fill("https://google.com")

        self.page.click("text=Submit Link")
        self.page.wait_for_load_state()

        body = self.page.locator("body")

        expect(body).to_contain_text("https://google.com")

    def test_link_submission_form_disappears_after_successful_submission(
        self,
    ):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            "course_component_details", kwargs={"project_id": self.recruit_project.id}
        )
        self.page.goto(self.link_project_url)

        self.assertEqual(self.page.url, self.link_project_url)

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
            "course_component_details", kwargs={"project_id": self.recruit_project.id}
        )
        self.page.goto(self.link_project_url)

        self.assertEqual(self.page.url, self.link_project_url)

        link_submission_form = self.page.locator('[id="link_submission_form"]')
        expect(link_submission_form).not_to_be_visible()

        expect(
            self.page.get_by_role("button", name="Edit link submission")
        ).to_be_visible()

        self.page.click("text=Edit link submission")
        self.page.wait_for_load_state()

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
            "course_component_details", kwargs={"project_id": self.recruit_project.id}
        )
        self.page.goto(self.link_project_url)

        self.assertEqual(self.page.url, self.link_project_url)

        self.page.get_by_label("Link submission").fill("")
        self.page.click("text=Submit Link")
        self.page.wait_for_load_state("networkidle")

        body = self.page.locator("body")
        expect(body).to_contain_text("This field is required")

    def test_link_submission_form_displays_correct_error_message_when_form_is_submitted_with_invalid_input(
        self,
    ):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            "course_component_details", kwargs={"project_id": self.recruit_project.id}
        )
        self.page.goto(self.link_project_url)

        self.assertEqual(self.page.url, self.link_project_url)

        self.page.get_by_label("Link submission").fill("http://google")
        self.page.click("text=Submit Link")
        self.page.wait_for_load_state("networkidle")

        body = self.page.locator("body")
        expect(body).to_contain_text("Enter a valid URL")
