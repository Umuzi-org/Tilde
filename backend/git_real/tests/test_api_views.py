from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin


from . import factories


class RepositoryViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "repository-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        return factories.RepositoryFactory(archived=True)
