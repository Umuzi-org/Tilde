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
    # User board
    path("users/<int:user_id>/board", views.user_board, name="user_board"),
    path(
        "users/<int:user_id>/board/<str:column_id>",
        views.partial_user_board_column,
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
