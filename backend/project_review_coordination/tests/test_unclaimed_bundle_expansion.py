from core.tests.factories import UserFactory, TeamFactory
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
)
from playwright.sync_api import expect
from curriculum_tracking.models import ContentItem, AgileCard
from frontend.tests.frontend_test_mixin import FrontendTestMixin
from guardian.shortcuts import assign_perm
from core.models import Team

UNCLAIMED_BUNDLES_VIEW = "project_review_coordination_unclaimed"

class TestUnclaimedBundleDetailExpansion(FrontendTestMixin):
    EXPAND_BTN_LABEL = "Show details"
    COLLAPSE_BTN_LABEL = "Hide details"

    def setUp(self):
        super().setUp()

        self.learner = UserFactory()

        self.reviewer = UserFactory(is_staff=True)
        self.reviewer.set_password(self.reviewer.email)
        self.reviewer.save()

        self.team = TeamFactory()
        self.team.user_set.add(self.learner)
        assign_perm(
            Team.PERMISSION_VIEW_ALL,
            self.reviewer,
            self.team,
        )

        self.card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.READY
        )

        self.card.assignees.set([self.learner])
        self.card.recruit_project.recruit_users.set([self.learner])
        self.card.start_project()
        self.card.recruit_project.request_review()

    def _get_unclaimed_bundles_url(self):
        return self.reverse_url(
            UNCLAIMED_BUNDLES_VIEW
        )

    def test_expand_bundle_button(self):
        self.do_login(self.reviewer)
        self.page.goto(self._get_unclaimed_bundles_url())
        self.page.wait_for_load_state()

        expanded_section = self.page.locator("div#bundle_0_drilldown")
        expand_button = self.page.get_by_role("button", name=self.EXPAND_BTN_LABEL)
        collapse_button = self.page.get_by_role("button", name=self.COLLAPSE_BTN_LABEL)
        
        expect(expand_button).to_be_visible()
        expect(collapse_button).to_be_hidden()
        expect(expanded_section).to_be_empty()

        expand_button.click()
        self.page.wait_for_load_state("networkidle")

        expect(expanded_section).to_be_visible()
        expect(collapse_button).to_be_visible()

        projects = expanded_section.locator("table>tbody>tr")

        expect(projects).to_have_count(1)
        expect(projects).to_contain_text(self.learner.email)