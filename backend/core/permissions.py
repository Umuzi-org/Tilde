from rest_framework.permissions import BasePermission


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


def RequestMethodIs(method_name):
    class _RequestMethodIs(BasePermission):
        def has_permission(self, request, view):
            return request.method == method_name

    return _RequestMethodIs


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


class IsMyUser(BasePermission):
    def has_permission(self, request, view):
        instance = view.get_object()
        return request.user == instance


# from rest_framework import  permissions

# permissions.IsAuthenticated
# permissions.AllowAny
# permissions.IsAuthenticatedOrReadOnly
# permissions.IsAdminUser
