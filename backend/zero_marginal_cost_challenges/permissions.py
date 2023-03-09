from rest_framework.permissions import BasePermission


class IsInstanceUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        instance = view.get_object()
        return instance.user_id == user.id
