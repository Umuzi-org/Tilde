from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_staff


def clean_user_id(user_id):
    import re

    if type(user_id) is str:
        return int(re.search("\d+", user_id)[0])
    return user_id


def IsCurrentUserInSpecificFilter(filter_name):
    class IsCurrentUserInFilter(BasePermission):
        def has_permission(self, request, view):
            user = request.user
            filter_by = dict(request.query_params).get(filter_name, [])
            if type(filter_by) is not list:
                filter_by = [filter_by]
            filter_by = [clean_user_id(user_id) for user_id in filter_by]
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

