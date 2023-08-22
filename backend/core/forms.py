from django import forms
from django.forms import ValidationError
from core import models
import re


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


class BulkAddUsersToTeamForm(forms.Form):
    email_addresses = forms.CharField(
        label="Email addresses",
        widget=forms.Textarea(attrs={"rows": 15, "style": "display: flex; width:100%"}),
        help_text="Emails can be separated by commas, spaces and newlines.",
        required=True,
        empty_value=False,
    )
    users = forms.ModelMultipleChoiceField(
        queryset=models.User.objects.none(),
        widget=forms.MultipleHiddenInput(),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        email_addresses_str = cleaned_data["email_addresses"]
        if not email_addresses_str:
            raise ValidationError(
                f"No email addresses entered.",
            )

        email_addresses = self.get_email_addresses_from_str(email_addresses_str)
        users = models.User.objects.filter(email__in=email_addresses)
        found_users_emails = [user.email for user in users]
        not_found_users_emails = [
            email for email in email_addresses if email not in found_users_emails
        ]
        if not_found_users_emails:
            raise ValidationError(
                f"Users with the following email addresses don't exist: {', '.join(not_found_users_emails)}",
            )

        cleaned_data["users"] = users

        return cleaned_data

    def get_email_addresses_from_str(self, email_addresses_str):
        """extract a list of email addresses from a string separated by spaces, commas and newlines"""
        email_addresses = re.split("[ ,\n]", email_addresses_str)
        email_addresses = [email.strip() for email in email_addresses]
        return [email for email in email_addresses if email]
