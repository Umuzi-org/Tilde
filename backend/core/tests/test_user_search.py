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
        SocialProfileFactory(user=self.lucy_chen, github_name="lucy_goosey")

        self.users = User.objects.all()

    def test_search_term_first_name_john(self):
        search_term = "jOHn"
        users = User.get_users_from_search_term(search_term, self.users)
        self.assertTrue(len(users), 1)
        self.assertIn(self.john_nolan, users)
        self.assertNotIn(self.lucy_chen, users)

    def test_search_term_last_name_chen(self):
        search_term = "CHEN"
        users = User.get_users_from_search_term(search_term, self.users)
        self.assertEqual(len(users), 1)
        self.assertIn(self.lucy_chen, users)
        self.assertNotIn(self.john_nolan, users)

    def test_search_term_email_c_at_yahoo(self):
        search_term = "c@yahoo"
        users = User.get_users_from_search_term(search_term, self.users)
        self.assertEqual(len(users), 1)
        self.assertIn(self.lucy_chen, users)
        self.assertNotIn(self.john_nolan, users)

    def test_search_term_github_lucy_goosey(self):
        search_term = "lucy_goosey"
        users = User.get_users_from_search_term(search_term, self.users)
        self.assertEqual(len(users), 1)
        self.assertIn(self.lucy_chen, users)
        self.assertNotIn(self.john_nolan, users)
