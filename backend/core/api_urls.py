from django.urls import path
from . import views

urlpatterns = [
    path("who_am_i/", views.who_am_i),
    path("logout/", views.delete_auth_token),
    path("test_logs/", views.test_logs),
    path("test_long_running_request/", views.test_long_running_request),
    path("test_kill_dramatic_worker/", views.test_kill_dramatic_worker),
]
