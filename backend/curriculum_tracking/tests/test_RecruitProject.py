from django.test import TestCase
from django.contrib.auth import get_user_model

from curriculum_tracking import models
from curriculum_tracking import constants
from curriculum_tracking import helpers
from curriculum_tracking.tests import factories

JAVASCRIPT = "js"
TYPESCRIPT = "ts"


User = get_user_model()


class generate_repo_name_for_project_Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="fooo@bar.com",
            first_name="fooo",
            last_name="baaar",
            password="top_secret",
        )

    def test_length_ok(self):
        project = factories.ProjectContentItemFactory()
        repo_name = models.RecruitProject._generate_repo_name_for_project(
            user=self.user, content_item=project, flavour_names=["javascript", "react"]
        )

        self.assertIn(str(project.id), repo_name)
        self.assertIn(project.slug, repo_name)
        self.assertIn(self.user.first_name, repo_name)
        self.assertIn(self.user.last_name, repo_name)

    def test_too_long(self):
        project = factories.ProjectContentItemFactory(title="test project " * 10)
        self.assertGreater(len(project.slug), 100)
        repo_name = models.RecruitProject._generate_repo_name_for_project(
            user=self.user, content_item=project, flavour_names=[]
        )

        self.assertIn(str(project.id), repo_name)
        self.assertIn("-test-project-", repo_name)
        self.assertIn(self.user.first_name, repo_name)
        self.assertIn(self.user.last_name, repo_name)

