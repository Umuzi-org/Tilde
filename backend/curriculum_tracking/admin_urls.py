from django.urls import path
from . import views


# http://localhost:8000/admin/curriculum_tracking/contentitem/1/change/
# http://localhost:8000/admin/curriculum_tracking/create_repos_for_project/


# http://localhost:8000/admin/core/cohort/13/change/


urlpatterns = [
    path(
        "cohort/<int:cohort_id>/create_repos_for_project/",
        views.create_repos_for_project,
        name="create_repos_for_project",
    ),
]
