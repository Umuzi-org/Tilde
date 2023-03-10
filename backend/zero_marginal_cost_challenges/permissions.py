from rest_framework.permissions import BasePermission


class IsInstanceUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        instance = view.get_object()
        return instance.user_id == user.id


class StepCanStart(BasePermission):
    def has_permission(self, request, view):
        """return True if the step either can start or has already started"""
        registration = view.get_object()
