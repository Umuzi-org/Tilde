from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.exceptions import ErrorDetail
from django.urls import reverse
from rest_framework.authtoken.models import Token

from core.tests.factories import UserFactory  # todo. this is a bit untidy here


class APITestCaseMixin:
    LIST_URL_NAME = "fill this in in inheriting classes"
    SUPPRESS_TEST_GET_LIST = False
    SUPPRESS_TEST_POST_TO_CREATE = False

    NUMBER_OF_INSTANCES_CREATED_BY_VERBOSE_FACTORY = 1
    LOGIN_AS_SUPERUSER = True
    FIELDS_THAT_CAN_BE_FALSEY = []

    def login_as_superuser(self):
        user = UserFactory(is_superuser=True, is_staff=True)
        self.login(user)

    def get_list_url(self):
        return reverse(self.LIST_URL_NAME)

    def get_instance_url(self, pk):
        return f"{self.get_list_url}/{pk}"

    def login(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def test_get_list(self):
        if self.SUPPRESS_TEST_GET_LIST:
            return

        if self.LOGIN_AS_SUPERUSER:
            self.login_as_superuser()

        url = self.get_list_url()
        response = self.client.get(url)
        # self.assertIn("count", response.data)
        # self.assertEqual(response.data, [])
        self.assertEqual(response.data, [])

        # make an instance. No attribute should be falsy
        instance = self.verbose_instance_factory()
        assert instance, "factory needs to return an instance"
        str(instance)  # just in case. this has broken before

        response = self.client.get(url)
        self.assertEqual(
            len(response.data), self.NUMBER_OF_INSTANCES_CREATED_BY_VERBOSE_FACTORY
        )
        # print(response.data)
        instance = response.data[0]
        assert "id" in instance, "please make sure your serialiser includes an id field"
        for key, value in instance.items():
            if key in self.FIELDS_THAT_CAN_BE_FALSEY:
                continue
            self.assertTrue(bool(value), f"{key} = {value}. The value must be truthy")
        for field in self.FIELDS_THAT_CAN_BE_FALSEY:
            self.assertTrue(field in instance)

    def test_post_to_create(self):
        if self.SUPPRESS_TEST_POST_TO_CREATE:
            return

        if self.LOGIN_AS_SUPERUSER:
            self.login_as_superuser()

        url = self.get_list_url()
        response = self.client.get(url)
        self.assertEqual(response.data, [])

        data = self.generate_post_create_data()

        response = self.client.post(url, data=data)

        # if there are any errors in the api call, then the response data will include some exceptions as values
        for _, value in response.data.items():
            has_error = (type(value) is ErrorDetail) or (
                (type(value) is list)
                and (len(value))
                and (type(value[0]) is ErrorDetail)
            )
            self.assertFalse(has_error, response.data)

        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

    def verbose_instance_factory(self):
        raise NotImplementedError(
            "use factory_boy (or other) factories to create an instance of the model under test"
        )

    def generate_post_create_data(self):
        raise NotImplementedError(
            "return a dictionary that can be posted to this viewset's list url in order to create an instance"
        )
