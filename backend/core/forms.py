from django import forms
from django.forms import ValidationError
from core import models


def get_choices(Model):
    return lambda: [("", "")] + [(o.id, str(o)) for o in Model.objects.all()]


class UserGroupForm(forms.Form):
    cohort = forms.ChoiceField(choices=get_choices(models.Cohort), required=False)
    product_team = forms.ChoiceField(
        choices=get_choices(models.ProductTeam), required=False
    )
    staff = forms.BooleanField(required=False)
    # everyone = forms.BooleanField(required=False)

    def clean(self):

        data = super(UserGroupForm, self).clean()

        number_of_fields = sum([bool(x) for x in data.values()])
        if number_of_fields != 1:
            # not sure why this isn't showing up...
            raise ValidationError("Choose one, and only one, filter to apply")

        return data
