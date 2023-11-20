from django.urls import path
from . import views

urlpatterns = [
    path(
        "bulk_add_users_to_team/<int:team_id>",
        views.BulkAddUsersToTeamView.as_view(),
        name="bulk_add_users_to_team",
    ),
    path(
        "add_github_collaborator/<int:user_id>",
        views.AddUserAsGithubCollaborator.as_view(),
        name="confirm_add_github_collaborator",
    ),
]
