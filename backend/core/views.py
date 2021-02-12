from . import models
from rest_framework import viewsets
from . import serializers

# from rest_framework.decorators import action

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions as drf_permissions
from guardian.shortcuts import get_objects_for_user

# from django.db.models import Q
from core import permissions as core_permissions
from core.filters import ObjectPermissionsFilter
from core.models import Team


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


def _get_teams_from_user(self, request, view):
    user = view.get_object()
    return Team.get_teams_from_user_ids([user.id])


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    permission_classes = [
        core_permissions.ActionIs("retrieve")
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

    # def assign_as_reviewer(self, request, pk=None):
    #     return Response("TODO")


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