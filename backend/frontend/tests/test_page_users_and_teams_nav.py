from core.tests.factories import UserFactory, TeamFactory
from .frontend_test_mixin import FrontendTestMixin


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
