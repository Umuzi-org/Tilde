# the api views from this file were moved to curriculum_tracking. This was done to preserve the direction of imports

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from core import permissions as core_permissions
from core.models import Team
from .models import Push, Repository
from .serializers import PushSerializer
from . import permissions


def _get_teams_from_repository_instance(repo):
    projects = repo.recruit_projects.all()
    for project in projects:
        user_ids = [user.id for user in project.recruit_users.all()]
        for team in Team.get_teams_from_user_ids(user_ids):
            yield team

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
        & core_permissions.HasObjectPermission(
            permissions=Team.PERMISSION_VIEW, get_objects=_get_teams_from_repository_filter
        )
        & permissions.IsCardAssignee
    ]
