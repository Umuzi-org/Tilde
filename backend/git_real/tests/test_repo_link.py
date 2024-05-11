from git_real.models import Repository
from rest_framework.test import APITestCase


class RepositoryTestCase(APITestCase):
    def test_get_github_repo_link(self):
        repository = Repository(
            owner="Umuzi-org",
            full_name="Tilde",
            ssh_url="git@github.com:Umuzi-org/Tilde.git",
            created_at="2020-09-28T00:00:00Z",
            private=False,
            archived=False,
        )
        repo_link = repository.get_github_repo_link()
        expected_link = "https://github.com/Umuzi-org/Tilde"
        self.assertEqual(repo_link, expected_link)