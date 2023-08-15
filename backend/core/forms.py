from django import forms
from django.forms import ValidationError
from core import models


def get_choices(Model):
    return lambda: [("", "")] + [(o.id, str(o)) for o in Model.objects.all()]


class TeamForm(forms.Form):
    team = forms.ChoiceField(choices=get_choices(models.Team), required=False)
    staff = forms.BooleanField(required=False)
    # everyone = forms.BooleanField(required=False)

    def clean(self):
        data = super(TeamForm, self).clean()

        number_of_fields = sum([bool(x) for x in data.values()])
        if number_of_fields != 1:
            # not sure why this isn't showing up...
            raise ValidationError("Choose one, and only one, filter to apply")

        return data


class BulkAddUsersForm(forms.Form):
    email_addresses = forms.CharField(
        label="Email addresses",
        widget=forms.Textarea(attrs={"rows": 15, "style": "display: flex; width:100%"}),
        help_text="Emails can be separated by commas, spaces and newlines.",
    )
