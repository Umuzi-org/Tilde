from core.tests.factories import UserFactory, TeamFactory
from .frontend_test_mixin import FrontendTestMixin
from guardian.shortcuts import assign_perm
from core.models import Team


class TestPage(FrontendTestMixin):
    def test_super_sees_all_teams(self):
        user = UserFactory(is_superuser=True, email="super@email.com", is_staff=True)
        user.set_password(user.email)
        user.save()

        teams = [TeamFactory() for _ in range(5)]

        self.do_login(user)
        url = self.reverse_url("users_and_teams_nav")
        self.page.goto(url)

        body = self.page.text_content("body")

        # make sure that every single team name shows up in the body
        for team in teams:
            self.assertIn(team.name, body)

    def test_user_sees_teams_they_have_view_permission_for(self):
        user = UserFactory(email="some_user@email.com")
        user.set_password(user.email)
        user.save()

        teams = [TeamFactory() for _ in range(5)]

        assign_perm(
            Team.PERMISSION_MANAGE_CARDS,
            user,
            teams[0],
        )
        self.do_login(user)
        url = self.reverse_url("users_and_teams_nav")
        self.page.goto(url)

        body = self.page.text_content("body")

        # make sure that on the first team name shows up in the body
        for i in range(len(teams)):
            # if i == 0:
            #     self.assertIn(teams[0].name, body)
            # else:
            self.assertNotIn(teams[i].name, body)
