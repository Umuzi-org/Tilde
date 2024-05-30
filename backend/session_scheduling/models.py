"""
TODO: 
- coderbyte based sessions
- @risk sessions 
- attendance monitoring. Missed sessions 
"""

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

    def __str__(self):
        return f"{self.name}({self.duration_minutes} mins)"


class Session(models.Model, FlavourMixin):
    """When we create one of these then it implies that a session is required.

    The facilitator is the person responsible for running the session. There can be a guest facilitator as well.

    When the session gets scheduled, we set the start and end time.
    The session is assumed complete once the end time has been passed

    If the session has not been scheduled by the due_date then it means we were under-resourced or something went wrong.
    """

    session_type = models.ForeignKey(SessionType, on_delete=models.PROTECT)
    attendees = models.ManyToManyField(
        User,
        related_name="attended_sessions",
        limit_choices_to={"active": True},
    )
    facilitator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="facilitated_sessions",
        limit_choices_to={"is_staff": True, "active": True},
    )
    guest_facilitators = models.ManyToManyField(
        User,
        blank=True,
        related_name="guest_facilitated_sessions",
        limit_choices_to={"active": True},
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
    # extra_event_body_text = models.TextField(blank=True, null=True)

    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    is_cancelled = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.get_title_copy()

    def get_title_copy(self):
        title = self.session_type.event_title.format(
            extra_title_text=self.extra_title_text,
            flavours=", ".join(self.flavour_names),
        )
        if self.facilitator:
            return f"[{self.id}] {title} {self.facilitator.email}"
        return f"[{self.id}] {title}"

    # def get_event_copy(self):

    #     todo
    #     greeting = "Dear learner(s)"
    #     return f"{greeting}\n\n{copy}\n\n{extra_event_body_text}\n\n{form}\n\n{recording}\n\n{regards}"

    def attendee_emails(self):
        emails = sorted([o.email for o in self.attendees.all()])
        return "\n".join(emails)


# class SessionFacilitatorProfile(models.Model):
#     user = models.ForeignKey(User)


# class SessionFacilitatorAllowedSession(FlavourMixin):
#     """
#     Can facilitate this type of session.
#     - extra_title_text can be regex
#     - flavours need to overlap. Eg if flavours=python, javascript then this can do a Python or a Javascript session
#     """
#     session_type = models.ForeignKey(SessionType, on_delete=models.CASCADE)
#     flavours = TaggableManager()
#     extra_title_text = models.CharField(max_length=128, blank=True, null=True)


# class AvailableTimeSlot:
#     """
#     order = the order in which slots will get filled
#     """
#     order = models.PositiveIntegerField(default=0, blank=False, null=False)
#     session_facilitator_user = models.ForeignKey(SessionFacilitatorProfile)
#     start_time = models.TimeField()
#     day_of_week = models
