from django import forms
from products.models import Product, ProductColor, ProductSize
from accounts.models import Address

class ProductOrderForm(forms.Form):
    # user = models.ForeignKey(EcomUser, on_delete=models.CASCADE)
    product = forms.ModelChoiceField(queryset=Product.objects.all(),to_field_name='slug')
    color = forms.ModelChoiceField(queryset=ProductColor.objects.all())
    size = forms.ModelChoiceField(queryset=ProductSize.objects.all())

class SelectAddressForm(forms.Form):
    address = forms.ModelChoiceField(queryset=Address.objects.all())