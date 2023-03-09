from django.db import models
from core.models import Curriculum, User


class ChallengeRegistration(models.Model):
    """associates a user with a curriculum"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="challenge_registrations"
    )
    curriculum = models.ForeignKey(Curriculum, on_delete=models.PROTECT)
    registration_date = models.DateField(auto_now_add=True)

    class Meta(object):
        unique_together = ["user", "curriculum"]
