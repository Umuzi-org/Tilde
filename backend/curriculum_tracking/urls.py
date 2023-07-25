from django.urls import path
from curriculum_tracking.admin import custom_admin_site
from . import views

urlpatterns = [
    path(
        "admin/bulk_add_learners_to_team",
        custom_admin_site.urls,
    ),
    path(
        "hey/core/team/bulk_add_learners_to_team/",
        views.bulk_add_learners_to_team,
        name="bulk_add_learners_to_team",
    ),
]
