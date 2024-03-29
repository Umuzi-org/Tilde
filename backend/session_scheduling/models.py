from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from model_mixins import FlavourMixin

User = get_user_model()


class SessionType(models.Model):
    name = models.CharField(
        max_length=128
    )  # "eg: card based session, bootcamp session"
    event_copy = models.TextField()
    event_title = models.CharField(max_length=256)
    description = models.TextField()
    duration_minutes = models.IntegerField()


# class SessionFacilitatorProfile(models.Model):
#     user = models.ForeignKey(User)
#     max_sessions_per_week = models.IntegerField(default=1)
#     max_sessions_per_day = models.IntegerField(default=1)


class Session(models.Model, FlavourMixin):
    """When we create one of these then it implies that a session is required.

    The facilitator is the person responsible for running the session. There can be a guest facilitator as well.

    When the session gets scheduled, we set the start and end time.
    The session is assumed complete once the end time has been passed

    If the session has not been scheduled by the due_date then it means we were under-resourced or something went wrong.
    """

    session_type = models.ForeignKey(SessionType, on_delete=models.PROTECT)
    attendees = models.ManyToManyField(User, related_name="attended_sessions")
    facilitator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="facilitated_sessions",
    )
    guest_facilitators = models.ManyToManyField(
        User, blank=True, related_name="guest_facilitated_sessions"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    related_object_content_type = models.ForeignKey(
        ContentType, on_delete=models.PROTECT, null=True, blank=True
    )
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey(
        "related_object_content_type",
        "related_object_id",
        # eg this might be related to a CB test, a bootcamp, a card, or anything else
    )
    flavours = TaggableManager(blank=True)
    extra_title_text = models.CharField(max_length=128, blank=True, null=True)

    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    is_cancelled = models.BooleanField(default=False)

    def __repr__(self):
        return self.get_title_copy()

    def get_title_copy(self):
        todo

    def get_event_copy(self):
        todo
        greeting = "Dear learner(s)"
        return f"{greeting}\n\n{copy}\n\n{form}\n\n{recording}\n\n{regards}"
