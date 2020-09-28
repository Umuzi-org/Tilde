from django.db import models
from django.conf import settings
from core import models as core_models
from django.contrib.auth import get_user_model
from model_mixins import Mixins

User = get_user_model()


class MorningAttendance(models.Model, Mixins):
    timestamp = models.DateTimeField()
    date = models.DateField()
    plan_of_action = models.TextField()
    problems_forseen = models.BooleanField()
    requests = models.TextField(blank=True, null=True)
    late_reason = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField()

    #########################################################
    # denormalised fields populated by signals start below
    is_staff = models.BooleanField(null=True)
    cohort = models.ForeignKey(
        core_models.Cohort, blank=True, null=True, on_delete=models.SET_NULL
    )
    product_teams = models.ManyToManyField(
        core_models.ProductTeam, related_name="morning_attendace",
    )

    class Meta:
        unique_together = [["date", "user"]]

    def graph_dict(self):
        return {
            "_type": "morning",
            "timestamp": self.timestamp,
            "user.email": self.user.email,
            "score": self.score,
            "plan_of_action": self.plan_of_action,
            "still_on_track": self.problems_forseen,
            "comments": self.requests,
            "late_reason": self.late_reason,
        }


class AfternoonAttendance(models.Model, Mixins):
    timestamp = models.DateTimeField()
    date = models.DateField()
    still_on_track = models.BooleanField()
    reason_for_not_on_track = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    late_reason = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField()

    #########################################################
    # denormalised fields populated by signals start below
    is_staff = models.BooleanField(null=True)
    cohort = models.ForeignKey(
        core_models.Cohort, blank=True, null=True, on_delete=models.SET_NULL
    )
    product_teams = models.ManyToManyField(
        core_models.ProductTeam,
        related_name="afternoon_attendace",
        related_query_name="afternoon_attendance_query",
    )

    class Meta:
        unique_together = [["date", "user"]]

    def graph_dict(self):
        return {
            "_type": "afternoon",
            "timestamp": self.timestamp,
            "user.email": self.user.email,
            "score": self.score,
            "late_reason": self.late_reason,
            "still_on_track": self.still_on_track,
            "comments": self.comments,
            "problems": self.reason_for_not_on_track,
        }


class EveningAttendance(models.Model, Mixins):
    timestamp = models.DateTimeField()

    date = models.DateField()

    plan_completed_sucessfully = models.BooleanField()
    reason_not_completed = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    late_reason = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField()

    #########################################################
    # denormalised fields populated by signals start below
    is_staff = models.BooleanField(null=True)
    cohort = models.ForeignKey(
        core_models.Cohort, blank=True, null=True, on_delete=models.SET_NULL
    )
    product_teams = models.ManyToManyField(
        core_models.ProductTeam,
        related_name="evening_attendace",
        related_query_name="evening_attendance_query",
    )

    class Meta:
        unique_together = [["date", "user"]]

    def graph_dict(self):
        return {
            "_type": "evening",
            "timestamp": self.timestamp,
            "user.email": self.user.email,
            "score": self.score,
            "late_reason": self.late_reason,
            "still_on_track": self.plan_completed_sucessfully,
            "comments": self.comments,
            "problems": self.reason_not_completed,
        }


class Leave(models.Model, Mixins):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="leave_requests")
    LEAVE_TYPE = (("1", "Annual Leave"),("2", "Sick Leave"),("3", "Family Responsibility"),("4", "Maternity Leave"),("5", "Paternity Leave"))
    type_of_leave = models.CharField(max_length=1, choices=LEAVE_TYPE)
    manager = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_staff': True},related_name="leave_approvals") 
    reason_for_leave = models.TextField(blank=True, null=True)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    amount_of_days = models.SmallIntegerField(null=True)



    
