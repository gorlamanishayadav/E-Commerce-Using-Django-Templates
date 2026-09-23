from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Address


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')



class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

        fields = [
            'full_name',
            'phone',
            'address_line',
            'city',
            'state',
            'pincode'
        ]

        widgets = {
            'address_line': forms.Textarea(attrs={
                'rows': 3
            }),
        }