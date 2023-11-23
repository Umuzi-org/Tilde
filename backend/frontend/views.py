import json

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.contrib.auth.forms import SetPasswordForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from django.core.signing import SignatureExpired, BadSignature

from taggit.models import Tag

from core.models import Team
from curriculum_tracking.models import AgileCard, RecruitProject, ContentItem

from .forms import ForgotPasswordForm


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


def is_super(user):
    return user.is_superuser


def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy("user_board", kwargs={"user_id": request.user.id}))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(
                request, "frontend/auth/page_login.html", {"error": "User not found"}
            )
        login(request, user)

        return redirect(reverse_lazy("user_board", kwargs={"user_id": user.id}))
    else:
        return render(request, "frontend/auth/page_login.html")


@login_required()
def user_logout(request):
    logout(request)
    return redirect(reverse_lazy("user_login"))


def _send_password_reset_email(request, form: ForgotPasswordForm) -> None:
    current_site = get_current_site(request)
    subject = "Reset your Password"

    body = render_to_string(
        template_name="frontend/auth/email_password_reset.html",
        context={
            "domain": current_site.domain,
            "url": form.get_password_reset_url(),
        },
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(body),
        from_email=None,
        to=[form.cleaned_data["email"]],
    )
    email.attach_alternative(body, "text/html")
    email.send(fail_silently=False)


def user_forgot_password(request):
    form = ForgotPasswordForm(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            if form.user_exists():
                _send_password_reset_email(request, form)
            return redirect(reverse_lazy("user_password_reset_done"))

    return render(request, "frontend/auth/page_forgot_password.html", {"form": form})


def user_password_reset_done(request):
    return render(request, "frontend/auth/page_password_reset_done.html")


def user_reset_password(request, token):
    signer = ForgotPasswordForm.signer
    try:
        email = signer.unsign(token, max_age=60 * 60)
    except (SignatureExpired, BadSignature):
        return render(
            request,
            "frontend/auth/page_password_reset.html",
            {"error": "Invalid token"},
        )

    user = User.objects.get(email=email)
    form = SetPasswordForm(user=user, data=request.POST)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.add_message(
                request=request,
                level=messages.INFO,
                message="Password reset successfully. You can now login.",
            )
            return redirect(reverse_lazy("user_login"))

    return render(request, "frontend/auth/page_password_reset.html", {"form": form})


@user_passes_test(is_super)
def user_board(request, user_id):
    """The user board page. this displays the kanban board for a user"""
    user = get_object_or_404(User, id=user_id)
    context = {"user": user, "columns": board_columns}
    return render(request, "frontend/user/page_board.html", context)


@user_passes_test(is_super)
def partial_user_board_column(request, user_id, column_id):
    """The contents of one of the columns of the user's board"""
    current_card_count = int(request.GET.get("count", 0))
    limit = 10

    user = get_object_or_404(User, id=user_id)
    all_cards = [d for d in board_columns if d["id"] == column_id][0]["query"](user)

    cards = all_cards[current_card_count : current_card_count + limit]
    has_next_page = len(all_cards) > current_card_count + limit

    context = {
        "cards": cards,
        "user_id": user_id,
        "column_id": column_id,
        "has_next_page": has_next_page,
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
        },
    )


@user_passes_test(is_super)
def users_and_teams_nav(request):
    """This lets a user search for users and teams. It should only display what the logged in user is allowed to see"""
    # teams = Team.objects.order_by("name")
    # users = User.objects.order_by("email")
    context = {
        # "teams": teams,
        # "users": users,
    }
    return render(request, "frontend/users_and_teams_nav/page.html", context)


@user_passes_test(is_super)
def partial_teams_list(request):
    limit = 20
    current_team_count = int(request.GET.get("count", 0))

    all_teams = Team.objects.filter(active=True).order_by(
        "name"
    )  # TODO: only show teams that the current user is allowed to see
    teams = all_teams[current_team_count : current_team_count + limit]
    has_next_page = len(all_teams) > current_team_count + limit

    context = {
        "teams": teams,
        "has_next_page": has_next_page,
    }

    return render(
        request, "frontend/users_and_teams_nav/partial_teams_list.html", context
    )


@user_passes_test(is_super)
def partial_team_users_list(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    users = team.active_users.order_by("email")
    context = {
        "users": users,
    }
    return render(
        request, "frontend/users_and_teams_nav/partial_team_users_list.html", context
    )


@user_passes_test(is_super)
def team_dashboard(request, team_id):
    """The team dashboard page. this displays the kanban board for a team"""
    team = get_object_or_404(Team, id=team_id)
    context = {
        "team": team,
    }
    return render(request, "frontend/team/page_dashboard.html", context)


@user_passes_test(is_super)
def partial_team_user_progress_chart(request, user_id):
    user = get_object_or_404(User, id=user_id)

    skill_tags = Tag.objects.filter(name__startswith="skill/")
    skill_names = []
    skill_values = []

    for skill in skill_tags:
        cards = AgileCard.objects.filter(
            content_item__tags=skill,
            assignees=user,
            content_item__content_type=ContentItem.PROJECT,
        ).prefetch_related("recruit_project")

        skill_total = cards.count()
        complete_count = cards.filter(status=AgileCard.COMPLETE).count()

        if skill_total == 0:
            continue

        skill_names.append(skill.name.replace("skill/", ""))

        final = int(complete_count / skill_total * 100)
        skill_values.append(final)

    context = {
        "canvas_id": f"progress-chart-{ user.id }",
        "chart_args": json.dumps(
            {
                "type": "polarArea",
                "options": {
                    "scale": {"r": {"min": 0, "max": 100}},
                    "plugins": {
                        "legend": {"position": "right"},
                    },
                },
                "data": {
                    "labels": skill_names,
                    "datasets": [
                        {
                            "data": skill_values,
                        },
                    ],
                },
            },
            indent=2,
        ),
    }

    return render(request, "frontend/components/chartjs.html", context)
