from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = [
    # path("health_check", views.health_check),
    path("who_am_i/", views.who_am_i),
    path("logout/", views.delete_auth_token),
    path("test_logs/", views.test_logs),
    path("test_long_running_request/", views.test_long_running_request),
]
