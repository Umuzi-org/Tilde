from core.tests.factories import UserFactory, TeamFactory
from .frontend_test_mixin import FrontendTestMixin
from guardian.shortcuts import assign_perm
from core.models import Team
from playwright.sync_api import expect


class TestPage(FrontendTestMixin):
    def test_super_sees_all_teams(self):
        user = UserFactory(is_superuser=True, email="super@email.com", is_staff=True)
        user.set_password(user.email)
        user.save()

        teams = [TeamFactory() for _ in range(5)]

        self.do_login(user)
        url = self.reverse_url("users_and_teams_nav")
        self.page.goto(url)
        self.page.wait_for_load_state()
        body = self.page.locator("body")

        # make sure that every single team name shows up in the body
        for team in teams:
            expect(body).to_contain_text(team.name)

    def test_user_sees_teams_they_have_view_permission_for(self):
        user = UserFactory(email="some_user@email.com")
        user.set_password(user.email)
        user.save()

        teams_user_has_view_permissions_for = [TeamFactory() for _ in range(3)]
        teams_user_has_no_view_permissions_for = [TeamFactory() for _ in range(3)]

        for team in teams_user_has_view_permissions_for:
            assign_perm(
                Team.PERMISSION_MANAGE_CARDS,
                user,
                team,
            )

        self.do_login(user)
        url = self.reverse_url("view_partial_teams_list")
        self.page.goto(url)
        self.page.wait_for_load_state()
        body = self.page.locator("body")

        # can see teams when the user has view perms
        for team in teams_user_has_view_permissions_for:
            expect(body).to_contain_text(team.name)

        # user cannot see teams without view permissions
        for team in teams_user_has_no_view_permissions_for:
            expect(body).not_to_contain_text(team.name)

    def test_load_more_button_appears(self):
        user = UserFactory(is_superuser=True, email="super@email.com", is_staff=True)
        user.set_password(user.email)
        user.save()

        teams = [TeamFactory() for _ in range(21)]
        for team in teams:
            assign_perm
            (
                Team.PERMISSION_MANAGE_CARDS,
                user,
                team,
            )

        self.do_login(user)
        url = self.reverse_url("view_partial_teams_list")
        self.page.goto(url)
        self.page.wait_for_load_state()
        
        body = self.page.locator("body")

        expect(body).to_contain_text("Load more")

    def test_user_sees_teams_that_match_the_search_term(self):
        user = UserFactory(email="learner@email.com")
        user.set_password(user.email)
        user.save()

        boots_1999_team = TeamFactory(name="boots 1999")
        boots_2014_team = TeamFactory(name="boots 2014")
        detectives_team = TeamFactory(name="detectives")

        teams = [boots_1999_team,boots_2014_team,detectives_team]
        
        for team in teams:
            assign_perm(
                Team.PERMISSION_MANAGE_CARDS,
                user,
                team,
            )

        self.do_login(user)
        url = self.reverse_url("users_and_teams_nav")
        self.page.goto(url)
        self.page.wait_for_load_state()

        body = self.page.locator("body")
        
        search_input_box = body.get_by_placeholder("Search Teams...")
        
        search_input_box.press_sequentially("boots")

        found_teams = body.page.locator("div#teams-list")

        expect(found_teams).to_contain_text(boots_1999_team.name)
        expect(found_teams).to_contain_text(boots_2014_team.name)
        expect(found_teams).not_to_contain_text(detectives_team.name)

        search_input_box.press_sequentially("zzzzzzzzzzz")

        expect(found_teams).to_contain_text("No teams found")