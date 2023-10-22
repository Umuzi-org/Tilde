from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from core.models import Team
from curriculum_tracking.models import AgileCard
from django.db.models import Q

User = get_user_model()

board_columns = [
    {
        "title": "Backlog",
        "id": "backlog",
        "query": lambda user: AgileCard.objects.filter(
            Q(status=AgileCard.READY) | Q(status=AgileCard.BLOCKED)
        )
        .order_by("order")
        .filter(assignees=user),
    },
    {
        "title": "In Progress",
        "id": "in_progress",
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.IN_PROGRESS)
        .order_by("order")
        .filter(assignees=user),
    },
    {
        "title": "Review Feedback",
        "id": "review_feedback",
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.REVIEW_FEEDBACK)
        .order_by("order")
        .filter(assignees=user),
    },
    {
        "title": "Review",
        "id": "review",
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.IN_REVIEW)
        .order_by("order")
        .filter(assignees=user),
    },
    {
        "title": "Complete",
        "id": "complete",
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.COMPLETE)
        .order_by("-order")
        .filter(assignees=user),
    },
]


def user_board(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {"user": user, "columns": board_columns}
    return render(request, "frontend/user_board.html", context)


def partial_user_board_column(request, user_id, column_id):
    user = get_object_or_404(User, id=user_id)
    cards = [d for d in board_columns if d["id"] == column_id][0]["query"](user)
    context = {"cards": cards}
    return render(request, "frontend/partial_user_board_column.html", context)


def users(request):
    # page_size = 20
    # page_number = 0

    teams = Team.objects.order_by("name")

    users = User.objects.order_by("email")
    context = {"teams": teams, "users": users}
    return render(request, "frontend/users.html", context)
