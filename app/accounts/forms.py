from django import forms
from django.contrib.auth import get_user_model

from .models import DailyLetter, User


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "password1",
            "password2",
        ]

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data["password1"] != cleaned_data["password2"]:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control form-control-lg",
                    "autocomplete": "off",
                }
            )


class DailyLetterForm(forms.ModelForm):
    class Meta:
        model = DailyLetter
        fields = [
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {
                "id": "daily-email-id",
                "name": "daily-email",
                "class": "form-control form-control-lg",
            }
        )


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.cleaned_data["username"] = email  # Set email as the username

        return self.cleaned_data

    def get_user(self):
        email = self.cleaned_data.get("email")
        if email:
            try:
                return get_user_model().objects.get(email=email)
            except User.DoesNotExist:
                return None
        return None
