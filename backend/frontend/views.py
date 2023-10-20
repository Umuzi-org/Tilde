from django.shortcuts import render, get_object_or_404
from core.models import Team
from django.contrib.auth import get_user_model

User = get_user_model()


def users(request):
    # page_size = 20
    # page_number = 0

    teams = Team.objects.order_by("name")
    # [
    #     page_number * page_size : (page_number + 1) * page_size
    # ]

    users = User.objects.order_by("email")
    context = {"teams": teams, "users": users}
    return render(request, "frontend/users.html", context)


def user_board(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {"user": user}
    return render(request, "frontend/user_board.html", context)
