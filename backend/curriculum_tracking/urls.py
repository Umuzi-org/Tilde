from django.urls import path
from . import views

urlpatterns = [
    path(
        "hey/core/team/bulk_add_learners_to_team/",
        views.bulk_add_learners_to_team,
        name="bulk_add_learners_to_team",
    ),
]
