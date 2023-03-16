from rest_framework.permissions import BasePermission
from . import models
from curriculum_tracking.models import ContentItem


class IsInstanceUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        instance = view.get_object()
        return instance.user_id == user.id


class StepPermissionMixin:
    @staticmethod
    def get_step(request, view):
        registration = view.get_object()
        index = request.data.get("index")
        if index == None:
            return

        return registration.get_steps()[int(index)]


class StepCanStart(BasePermission, StepPermissionMixin):
    def has_permission(self, request, view):
        """return True if the step either can start or has already started"""
        step = self.get_step(request, view)
        if step:
            return step.status == models.ChallengeRegistration.STATUS_READY


class StepCanFinish(BasePermission, StepPermissionMixin):
    def has_permission(self, request, view):
        """return True if the step is a topic, and it has already started"""
        step = self.get_step(request, view)
        if step:
            return (
                step.content_item.content_type == ContentItem.TOPIC
                and step.progress
                and step.progress.start_time
            )


class StepCanSubmitLink(BasePermission, StepPermissionMixin):
    def has_permission(self, request, view):
        step = self.get_step(request, view)
        if step:
            return (
                step.content_item.content_type == ContentItem.PROJECT
                and step.content_item.project_submission_type == ContentItem.LINK
                and step.progress
                and step.progress.start_time
            )
