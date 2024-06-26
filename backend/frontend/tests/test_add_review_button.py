from django.urls import reverse_lazy
from core.tests.factories import UserFactory, TeamFactory
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
)
from playwright.sync_api import expect
from curriculum_tracking.models import ContentItem, AgileCard
from .frontend_test_mixin import FrontendTestMixin
from activity_log.models import LogEntry
import curriculum_tracking.activity_log_entry_creators as creators
from guardian.shortcuts import assign_perm
from core.models import Team
from django.test import TestCase

PROGRESS_DETAILS_VIEW = "progress_details"


class TestProgressDetailsAddReviewButton(FrontendTestMixin):
    SAMPLE_REVIEW_COMMENT = "This is a comment"

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.user.set_password(self.user.email)
        self.user.save()

        self.superuser = UserFactory(is_superuser=True)
        self.superuser.set_password(self.superuser.email)
        self.superuser.save()

    def make_in_review_project_card(self):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.IN_REVIEW,
        )
        self.card.assignees.set([self.user])
        self.card.recruit_project.recruit_users.set([self.user])

    def get_project_progress_details_url(self, project):
        return self.reverse_url(
            PROGRESS_DETAILS_VIEW,
            kwargs={"id": project.id, "content_type": "project"},
        )

    def submit_review(self, status):
        self.page.get_by_role("button", name="Add Review").click()
        self.page.wait_for_load_state()
        self.page.select_option("select#id_status", status)
        self.page.query_selector("textarea#id_comments").fill(
            self.SAMPLE_REVIEW_COMMENT
        )
        self.page.query_selector("#submit-review-button").click()
        self.page.wait_for_load_state("networkidle")

    def test_add_review_logs_event(self):
        self.make_in_review_project_card()

        self.do_login(self.superuser)
        self.page.wait_for_load_state()

        self.page.goto(
            self.get_project_progress_details_url(project=self.card.recruit_project)
        )
        self.page.wait_for_load_state()

        self.submit_review("competent")

        log_entries = LogEntry.objects.all()
        self.assertEqual(log_entries.count(), 2)
        log_entry = log_entries.first()
        self.assertEqual(log_entry.actor_user, self.superuser)
        self.assertEqual(log_entry.effected_user, self.user)
        self.assertEqual(log_entry.event_type.name, creators.COMPETENCE_REVIEW_DONE)
        self.assertEqual(
            log_entry.object_1, self.card.recruit_project.project_reviews.first()
        )
        self.assertEqual(log_entry.object_2, self.card.recruit_project)
