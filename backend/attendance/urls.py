from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "cohort/<int:id>/attendance",
        views.cohort_attendance_graph,
        name="cohort_attendance",
    ),
    path(
        "product/<int:id>/attendance",
        views.product_attendance_graph,
        name="product_attendance",
    ),
    path("staff/attendance", views.staff_attendance_graph, name="staff_attendance"),
    # path("all/attendance", views.attendance_graph, name="all_attendance"),
]
