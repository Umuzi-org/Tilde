from guardian.shortcuts import assign_perm
from core.models import Team
from core.tests.factories import UserFactory, TeamFactory
from .frontend_test_mixin import FrontendTestMixin


class TestUserBoardAuthorization(FrontendTestMixin):
    def setUp(self):
        super().setUp()

        self.viewed_user_team = TeamFactory()
        self.viewed_user = UserFactory(
            email="learner.umuzi.org",
        )
        self.viewed_user.set_password(self.viewed_user.email)
        self.viewed_user.save()
        self.viewed_user_team.user_set.add(self.viewed_user)

        self.user_without_access = UserFactory(
            email="user_without_access.umuzi.org",
        )
        self.user_without_access.set_password(self.user_without_access.email)
        self.user_without_access.save()

        self.superuser = UserFactory(
            is_superuser=True,
            email="super@email.com",
        )
        self.superuser.set_password(self.superuser.email)
        self.superuser.save()

        self._setup_users_who_can_view_user_board()

    def _setup_users_who_can_view_user_board(self):
        self._setup_user_with_manage_card_permission()
        self._setup_user_with_view_permission()
        self._setup_user_with_review_cards_permission()
        self._setup_trusted_user()

    def _setup_user_with_manage_card_permission(self):
        self.user_with_manage_card_permission = UserFactory(
            email="user_with_manage_card_permission.umuzi.org"
        )
        self.user_with_manage_card_permission.set_password(
            self.user_with_manage_card_permission.email
        )
        self.user_with_manage_card_permission.save()
        assign_perm(
            Team.PERMISSION_MANAGE_CARDS,
            self.user_with_manage_card_permission,
            self.viewed_user_team,
        )

    def _setup_user_with_view_permission(self):
        self.user_with_view_permission = UserFactory(
            email="user_with_view_permission.umuzi.org"
        )
        self.user_with_view_permission.set_password(
            self.user_with_view_permission.email
        )
        self.user_with_view_permission.save()
        assign_perm(
            Team.PERMISSION_VIEW_ALL,
            self.user_with_view_permission,
            self.viewed_user_team,
        )

    def _setup_user_with_review_cards_permission(self):
        self.user_with_review_cards_permission = UserFactory(
            email="user_with_review_cards_permission.umuzi.org"
        )
        self.user_with_review_cards_permission.set_password(
            self.user_with_review_cards_permission.email
        )
        self.user_with_review_cards_permission.save()
        assign_perm(
            Team.PERMISSION_REVIEW_CARDS,
            self.user_with_review_cards_permission,
            self.viewed_user_team,
        )

    def _setup_trusted_user(self):
        self.trusted_reviewer = UserFactory(email="trusted_reviewer.umuzi.org")
        self.trusted_reviewer.set_password(self.trusted_reviewer.email)
        self.trusted_reviewer.save()
        assign_perm(
            Team.PERMISSION_TRUSTED_REVIEWER,
            self.trusted_reviewer,
            self.viewed_user_team,
        )

    def test_super_user_can_view_user_board(self):
        self.do_login(self.superuser)
        url = self.reverse_url("user_board", kwargs={
                               "user_id": self.viewed_user.id})
        self.page.goto(url)

        body = self.page.text_content("body")

        self.assertIn(f"Viewing {self.viewed_user.email}", body)

    def test_user_can_view_own_board(self):
        self.do_login(self.viewed_user)
        url = self.reverse_url("user_board", kwargs={
                               "user_id": self.viewed_user.id})
        self.page.goto(url)

        body = self.page.text_content("body")

        self.assertIn(f"Viewing {self.viewed_user.email}", body)

    def test_user_without_view_access_cannot_view_other_user_board(self):
        """
        Custom @user_passes_test_or_forbidden(func) mixin we use to control
        access to user board views should return a 403 response if the user
        does not have access to the user board.
        """
        self.do_login(self.user_without_access)
        url = self.reverse_url("user_board", kwargs={
                               "user_id": self.viewed_user.id})

        self.page.goto(url)

        body = self.page.text_content("body")
        
        self.assertIn("Permission Denied", body)
        

    def test_login_redirection_if_unauthenticated(self):
        """
        Custom @user_passes_test_or_forbidden(func) should redirect to login if
        the user is not authenticated.
        """
        url = self.reverse_url("user_board", kwargs={
                               "user_id": self.viewed_user.id})

        self.page.goto(url)

        body = self.page.text_content("body")

        self.assertIn("Log in", body)

    def test_user_with_manage_card_permission_can_view_user_board(self):
        self.do_login(self.user_with_manage_card_permission)
        url = self.reverse_url("user_board", kwargs={
                               "user_id": self.viewed_user.id})
        self.page.goto(url)

        body = self.page.text_content("body")

        self.assertIn(f"Viewing {self.viewed_user.email}", body)

    def test_user_with_view_all_permission_can_view_user_board(self):
        self.do_login(self.user_with_view_permission)
        url = self.reverse_url("user_board", kwargs={
                               "user_id": self.viewed_user.id})
        self.page.goto(url)

        body = self.page.text_content("body")

        self.assertIn(f"Viewing {self.viewed_user.email}", body)

    def test_user_with_review_cards_permission_can_view_user_board(self):
        self.do_login(self.user_with_review_cards_permission)
        url = self.reverse_url("user_board", kwargs={
                               "user_id": self.viewed_user.id})
        self.page.goto(url)

        body = self.page.text_content("body")

        self.assertIn(f"Viewing {self.viewed_user.email}", body)

    def test_trusted_reviewer_can_view_user_board(self):
        self.do_login(self.trusted_reviewer)
        url = self.reverse_url("user_board", kwargs={
                               "user_id": self.viewed_user.id})
        self.page.goto(url)

        body = self.page.text_content("body")

        self.assertIn(f"Viewing {self.viewed_user.email}", body)
