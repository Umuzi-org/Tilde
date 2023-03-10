from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
import core.permissions as core_permissions

# import core.serializers as core_serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from curriculum_tracking.models import ContentItem, RecruitProject, TopicProgress
from . import serializers
from . import models
from . import permissions
from django.utils import timezone


class ChallengeRegistrationViewset(viewsets.ModelViewSet):

    queryset = models.ChallengeRegistration.objects.order_by("pk")

    # serializer_class = serializers.ChallengeRegistrationListSerializer

    permission_classes = [
        (
            core_permissions.ActionIs("list")
            & core_permissions.IsCurrentUserInSpecificFilter("user")
        )
        | (
            core_permissions.ActionIs("create")
            & core_permissions.IsCurrentUserInRequestData("user")
        )
        | (core_permissions.ActionIs("retrieve") & permissions.IsInstanceUser)
    ]
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["user"]

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return serializers.ChallengeRegistrationListSerializer
        if self.action in ["retrieve"]:
            return serializers.ChallengeRegistrationDetailsSerializer
        return super(ChallengeRegistrationViewset, self).get_serializer_class()

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.StepIndexSerializer,
        permission_classes=[permissions.IsInstanceUser & permissions.StepCanStart],
    )
    def start_step(self, request, pk=None):
        # TODO: flavours

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            registration = self.get_object()
            user = registration.user
            steps = registration.get_steps()
            step = steps[serializer.data["index"]]

            if not step.progress:
                if step.content_item.content_type == ContentItem.PROJECT:
                    progress = RecruitProject.objects.create(
                        content_item=step.content_item
                    )
                    progress.recruit_users.add(user)
                    progress.save()
                elif step.content_item.content_type == ContentItem.TOPIC:
                    progress = TopicProgress.objects.create(
                        user=user, content_item=step.content_item
                    )
                step.progress = progress

            if not step.progress.start_time:
                step.progress.start_time = timezone.now()
                step.progress.save()

            return Response({"success": "OK"})  # TODO..
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.StepIndexSerializer,
        permission_classes=[permissions.IsInstanceUser & permissions.StepCanFinish],
    )
    def finish_step(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            registration = self.get_object()
            user = registration.user
            steps = registration.get_steps()
            step = steps[serializer.data["index"]]

            step.progress.complete_time = timezone.now()
            step.progress.save()

            return Response({"success": "OK"})  # TODO..
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def submit_link_for_review
