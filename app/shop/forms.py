from django import forms
from .models import Shop, Category, Item, ItemImage
from orders.models import ShopOrder


class ShopForm(forms.ModelForm):
    shop_name = forms.CharField(required=False)
    docs = forms.FileField(required=False)

    class Meta:
        model = Shop
        fields = ['shop_name', 'docs']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shop_name'].required = False
        self.fields['docs'].required = False
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-lg',
                'autocomplete': 'off',
                })
            # self.fields[field].required = False
        # self.fields['shop_name'].required = False
        # self.fields['docs'].required = False

    def clean(self):
        data = self.cleaned_data
        if data.get('role', None) == 'thisshop':
            for field in self.fields:
                self.fields[field].required = True
        else:
            for field in self.fields:
                self.fields[field].required = False
        return data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-lg',
                'autocomplete': 'off',
                })


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'title',
            'description',
            'category',
            'price',
            'is_available'
            ]

    def __init__(self, *args, **kwargs):
        self.shop = kwargs.pop('shop', None)
        super().__init__(*args, **kwargs)
        if self.shop is not None:
            self.fields['category'].queryset = \
                Category.objects.filter(shop=self.shop)

        for field in self.fields:
            if field == 'is_available':
                continue
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-lg',
                'autocomplete': 'off',
                })


class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'autocomplete': 'off',
            })
        self.fields['image'].required = False


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = ShopOrder
        fields = ['status',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'autocomplete': 'off',
            })


class ShopStatusForm(forms.ModelForm):
    is_approved = forms.ChoiceField(
        choices=((True, 'Approved'), (False, 'Pending')),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Shop
        fields = ['is_approved',]
