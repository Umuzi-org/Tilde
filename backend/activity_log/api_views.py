from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from . import serializers
from django.db.models.functions import Cast
from django.db.models import DateField, Count
import core.permissions as core_permissions
from core.models import Team
from . import models


class ActivityLogDayCountViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ActivityLogDayCountSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["event_type", "actor_user" "effected_user"]

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
        # TODO: annotate filters
        # breakpoint()
        return query


# class ActivityLogViewSet TODO
# a normal model viewset allowing list and retrieve actions
# default order = -timestamp
# filter by users, event type
