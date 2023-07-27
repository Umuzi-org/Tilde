from django import forms
from core import models as core_models
from curriculum_tracking import models as curriculum_models
from social_auth import models as social_models
from core.models import User


def get_curriculum_choices():
    return [
        (o.id, str(o))
        for o in curriculum_models.ContentItem.objects.filter(
            content_type=curriculum_models.ContentItem.PROJECT
        )
    ]


def user_to_str_and_github(user):
    ERROR = "----- ERROR: NO GITHUB NAME -----"
    try:
        social = social_models.SocialProfile.objects.get(user=user)
        github_name = social.github_name or ERROR
    except social_models.SocialProfile.DoesNotExist:
        github_name = ERROR

    return f"{user} [{github_name}]"


def get_user_choices(cohort):
    return [(o.id, user_to_str_and_github(o)) for o in cohort.get_member_users()]


class SelectRecruitsAndProjectForm(forms.Form):
    project = forms.ChoiceField(
        choices=get_curriculum_choices,
        required=True,
    )
    recruits = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={"checked": ""}),
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        cohort = kwargs["cohort"]
        del kwargs["cohort"]
        super(SelectRecruitsAndProjectForm, self).__init__(*args, **kwargs)
        self.fields["recruits"].choices = get_user_choices(cohort)

    def get_recruits(self):
        for pk in self.cleaned_data["recruits"]:
            yield User.objects.get(pk=pk)

    def get_project(self):
        project = curriculum_models.ContentItem.objects.get(
            pk=self.cleaned_data["project"]
        )
        assert (
            project.content_type == curriculum_models.ContentItem.PROJECT
        ), f"invalid content type '{project.content_type}'' for project '{project}'' [id={project.id}]. Expected '{curriculum_models.ContentItem.PROJECT}'"
        return project


class BulkUsersAndTeamOperationForm(forms.ModelForm):
    class Meta:
        model = curriculum_models.BulkUsersAndTeamOperation
        fields = "__all__"
        widgets = {
            "email_addresses": forms.Textarea(attrs={"rows": 5}),
        }
