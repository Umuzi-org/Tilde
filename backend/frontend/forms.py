from django import forms
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner
from django.urls import reverse_lazy

User = get_user_model()


class ForgotPasswordForm(forms.Form):
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
