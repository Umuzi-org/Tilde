from curriculum_tracking.serializers import UserStatsPerWeekSerializer, CardSummarySerializer, AgileCardSerializer
from . import models
from rest_framework import viewsets
from rest_framework.decorators import action
from . import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions as drf_permissions
from core import permissions as core_permissions
from core.filters import ObjectPermissionsFilter
from core.models import Team
from rest_framework import viewsets, status
from core.permissions import HasObjectPermission
from curriculum_tracking.serializers import TeamStatsSerializer
from curriculum_tracking.management.helpers import get_team_cards


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


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeamSerializer
    filter_backends = [
        DjangoFilterBackend,
        ObjectPermissionsFilter(models.Team.PERMISSION_VIEW),
    ]
    filterset_fields = ["active"]

    permission_classes = [
        drf_permissions.IsAuthenticated and core_permissions.IsReadOnly
    ]

    def get_queryset(self):
        queryset = (
            models.Team.objects.all()
            .order_by("name")
            .prefetch_related("user_set")
            # .prefetch_related("team_memberships__user")
        )
        return queryset

    def get_object(self):
        return self.get_queryset()

    @action(
        detail=False,
        methods=["GET"],
        serializer_class=TeamStatsSerializer,
        permission_classes=[
            IsAdminUser
            | core_permissions.HasObjectPermission(
                permissions=models.Team.PERMISSION_VIEW,
            )
        ],
    )
    def summary_stats(self, request, pk=None):

        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

        # serializer = self.get_serializer(data=request.data)
        # if serializer.is_valid():
        #     team = self.get_object()
        #     return Response(TeamStatsSerializer(team).data)
        # else:
        #     return Response(serializer.errors, status="BAD_REQUEST")

    # @action(
    #     detail=True,
    #     methods=["get"],
    #     permission_classes=[
    #         core_permissions.HasObjectPermission(
    #             models.Team.PERMISSION_ASSIGN_REVIEWERS
    #         )
    #     ],
    # )
    # def shuffle_reviewers(self, request, pk=None):
    #     return Response("TODO")

    @action(
        detail=False,
        methods=["POST"],
        serializer_class=CardSummarySerializer,
        permission_classes=[HasObjectPermission(permissions=Team.PERMISSION_MANAGE_CARDS)]
    )
    def bulk_set_due_dates(self, request, pk=None):

        team: models.Team = models.Team.objects.filter(name=request.data.get('team')).first()
        team_cards = get_team_cards(team, request.data.get('content_item'))
        [card.set_due_time(request.data.get('due_time')) for card in team_cards]

        return Response(AgileCardSerializer([card for card in team_cards][0]).data)


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
        )
    ]

    queryset = models.User.objects.all().order_by("last_name")
    serializer_class = serializers.UserSerializer
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["groups"]

    @action(
        detail=True,
        methods=["GET"],
        serializer_class=UserStatsPerWeekSerializer,
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
            return Response(UserStatsPerWeekSerializer(user_object).data)
        else:
            return Response(serializer.errors, status="BAD_REQUEST")

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
