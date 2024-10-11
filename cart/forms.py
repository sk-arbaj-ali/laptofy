from django import forms
from products.models import Product, ProductColor, ProductSize


class CartForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),to_field_name='slug')
    color = forms.ModelChoiceField(queryset=ProductColor.objects.all())
    size = forms.ModelChoiceField(queryset=ProductSize.objects.all())