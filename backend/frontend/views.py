from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from core.models import Team
from curriculum_tracking.models import AgileCard
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

board_columns = [
    {
        "title": "Backlog",
        "id": f"{AgileCard.READY}{AgileCard.BLOCKED}",
        "query": lambda user: AgileCard.objects.filter(
            Q(status=AgileCard.READY) | Q(status=AgileCard.BLOCKED)
        )
        .order_by("order")
        .filter(assignees=user),
    },
    {
        "title": "In Progress",
        "id": AgileCard.IN_PROGRESS,
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.IN_PROGRESS)
        .order_by("order")
        .filter(assignees=user),
    },
    {
        "title": "Review Feedback",
        "id": AgileCard.REVIEW_FEEDBACK,
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.REVIEW_FEEDBACK)
        .order_by("order")
        .filter(assignees=user),
    },
    {
        "title": "Review",
        "id": AgileCard.IN_REVIEW,
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.IN_REVIEW)
        .order_by("order")
        .filter(assignees=user),
    },
    {
        "title": "Complete",
        "id": AgileCard.COMPLETE,
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.COMPLETE)
        .order_by("-order")
        .filter(assignees=user),
    },
]

styles = {
    "button_primary_small": "rounded bg-indigo-600 px-2 py-1 text-xs font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600",
    "button_secondary_small": "rounded bg-white px-2 py-1 text-xs font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 ring-1 ring-inset ring-gray-300",
}


from django.contrib.auth.decorators import user_passes_test


def is_super(user):
    return user.is_superuser


@user_passes_test(is_super)
def user_board(request, user_id):
    """The user board page. this displays the kanban board for a user"""
    user = get_object_or_404(User, id=user_id)
    context = {"user": user, "columns": board_columns}
    return render(request, "frontend/user/page_board.html", context)


@user_passes_test(is_super)
def partial_user_board_column(request, user_id, column_id):
    """The contents of one of the columns of the user's board"""
    current_card_count = int(request.GET.get("card_count", 0))
    limit = 2

    user = get_object_or_404(User, id=user_id)
    all_cards = [d for d in board_columns if d["id"] == column_id][0]["query"](user)

    cards = all_cards[current_card_count : current_card_count + limit]
    has_next_page = len(all_cards) > current_card_count + limit

    context = {
        "cards": cards,
        "user_id": user_id,
        "column_id": column_id,
        "has_next_page": has_next_page,
        "styles": styles,
    }
    return render(request, "frontend/user/partial_user_board_column.html", context)


@user_passes_test(is_super)
@csrf_exempt
def action_start_card(request, card_id):
    """The card is in the backlog and the user has chosen to start it"""
    card = get_object_or_404(AgileCard, id=card_id)
    # TODO implement this
    return render(
        request,
        "frontend/user/action_card_moved.html",
        {
            "card": card,
            "styles": styles,
        },
    )


@user_passes_test(is_super)
def users_and_teams(request):
    """This lets a user search for users and teams. It should only display what the logged in user is allowed to see"""
    teams = Team.objects.order_by("name")
    users = User.objects.order_by("email")
    context = {
        "teams": teams,
        "users": users,
        "styles": styles,
    }
    return render(request, "frontend/users.html", context)
