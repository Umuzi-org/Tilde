from django.shortcuts import render
from . import models
from . import forms
from . import serializers
from core import models as core_models
from git_real import helpers as git_helpers
from social_auth import models as social_models
from git_real.constants import ORGANISATION as GITHUB_ORG
from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from . import helpers

User = get_user_model()



def create_repos_for_project(request, cohort_id):
    cohort = core_models.Cohort.objects.get(pk=cohort_id)
    if request.method == "POST":
        form = forms.SelectRecruitsAndProjectForm(request.POST, cohort=cohort)
        if form.is_valid():
            # project_id = int(form.cleaned_data["project"])
            # recruit_ids = int(form.cleaned_data["recruits"])
            github_auth_login = request.user.social_profile.github_name

            project = form.get_project()

            creation_log = [
                {
                    "recruit": recruit,
                    "project": helpers.create_recruit_project(
                        github_auth_login, recruit, project
                    ),
                }
                for recruit in form.get_recruits()
            ]

            # breakpoint()
            for d in creation_log:
                helpers.create_or_update_single_project_card(d['project'])

            return render(
                request,
                "admin/create_repos_for_project_success.html",
                {"creation_log": creation_log},
            )

    else:
        form = forms.SelectRecruitsAndProjectForm(cohort=cohort)

    return render(
        request,
        "admin/create_repos_for_project.html",
        {"form": form, "cohort": cohort},
    )
