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
        "users/view_partial_users_list/",
        views.view_partial_users_list,
        name="view_partial_users_list",
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
        "cards/<int:card_id>/finish_topic",
        views.action_finish_topic,
        name="action_finish_topic",
    ),
    path(
        "cards/<int:card_id>/request_review",
        views.action_request_review,
        name="action_request_review",
    ),
    path(
        "cards/<int:card_id>/cancel_review_request",
        views.action_cancel_review_request,
        name="action_cancel_review_request",
    ),
    path(
        "cards/<int:card_id>/stop_card",
        views.action_stop_card,
        name="action_stop_card",
    ),
    # user review trust
    path(
        "users/<int:user_id>/user_review_trust_list/",
        views.user_review_trust_list,
        name="user_review_trust_list",
    ),
    # Team dashboard
    path("teams/<int:team_id>/dashboard", views.team_dashboard, name="team_dashboard"),
    path(
        "teams/any/dashboard/users/<int:user_id>/progress",
        views.view_partial_team_user_progress_chart,
        name="view_partial_team_user_progress_chart",
    ),
    # Progress details
    path(
        "progress_details/<content_type>/<int:id>",
        views.progress_details,
        name="progress_details",
    ),
    path(
        "progress_details/<content_type>/<int:id>/add_review/",
        views.action_add_review,
        name="action_add_review",
    ),
    # Project review coordination
    path(
        "project_review_coordination/unclaimed/",
        views.project_review_coordination_unclaimed,
        name="project_review_coordination_unclaimed",
    ),
    path(
        "project_review_coordination/my_claims/",
        views.project_review_coordination_my_claims,
        name="project_review_coordination_my_claims",
    ),
    path(
        "project_review_coordination/claims/",
        views.project_review_coordination_all_claims,
        name="project_review_coordination_all_claims",
    ),
    path(
        "project_review_coordination/claim_bundle/",
        views.action_project_review_coordination_claim_bundle,
        name="action_project_review_coordination_claim_bundle",
    ),
    path(
        "project_review_coordination/claims/<int:claim_id>/unclaim/",
        views.action_project_review_coordination_unclaim_bundle,
        name="action_project_review_coordination_unclaim_bundle",
    ),
    path(
        "project_review_coordination/claims/<int:claim_id>/add_time/",
        views.action_project_review_coordination_add_time,
        name="action_project_review_coordination_add_time",
    ),
    # Dashboards
    path(
        "dashboards/project_review_health/",
        views.dashboard_project_review_health,
        name="dashboard_project_review_health",
    ),
]
