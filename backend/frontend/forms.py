from django import forms
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner
from django.urls import reverse_lazy
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm

from .theme import styles

User = get_user_model()


class ThemedFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": styles["input_small"],
                }
            )


class CustomAuthenticationForm(ThemedFormMixin, AuthenticationForm):
    username = forms.EmailField()


class CustomSetPasswordForm(ThemedFormMixin, SetPasswordForm):
    pass


class LinkSubmissionForm(ThemedFormMixin, forms.Form):
    link_submission = forms.URLField()


class ForgotPasswordForm(ThemedFormMixin, forms.Form):
    email = forms.EmailField()

    signer = TimestampSigner(salt="password.Reset")

    def user_exists(self):
        return User.objects.filter(email=self.cleaned_data.get("email")).exists()

    def _get_password_reset_token(self):
        token = self.signer.sign(self.cleaned_data.get("email"))
        return token

    def get_password_reset_url(self):
        return reverse_lazy(
            "user_reset_password",
            kwargs={"token": self._get_password_reset_token()},
        )

class SimpleSearchForm(forms.Form):
    search_term = forms.CharField(required=True)