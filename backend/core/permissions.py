from rest_framework.permissions import BasePermission
from core import models


def get_teams_from_user_ids(user_ids):
    yielded = []
    for user_id in user_ids:
        try:
            user = models.User.objects.get(pk=user_id)
        except models.User.DoesNotExist:
            # someone is trying to filter by a user that doesn't exist
            # therefore no teams to be retured
            continue

        for team in user.teams():
            if team.id not in yielded:
                yielded.append(team.id)
                yield team


class DenyAll(BasePermission):
    def has_permission(self, request, view):
        return False


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_staff


def ActionIs(action_name):
    class _ActionIs(BasePermission):
        def has_permission(self, request, view):
            return view.action == action_name

    return _ActionIs


def HasObjectPermission(permissions, get_object=None, get_objects=None):
    class _HasObjectPermission(BasePermission):
        def has_permission(self, request, view):
            user = request.user
            if user.is_superuser:
                return True

            if type(permissions) is str:
                all_permissions = [permissions]
            else:
                all_permissions = permissions

            if get_objects:
                instances = list(get_objects(self, request, view))
            elif get_object:
                instances = [get_object(self, request, view)]
            else:
                instances = view.get_object()

            # has_permissions = user.get_permissions()
            for instance in instances:

                for permission in all_permissions:
                    if user.has_perm(permission, instance):
                        return True
            return False

    return _HasObjectPermission


def clean_user_id(user_id):
    import re

    if type(user_id) is str:
        return int(re.search("\d+", user_id)[0])
    return user_id


def get_clean_user_ids_from_filter(request, filter_name):
    filter_by = dict(request.query_params).get(filter_name, [])
    if type(filter_by) is not list:
        filter_by = [filter_by]
    filter_by = [clean_user_id(user_id) for user_id in filter_by]
    return filter_by


def IsCurrentUserInSpecificFilter(filter_name):
    class IsCurrentUserInFilter(BasePermission):
        def has_permission(self, request, view):
            user = request.user
            filter_by = get_clean_user_ids_from_filter(request, filter_name)
            return user.id in filter_by

    return IsCurrentUserInFilter


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "OPTIONS"]:
            return True


# from rest_framework import  permissions

# permissions.IsAuthenticated
# permissions.AllowAny
# permissions.IsAuthenticatedOrReadOnly
# permissions.IsAdminUser
