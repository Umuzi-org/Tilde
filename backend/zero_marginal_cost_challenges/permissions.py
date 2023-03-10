from rest_framework.permissions import BasePermission
from . import models


class IsInstanceUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        instance = view.get_object()
        return instance.user_id == user.id


class StepCanStart(BasePermission):
    def has_permission(self, request, view):
        """return True if the step either can start or has already started"""
        registration = view.get_object()
        breakpoint()
        index = request.data["index"]
        step = registration.steps()[index]
        return step.status == models.ChallengeRegistration.STATUS_READY
