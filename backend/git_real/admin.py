from django.contrib import admin
from . import models

admin.site.register(models.Repository)
admin.site.register(models.Commit)
admin.site.register(models.PullRequest)
admin.site.register(models.PullRequestReview)
