import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from core.models import Team
from curriculum_tracking.models import AgileCard, RecruitProject, ContentItem
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from taggit.models import Tag

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


def user_has_view_access(user, request):
    user_teams = user.teams()
    can_manage_cards = [
        request.user.has_perm(Team.PERMISSION_MANAGE_CARDS, team) for team in user_teams
    ]
    can_view_all = [
        request.user.has_perm(Team.PERMISSION_VIEW_ALL, team) for team in user_teams
    ]
    can_assign_reviewers = [
        request.user.has_perm(Team.PERMISSION_ASSIGN_REVIEWERS, team)
        for team in user_teams
    ]
    can_review_cards = [
        request.user.has_perm(Team.PERMISSION_REVIEW_CARDS, team) for team in user_teams
    ]
    is_trusted_reviewer = [
        request.user.has_perm(Team.PERMISSION_TRUSTED_REVIEWER, team)
        for team in user_teams
    ]

    has_view_access = (
        any(can_manage_cards)
        or any(can_view_all)
        or any(can_assign_reviewers)
        or any(can_review_cards)
        or any(is_trusted_reviewer)
    )

    return has_view_access or user.id == request.user.id or request.user.is_superuser


class UserBoard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """The user board page. this displays the kanban board for a user"""

    template_name = "frontend/user/page_board.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, id=kwargs["user_id"])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return user_has_view_access(self.user, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        context["columns"] = board_columns
        return context


class PartialUserBoardColumn(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """The contents of one of the columns of the user's board"""

    template_name = "frontend/user/partial_user_board_column.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, id=kwargs["user_id"])
        self.column_id = kwargs["column_id"]
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return user_has_view_access(self.user, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_card_count = int(self.request.GET.get("count", 0))
        limit = 10

        all_cards = [d for d in board_columns if d["id"] == self.column_id][0]["query"](
            self.user
        )

        cards = all_cards[current_card_count : current_card_count + limit]
        has_next_page = len(all_cards) > current_card_count + limit

        context = {
            "cards": cards,
            "user_id": self.user.id,
            "column_id": self.column_id,
            "has_next_page": has_next_page,
        }
        return context


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
