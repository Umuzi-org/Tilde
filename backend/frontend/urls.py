from django.urls import path
from . import views

urlpatterns = [
    # Users and teams navigation page
    path("users_and_teams_nav/", views.users_and_teams_nav, name="users_and_teams_nav"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("forgot_password/", views.user_forgot_password, name="user_forgot_password"),
    path(
        "forgot_password/done",
        views.user_password_reset_done,
        name="user_password_reset_done",
    ),
    path(
        "reset-password/<str:token>/",
        views.user_reset_password,
        name="user_reset_password",
    ),
    path(
        "users_and_teams_nav/view_partial_teams_list/",
        views.view_partial_teams_list,
        name="view_partial_teams_list",
    ),
    path(
        "users_and_teams_nav/team/<int:team_id>/view_partial_team_users_list/",
        views.view_partial_team_users_list,
        name="view_partial_team_users_list",
    ),
    # User board
    path("users/<int:user_id>/board", views.user_board, name="user_board"),
    path(
        "users/<int:user_id>/board/<str:column_id>",
        views.view_partial_user_board_column,
        name="view_partial_user_board_column",
    ),
    path(
        "cards/<int:card_id>/start",
        views.action_start_card,
        name="action_start_card",
    ),
    path(
        "cards/<int:card_id>/request_review",
        views.action_request_review,
        name="action_request_review",
    ),
    # Team dashboard
    path("teams/<int:team_id>/dashboard", views.team_dashboard, name="team_dashboard"),
    path(
        "teams/any/dashboard/users/<int:user_id>/progress",
        views.view_partial_team_user_progress_chart,
        name="view_partial_team_user_progress_chart",
    ),
]
