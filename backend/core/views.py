from . import models
from rest_framework import viewsets
from rest_framework.decorators import action
from . import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core import permissions as core_permissions
from core.models import Team
from rest_framework import viewsets
from curriculum_tracking.serializers import UserDetailedStatsSerializer
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .forms import (
    BulkAddUsersToTeamForm,
    AddGithubCollaboratorForm,
    DeleteAndRecreateCardsForm,
)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()

# TODO: REFACTOR. If the management helper is used ourtside the management dir then it should be moved


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_auth_token(request):
    # TODO: turn this into a class based view and add it to router
    # any logged in user has access
    request.auth.delete()
    return Response({"status": "OK"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def who_am_i(request):
    # TODO: turn this into a class based view
    # anyone can access it. No permission needed
    serialiser = serializers.WhoAmISerializer(request.auth)
    return Response(serialiser.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def test_long_running_request(request):
    from long_running_request_actors import test_long_running_request as actor

    response = actor.send()
    return Response({"status": "OK", "data": response.asdict()})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def test_kill_dramatic_worker(request):
    from long_running_request_actors import test_kill_pod as actor

    response = actor.send()
    return Response({"status": "OK", "data": response.asdict()})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def test_logs(request):
    import logging

    # Get an instance of a logger
    logger = logging.getLogger(__name__)

    logger.debug(
        "DEBUG message blah blah blah woooo stuuufffff ------------\n\tetc etc etc"
    )
    logger.info(
        "INFO message blah blah blah woooo stuuufffff ------------\n\tetc etc etc"
    )
    logger.warn(
        "WARN message blah blah blah woooo stuuufffff ------------\n\tetc etc etc"
    )
    logger.error(
        "ERROR message blah blah blah woooo stuuufffff ------------\n\tetc etc etc"
    )
    logger.exception(
        "EXCEPTION message blah blah blah woooo stuuufffff ------------\n\tetc etc etc"
    )

    raise Exception(f"{__name__}:Not really an error. It's all going quite swimmingly")


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user profiles to be viewed or edited.
    """

    queryset = models.UserProfile.objects.all().order_by("rocketchat_name")
    serializer_class = serializers.UserProfileSerializer


class CurriculumViewSet(viewsets.ModelViewSet):
    queryset = models.Curriculum.objects.all().order_by("name")
    serializer_class = serializers.CurriculumSerializer

    permission_classes = [core_permissions.IsReadOnly]


def _get_teams_from_user(self, request, view):
    user = view.get_object()
    return Team.get_teams_from_user_ids([user.id])


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    permission_classes = [
        IsAdminUser
        | core_permissions.ActionIs("retrieve")
        & (
            core_permissions.IsMyUser
            | core_permissions.HasObjectPermission(
                permissions=models.Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_user,
            )
            | IsAuthenticated  # TODO: remove this. it's a dodgy fix. A user needs to be able to view users if they can see that user's card. As in, reviewers should see reviewees.
        )
    ]

    queryset = models.User.objects.all().order_by("last_name")
    serializer_class = serializers.UserSerializer
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["groups"]

    @action(
        detail=True,
        methods=["GET"],
        serializer_class=UserDetailedStatsSerializer,
        permission_classes=[
            IsAdminUser
            | core_permissions.IsMyUser
            | core_permissions.HasObjectPermission(
                permissions=models.Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_user,
            )
        ],
    )
    def stats(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_object = self.get_object()
            return Response(UserDetailedStatsSerializer(user_object).data)
        else:
            return Response(serializer.errors, status="BAD_REQUEST")

    @action(
        detail=True,
        methods=["DELETE"],
        serializer_class=serializers.NoArgs,
        permission_classes=[IsAdminUser],
    )
    def danger_delete_all_progress(self, request, pk=None):
        from curriculum_tracking.models import (
            AgileCard,
            RecruitProject,
            TopicProgress,
            WorkshopAttendance,
        )

        user = self.get_object()

        AgileCard.objects.filter(assignees__in=[user]).delete()
        RecruitProject.objects.filter(recruit_users__in=[user]).delete()
        TopicProgress.objects.filter(user=user).delete()
        WorkshopAttendance.objects.filter(attendee_user=user).delete()

        return Response({"status": "OK"})

    @action(
        detail=True,
        methods=["POST", "GET"],
        serializer_class=serializers.NoArgs,
        permission_classes=[IsAdminUser],
    )
    def danger_delete_and_recreate_user_board(self, request, pk=None):
        if request.method == "GET":
            return Response(
                {
                    "status": "OK",
                }
            )
        else:
            from long_running_request_actors import (
                delete_and_recreate_user_cards as actor,
            )

            user = self.get_object()
            response = actor.send_with_options(kwargs={"user_id": user.id})
            return Response({"status": "OK", "data": response.asdict()})

    @action(
        detail=True,
        methods=["POST", "GET"],
        serializer_class=serializers.NoArgs,
        permission_classes=[IsAdminUser],
    )
    def invite_to_github_org(self, request, pk=None):
        if request.method == "GET":
            return Response(
                {
                    "status": "OK",
                }
            )
        else:
            from long_running_request_actors import invite_user_to_github_org as actor

            user = self.get_object()
            response = actor.send_with_options(kwargs={"user_id": user.id})
            return Response({"status": "OK", "data": response.asdict()})

    @action(
        detail=True,
        methods=["GET"],
        serializer_class=serializers.NoArgs,
        permission_classes=[
            IsAdminUser
            | core_permissions.IsMyUser
            | core_permissions.HasObjectPermission(
                permissions=models.Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_user,
            )
        ],
    )
    def competence_reviews_outstanding(self, request, pk=None):
        from curriculum_tracking.helpers import agile_card_reviews_outstanding
        from curriculum_tracking.serializers import (
            OutstandingCompetenceReviewSerializer,
        )

        user = self.get_object()
        cards = agile_card_reviews_outstanding(user)
        return Response(
            OutstandingCompetenceReviewSerializer(card).data for card in cards
        )

    # @action(
    #     detail=False,
    #     methods=["GET"],
    #     serializer_class=UserSummaryStatsSerializer,
    #     permission_classes=[
    #         IsAdminUser
    #         | core_permissions.HasObjectPermission(
    #             permissions=models.Team.PERMISSION_VIEW,
    #         )
    #     ],
    # )
    # def summary_stats(self, request, pk=None):

    #     page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(self.get_queryset(), many=True)
    #     return Response(serializer.data)
    # def assign_as_reviewer(self, request, pk=None):
    #     return Response("TODO")

    # @action(
    #     detail=True,
    #     methods=["get"],
    #     serializer_class=serializers.UserStatsSerializer,
    #     permission_classes=core_permissions.HasObjectPermission(
    #         permissions=Team.PERMISSION_VIEW, get_objects=_get_teams_from_user
    #     ),
    # )
    # def stats(self, request, pk=None):
    #     breakpoint()
    #     woo


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def team_permissions(request):
#     result = {}

#     for permission, _ in models.Team._meta.permissions:
#         teams = get_objects_for_user(
#             user=request.user,
#             perms=permission,
#             klass=models.Team.objects.all(),
#             with_superuser=False,
#             any_perm=True,
#         )

#         for team in teams:
#             result[team.id] = result.get(
#                 team.id, {"id": team.id, "name": team.name, "permissions": []}
#             )
#             result[team.id]["permissions"].append(permission)

#     return Response(result)


class BulkAddUsersToTeamView(LoginRequiredMixin, FormView):
    form_class = BulkAddUsersToTeamForm
    template_name = "admin/core/bulk_add_users_form.html"
    success_url = reverse_lazy("bulk_add_users_to_team")

    def get_login_url(self):
        return reverse("admin:login")

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        team_id = self.kwargs["team_id"]
        self.team = get_object_or_404(Team, id=team_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.team
        return context

    def form_valid(self, form):
        users = form.cleaned_data["users"]
        team = self.team

        team.user_set.add(*users)

        messages.success(
            self.request,
            f'Users were successfully added to the "{team}" team',
        )
        return redirect(
            reverse("admin:core_team_change", kwargs={"object_id": team.id})
        )


class AddUserAsGithubCollaborator(LoginRequiredMixin, FormView):
    template_name = "admin/core/confirm_add_github_collaborator.html"
    form_class = AddGithubCollaboratorForm

    def get_login_url(self) -> str:
        return reverse("admin:login")

    def form_valid(self, form):
        include_complete_projects = form.cleaned_data.get("include_complete_projects")
        self._add_as_collaborator(self.user, include_complete_projects)
        messages.success(
            self.request,
            f"Adding user as a collaborator in the background. {'(Including complete projects)' if include_complete_projects else ''}",
        )
        return super().form_valid(form)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = get_object_or_404(User, id=self.kwargs["user_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        context["teams"] = AddGithubCollaboratorForm.get_permitted_teams_for_user(
            self.user
        )
        return context

    def get_success_url(self) -> str:
        return reverse("admin:core_user_change", kwargs={"object_id": self.user.pk})

    @staticmethod
    def _add_as_collaborator(user, include_complete_projects=False):
        from long_running_request_actors import (
            invite_collaborators_for_team_projects as actor,
        )

        permitted_teams_for_user = (
            AddGithubCollaboratorForm.get_permitted_teams_for_user(user)
        )

        for team_name in permitted_teams_for_user:
            actor.send_with_options(
                kwargs={
                    "team_name": team_name,
                    "include_complete": include_complete_projects,
                }
            )


class DeleteAndRecreateCards(LoginRequiredMixin, FormView):
    template_name = "admin/core/confirm_delete_recreate_cards.html"
    form_class = DeleteAndRecreateCardsForm

    def get_login_url(self) -> str:
        return reverse("admin:login")

    def form_valid(self, form):
        self._delete_and_recreate_cards(self.user.id)
        messages.success(
            self.request,
            f"Deleting and recreating cards in the background",
        )
        return super().form_valid(form)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = get_object_or_404(User, id=self.kwargs["user_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_success_url(self) -> str:
        return reverse("admin:core_user_change", kwargs={"object_id": self.user.pk})

    @staticmethod
    def _delete_and_recreate_cards(user_id):
        from long_running_request_actors import delete_and_recreate_user_cards as actor

        actor.send_with_options(kwargs={"user_id": user_id})


class DeleteAndRecreateCardsForTeam(LoginRequiredMixin, FormView):
    form_class = DeleteAndRecreateCardsForm
    template_name = "admin/core/confirm_delete_recreate_cards_for_team.html"

    def get_login_url(self):
        return reverse("admin:login")

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        team_id = self.kwargs["team_id"]
        self.team = get_object_or_404(Team, id=team_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.team
        return context

    def form_valid(self, form):
        self._delete_and_recreate_cards_for_team(self.team.id)
        messages.success(
            self.request,
            f"Deleting and recreating cards for team in the background",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("admin:core_team_change", kwargs={"object_id": self.team.id})

    @staticmethod
    def _delete_and_recreate_cards_for_team(team_id):
        from long_running_request_actors import bulk_regenerate_cards_for_team as actor

        actor.send_with_options(kwargs={"team_id": team_id})
