from django.db import models
from core.models import Stream, Team


class Bootcamp(models.Model):
    """
    While the bootcamp is active, it will have a series of sessions

    The bootcamp end date is when the learners are expected to finish. But there might still be sessions run
    """

    active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    stream = models.ForeignKey(
        Stream, on_delete=models.CASCADE
    )  # eg: Bootcamp Data Science
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # eg: Data Science Team

    def __str__(self):
        return f"{self.team} [{self.stream}]"
