from django.urls import path
from . import views

urlpatterns = [
    path(
        "github_oauth_start/",
        views.authorize_github_start,
        name="authorize_github_start",
    ),
    path(
        "github_oauth_callback/",
        views.authorize_github_callback,
        name="authorize_github_callback",
    ),
    path(
        "oauth_one_time_token_auth/",
        views.oauth_one_time_token_auth,
        name="oauth_one_time_token_auth",
    ),
]
