from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    # path("cohort/<int:id>/commits", views.commit_history_graph, name="cohort_commits"),
    # path(
    #     "product/<int:id>/commits", views.commit_history_graph, name="product_commits"
    # ),
    # path("staff/commits", views.commit_history_graph, name="staff_commits"),
    # path("all/commits", views.commit_history_graph, name="all_commits"),
    path(
        "github_webhook",
        views.github_webhook,
        name="github_webhook",
    ),
]
