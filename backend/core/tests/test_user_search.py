from core.tests.factories import UserFactory
from social_auth.tests.factories import SocialProfileFactory
from core.models import User
from django.test import TestCase


class TeamSearchTestCase(TestCase):

    def setUp(self):
        self.john_nolan = UserFactory(
            first_name="john",
            last_name="nolan",
            email="john_nolan@hotmail.com",
            active=True,
        )
        self.lucy_chen = UserFactory(
            first_name="lucy", last_name="chen", email="lucy.c@yahoo.com", active=True
        )

        self.users = User.objects.all()

    def test_search_term_first_name_john(self):
        search_term = "jOHn"
        users = User.get_users_from_search_term(search_term, self.users)
        self.assertIn(self.john_nolan, users)
        self.assertNotIn(self.lucy_chen, users)

    def test_search_term_last_name_chen(self):
        search_term = "CHEN"
        users = User.get_users_from_search_term(search_term, self.users)
        self.assertIn(self.lucy_chen, users)
        self.assertNotIn(self.john_nolan, users)

    def test_search_term_email_chen(self):
        search_term = "CHEN"
        users = User.get_users_from_search_term(search_term, self.users)
        self.assertIn(self.lucy_chen, users)
        self.assertNotIn(self.john_nolan, users)
