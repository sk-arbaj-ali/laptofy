from django import forms
from .models import Category, SubCategory, ProductSize


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class CustomTextInput(forms.TextInput):
    attrs = {'class':"appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,self.attrs, **kwargs)

class CustomPasswordInput(forms.PasswordInput):
    attrs = {'class':"appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,self.attrs, **kwargs)

class CustomTextArea(forms.Textarea):
    attrs = {'class':"appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,self.attrs, **kwargs)

class MultipleFileField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=100, widget=CustomTextInput())

class SubCategoryForm(forms.Form):
    name = forms.CharField(max_length=100, widget=CustomTextInput())
    description = forms.CharField(widget=CustomTextArea())
    category = forms.ModelChoiceField(queryset=Category.objects.all())

class ProductForm(forms.Form):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.all())
    name = forms.CharField(max_length=100, widget=CustomTextInput(), strip=True)
    brand_name = forms.CharField(max_length=100, widget=CustomTextInput(), strip=True)
    description = forms.CharField(widget=CustomTextArea())
    original_price = forms.IntegerField(initial=0,min_value=0, widget=CustomTextInput())
    
    image = MultipleFileField(required=False)

class ProductColorAndSizeForm(forms.Form):
    color = forms.CharField(max_length=100, widget=CustomTextInput, strip=True)
    size = forms.DecimalField(max_digits=4,widget=CustomTextInput(), decimal_places=2, help_text='Provide the size in scale of inch(e.g: 15.6, 17 etc.)')
    price_to_add = forms.IntegerField(initial=0,min_value=0, required=False, widget=CustomTextInput())
    price_to_subtract = forms.IntegerField(initial=0,min_value=0, required=False, widget=CustomTextInput())
    available_stock = forms.IntegerField(initial=1, widget=CustomTextInput(),min_value=1)


class ProductFilterForm(forms.Form):
    product_category = forms.ModelChoiceField(queryset=SubCategory.objects.all(),required=False)
    display_sizes = forms.ChoiceField(choices={}, required=False)
    prices = forms.ChoiceField(choices={
        None:'----------',
        20000:'20000-40000',
        40000:'40000-60000',
        60000:'60000-80000',
        80000:'Above 80000'
    }, required=False)

    def __init__(self, product_category, display_sizes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('product_category').queryset = product_category
        self.fields.get('display_sizes').choices = display_sizes