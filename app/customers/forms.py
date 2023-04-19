from django import forms
from accounts.models import UserProfile
from django.contrib.auth import get_user_model
from django.forms.widgets import NumberInput


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-lg',
            })


class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = UserProfile
        fields = [
            'profile_picture',
            'phone_number',
            'address',
            'country',
            'state',
            'city',
            'pin_code',
            'dob',

        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dob'].required = False
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-lg',
            })
