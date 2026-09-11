from django import forms
from users.models import Address


class CheckoutForm(forms.Form):

    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        empty_label="Select Address"
    )

    def __init__(self, user, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['address'].queryset = Address.objects.filter(
            user=user
        )