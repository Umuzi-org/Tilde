from django.db import models

from session_scheduling.models import Session


class SupportIniatiativeReason(models.Model):
    id = models.BigIntegerField(primary_key=True)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "learner_support_initiative_reasons"
        managed = False
        app_label = "sis_integrations"

    def __str__(self):
        return self.reason


class SupportInitiativeSubtype(models.Model):
    id = models.BigIntegerField(primary_key=True)
    subtype = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "learner_support_initiative_subtypes"
        managed = False
        app_label = "sis_integrations"

    def __str__(self):
        return self.subtype


class SupportInitiative(models.Model):
    TYPE_ACADEMIC = "academic"
    TYPE_HOLISTIC = "holistic"
    TYPE_CHOICES = [
        (TYPE_ACADEMIC, "Academic"),
        (TYPE_HOLISTIC, "Holistic"),
    ]
    id = models.BigIntegerField(primary_key=True)
    date_happened = models.DateField()
    date_added = models.DateField()
    added_by_user_id = models.BigIntegerField()
    updated_by_user_id = models.BigIntegerField(null=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    subtype_id = models.BigIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    learner_id = models.BigIntegerField()
    reason_id = models.BigIntegerField()
    support_session_host_user_id = models.BigIntegerField(null=True)

    class Meta:
        db_table = "learner_support_initiatives"
        managed = False
        app_label = "sis_integrations"

    def __str__(self):
        return f"{self.learner_id} - {self.type}"

    @classmethod
    def create_from_tilde_session(cls, tilde_session: Session) -> "SupportInitiative":
        session_type = tilde_session.session_type

        cls.objects.create(
            date_happened=tilde_session.date_happened,
            date_added=tilde_session.date_added,
            added_by_user_id=tilde_session.added_by_user_id,
            updated_by_user_id=tilde_session.updated_by_user_id,
            type=cls.TYPE_ACADEMIC,
            subtype_id=tilde_session.subtype_id,
            created_at=tilde_session.created_at,
            updated_at=tilde_session.updated_at,
        )

    ...
