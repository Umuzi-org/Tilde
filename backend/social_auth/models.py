from django.db import models
from django.contrib.auth import get_user_model

from model_mixins import Mixins

User = get_user_model()


class SocialProfile(models.Model, Mixins):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="social_profile"
    )
    github_name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    # rocketchat_name
    # stackoverflow

    def __str__(self):
        return f"{self.user} [github_name={self.github_name}]"


class GithubOAuthToken(models.Model, Mixins):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=40)
    token_type = models.CharField(max_length=10)
    scope = models.CharField(max_length=20)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
