from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
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
                    "class": f"block {styles['input_small']}",
                }
            )


class CustomAuthenticationForm(ThemedFormMixin,AuthenticationForm,forms.Form):
    username = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not self.user_exists():
            raise forms.ValidationError('Email address provided does not exist with us')

        return username
    
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if self.user_exists():
            user = User.objects.get(email=username)
            password_correct = check_password(password, user.password)

            if not password_correct:
                raise forms.ValidationError("The entered password is incorrect")

        return password
    
    def user_exists(self):
        return User.objects.filter(email=self.cleaned_data.get("username")).exists()



class CustomSetPasswordForm(ThemedFormMixin, SetPasswordForm):
    pass


class ForgotPasswordForm(ThemedFormMixin, forms.Form):
    email = forms.EmailField()

    signer = TimestampSigner(salt="password.Reset")

    def clean_email(self):
        username = self.cleaned_data.get('email')

        if not self.user_exists():
            raise forms.ValidationError('Email address provided does not exist with us')

        return username

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
