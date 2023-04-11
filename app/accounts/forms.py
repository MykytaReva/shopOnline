from django import forms
from .models import User, DailyLetter


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'role',
            'password1',
            'password2',
            ]

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-lg',
                'autocomplete': 'off',
                })


class DailyLetterForm(forms.ModelForm):
    class Meta:
        model = DailyLetter
        fields = ['email',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'id': 'daily-email-id',
            'name': 'daily-email',
            'class': 'form-control form-control-lg',
            })
