from django.urls import path
from . import views

urlpatterns = [
    # Users and teams navigation page
    path("users_and_teams_nav/", views.users_and_teams_nav, name="users_and_teams_nav"),
    path(
        "users_and_teams_nav/partial_teams_list/",
        views.partial_teams_list,
        name="partial_teams_list",
    ),
    path(
        "users_and_teams_nav/team/<int:team_id>/partial_team_users_list/",
        views.partial_team_users_list,
        name="partial_team_users_list",
    ),
    # User board
    path("users/<int:user_id>/board", views.UserBoard.as_view(), name="user_board"),
    path(
        "users/<int:user_id>/board/<str:column_id>",
        views.PartialUserBoardColumn.as_view(),
        name="partial_user_board_column",
    ),
    path(
        "cards/<int:card_id>/start",
        views.action_start_card,
        name="action_start_card",
    ),
    # Team dashboard
    path("teams/<int:team_id>/dashboard", views.team_dashboard, name="team_dashboard"),
    path(
        "teams/any/dashboard/users/<int:user_id>/progress",
        views.partial_team_user_progress_chart,
        name="partial_team_user_progress_chart",
    ),
]
