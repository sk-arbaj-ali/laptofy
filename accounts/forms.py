from django import forms
from .models import EcomUser
from products.forms import CustomTextInput, CustomPasswordInput
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# # class UserCreationForm(forms.ModelForm):

# #     class Meta:
# #         model = EcomUser
# #         fields = ['first_name', 'last_name', 'email', 'password']
# #         widgets = {
# #             'first_name':CustomTextInput(),
# #             'last_name':CustomTextInput(),
# #             'email':CustomTextInput(),
# #             'password':CustomPasswordInput(),
# #         }
class UserCreationForm(BaseUserCreationForm):
    # field_order

    class Meta:
        model = EcomUser
        fields = ['email', 'first_name', 'last_name','password1','password2']
        widgets = {
            'email':CustomTextInput(),
            'first_name':CustomTextInput(),
            'last_name':CustomTextInput(),
            # 'password1':CustomPasswordInput(),
            # 'password2':CustomPasswordInput(),
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields.get('password1').widget = CustomPasswordInput()
        self.fields.get('password2').widget = CustomPasswordInput()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            email
            and self._meta.model.objects.filter(email=email).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email

class CustomAuthForm(forms.Form):

    email = forms.EmailField(label='Email address')
    password = forms.CharField(label='Password')
    user_cache = None
    request = None
    def __init__(self,request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields.get('email').widget = CustomTextInput()
        self.fields.get('password').widget = CustomPasswordInput()

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise ValidationError(_('Credentials are not valid'), code='invalid_credentials')

        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache


class AddressForm(forms.Form):
    city = forms.CharField(max_length=100, widget=CustomTextInput)
    street = forms.CharField(max_length=100, widget=CustomTextInput)
    landmark = forms.CharField(max_length=100, widget=CustomTextInput)
    pincode = forms.IntegerField(widget=CustomTextInput)
    phone = forms.IntegerField(widget=CustomTextInput)