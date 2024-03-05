
from django.test import TestCase

from guardian.shortcuts import assign_perm

from core.tests import factories as core_factories
from core.models import Team
from core.forms import AddGithubCollaboratorForm


class TestAddGitHubCollaborator(TestCase):
    def setUp(self) -> None:
        self.staff_member = core_factories.UserFactory()
        self.learner = core_factories.UserFactory()

        self.staff_group = core_factories.TeamFactory()
        self.staff_group.user_set.add(self.staff_member)

        self.team_a = core_factories.TeamFactory()
        self.team_a.user_set.add(self.learner)

        self.team_b = core_factories.TeamFactory()

        assign_perm(
            Team.PERMISSION_MANAGE_CARDS,
            self.staff_group,
            self.team_a,
        )
        assign_perm(
            Team.PERMISSION_MANAGE_CARDS,
            self.staff_group,
            self.team_b,
        )

        assign_perm(
            Team.PERMISSION_MANAGE_CARDS,
            self.learner,
            self.team_a,
        )
    
    def test_staff_member_can_be_added_as_collaborator_indirect_teams(self):
        permitted_teams_staff_member = AddGithubCollaboratorForm.get_permitted_teams_for_user(self.staff_member)
        assert set(permitted_teams_staff_member) == set([self.team_a.name, self.team_b.name])

    def test_learner_can_be_added_as_collaborator_to_team_a_projects_only(self):
        permitted_teams_for_learner = AddGithubCollaboratorForm.get_permitted_teams_for_user(self.learner)
        assert set(permitted_teams_for_learner) == set([self.team_a.name])
