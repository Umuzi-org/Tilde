from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CoderbyteTestResult(models.Model):
    STATUS_SUBMITTED = "Submitted"
    STATUS_TIME_EXPIRED = "Time expired"
    STATUS_IN_PROGRESS = "In progress"
    STATUS_INVITED = "Invited"

    status_choices = [
        (STATUS_SUBMITTED, STATUS_SUBMITTED),
        (STATUS_TIME_EXPIRED, STATUS_TIME_EXPIRED),
        (STATUS_IN_PROGRESS, STATUS_IN_PROGRESS),
        (STATUS_INVITED, STATUS_INVITED),
    ]

    PLAGIARISM_LIKELY = "Likely"
    PLAGIARISM_NOT_DETECTED = "Not detected"
    PLAGIARISM_DETECTED = "Detected"

    PLAGIARISM_CHOICES = [
        (PLAGIARISM_LIKELY, PLAGIARISM_LIKELY),
        (PLAGIARISM_NOT_DETECTED, PLAGIARISM_NOT_DETECTED),
        (PLAGIARISM_DETECTED, PLAGIARISM_DETECTED),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_link = models.URLField(null=True, blank=True, unique=True)

    status = models.CharField(max_length=12, choices=status_choices)
    date_joined = models.DateField(null=True, blank=True)
    date_invited = models.DateField(null=True, blank=True)
    assessment_name = models.CharField(max_length=100)
    assessment_id = models.CharField(max_length=100)
    plagiarism = models.CharField(
        max_length=13, choices=PLAGIARISM_CHOICES, null=True, blank=True
    )
    time_taken_minutes = models.IntegerField(null=True, blank=True)
    challenges_completed = models.IntegerField(null=True, blank=True)
    challenge_score = models.IntegerField(null=True, blank=True)
    multiple_choice_score = models.IntegerField(null=True, blank=True)
    final_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.assessment_name}"


# class UserProblemSolvingLevel(models.model)
