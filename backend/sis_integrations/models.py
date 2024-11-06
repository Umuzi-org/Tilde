import pandas as pd

from django.db import models

from session_scheduling.models import Session


class Learner(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    last_signed_in = models.DateTimeField()
    is_logged_in = models.BooleanField()
    authentication_token = models.TextField()
    id_number = models.CharField(max_length=255)
    cellphone_number = models.CharField(max_length=255)
    whatsapp_number = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    race = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    home_language = models.CharField(max_length=255)
    second_language = models.CharField(max_length=255)
    # ...
    email = models.EmailField(max_length=150)
    # ...
    is_active = models.BooleanField()

    class Meta:
        db_table = "learners"
        app_label = "sis_integrations"
        managed = False

    @classmethod
    def get_from_email(cls, email: str) -> "Learner":
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None


class SupportIniatiativeReason(models.Model):
    id = models.BigAutoField(primary_key=True)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "learner_support_initiative_reasons"
        managed = False
        app_label = "sis_integrations"

    def __str__(self):
        return self.reason


class SupportInitiativeSubtype(models.Model):
    id = models.BigAutoField(primary_key=True)
    subtype = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "learner_support_initiative_subtypes"
        managed = False
        app_label = "sis_integrations"

    def __str__(self):
        return self.subtype


class SupportInitiativeStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "support_initiative_statuses"
        managed = False
        app_label = "sis_integrations"

    def __str__(self):
        return self.name


class SupportInitiative(models.Model):
    TYPE_ACADEMIC = "academic"
    TYPE_HOLISTIC = "holistic"
    TYPE_CHOICES = [
        (TYPE_ACADEMIC, "Academic"),
        (TYPE_HOLISTIC, "Holistic"),
    ]
    id = models.BigAutoField(primary_key=True)
    date_happened = models.DateField(auto_now_add=True)
    date_added = models.DateField(auto_now_add=True)
    added_by_user_id = models.BigIntegerField()
    updated_by_user_id = models.BigIntegerField(null=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    subtype_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    learner_id = models.BigIntegerField()
    reason_id = models.BigIntegerField()
    support_session_host_user_id = models.BigIntegerField(null=True)
    status_id = models.BigIntegerField(null=True)
    learners_flagged_academic_support_id = models.BigIntegerField(null=True)

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


class AcademicSupportFlagReason(models.Model):
    id = models.BigAutoField(primary_key=True)
    reason = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "learners_flagged_academic_support_reasons"
        app_label = "sis_integrations"
        managed = False

    def __str__(self) -> str:
        return self.reason


class LearnerFlaggedForAcademicSupport(models.Model):
    id = models.BigAutoField(primary_key=True)
    learner_id = models.BigIntegerField()
    reason_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "learners_flagged_academic_support"
        app_label = "sis_integrations"
        managed = False

    @classmethod
    def create_from_at_risk_df(cls, at_risk_df: pd.DataFrame):
        for index, row in at_risk_df.iterrows():
            # Currently only picking highest priority problem
            psf_risk = row["psf_risk"]
            progress_risk = row["progress_risk"]

            if all(pd.isna([psf_risk, progress_risk])):
                continue

            learner_email = row["email"]
            learner = Learner.get_from_email(learner_email)

            if learner is None:
                continue

            def create_flag_and_support_initiative(risk: str):
                reason_obj, _ = AcademicSupportFlagReason.objects.get_or_create(
                    reason=risk,
                )
                flag = cls.objects.create(
                    learner_id=learner.id,
                    reason_id=reason_obj.id,
                )
                flag.create_support_initiative(risk)

            if not pd.isna(psf_risk):
                create_flag_and_support_initiative(psf_risk)

            if not pd.isna(progress_risk):
                create_flag_and_support_initiative(progress_risk)

    def create_support_initiative(self, risk: str):
        subtype_obj, _ = SupportInitiativeSubtype.objects.get_or_create(
            subtype=f"At Risk - {risk}",
        )
        status, _ = SupportInitiativeStatus.objects.get_or_create(
            name="Pending",
        )
        support_initiative_reson, _ = SupportIniatiativeReason.objects.get_or_create(
            reason=f"Flagged for Academic Support",
        )
        SupportInitiative.objects.create(
            type=SupportInitiative.TYPE_ACADEMIC,
            subtype_id=subtype_obj.id,
            learner_id=self.learner_id,
            reason_id=support_initiative_reson.id,
            status_id=status.id,
            learners_flagged_academic_support_id=self.id,
        )
