# the api views from this file were moved to curriculum_tracking. This was done to preserve the direction of imports

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import permissions
from curriculum_tracking import permissions as curriculum_permissions
from core import permissions as core_permissions

# from core.permissions import (
#     ActionIs,
#     IsStaffUser,
#     HasObjectPermission,
#     IsReadOnly,
#     DenyAll,
#     IsCurrentUserInSpecificFilter,
# )

from core.models import Team
from .models import Push, Repository
from .serializers import PushSerializer


def _get_teams_from_repository_filter(self, request, view):
    repo_id = dict(request.query_params).get("repository")
    if not repo_id:
        return ()
    if type(repo_id) is list:
        assert len(repo_id) == 1
        repo = Repository.objects.get(pk=repo_id[0])
    else:
        repo = Repository.objects.get(pk=repo_id)

    return _get_teams_from_repository_instance(repo)

class PushViewSet(viewsets.ModelViewSet):
    serializer_class = PushSerializer
    queryset = Push.objects.order_by("-pushed_at_time")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["repository"]

    permission_classes = [
        core_permissions.ActionIs("list")
        & (
            curriculum_permissions.IsFilteredByRepoAttachedToProjectICanSee
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_repository_filter,
            )
        )
    ]
