from django.db import models
from core.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ObjectEffected(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class EventType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    actor_user = models.ForeignKey(User)
    effected_user = models.ForeignKey(User)

    objects_effected = models.ManyToManyField(ObjectEffected)

    event_type = models.ForeignKey(EventType)
