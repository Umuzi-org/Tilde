from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
import core.permissions as core_permissions
import core.serializers as core_serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from . import models
from . import permissions


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
        return serializers.ChallengeRegistrationDetailsSerializer

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.StepIndexSerializer,
        permission_classes=[permissions.IsInstanceUser, permissions.StepCanStart],
    )
    def start_step(self, request, pk=None):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            registration = self.get_object()
            steps = registration.get_steps()
            steps[request.data["index"]]

            return Response({"success": "OK"})  # TODO..
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
