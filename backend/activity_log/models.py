from django.db import models
from core.models import User
from django.utils import timezone

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import json

# see https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/#django.contrib.contenttypes.fields.GenericForeignKey


# class ObjectEffected(models.Model):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey("content_type", "object_id")

#     class Meta:
#         unique_together = [
#             [
#                 "content_type",
#                 "object_id",
#             ]
#         ]


class EventType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)


class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    actor_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="log_entries_as_actor",
        null=True,
        blank=True,
    )

    effected_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="log_entries_as_effected_user",
        null=True,
        blank=True,
    )

    # object_1 = models.ForeignKey(ObjectEffected)
    # object_2 = models.ForeignKey(ObjectEffected)

    object_1_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="log_entries_object_1_set",
        null=True,
        blank=True,
    )
    object_1_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    # object_1 = GenericRelation(
    #     object_id_field="object_1_id", content_type_field="object_1_content_type", to=
    # )
    object_1 = GenericForeignKey("object_1_content_type", "object_1_id")

    object_2_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="log_entries_object_2_set",
        null=True,
        blank=True,
    )
    object_2_id = models.PositiveIntegerField(null=True, blank=True)
    object_2 = GenericForeignKey(
        "object_2_content_type",
        "object_2_id",
    )

    event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        # <sanity_checks>

        # the get_activity_log_summary_data function gets used when serializing a log entry
        # for the apis. If it doesn't return serializable data then we will get problems later.
        # there is probably a more efficient way to do this

        for object in [self.object_1, self.object_2]:
            if object is not None:
                data = object.get_activity_log_summary_data()
                json.dumps(data)
                assert data.__class__ == dict

        # </sanity checks>

        super(LogEntry, self).save(*args, **kwargs)

    @classmethod
    def debounce_create(
        Cls,
        event_type,
        actor_user,
        effected_user,
        object_1,
        object_2=None,
        debounce_seconds=120,
        timestamp=None,
    ):
        """
        Create a log entry if there isn't a similar log entry that was created within the debounce period.

        Why?

        Some actions can be repeated, eg a card can be started and stopped several times over. If someone is randomly clicking around then we probably don't want a record of all their random clicks. We would just want to store the first event that happened within a set duration"""

        match = Cls.objects.filter(
            actor_user=actor_user,
            effected_user=effected_user,
            # object_1=object_1,
            # object_2=object_2,
            object_1_content_type=ContentType.objects.get_for_model(object_1),
            object_1_id=object_1.id,
            object_2_content_type=(
                ContentType.objects.get_for_model(object_2) if object_2 else None
            ),
            object_2_id=object_2.id if object_2 else None,
            event_type=event_type,
        )

        if debounce_seconds:
            assert not timestamp
            match = match.filter(
                timestamp__gte=timezone.now()
                - timezone.timedelta(seconds=debounce_seconds)
            )

        if timestamp:
            assert not debounce_seconds
            match = match.filter(timestamp=timestamp)

        match = match.first()
        if match:
            return match

        o = Cls.objects.create(
            actor_user=actor_user,
            effected_user=effected_user,
            object_1=object_1,
            object_2=object_2,
            event_type=event_type,
        )
        if timestamp:
            o.timestamp = timestamp
            o.save()
        return o

    # def set_object(self, number,object):
    #     content_type = ContentType.objects.get_for_model(object)
    #     if number == 1:
    #         self.object_1_
