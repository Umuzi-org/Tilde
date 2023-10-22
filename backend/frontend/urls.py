from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.users, name="users"),
    path("users/<int:user_id>/board", views.user_board, name="user_board"),
    path(
        "users/<int:user_id>/board/<str:column_id>",
        views.partial_user_board_column,
        name="partial_user_board_column",
    ),
]
