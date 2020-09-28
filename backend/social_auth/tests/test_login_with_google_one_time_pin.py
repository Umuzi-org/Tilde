from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework import status

from social_auth.views import oauth_one_time_token_auth

from core.tests.factories import UserFactory

from unittest import mock
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()


class oauth_one_time_token_auth_TestCase(APITestCase):
    def make_request(self, data=None):
        data = data or {"code": "asdsadf", "provider": "google"}
        url = reverse("oauth_one_time_token_auth")
        factory = APIRequestFactory()
        request = factory.post(url, data, format="json")
        return oauth_one_time_token_auth(request)

    @mock.patch("social_auth.google_helpers.get_email_from_one_time_code")
    def test_existing_user_gets_logged_in(self, get_email_from_one_time_code):
        user = UserFactory()
        user = User.objects.get(email=user.email)
        get_email_from_one_time_code.return_value = user.email
        response = self.make_request()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token_value = response.data["token"]
        Token.objects.get(key=token_value)

    @mock.patch("social_auth.google_helpers.get_email_from_one_time_code")
    def test_bad_user_gets_error_response(self, get_email_from_one_time_code):
        get_email_from_one_time_code.return_value = "not.ok@bugger.com"
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
