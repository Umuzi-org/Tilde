from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from . import serializers
from django.db.models.functions import Cast
from django.db.models import DateField, Count, Value, CharField
import core.permissions as core_permissions
from core.models import Team
from . import models


class ActivityLogDayCountViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ActivityLogDayCountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["event_type__name", "actor_user", "effected_user"]

    permission_classes = [
        core_permissions.ActionIs("list")
        & (
            core_permissions.IsCurrentUserInSpecificFilter("actor_user")
            | core_permissions.IsCurrentUserInSpecificFilter("effected_user")
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter("actor_user"),
            )
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter(
                    "effected_user"
                ),
            )
        )
    ]

    def get_queryset(self):
        query = models.LogEntry.objects.annotate(
            date=Cast("timestamp", output_field=DateField())
        )
        query = query.values("date").annotate(total=Count("date"))
        query = query.order_by("-date")

        filters = "&".join(
            [f"{key}={value}" for key, value in self.request.GET.items()]
        )

        query = query.annotate(filters=Value(filters, output_field=CharField()))

        return query


class ActivityLogViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ActivityLogEventTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["event_type", "actor_user", "effected_user"]

    permission_classes = [
        core_permissions.ActionIs("list")
        & (
            core_permissions.IsCurrentUserInSpecificFilter("actor_user")
            | core_permissions.IsCurrentUserInSpecificFilter("effected_user")
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter("actor_user"),
            )
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter(
                    "effected_user"
                ),
            )
        )
    ]

    def get_queryset(self):
        query = models.LogEntry.objects.annotate(
            date=Cast("timestamp", output_field=DateField())
        )
        query = query.order_by("-timestamp")        
        filters = "&".join(
            [f"{key}={value}" for key, value in self.request.GET.items()]
        )
        query = query.annotate(filters=Value(filters, output_field=CharField()))
        return query