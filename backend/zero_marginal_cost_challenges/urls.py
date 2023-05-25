from django.urls import path
from . import api_views

urlpatterns = [
    path("who_am_i/", api_views.who_am_i),
]
