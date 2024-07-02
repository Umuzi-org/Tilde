from django.test import TestCase

from .factories import RepositoryFactory


class RepositoryTestCase(TestCase):
    def test_get_github_repo_link(self):
        repo = RepositoryFactory(full_name="Umuzi-org/Tilde")
        expected_link = "https://github.com/Umuzi-org/Tilde"
        self.assertEqual(repo.get_github_link(), expected_link)
