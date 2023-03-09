from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
import core.permissions as core_permissions
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
