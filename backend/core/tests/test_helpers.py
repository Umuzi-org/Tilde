from django.test import TestCase
from django.contrib.auth import get_user_model

from core.constants import BUSINESS_EMAIL_DOMAIN
from core.tests.factories import UserFactory
from core.helpers import get_auth_token_for_email


class get_auth_token_for_email_TestCase(TestCase):
    external_email = "foo@bar.com"
    internal_email = f"first.last@{BUSINESS_EMAIL_DOMAIN}"

    def test_outside_email_user_exists(self):
        user = UserFactory(email=self.external_email)
        token, user_created = get_auth_token_for_email(self.external_email)
        self.assertIsNotNone(token)
        self.assertFalse(user_created)
        self.assertEqual(user, token.user)

    def test_outside_email_user_does_not_exist(self):
        token, user_created = get_auth_token_for_email(self.external_email)
        self.assertIsNone(token)
        self.assertFalse(user_created)

    def test_internal_email_user_exists(self):
        user = UserFactory(email=self.internal_email)
        token, user_created = get_auth_token_for_email(self.internal_email)
        self.assertIsNotNone(token)
        self.assertFalse(user_created)
        self.assertEqual(user, token.user)

    def test_internal_email_user_does_not_exist(self):
        token, user_created = get_auth_token_for_email(self.internal_email)
        self.assertIsNotNone(token)
        self.assertTrue(user_created)
        self.assertEqual(token.user.email, self.internal_email)
