import datetime
from django.utils import timezone
from playwright.sync_api import expect
from datetime import datetime
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from core.tests.factories import UserFactory
from .frontend_test_mixin import SuperuserLoggedInFrontendMixin
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
    RecruitProjectFactory,
    TopicProgressFactory,
    RepoProjectAgileCardFactory,
)
from curriculum_tracking.models import AgileCard, ContentItem
from git_real.models import PullRequest
from git_real.tests.factories import PullRequestFactory, RepositoryFactory

PROGRESS_DETAILS_VIEW = "progress_details"


class TestLinkProjectDetailsPage(SuperuserLoggedInFrontendMixin):

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

    @patch("django.utils.timezone.get_current_timezone")
    def test_progress_details_page_displays_correct_details_for_link_project(
        self, mock_get_current_timezone
    ):
        mock_get_current_timezone.return_value = timezone.utc

        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            PROGRESS_DETAILS_VIEW,
            kwargs={
                "content_type": "project",
                "id": self.recruit_project.id,
            },
        )

        self.page.goto(self.link_project_url)
        self.page.wait_for_load_state()

        self.assertEqual(self.page.url, self.link_project_url)

        body = self.page.locator("body")

        expect(body).to_contain_text(self.user.email)
        expect(body).to_contain_text("In Progress")

        expect(body).to_contain_text("Start Date: Feb. 12, 2024, 2:06 p.m.")
        expect(body).to_contain_text("Due Date: Feb. 13, 2024, 2:06 p.m.")

        expect(body).to_contain_text("learner_reviewer@umuzi.org")
        expect(body).to_contain_text(self.recruit_project.content_url)
        expect(body).to_contain_text("No link submitted yet")

    def test_link_submission_form_correctly_updates_link_submission(
        self,
    ):
        self.make_ip_project_card(ContentItem.LINK)

        self.link_project_url = self.reverse_url(
            PROGRESS_DETAILS_VIEW,
            kwargs={
                "content_type": "project",
                "id": self.recruit_project.id,
            },
        )
        self.page.goto(self.link_project_url)
        self.page.wait_for_load_state()

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
            PROGRESS_DETAILS_VIEW,
            kwargs={
                "content_type": "project",
                "id": self.recruit_project.id,
            },
        )
        self.page.goto(self.link_project_url)
        self.page.wait_for_load_state()

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
            PROGRESS_DETAILS_VIEW,
            kwargs={
                "content_type": "project",
                "id": self.recruit_project.id,
            },
        )
        self.page.goto(self.link_project_url)
        self.page.wait_for_load_state()

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
            PROGRESS_DETAILS_VIEW,
            kwargs={
                "content_type": "project",
                "id": self.recruit_project.id,
            },
        )
        self.page.goto(self.link_project_url)
        self.page.wait_for_load_state()

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
            PROGRESS_DETAILS_VIEW,
            kwargs={
                "content_type": "project",
                "id": self.recruit_project.id,
            },
        )
        self.page.goto(self.link_project_url)
        self.page.wait_for_load_state()

        self.assertEqual(self.page.url, self.link_project_url)

        self.page.get_by_label("Link submission").fill("http://google")
        self.page.click("text=Submit Link")
        self.page.wait_for_load_state("networkidle")

        body = self.page.text_content("body")
        self.assertIn("Enter a valid URL", body)


class TestTopicDetailsPage(SuperuserLoggedInFrontendMixin):

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

    @patch("django.utils.timezone.get_current_timezone")
    def test_progress_details_displays_correct_details_for_topic(
        self, mock_get_current_timezone
    ):
        mock_get_current_timezone.return_value = timezone.utc
        self.make_topic_card(AgileCard.IN_PROGRESS)

        topic_url = self.reverse_url(
            PROGRESS_DETAILS_VIEW,
            kwargs={
                "content_type": "topic",
                "id": self.topic.id,
            },
        )
        self.page.goto(topic_url)

        body = self.page.text_content("body")

        self.assertIn(self.user.email, body)
        self.assertIn("In Progress", body)
        self.assertIn("Feb. 12, 2024, 2:06 p.m.", body)
        self.assertIn("Feb. 13, 2024, 2:06 p.m.", body)
        self.assertIn(
            self.topic.content_url,
            body,
        )


class TestRepoProjectDetailsPage(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.user.set_password(self.user.email)
        self.user.save()

        self.client.login(username=self.user.email, password=self.user.email)

        self.card = RepoProjectAgileCardFactory(user=self.user)

    def _get_project_progress_details_url(self):
        return reverse(
            PROGRESS_DETAILS_VIEW,
            kwargs={"content_type": "project", "id": self.card.recruit_project.id},
        )

    def test_progress_details_page_displays_repo_for_repo_project(self):
        repo_project_progress_details_url = self._get_project_progress_details_url()
        response = self.client.get(repo_project_progress_details_url)
        self.assertContains(response, self.card.recruit_project.repository.full_name)

    def test_progress_details_page_displays_open_prs_for_repo_project(self):
        pr = PullRequestFactory(
            repository=self.card.recruit_project.repository, state=PullRequest.OPEN
        )
        repo_project_progress_details_url = self._get_project_progress_details_url()
        response = self.client.get(repo_project_progress_details_url)
        self.assertContains(response, pr.title)
