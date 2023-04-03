from django import forms
from .models import Shop


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shop_name', 'docs']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control form-control-lg'}
                )
            self.fields[field].required = False

    def clean(self):
        data = self.cleaned_data
        if data.get('role', None) == 'thisshop':
            for field in self.fields:
                self.fields[field].required = True
        else:
            for field in self.fields:
                self.fields[field].required = False
        return data
