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

PROGRESS_DETAILS_VIEW = "progress_details"

class TestProgressDetailsAddReviewButton(FrontendTestMixin):
    sample_review_comment = "This is a comment"

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.user.set_password(self.user.email)
        self.user.save()

        self.reviewer_by_assignment = UserFactory()
        self.reviewer_by_assignment.set_password(self.reviewer_by_assignment.email)
        self.reviewer_by_assignment.save()

        self.reviewer_by_permission = UserFactory()
        self.reviewer_by_permission.set_password(self.reviewer_by_permission.email)
        self.reviewer_by_permission.save()

        self.superuser = UserFactory(is_superuser=True)
        self.superuser.set_password(self.superuser.email)
        self.superuser.save()

        self.assignee_team = TeamFactory()
        self.assignee_team.user_set.add(self.user)
        self.assignee_team.save()

        assign_perm(
            Team.PERMISSION_MANAGE_CARDS,
            self.reviewer_by_permission,
            self.assignee_team,
        )


    def make_in_review_project_card(self):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.IN_REVIEW,
        )
        self.card.assignees.set([self.user])
        self.card.reviewers.add(self.reviewer_by_assignment)
        self.card.recruit_project.recruit_users.set([self.user])

    
    def _get_project_progress_details_url(self, project):
        return self.reverse_url(
            PROGRESS_DETAILS_VIEW, kwargs={"id": project.id, "content_type": "project"},
            
        )
    
    def test_super_user_can_add_review(self):
        self.make_in_review_project_card()

        self.do_login(self.superuser)
        self.page.wait_for_load_state()

        self.page.goto(self._get_project_progress_details_url(
            project=self.card.recruit_project
        ))
        self.page.wait_for_load_state()

        self.page.get_by_role("button", name="Add Review").click()
        self.page.wait_for_load_state()

        self.page.select_option("select#id_status", "competent")
        self.page.query_selector("textarea#id_comments").fill(self.sample_review_comment)

        self.page.locator("text=Submit Review").click()
        self.page.wait_for_load_state('networkidle')

        expect(self.page.locator("div#reviews")).to_contain_text(self.sample_review_comment)

    def test_reviewer_by_assignment_can_add_review(self):
        self.make_in_review_project_card()

        self.do_login(self.reviewer_by_assignment)
        self.page.wait_for_load_state()

        self.page.goto(self._get_project_progress_details_url(
            project=self.card.recruit_project
        ))
        self.page.wait_for_load_state()

        self.page.get_by_role("button", name="Add Review").click()
        self.page.wait_for_load_state()

        
        self.page.select_option("select#id_status", "competent")
        self.page.query_selector("textarea#id_comments").fill(self.sample_review_comment)

        self.page.locator("text=Submit Review").click()
        self.page.wait_for_load_state('networkidle')

        expect(self.page.locator("div#reviews")).to_contain_text(self.sample_review_comment)
    
    def test_reviewer_by_permission_can_add_review(self):
        self.make_in_review_project_card()

        self.do_login(self.reviewer_by_permission)
        self.page.wait_for_load_state()

        self.page.goto(self._get_project_progress_details_url(
            project=self.card.recruit_project
        ))
        self.page.wait_for_load_state()

        self.page.get_by_role("button", name="Add Review").click()
        self.page.wait_for_load_state()

        
        self.page.select_option("select#id_status", "competent")
        self.page.query_selector("textarea#id_comments").fill(self.sample_review_comment)

        self.page.locator("text=Submit Review").click()
        self.page.wait_for_load_state('networkidle')

        expect(self.page.locator("div#reviews")).to_contain_text(self.sample_review_comment)
    
    def test_add_review_logs_event(self):
        self.make_in_review_project_card()

        self.do_login(self.superuser)
        self.page.wait_for_load_state()

        self.page.goto(self._get_project_progress_details_url(
            project=self.card.recruit_project
        ))
        self.page.wait_for_load_state()

        self.page.get_by_role("button", name="Add Review").click()
        self.page.wait_for_load_state()
        
        self.page.select_option("select#id_status", "competent")
        self.page.query_selector("textarea#id_comments").fill(self.sample_review_comment)

        self.page.locator("text=Submit Review").click()
        self.page.wait_for_load_state('networkidle')

        log_entries = LogEntry.objects.all()
        self.assertEqual(log_entries.count(), 2)
        log_entry = log_entries.first()
        self.assertEqual(log_entry.actor_user, self.superuser)
        self.assertEqual(log_entry.effected_user, self.user)
        self.assertEqual(log_entry.event_type.name, creators.COMPETENCE_REVIEW_DONE)
        self.assertEqual(log_entry.object_1, self.card.recruit_project.project_reviews.first())
        self.assertEqual(log_entry.object_2, self.card.recruit_project)